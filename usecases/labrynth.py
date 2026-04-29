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



def labrynth():
    recalibrate()
    labrynth_list = [
        "Home.Labrynth.CaveOfMonster",
        "Home.Labrynth.CharmMine",
        "Home.Labrynth.ResearchCenter",
        "Home.Labrynth.GearForge"
    ]
    status = tap_on_template("Home.Labrynth", sleep=1)
    if not status:
        print("Labrynth task is already completed, Exiting the task")
        return None
    
    for lab in labrynth_list:
        status = tap_on_text(lab, wait=2)
        if not status:
            continue
        status = tap_on_text("Home.Labrynth.Raid", wait=2)
        if status:
            tap_on_text("Home.Labrynth.Raid.Claim", wait=2)
        status = tap_on_text("Home.Labrynth.Challenge", wait=2)
        if not status:
            continue
        status = tap_on_text("Home.Labrynth.Challenge.Deploy", wait=2)
        if not status:
            tap_on_template("Global.Back")
            continue
        
        while True:
            tap_on_text("Home.Labrynth.Challenge.Skip", wait=3, threshold=0.5)
            status = tap_on_text("Home.Labrynth.Challenge.Victory.Title", wait=2, tap=False)
            if status:
                status = tap_on_text("Home.Labrynth.Challenge.Victory.Next", wait=2)
                if not status:
                    tap_on_text("Home.Labrynth.Challenge.Victory.NextChapter", wait=2, sleep=4)
                    tap_on_text("Home.Labrynth.Challenge", wait=2)
                    tap_on_text("Home.Labrynth.Challenge.Deploy", wait=2)
                continue
            status = tap_on_text("Home.Labrynth.Challenge.Defeat.Title", wait=2, tap=False)
            if status:
                remaining_attempts = 0

                try:
                    remaining_attempts = req_text("Home.Labrynth.Challenge.Defeat.RemainingAttempts")
                    remaining_attempts = int(remaining_attempts[0][0])
                    if remaining_attempts > 5 or remaining_attempts == 0:
                        remaining_attempts = 0
                except Exception as e:
                    remaining_attempts = 0
                
                if remaining_attempts == 0:
                    tap_screen(550, 2000)
                    time.sleep(1)
                    tap_on_template("Global.Back")
                    break

                tap_on_text("Home.Labrynth.Challenge.Defeat.Retry", wait=2)
        

    return True


