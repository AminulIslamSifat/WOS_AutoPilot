from core.core import (
    req_ocr,
    req_temp_match,
    tap_on_template,
    tap_on_text
)
import time
from core.recalibrate import recalibrate
from cmd_program.screen_action import swipe_screen, tap_screen



def gather():
    print("Started Gathering...")
    search_box = [[0, 1940, 1080,1980]]
    gathering_nodes = ["meat", "wood", "coal", "iron", "coal"]

    recalibrate()
    time.sleep(2)

    tap_on_text("Home.World", sleep=2)

    try:
        res = req_ocr(rois=[[294, 421, 364, 463]])
        data = res[0]['text'].split("/")
        remaining_march = int(data[1])-int(data[0])
    except Exception as e:
        print(f"Reading Error - {e}")
        remaining_march = 4
    
    i = 0
    while remaining_march>0 and i<5:
        print(f"Remaining march queue: {remaining_march}")
        tap_on_template("World.Search", sleep=1)
        found = tap_on_text(gathering_nodes[i], rois=search_box, sleep=1)
        if found is None:
            swipe_screen(1000, 1920, 0, 1920)
            tap_on_text(gathering_nodes[i], rois=search_box, sleep=1)
        
        #from here its needs to be optimized
        tap_on_text("World.Search.Search", sleep=3)
        tap_on_text("World.Search.Gather", sleep=1)
        tap_on_template("World.Deploy.RemoveHero", threshold=0.6, rois=[[300, 500, 400, 650]]) #removing hero
        tap_on_text("World.Deploy.Deploy", sleep=1)

        i = i+1

        try:
            res = req_ocr(rois=[[294, 421, 364, 463]])
            data = res[0]['text'].split("/")
            remaining_march = int(data[1])-int(data[0])
        except Exception as e:
            print(f"Reading Error - {e}")
            remaining_march = remaining_march - 1
    
    print("Completed the gathering task, Returning to homepage...")
    recalibrate()



gather()