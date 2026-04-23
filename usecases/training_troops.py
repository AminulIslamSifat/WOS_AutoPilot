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


side_panel = [0, 690, 670, 1650]
training_menu = [250, 1400, 930, 1800]


def train():

    recalibrate()

    status = tap_on_template("Global.SidePanel", sleep=1)

    if not status:
        print("Side Panel Not found, Exiting The Task")
        return None

    tap_on_text("Infantry", rois=[side_panel], sleep=1)
    tap_on_text("Train", rois = [training_menu], sleep=1)

    tap_screen(550, 1100)            #Taping at the middle of the screen to remove the tutorial hand icon
    
    status = tap_on_text("Home.TroopTraining.Train", sleep=1)
    if not status:
        print("Infantry Training is not finished yet, Skipping Infantry...")

    tap_on_text("Home.TroopTraining.LancerCamp", sleep=1)
    status = tap_on_text("Home.TroopTraining.Train", sleep=1)
    if not status:
        print("Lancer Training is not finished yet, Skipping Lancer...")

    tap_on_text("Home.TroopTraining.MarksmanCamp", sleep=1)
    status = tap_on_text("Home.TroopTraining.Train", sleep=1)
    if not status:
        print("Marksman Training is not finished yet, Skipping Marksman...")

    return True



def train_infantry(Amount=None):

    recalibrate()

    status = tap_on_template("Global.SidePanel", sleep=1)
    if not status:
        print("Side Panel Not found, Exiting The Task")
        return None

    tap_on_text("Infantry", rois=[side_panel], sleep=1)
    tap_on_text("Train", rois = [training_menu], sleep=1)

    tap_screen(550, 1100)            #Taping at the middle of the screen to remove the tutorial hand icon
    traned = 0

    while(trained < Amount):
        training_amount = req_text("Home.TroopTraining.TrainingAmount")
        try:
            training_amount = int(training_amount[0])
            trained += training_amount
        except Exception as e:
            print(f"Training Amount can't be read, Only training for one time - {e}")
            tap_on_text("Home.TroopTraining.Train", sleep=1)
            break

        tap_on_text("Home.TroopTraining.Train", sleep=1)
        status = tap_on_text("Home.TroopTraining.Speedup", sleep=1)

        if status:
            status = tap_on_text("Home.TroopTraining.Speedup.QuickUse", sleep=1)
        if status:
            tap_on_text("Home.TroopTraining.Speedup.QuickUse.Use", sleep=1)
        


def train_lancer(Amount=None):

    recalibrate()

    status = tap_on_template("Global.SidePanel", sleep=1)
    if not status:
        print("Side Panel Not found, Exiting The Task")
        return None

    tap_on_text("Lancer", rois=[side_panel], sleep=1)
    tap_on_text("Train", rois = [training_menu], sleep=1)
    
    tap_screen(550, 1100)            #Taping at the middle of the screen to remove the tutorial hand icon
    traned = 0

    while(trained < Amount):
        training_amount = req_text("Home.TroopTraining.TrainingAmount")
        try:
            training_amount = int(training_amount[0])
            trained += training_amount
        except Exception as e:
            print(f"Training Amount can't be read, Only training for one time - {e}")
            tap_on_text("Home.TroopTraining.Train", sleep=1)
            break

        tap_on_text("Home.TroopTraining.Train", sleep=1)
        status = tap_on_text("Home.TroopTraining.Speedup", sleep=1)

        if status:
            status = tap_on_text("Home.TroopTraining.Speedup.QuickUse", sleep=1)
        if status:
            tap_on_text("Home.TroopTraining.Speedup.QuickUse.Use", sleep=1)



def train_marksman(Amount=None):
    
    recalibrate()

    status = tap_on_template("Global.SidePanel", sleep=1)
    if not status:
        print("Side Panel Not found, Exiting The Task")
        return None

    tap_on_text("Marksman", rois=[side_panel], sleep=1)
    tap_on_text("Train", rois = [training_menu], sleep=1)

    tap_screen(550, 1100)            #Taping at the middle of the screen to remove the tutorial hand icon
    traned = 0

    while(trained < Amount):
        training_amount = req_text("Home.TroopTraining.TrainingAmount")
        try:
            training_amount = int(training_amount[0])
            trained += training_amount
        except Exception as e:
            print(f"Training Amount can't be read, Only training for one time - {e}")
            tap_on_text("Home.TroopTraining.Train", sleep=1)
            break

        tap_on_text("Home.TroopTraining.Train", sleep=1)
        status = tap_on_text("Home.TroopTraining.Speedup", sleep=1)

        if status:
            status = tap_on_text("Home.TroopTraining.Speedup.QuickUse", sleep=1)
        if status:
            tap_on_text("Home.TroopTraining.Speedup.QuickUse.Use", sleep=1)
