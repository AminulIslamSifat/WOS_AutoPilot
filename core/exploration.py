import time
import json

from core.recalibrate import(
    recalibrate
)
from cmd_program.screen_action import(
    tap_screen
)
from core.core import(
    req_ocr,
    req_temp_match,
    create_box,
    tap_on_template,
    tap_on_templates_batch
)





with open("config/ui_config.json") as file:
    ui_element = json.load(file)





def claim_exploration_idle_income():
    def ensure_exploration_open():
        coord = req_temp_match("exploration")
        if coord is None:
            recalibrate()
        tap_on_template("exploration")

    def perform_claim():
        tap_on_template("exploration_claim")
        return tap_on_template("exploration_final_claim")

    def collect_rewards():
        time.sleep(2)
        for _ in range(2):
            tap_screen(540, 1750)

    # --- Flow ---
    ensure_exploration_open()

    coord = perform_claim()
    if not coord:
        recalibrate()
        return

    collect_rewards()
    recalibrate()


    



def continue_exploring(stopping_level=None):
    def ensure_open_exploration():
        if not tap_on_template("exploration"):
            recalibrate()
            tap_on_template("exploration")

    def setup_exploration():
        tap_on_template("exploration_explore")
        tap_on_template("exploration_quick_deploy")

    def handle_auto_mode(is_auto):
        if not is_auto:
            return False, None

        if not tap_on_template("exploration_return_to_city", wait=30, tap=False):
            return True, None

        results = tap_on_templates_batch(
            [
                "exploration_retry",
                "exploration_auto_challenge_checked",
                "exploration_auto_challenge_unchecked"
            ],
            tap=[False, True, False]
        )

        retry_found = results[0]

        if retry_found:
            tap_on_template("exploration_return_to_city", wait=30)
            return False, "failed"

        return False, None

    def handle_continue_or_exit():
        if tap_on_template("exploration_continue_button", wait=30):
            return None

        if tap_on_template("exploration_return_to_city"):
            return True

        return False

    # --- start ---
    ensure_open_exploration()
    setup_exploration()


    is_auto = True

    while True:

        if stopping_level:
            texts = req_ocr(rois=[[480, 270, 600, 400]])
            texts = [t["text"] for t in texts if t["score"] > 0.9]
            level = int(texts[0])
            if level > stopping_level:
                print("Exploration Completed...")
                recalibrate()
                break

        tap_on_template("exploration_fight")

        is_auto, status = handle_auto_mode(is_auto)

        if status == "failed":
            break

        result = handle_continue_or_exit()

        if result is None:
            continue

        return result

