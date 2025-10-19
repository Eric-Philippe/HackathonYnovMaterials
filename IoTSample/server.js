const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const { SerialPort } = require("serialport");
const { ReadlineParser } = require("@serialport/parser-readline");

// --- Configuration ---
const HTTP_PORT = 5000;
const SERIAL_PORT_PATH = "/dev/ttyACM0"; // Or your Arduino's serial port
const BAUD_RATE = 9600;
const HAPPY_CARD_UID = "6A3C5473";
const UNHAPPY_CARD_UID = "40547CA6";

// --- App Setup ---
const app = express();
const server = http.createServer(app);
const io = new Server(server);

// --- Global State ---
let is_admin_unlocked = false;
let last_card_scan = null;
let arduino_serial = null;
let last_processed_uid = null;
let last_card_time = 0;

// --- Express Setup ---
// Serve static files from the 'templates' directory
app.use(express.static("templates"));

// Serve the main index.html file
app.get("/", (req, res) => {
  res.sendFile(__dirname + "/templates/index.html");
});

// API endpoint to get current status
app.get("/api/status", (req, res) => {
  res.json({
    admin_unlocked: is_admin_unlocked,
    last_card_scan: last_card_scan,
    arduino_connected: arduino_serial && arduino_serial.isOpen,
  });
});

// --- Socket.IO Logic ---
io.on("connection", (socket) => {
  debug_current_status();
  console.log(
    `🔗 Client connected (${socket.id}) - Status: ${
      is_admin_unlocked ? "UNLOCKED" : "LOCKED"
    }`
  );

  // Send current status to the newly connected client
  socket.emit("status_update", {
    admin_unlocked: is_admin_unlocked,
    last_card_scan: last_card_scan,
  });
  console.log("📤 Initial status sent to client");

  socket.on("disconnect", () => {
    console.log(`🔌 Client disconnected (${socket.id})`);
  });

  socket.on("manual_unlock", () => {
    console.log("🔧 Manual unlock triggered");
    is_admin_unlocked = true;
    last_card_scan = {
      uid: "MANUAL",
      timestamp: new Date().toISOString(),
      status: "manual_unlock",
    };
    // Broadcast to all clients
    io.emit("status_update", {
      admin_unlocked: is_admin_unlocked,
      last_card_scan: last_card_scan,
    });
  });

  socket.on("manual_lock", () => {
    console.log("🔧 Manual lock triggered");
    is_admin_unlocked = false;
    last_card_scan = {
      uid: "MANUAL",
      timestamp: new Date().toISOString(),
      status: "manual_lock",
    };
    // Broadcast to all clients
    io.emit("status_update", {
      admin_unlocked: is_admin_unlocked,
      last_card_scan: last_card_scan,
    });
  });

  socket.on("test_connection", (data) => {
    console.log(`🧪 Test connection received:`, data);
    socket.emit("test_response", {
      message: "Connection test successful!",
      server_time: new Date().toISOString(),
      client_data: data,
    });
  });
});

// --- Helper Functions ---
function debug_current_status() {
  console.log(
    `🔍 CURRENT GLOBAL STATUS: is_admin_unlocked = ${is_admin_unlocked}`
  );
  console.log(`🔍 LAST CARD SCAN:`, last_card_scan);
}

// --- Serial Port Logic ---
function init_arduino_connection() {
  console.log("🔄 Trying to connect to Arduino...");
  try {
    arduino_serial = new SerialPort({
      path: SERIAL_PORT_PATH,
      baudRate: BAUD_RATE,
      autoOpen: false,
    });

    const parser = arduino_serial.pipe(new ReadlineParser({ delimiter: "\n" }));

    arduino_serial.on("open", () => {
      console.log(`✅ Connected to Arduino on ${SERIAL_PORT_PATH}`);
    });

    parser.on("data", (line) => {
      console.log(`📥 Arduino data: ${line}`);
      process_arduino_line(line);
    });

    arduino_serial.on("error", (err) => {
      console.error("❌ Serial Port Error:", err.message);
      reconnect_arduino();
    });

    arduino_serial.on("close", () => {
      console.log("⚠️ Arduino connection closed.");
      reconnect_arduino();
    });

    arduino_serial.open();
  } catch (e) {
    console.error(`❌ Error initializing Arduino connection: ${e.message}`);
    reconnect_arduino();
  }
}

function reconnect_arduino() {
  // Avoid rapid reconnection attempts
  setTimeout(() => {
    console.log("Retrying Arduino connection in 5 seconds...");
    init_arduino_connection();
  }, 5000);
}

function process_arduino_line(line) {
  if (line.includes("Card UID:")) {
    const uid_match = line.match(
      /Card UID: ([0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2})/
    );
    if (uid_match && uid_match[1]) {
      const uid = uid_match[1].replace(/:/g, "").toUpperCase();
      console.log(`🎯 Clean UID extracted: ${uid}`);

      if (uid.length === 8 && /^[0-9A-F]+$/.test(uid)) {
        const current_time = Date.now();
        if (
          last_processed_uid === uid &&
          current_time - last_card_time < 2000
        ) {
          console.log(`⏭️ Skipping duplicate scan of ${uid}`);
          return;
        }

        last_card_time = current_time;
        last_processed_uid = uid;
        const timestamp = new Date().toISOString();
        let card_type = "unknown";
        const old_status = is_admin_unlocked;

        if (uid === HAPPY_CARD_UID) {
          is_admin_unlocked = true;
          card_type = "admin_unlock";
          console.log("🔓 Happy card detected - Unlocking!");
        } else if (uid === UNHAPPY_CARD_UID) {
          is_admin_unlocked = false;
          card_type = "lock";
          console.log("🔒 Unhappy card detected - Locking!");
        } else {
          console.log("❓ Unknown card detected");
        }
        console.log(`🔄 Status changed: ${old_status} -> ${is_admin_unlocked}`);

        last_card_scan = { uid, timestamp, status: card_type };

        console.log("🌐 Emitting 'card_processed' WebSocket event...");
        io.emit("card_processed", {
          uid,
          timestamp,
          type: card_type,
          admin_unlocked: is_admin_unlocked,
          last_card_scan: last_card_scan,
        });
        console.log(
          `✅ Event sent - Status: ${is_admin_unlocked ? "UNLOCKED" : "LOCKED"}`
        );
        debug_current_status();
      } else {
        console.log(`⚠️ Invalid UID format: '${uid}'`);
      }
    } else {
      console.log(`⚠️ Could not extract UID from: '${line}'`);
    }
  }
}

// --- Server Start ---
server.listen(HTTP_PORT, () => {
  console.log(`🚀 Starting RFID Authentication Server...`);
  console.log(`🌐 Web server running on http://localhost:${HTTP_PORT}`);
  init_arduino_connection();
});
