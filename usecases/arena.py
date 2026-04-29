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





def challenge_lowest_power():
    challenge_icons = [
        {'box': [883, 815, 986, 920]}, 
        {'box': [883, 1007, 986, 1112]}, 
        {'box': [883, 1200, 986, 1305]}, 
        {'box': [883, 1392, 986, 1497]}, 
        {'box': [883, 1585, 986, 1690]}
    ]
    powers = []
    res = req_ocr(rois=[[220, 815, 986, 1690]])
    try:
        for item in res:
            text = item.get("text", "")
            text = text.replace(",", "").replace(".", "")
            if text.endswith("M") and text[:-1].isdigit():
                powers.append(int(text[:-1])*100000)
            elif text.isdigit() and int(text) > 50000:
                powers.append(int(text))
    except Exception as e:
        print(f"Power Reading Error - {e}")

    if powers:
        lowest_power = min(powers) if len(powers) > 0 else 0
        i = powers.index(lowest_power)
        tap_on_template("Home.Arena.Challenge.Challenge", rois=[challenge_icons[i]["box"]], wait=2)
    else:
        tap_on_template("Home.Arena.Challenge.Challenge", wait=2)




def find_arena():
    print("Swiping down the screen to find arena")
    for i in range(7):
        swipe_screen(1000, 1200, 100, 1200)
        time.sleep(0.5)
    for i in range(8):
        swipe_screen(540, 2000, 540, 1000)
        time.sleep(0.5)
    for i in range(3):
        swipe_screen(540, 1000, 420, 1850)
        time.sleep(1)
        available = tap_on_template("Home.Arena", threshold=0.5, wait=2)
        if available:
           break 

    if not available:
        return None
    return True



def arena():
    attempt = 0
    recalibrate()
    print("Starting the fight in Arena of Glory...")

    availabe = find_arena()
    if not availabe:
        print("Arena challenge is not availabe, Ending the task")
        return None
    tap_on_text("Home.Arena.Challenge", wait=2, sleep=1)

    res = req_ocr(rois=[[300, 1725, 665, 1830]])

    try:
        attempt = int(res[0]['text'].split(":")[1])
    except Exception as e:
        print(f"Attempt Reading error -{e}")

    while(attempt > 0):
        res = req_ocr(rois=[[300, 1725, 665, 1830]])
        try:
            attempt = int(res[0]['text'].split(":")[1])-1
            print(f"Remaining Challenge {attempt}")
        except Exception as e:
            print(f"Attempt counting error -{e}")

        challenge_lowest_power()

        tap_on_text("Home.Arena.Challenge.Challenge.QuickDeploy", sleep=0.1)
        tap_on_text("Home.Arena.Challenge.Challenge.Fight", wait=2, sleep=3)
        tap_on_template("Home.Arena.Challenge.Challenge.Fight.Pause", wait=5)
        tap_on_template("Home.Arena.Challenge.Challenge.Fight.Pause.Retreat", wait=2)
        status = tap_on_text("Home.Arena.Challenge.Challenge.Fight.End.Title", tap=False, wait=3)
        if status:
            tap_on_text("Home.Arena.Challenge.Challenge.Fight.End.TapAnywhereToExit", wait=2)
            tap_on_text("Home.Arena.Challenge.FreeRefresh", wait=2)
        else:
            tap_on_text("Home.Arena.Challenge.Challenge.Fight.End.TapAnywhereToExit", wait=5)
        
    print("Finished the task - Arena Of Glory, Returning to homepage...")
    recalibrate()



