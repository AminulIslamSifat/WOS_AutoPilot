import time

from core.core import (
    req_ocr,
    req_temp_match,
    tap_on_template
)
from core.recalibrate import (
    recalibrate
)
from cmd_program.screen_action import (
    tap_screen,
    swipe_screen
)

def arena():
    recalibrate()
    for i in range(5):
        swipe_screen(1000, 1200, 100, 1200)
        time.sleep(0.3)
    for i in range(6):
        swipe_screen(540, 2000, 540, 1000)
        time.sleep(0.3)
    for i in range(2):
        swipe_screen(540, 1000, 450, 1900)
        time.sleep(0.3)

    time.sleep(2)
    tap_on_template("arena", threshold=0.6)
    time.sleep(1)
    tap_on_template("arena_challenge")
    time.sleep(1)
    res = req_ocr(rois=[[300, 1725, 665, 1830]])
    res = [t["text"] for t in res if t["score"] > 0.9]
    try:
        attemp = int(res[1])-1
    except Exception as e:
        print(e)
    while(attemp > 0):
        res = req_ocr(rois=[[300, 1725, 665, 1830]])
        res = [t["text"] for t in res if t["score"] > 0.9]
        try:
            attemp = int(res[1])-1
        except Exception as e:
            print(e)

        tap_on_template("arena_select_opponent")
        time.sleep(1)
        tap_on_template("arena_quick_deploy")
        time.sleep(1)
        tap_on_template("arena_fight")
        time.sleep(4)
        tap_on_template("arena_pause")
        time.sleep(1)
        tap_on_template("arena_retreat")
        res = tap_on_template("arena_replay", wait=10, tap=False)
        
        if res:
            tap_screen(540, 2300)
            time.sleep(2)
        else:
            print("Error")





arena()