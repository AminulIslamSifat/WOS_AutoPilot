#coming soon
import time
from core.core import (
    tap_on_template,
    tap_on_text,
    req_text,
    tap_on_templates_batch
)
from cmd_program.screen_action import(
    tap_screen,
    swipe_screen
)
from core.recalibrate import recalibrate









def change_account(next_email):
    recalibrate()
    tap_screen(100, 170)
    tap_on_text("ChiefProfile.Settings", wait=2)
    tap_on_text("ChiefProfile.Settings.Account", wait = 2, sleep=2)
    tap_on_text("ChiefProfile.Settings.Account.ChangeAccount", wait=5, sleep=0.5)
    tap_on_text("ChiefProfile.Settings.Account.ChangeAccount.SignInWithGoogle", wait=5)
    status = tap_on_text(next_email, wait=5)
    if not status:
        swipe_screen(550, 1800, 550, 400)
        status = tap_on_text(next_email, wait=10)
        if not status:
            print("Email not found, Exiting...")
            return None
    tap_on_text("ChiefProfile.Settings.Account.ChangeAccount.SignInWithGoogle.Continue", wait=20, sleep=2)
    recalibrate(timeout=80)
    return True




def change_character(next_name):
    recalibrate()
    tap_screen(100, 170)
    tap_on_text("ChiefProfile.Title", wait=2, tap=False)
    time.sleep(1)
    text = req_text("ChiefProfile.Title")[0][0]
    if text.lower() != "chief profile":
        print("Chief Profile not found, Exiting...")
        return None
    tap_on_text("ChiefProfile.Settings", wait=1)
    tap_on_text("ChiefProfile.Settings.Characters", wait=2)
    time.sleep(1)
    players = req_text(
        ["ChiefProfile.Settings.Characters.FirstCharacterName",
        "ChiefProfile.Settings.Characters.SecondCharacterName"]
    )
    names = [player[0].split(']')[1].lower() for player in players]
    if next_name.lower() not in names:
        print("Character not found, Exiting...")
        return None
    index = names.index(next_name.lower())
    status = tap_on_text(players[index][0], rois=[0, 1000, 1080, 1450])
    
    if not status:
        print("Finding player failed")
        return None

    tap_on_text("ChiefProfile.Settings.Characters.Login.Confirm", wait=2, sleep=2)
    recalibrate(timeout=80)
    return True



