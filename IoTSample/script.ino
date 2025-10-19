#include <MFRC522.h>
#include <MFRC522Extended.h>
#include <SPI.h>

// Pin definitions
#define SS_PIN 53
#define RST_PIN 49     // Reset pin
#define BUZZER_PIN 6  // Buzzer pin

// Card UIDs
#define HAPPY_CARD_UID "6A3C5473"
#define UNHAPPY_CARD_UID "40547CA6"

MFRC522 rfid(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  SPI.begin();
  rfid.PCD_Init();
  pinMode(BUZZER_PIN, OUTPUT);
  Serial.println("RFID Scanner Ready - Scan a card...");
}

void happyBeep() {
  // Happy melody - ascending tones
  tone(BUZZER_PIN, 523, 150);  // C5
  delay(200);
  tone(BUZZER_PIN, 659, 150);  // E5
  delay(200);
  tone(BUZZER_PIN, 784, 300);  // G5
  delay(350);
}

void unhappyBeep() {
  // Unhappy melody - descending tones
  tone(BUZZER_PIN, 784, 150);  // G5
  delay(200);
  tone(BUZZER_PIN, 659, 150);  // E5
  delay(200);
  tone(BUZZER_PIN, 523, 300);  // C5
  delay(350);
}

String getCardUID() {
  String uid = "";
  for(byte i = 0; i < rfid.uid.size; i++){
    if(rfid.uid.uidByte[i] < 0x10) uid += "0";
    uid += String(rfid.uid.uidByte[i], HEX);
  }
  uid.toUpperCase();
  return uid;
}

void loop() {
  // Check if a new card is present
  if(!rfid.PICC_IsNewCardPresent()) return;
  if(!rfid.PICC_ReadCardSerial()) return;

  // Get the card UID
  String cardUID = getCardUID();
  
  // Play appropriate sound based on card type
  if(cardUID == HAPPY_CARD_UID) {
    happyBeep();
    Serial.println("Happy card detected!");
  } else if(cardUID == UNHAPPY_CARD_UID) {
    unhappyBeep();
    Serial.println("Unhappy card detected!");
  } else {
    // Default beep for unknown cards
    tone(BUZZER_PIN, 500, 200);
    delay(250);
    Serial.println("Unknown card detected!");
  }

  // Flush any pending serial data to prevent corruption
  Serial.flush();
  
  // Print UID to Serial with clear delimiters
  Serial.print("Card UID: ");
  for(byte i = 0; i < rfid.uid.size; i++){
    if(rfid.uid.uidByte[i] < 0x10) Serial.print("0");
    Serial.print(rfid.uid.uidByte[i], HEX);
    if(i < rfid.uid.size - 1) Serial.print(":");
  }
  Serial.println();
  
  // Ensure data is fully transmitted
  Serial.flush();

  // Stop reading this card
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
  
  // Wait to prevent rapid successive scans
  delay(2000);
  
  // Clear any remaining card presence
  while(rfid.PICC_IsNewCardPresent()) {
    rfid.PICC_ReadCardSerial();
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
    delay(100);
  }
}
