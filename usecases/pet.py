import time
from core.recalibrate import recalibrate

from core.core import (
    req_ocr,
    req_text,
    tap_on_text,
    req_temp_match,
    tap_on_template,
    tap_on_templates_batch
)
from cmd_program.screen_action import(
    tap_screen,
    swipe_screen,
    input_text
)

def collect_ally_treasure():
    recalibrate()
    tap_on_template("Home.Pet", wait=2)
    tap_on_text("Home.Pet.Skill.BeastCage", sleep=1, wait=2)
    tap_on_text("Home.Pet.BeastCage.Adventure", wait=2)
    tap_on_text("Home.Pet.BeastCage.Adventure.AllyTreasure", wait=2, align=[0, -50])
    tap_on_text("Home.Pet.BeastCage.Adventure.AllyTreasure.AllianceShares", wait=2, sleep=0.5)
    tap_on_text("Home.Pet.BeastCage.Adventure.AllyTreasure.AllianceShares.ClaimAll", wait=2)
    tap_on_text("Tap anywhere to exit", sleep=1)
    tap_on_text("Home.Pet.BeastCage.Adventure.AllyTreasure.MyShares", wait=2)
    tap_on_text("Home.Pet.BeastCage.Adventure.AllyTreasure.MyShares.Share", wait=2, sleep=1)
    return True



def start_pet_exploration():
    exploration_roi = [0, 400, 1080, 2200]
    recalibrate()
    tap_on_template("Home.Pet", wait=2)
    tap_on_text("Home.Pet.Skill.BeastCage", sleep=1, wait=2)
    tap_on_text("Home.Pet.BeastCage.Adventure", wait=2, sleep=1)
    text = req_text(["Home.Pet.BeastCage.Adventure.RemainingAttempt", "Home.Pet.BeastCage.Adventrue.AdventureGround"])
    adventuring = 0
    remaining_attempts = 4
    try:
        remaining_attempts = int(text[0][0])
        for t in text:
            if len(t[0].split(":")) == 3:
                adventuring += 1
    except Exception as e:
        print(f"Reading Error - {e}, Exiting the task...")
        return None
    print(adventuring, remaining_attempts)

    status = True
    while(status):
        status = tap_on_template("Home.Pet.BeastCage.Adventure.CompletedAdventure", wait=2)
        if not status:
            print("No adventure Completed")
            break
        if tap_on_text("Home.Pet.BeastCage.Adventure.Completed", wait=2, tap=False):
            tap_screen(560, 1540)
            time.sleep(1)

    while(adventuring<3 and remaining_attempts>0):
        print("hi")
        try:
            remaining_attempts = int(text[0][0])
            for t in text:
                if len(t[0].split(":")) == 3:
                    adventuring += 1
        except Exception as e:
            print(f"Reading Error - {e}, Exiting the task...")
            adventuring += 1
            remaining_attempts -= 1

        treasure_boxs = [
            "Home.Pet.BeastCage.Adventure.RedTreasure.png",
            "Home.Pet.BeastCage.Adventure.PurpleTreasure.png",
            "Home.Pet.BeastCage.Adventure.BlueTreasure.png"
        ]
        for treasure_box in treasure_boxs:
            status = tap_on_template(treasure_box, wait=2)
            if not status:
                continue
            status = tap_on_text("Home.Pet.BeastCage.Adventure.SelectPet", wait=2, sleep=1)
            if status:
                continue
            status = tap_on_text("Home.Pet.BeastCage.Adventure.Completed", wait=2, tap=False)
            if status:
                tap_screen(560, 1540)
                time.sleep(1)
            else:
                print("Something went wrong")

    #some more logic
    print("Sent pet to adventure, Returning to homepage...")
    return True

def activate_reward_pet_skill():
    return

def activate_war_pet_skill():
    return



