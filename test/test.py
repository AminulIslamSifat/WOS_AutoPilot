import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import json
import time
import uvicorn
import numpy as np
from typing import Optional
from fastapi import FastAPI
from paddleocr import PaddleOCR
from pydantic import BaseModel

from core.core import req_ocr

from cmd_program.screen_action import take_screenshot




def match_template(img, template, threshold=None, save_result=False):
    #checking if the element data exist or not
    img = cv2.imread(img)
    template = cv2.imread(template)
        
    if threshold is None:
        threshold = 0.8
        

    #getting the maximum matched result. when threshold is less than 1 there could be multiple result.
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_value, _, max_loc = cv2.minMaxLoc(result)
    print(f"Location: {max_loc}, Confidence: {max_value}")

    if (max_value < threshold):
        if save_result:
            cv2.imwrite(f"test/debug/{time.time()}.png", img)
        return None

    #result returns the top-left location of the match. 
    h, w = template.shape[:2]
    #pointing to the middle of the matched box
    x = max_loc[0] + w//2
    y = max_loc[1] + h//2

    #saving the result for future debugging
    if save_result:
        debug_img = img.copy()
        cv2.rectangle(debug_img, max_loc, (max_loc[0]+w, max_loc[1]+h), (0,0,255), 2)
        cv2.imwrite(f"test/debug/{time.time()}.png", debug_img)

    return {"x" : x, "y" : y}




path = "cache/chief_profile.json"

with open(path, "r") as file:
    data = json.load(file)


rois = []
for res in data:
    rois.append(res["box"])

print(rois)



res = req_ocr(rois=rois, save_result=True)
for r in res:
    print(r["text"])
