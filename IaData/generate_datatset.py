# Fixing the syntax error (removed leading zero in randint range).
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

N_ROWS = 100_000
PLAYERS = 800  # unique players pool
GAMES = N_ROWS // 4  # approx games (4 players per game)

# Helper lists
first_names = ["Eric","Alex","Sam","Jordan","Taylor","Chris","Morgan","Casey","Jamie","Riley",
               "Leo","Lucas","Mateo","Noah","Liam","Hugo","Mila","Emma","Sofia","Chloe",
               "Pierre","Paul","Luc","Antoine","Julien","Camille","Julie","Sarah","Ana","Lena",
               "Mohamed","Youssef","Carlos","Diego","Maria","Isabella","Olivia","Ethan","Ava","Maya"]
last_names = ["Philippe","Durand","Martin","Bernard","Thomas","Petit","Robert","Richard","Moreau","Laurent",
              "Leroy","Rousseau","Garnier","Blanc","Faure","Morel","Girard","Clement","Mercier","Andre",
              "Lopez","Garcia","Silva","Rossi","Bianchi","Schmidt","Muller","Kovacs","Nakamura","Kim"]
locations = ["Ynov Toulouse","Ynov Tls","Campus - Cafeteria","Lab 204","Student House","Bar Le Foos",
             "Gym Hall","Salle Polyvalente","Cafeteria (1st floor)","Ynov - Bâtiment A"]
table_conditions = ["good","worn","broken leg","beer stains","sticky handles","out of alignment","new","scratched","needs cleaning","missing screw"]
ball_types = ["classic","orange soft","white hard","3-ball set","trainer ball","mini ball","old worn"]
music_tracks = ["Silence","","Spotify: Queen - We Will Rock You","Lo-fi beats","EDM mix","Radio 104.5","Classical - Beethoven","Indie playlist","Spotify: Dua Lipa - Physical","Oldies 80s"]
comments = ["amazing comeback!","rage quit","close match","8 goals in one minute","ref biased","spectacular assist","no comment","team spirit high","table slippery","beer spilled"]
recorders = ["phone","camera","admin","auto_recorder","referee","player phone","Discord Bot","GoPro"]
seasons = ["2023/2024","2024/2025","s24/25","Season 24-25","2025 Season"]

# Create player pool with variant name spellings
players = []
for i in range(PLAYERS):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    base = f"{fn} {ln}"
    variants = [base,
                f"{fn[0]}. {ln}",
                f"{ln} {fn}",
                f"{fn} {ln[0]}.",
                f"{fn}",
                f"{fn} {ln}".lower(),
                base.upper(),
                f"{fn} {ln}".replace("e","3")]
    players.append({
        "player_id": f"P{i+1:04d}",
        "name": base,
        "variants": list(set(variants))
    })

# function to randomly format dates differently
def random_date_str(start_year=2023, end_year=2025):
    start = datetime(start_year,1,1)
    end = datetime(end_year,12,31)
    delta = end - start
    d = start + timedelta(days=random.randint(0, delta.days), seconds=random.randint(0, 86399))
    fmt = random.choice([ "%Y-%m-%d", "%d/%m/%y", "%b %d %Y", "%d %b %y", "%d-%m-%Y", "%m/%d/%Y", "%Y/%m/%d" ])
    s = d.strftime(fmt)
    # some messy variants
    if random.random() < 0.02:
        s = d.strftime("%b %dst %Y").replace("1st","1st")
    if random.random() < 0.01:
        s = d.strftime("%Y.%m.%d")
    return s

rows = []
game_id_typos = set()

for g in range(GAMES):
    game_id = f"G{g+1:06d}"
    # introduce occasional typographical duplication/typo
    if random.random() < 0.005:
        # create a typo variant of game_id sometimes (e.g., missing leading zero)
        game_id_variants = [game_id, game_id.replace("0","",1), game_id.lower(), game_id + random.choice(["","a","_1"])]
        game_id = random.choice(game_id_variants)
        game_id_typos.add(game_id)
    date = random_date_str()
    location = random.choice(locations)
    table_id = f"T{random.randint(1,30):02d}"
    table_condition = random.choice(table_conditions)
    ball_type = random.choice(ball_types + ["", None])  # some missing
    music = random.choice(music_tracks)
    referee = random.choice([None, "", random.choice(first_names)+" "+random.choice(last_names)]) if random.random()<0.9 else random.choice(["yes","no","Player1"])
    duration = random.choice([f"{random.randint(5,20)}min", f"{random.randint(5,20)}.{random.randint(0,59)}", 
                              f"00:{random.randint(5,59):02d}:{random.randint(0,59):02d}", f"{random.uniform(5,20):.2f}"])
    # generate final score
    score_r = random.randint(0,10)
    score_b = random.randint(0,10)
    # Make some data inconsistent: sometimes scores stored as "5 - 3" or text
    if random.random() < 0.05:
        final_score_red = f"{score_r} - {score_b}"
        final_score_blue = ""
    else:
        final_score_red = score_r
        final_score_blue = score_b
    # winner field sometimes wrong or empty
    if isinstance(final_score_red,int) and isinstance(final_score_blue,int):
        if score_r>score_b: winner = random.choice(["Red","red","RED","Rouge","R"]) 
        elif score_b>score_r: winner = random.choice(["Blue","blue","BLUE","Bleu","B"])
        else: winner = random.choice(["draw","tie","TIE",""])
    else:
        winner = random.choice(["Red","Blue","", None])
    attendance_count = random.choice([2,3,4,5,6,7,8, "4 players", None])
    season = random.choice(seasons)
    recorded_by = random.choice(recorders)
    rating = random.choice([1,2,3,4,5,"five","four","⭐⭐⭐","👍","🙂","😡"])
    
    # create 4 players per game (2v2 typical)
    players_in_game = random.sample(players,4)
    teams = ["Red","Blue","Red","Blue"]
    roles = ["attack","defense","attck","defence","def","ATTACK","Defense"]
    for idx, p in enumerate(players_in_game):
        # variant of name to create messy name entries
        name_variant = random.choice(p["variants"] + [p["name"]])
        # sometimes use initials or abbreviations
        if random.random() < 0.03:
            name_variant = name_variant.replace(" ", ". ")
        player_age = random.choice([random.randint(16,45), None, "twenty", "21 yrs", ""]) 
        # stats (some as text)
        goals = random.randint(0, score_r if teams[idx]=="Red" else score_b) if isinstance(score_r,int) and isinstance(score_b,int) else random.randint(0,5)
        if random.random() < 0.02:
            goals = ["one","two","three","ten"][random.randint(0,3)]
        own_goals = 0 if random.random()>0.02 else random.randint(1,2)
        assists = random.randint(0,5)
        saves = random.randint(0,10)
        possession_time = random.choice([random.randint(10,600), f"{random.randint(0,9)}:{random.randint(0,59):02d}", f"{random.uniform(0.5,10):.2f}min", ""]) 
        mood = random.choice(["🙂","😡","😂","1","2","3","happy","angry",""])
        comment = random.choice(comments + ["", None])
        team_color = teams[idx] if random.random() < 0.95 else random.choice(["red","blue","🔴","🔵","R","B"])
        is_sub = random.choice(["yes","no", None, "maybe"])
        ping_ms = random.choice([random.randint(10,200), "", None, f"{random.randint(10,200)}ms"])
        notes = random.choice(["", "captain", "injured", "late", "double booked", ""])
        duplicate_flag = random.choice([0,1, "yes", "", None])
        misc_field = random.choice(["N/A", "", "null", "—", "-"])
        
        row = {
            "game_id": game_id,
            "game_date": date,
            "location": location,
            "table_id": table_id,
            "table_condition": table_condition,
            "ball_type": ball_type,
            "music_playing": music,
            "referee": referee,
            "game_duration": duration,
            "final_score_red": final_score_red,
            "final_score_blue": final_score_blue,
            "winner": winner,
            "attendance_count": attendance_count,
            "season": season,
            "recorded_by": recorded_by,
            "rating_raw": rating,
            "player_id": p["player_id"],
            "player_name": name_variant,
            "player_canonical_name": p["name"],
            "player_age": player_age,
            "player_role": random.choice(roles),
            "player_goals": goals,
            "player_own_goals": own_goals,
            "player_assists": assists,
            "player_saves": saves,
            "possession_time": possession_time,
            "mood": mood,
            "player_comment": comment,
            "team_color": team_color,
            "is_substitute": is_sub,
            "ping_ms": ping_ms,
            "notes": notes,
            "duplicate_flag": duplicate_flag,
            "misc": misc_field,
            "created_at": datetime.utcnow().isoformat()[:19]  # consistent but in UTC ISO
        }
        rows.append(row)

# Convert to DataFrame
df = pd.DataFrame(rows)

# Introduce some duplicated rows intentionally and shuffle
dups = df.sample(frac=0.002, random_state=1)
df = pd.concat([df, dups])
df = df.sample(frac=1, random_state=2).reset_index(drop=True)

# Introduce some deliberate corrupted rows / encoding-like issues
for _ in range(50):
    i = random.randint(0, len(df)-1)
    col = random.choice(df.columns.tolist())
    df.at[i, col] = str(df.at[i, col]) + "�"  # replacement character to simulate encoding issues

# Save to CSV
out_path = "/mnt/data/babyfoot_dataset_100k.csv"
df.to_csv(out_path, index=False, encoding="utf-8")

# Also create a small preview CSV for quick inspection
preview_path = "/mnt/data/babyfoot_dataset_100k_preview.csv"
df.head(50).to_csv(preview_path, index=False, encoding="utf-8")

len_df = len(df)
out_path, preview_path, len_df, df.columns.tolist()[:20]
