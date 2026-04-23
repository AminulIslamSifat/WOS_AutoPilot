import os
import sys
import cv2
import time
import json
import requests
import numpy as np
from datetime import datetime

from cmd_program.screen_action import (
    tap_screen,
    swipe_screen,
    long_press,
    take_screenshot
)

from core.core import (
    req_ocr,
    req_temp_match,
    tap_on_template,
    req_text
)

from usecases.exploration import(
    claim_exploration_idle_income,
    continue_exploring
)
from usecases.alliance import(
    tech_contribution,
    auto_join,
    collect_chests,
    help
)
from usecases.vip import (
    collect_vip_rewards,
    buy_vip_time
)
from usecases.heal import (
    heal
)
from usecases.arena import (
    arena
)
from usecases.mail import (
    collect_mail_rewards
)
from usecases.training_troops import(
    train,
    train_lancer,
    train_infantry,
    train_marksman
)
from core.recalibrate import recalibrate
from core.change_player import change_account, change_character

from usecases.gather import gather





class Player:
    def __init__(self, name, id, state, email, stamina):
        self.name = name
        self.id = id
        self.state = state
        self.email = email 
        self.stamina = stamina


COMPLETION_LOG_PATH = "db/completion_log.txt"
SKIP_WINDOW_SECONDS = 3 * 60 * 60


def load_completion_log():
    records = {}

    if not os.path.exists(COMPLETION_LOG_PATH):
        return records

    with open(COMPLETION_LOG_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split("|")
            if len(parts) < 2:
                continue

            player_id = parts[0].strip().lower()
            try:
                ts = float(parts[1].strip())
            except ValueError:
                continue

            records[player_id] = ts

    return records


def save_completion_log(records):
    lines = []
    for player_id, ts in sorted(records.items()):
        iso_time = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"{player_id}|{ts}|{iso_time}")

    with open(COMPLETION_LOG_PATH, "w") as f:
        f.write("\n".join(lines))
        if lines:
            f.write("\n")


def should_skip_player(player_id, records):
    ts = records.get(player_id.lower())
    if ts is None:
        return False
    return (time.time() - ts) < SKIP_WINDOW_SECONDS


def mark_player_completed(player_id, records):
    records[player_id.lower()] = time.time()
    save_completion_log(records)




def init_database():
    global player_data, email_list, player_list
    path = "db/account.json"
    with open(path) as f:
        player_data = json.load(f)
    
    sorted_player_data = sorted(
        player_data.items(),
        key = lambda item: item[1].get("priority", float("inf"))
    )

    player_list = []
    email_list = []

    for email, data in sorted_player_data:
        email_list.append(email)
        for player in data["player"]:
            player_list.append(player["id"])

    player_data = sorted_player_data



def player_initialization():
    recalibrate()
    tap_screen(50, 150)
    time.sleep(2)
    global current_player
    try:
        page_title = req_text("ChiefProfile.Title")[0]
        if page_title.lower() != "Chief Profile".lower():
            print("Failed to load chief profile")
            return None
    except Exception as e:
        print(f"Reading error - {e}, Ending the task")
        return None

    data = req_text(["ChiefProfile.PlayerName", "ChiefProfile.PlayerID", "ChiefProfile.FurnaceLevel", "ChiefProfile.Stamina", "ChiefProfile.State"])
    name, id, furnace, state = (data[0].split(']')[1], data[1].split(':')[1], data[2], data[4].split('#')[1])
    stamina = data[3].split('/')[0]
    
    current_player_id = None
    current_email = None

    for email, info in player_data:
        for player in info["player"]:
            if player.get("id") == id.lower():
                current_player_id = player.get("id")
                current_email = email

    if current_player_id is None or current_email is None:
        print("No player data found for this ID, Exiting this character...")
        raise RuntimeError("Player Initialization Failed, Stopping the Bot...")

    current_player = Player(name, id, state, current_email, stamina)
    print(f"    Email: {current_email}\n    Name:{name}\n    ID: {id}\n    Furnace Level: {furnace}\n    Stamina: {stamina}\n    State: {state}")
    
    



init_database()


def get_next_email(current_email):
    if not email_list:
        return None

    try:
        idx = email_list.index(current_email)
        return email_list[(idx + 1) % len(email_list)]
    except ValueError:
        return email_list[0]


def get_players_by_email(target_email):
    for email, info in player_data:
        if email == target_email:
            return info.get("player", [])
    return []



def run_task(current_player_id):
    collect_vip_rewards()
    claim_exploration_idle_income()
    collect_mail_rewards()
    train()
    arena()
    #Alliance
    auto_join()
    collect_chests()
    tech_contribution()
    help()
    #World
    heal()
    if current_player_id == "578380047":
        gather(remove_hero=True, equalize=False)
    else:
        gather(remove_hero=False, equalize=True)




def run_bot():
    completion_records = load_completion_log()

    while True:
        player_initialization()

        #----Config----
        current_email = current_player.email
        next_email = get_next_email(current_email)

        #----- Run all characters under current email -----
        current_email_players = get_players_by_email(current_email)
        if not current_email_players:
            raise RuntimeError(f"No players configured for email: {current_email}")

        processed_ids = set()

        while len(processed_ids) < len(current_email_players):
            active_id = current_player.id.lower()
            if active_id not in processed_ids:
                if should_skip_player(current_player.id, completion_records):
                    last_ts = completion_records.get(active_id)
                    last_time = datetime.fromtimestamp(last_ts).strftime("%Y-%m-%d %H:%M:%S")
                    print(f"Skipping {current_player.name} ({current_player.id}) - completed recently at {last_time}")
                else:
                    print(f"Running tasks for: {current_player.name} ({current_player.id})")
                    run_task(current_player.id)
                    mark_player_completed(current_player.id, completion_records)
                    print(f"Marked completed: {current_player.id} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                processed_ids.add(active_id)

            next_player = next(
                (p for p in current_email_players if p["id"].lower() not in processed_ids),
                None,
            )

            if not next_player:
                break

            print(f"Switching to sibling character: {next_player['name']}")
            change_character(next_player["name"])
            player_initialization()

            if current_player.email != current_email:
                raise RuntimeError(
                    f"Unexpected email after character switch. Expected {current_email}, got {current_player.email}"
                )

        print(f"Progressing to the next email: {next_email}")
        status = change_account(next_email)
        if not status:
            raise RuntimeError("Account changing error")



if __name__=="__main__":
    run_bot()
