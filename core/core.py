import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import json
import requests
from pathlib import Path
from cmd_program.screen_action import tap_screen
from concurrent.futures import ThreadPoolExecutor





ocr_url = "http://127.0.0.1:8000/ocr"
template_matching_url = "http://127.0.0.1:8000/template"


#------------------- DataBase --------------------------#
text_area = {}
template_area = {}


def init_database():
    global text_area, template_area

    with open("references/icon/template_config.json") as f:
        template_area = json.load(f)

    files = [f for f in Path("references/TextArea").rglob("*.json") if f.is_file()]

    for file in files:
        try:
            with open(file, "r") as f:
                data = json.load(f)

                if isinstance(data, dict):
                    text_area.update(data)
                else:
                    print(f"Skipped non-dict file: {file}")

        except Exception as e:
            print(f"Error in {file} - {e}")






def req_ocr(img_path=None, save_result=None, rois=None):
    payload = {
        "img_path": img_path,
        "save_result" : save_result,
        "rois": rois
    }

    response = requests.post(ocr_url, json=payload)
    data = response.json()

    if data["success"] != True:
        return None
    
    result = data["results"]
    return result



def req_temp_match(name, threshold=0.8, save_result=None, rois=None):
    payload = {
        "name" : name,
        "threshold" : threshold,
        "save_result": save_result,
        "rois": rois
    }

    response = requests.post(template_matching_url, json=payload)
    data = response.json()

    if data["success"] != True:
        return None
    
    results = data["results"]
    return results



def tap_on_template(name, threshold=None, save_result=None, wait=None, sleep=None, tap=True, rois=None):
    if name in template_area:
        if threshold == None:
            threshold = (template_area[name]["threshold"] or 0.8)
        rois = template_area.get(name,{}).get("box", None)
    
    if not threshold:
        threshold = 0.8

    def try_match():
        results = req_temp_match(name, threshold, save_result, rois)
        if not results:
            return None
        result = max(results, key=lambda x:x["score"])
        coord = result["box"]
        coord = ((coord[0]+coord[2])//2, (coord[1]+coord[3])//2)

        if coord and tap:
            tap_screen(coord)

            if sleep:
                time.sleep(sleep)

        return bool(coord)

    # --- wait mode ---
    if wait:
        start = time.time()
        while time.time() - start < wait:
            if try_match():
                return True
        return None

    # --- retry mode ---
    for _ in range(3):
        if try_match():
            print(f"Pressed on - {name}")
            return True
        else:
            print(f"No match found for - {name}")

    return None



def tap_on_text(text, img_path=None, save_result=None, rois=None, wait=None, sleep=None, skip_ocr=False, tap=True):
    def normalize_rois(box):
        if box is None:
            return None

        # already correct format [[...]]
        if isinstance(box, list) and len(box) == 1 and isinstance(box[0], list):
            return box

        # single box → wrap it
        if isinstance(box, list) and len(box) == 4:
            return [box]

        print("Invalid ROI format:", box)
        return None

    def load_config(text, rois=None):
        if isinstance(text, str):
            text = [text]

        text_data = {}

        for t in text:
            if t in text_area:
                item = text_area[t].copy()
            else:
                item = {"text": t, "score": None, "box": None}

            if rois is not None:
                item["box"] = rois

            text_data[t] = item

        return text_data


    def try_match(texts):
        for key, value in texts.items():
            target_text = value["text"]
            box = value["box"]

            if skip_ocr and box is not None:
                coord = (
                    (box[0] + box[2]) // 2,
                    (box[1] + box[3]) // 2
                )
                if coord and tap:
                    tap_screen(coord)
                    print(f"Pressed on {target_text}, Skipped OCR")
                if sleep:
                    time.sleep(sleep)
                return True

            box = normalize_rois(box)
            res = req_ocr(img_path, save_result, rois=box)

            if res is None:
                print("OCR failed")
                continue

            for item in res:
                if item["text"].lower() == target_text.lower():

                    use_box = item.get("box")
                    if not use_box:
                        continue

                    coord = (
                        (use_box[0] + use_box[2]) // 2,
                        (use_box[1] + use_box[3]) // 2
                    )
                    if coord and tap:
                        tap_screen(coord)
                        print(f"Pressed on {item["text"]}")

                    if sleep:
                        time.sleep(sleep)

                    return True

        return False


    # ✅ FIXED POSITION (outside try_match)
    texts = load_config(text, rois=rois)

    if not texts:
        print("No text to press on")
        return None

    if wait:
        start = time.time()

        while time.time() - start < wait:
            if try_match(texts):
                return True

        print(f"No match found for the text - {texts[text]["text"]}")
        return None

    for _ in range(3):
        if try_match(texts):
            return True

    print(f"No match found for the text - {texts[text]["text"]}")
    return None






def find_templates_batch(
    names,
    thresholds=None,
    save_results=None,
    wait=None,
    tap=False
):
    """
    names: list of template names
    thresholds: list or None
    save_results: list or None
    wait: timeout per batch loop
    tap: whether to tap when found
    """

    n = len(names)

    thresholds = thresholds or [None] * n
    save_results = save_results or [None] * n
    tap = tap or [None] * n

    def match_one(i):
        coord = req_temp_match(names[i], thresholds[i], save_results[i])
        if coord and tap[i]:
            tap_screen(coord)
        return bool(coord)

    def run_batch():
        with ThreadPoolExecutor(max_workers=n) as ex:
            return list(ex.map(match_one, range(n)))

    # --- wait mode ---
    if wait:
        start = time.time()
        while time.time() - start < wait:
            result = run_batch()
            if any(result):
                return result
        return [False] * n

    # --- retry mode ---
    for _ in range(3):
        result = run_batch()
        if any(result):
            return result

    return [False] * n




init_database()