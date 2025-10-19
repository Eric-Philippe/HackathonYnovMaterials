# Dataset Dictionary

This document provides a detailed dictionary for the foosball match dataset, describing each column, its possible values, and any known data quality issues. The dataset contains information about games, players, and contextual details, with many fields exhibiting inconsistencies, missing values, or typos.

| column_name             | example_value         | description                                                                | category |
| ----------------------- | --------------------- | -------------------------------------------------------------------------- | -------- |
| `game_id`               | `G000001`             | Unique identifier for each game (may contain typos or duplicates).         | Game     |
| `game_date`             | `2024-03-15`          | Date/time of the game (multiple formats, inconsistent).                    | Game     |
| `location`              | `Ynov Toulouse`       | Location where the match took place (sometimes abbreviated or with typos). | Game     |
| `table_id`              | `T05`                 | Identifier of the foosball table used.                                     | Game     |
| `table_condition`       | `worn`                | Condition of the table (inconsistent descriptions).                        | Game     |
| `ball_type`             | `orange soft`         | Type of ball used, sometimes missing.                                      | Game     |
| `music_playing`         | `Lo-fi beats`         | Background music or playlist. May be empty or inconsistent.                | Context  |
| `referee`               | `Alex Martin`         | Name of the referee, sometimes “yes/no” or player name.                    | Context  |
| `game_duration`         | `00:10:23`            | Duration of the game (many different formats: minutes, seconds, text).     | Game     |
| `final_score_red`       | `5`                   | Score of Red team; may be number or text (e.g., “5 - 3”).                  | Game     |
| `final_score_blue`      | `3`                   | Score of Blue team; may be empty or inconsistent.                          | Game     |
| `winner`                | `Red`                 | Team that won (can be “Red”, “rouge”, “R”, etc.).                          | Game     |
| `attendance_count`      | `4 players`           | Number of people present (number or text).                                 | Context  |
| `season`                | `2024/2025`           | Season label (different formats).                                          | Meta     |
| `recorded_by`           | `camera`              | Who recorded the game (device/person/bot).                                 | Meta     |
| `rating_raw`            | `⭐⭐⭐`              | Post-game rating (numeric, stars, emoji, or words).                        | Meta     |
| `player_id`             | `P0043`               | Unique ID of player (consistent across games).                             | Player   |
| `player_name`           | `E. Philippe`         | Player’s name (many messy variants).                                       | Player   |
| `player_canonical_name` | `Eric Philippe`       | Canonical/clean version of the player’s name (useful for cleaning).        | Player   |
| `player_age`            | `21 yrs`              | Player’s age (sometimes numeric, text, or missing).                        | Player   |
| `player_role`           | `attack`              | Player’s position (attack/defense, may have typos).                        | Player   |
| `player_goals`          | `3`                   | Number of goals scored (sometimes text like “two”).                        | Player   |
| `player_own_goals`      | `1`                   | Number of own goals.                                                       | Player   |
| `player_assists`        | `2`                   | Number of assists.                                                         | Player   |
| `player_saves`          | `5`                   | Number of saves.                                                           | Player   |
| `possession_time`       | `4:32`                | Time spent controlling the ball (many formats).                            | Player   |
| `mood`                  | `🙂`                  | Player’s mood (emoji, text, numbers).                                      | Player   |
| `player_comment`        | `close match`         | Free comment after the game.                                               | Player   |
| `team_color`            | `Red`                 | Team the player belongs to (inconsistent values).                          | Player   |
| `is_substitute`         | `no`                  | Whether player was a substitute (yes/no/maybe).                            | Player   |
| `ping_ms`               | `45ms`                | Ping/latency (ms or text).                                                 | Tech     |
| `notes`                 | `captain`             | Misc. info about player (captain, injured, etc.).                          | Meta     |
| `duplicate_flag`        | `1`                   | Flag for suspected duplicate rows (may be inconsistent).                   | Meta     |
| `misc`                  | `N/A`                 | Random extra field (contains meaningless or placeholder values).           | Meta     |
| `created_at`            | `2025-03-01T10:23:45` | Timestamp of record creation (UTC ISO format).                             | Meta     |
