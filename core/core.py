import time
import requests
from cmd_program.screen_action import tap_screen
from concurrent.futures import ThreadPoolExecutor





ocr_url = "http://127.0.0.1:8000/ocr"
template_matching_url = "http://127.0.0.1:8000/template"



def create_box(coord, radius):
    """
    Create a padded search region around a coordinate box or point.

    coord formats:
        - (x, y)
        - (x1, y1, x2, y2)

    returns:
        [x1, y1, x2, y2]
    """

    def pad_box(x1, y1, x2, y2):
        return [
            x1 - radius,
            y1 - radius,
            x2 + radius,
            y2 + radius
        ]

    if len(coord) == 2:
        x, y = coord
        return pad_box(x, y, x, y)

    if len(coord) == 4:
        return pad_box(*coord)

    raise RuntimeError(f"Invalid coordinate format: {coord}")





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



def req_temp_match(name, threshold=None, save_result=None):
    payload = {
        "name" : name,
        "threshold" : threshold,
        "save_result": save_result
    }

    response = requests.post(template_matching_url, json=payload)
    data = response.json()

    if data["success"] != True:
        return None
    
    results = data["results"]
    result = (results["x"], results["y"])
    return result


def tap_on_template(name, threshold=None, save_result=None, wait=None, tap=True):
    def try_match():
        coord = req_temp_match(name, threshold, save_result)
        if coord and tap:
            tap_screen(coord)
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
            return True

    return None








def tap_on_templates_batch(
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

