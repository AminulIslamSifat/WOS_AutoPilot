import os
import sys
import cv2
import json
import time
import uvicorn
import numpy as np
from typing import Optional
from fastapi import FastAPI
from paddleocr import PaddleOCR
from pydantic import BaseModel

from cmd_program.screen_action import take_screenshot



app = FastAPI()


#initializeng the ocr once for all
ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False
    )




def clamp_roi(roi, width, height):
    x1, y1, x2, y2 = roi

    # clamp values inside image bounds
    x1 = max(0, min(x1, width - 1))
    y1 = max(0, min(y1, height - 1))
    x2 = max(0, min(x2, width))
    y2 = max(0, min(y2, height))

    # ensure valid rectangle
    if x2 <= x1 or y2 <= y1:
        return None

    return [x1, y1, x2, y2]



#input schema for fastapi
class OCRRequest(BaseModel):
    img_path: Optional[str] = None
    save_result: Optional[bool] = False
    rois: Optional[list[list[int]]] = None


class TemplateMatchRequest(BaseModel):
    name: str
    threshold: Optional[float] = None
    save_result: Optional[bool] = False


#loading all the ui elements from config
with open("config/ui_config.json", "r") as file:
    ui_element = json.load(file)


def match_template(name, threshold=None, save_result=None, get_all=False):
    #checking if the element data exist or not
    if name not in ui_element:
        template = cv2.imread(name)
    else:
        temp = ui_element[name]
        template = cv2.imread(temp["image"])
        if threshold == None:
            threshold  = temp["threshold"]
        
    if threshold is None:
        threshold = 0.8
        
    #loading threshold if not passed
    try:
        img = take_screenshot()
    except Exception as e:
        raise RuntimeError(f"Error loading image - {e}")
    

    if template is None:
        return None

    if len(img.shape) != len(template.shape):
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #getting the maximum matched result. when threshold is less than 1 there could be multiple result.
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_value, _, max_loc = cv2.minMaxLoc(result)
    print(max_value, max_loc)

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




def run_ocr(img_path=None, save_result=False, rois=None):
    if img_path:
        img = cv2.imread(img_path)
    else:
        img = take_screenshot()

    all_results = []

    # 👉 If ROI is provided
    if rois:
        h, w = img.shape[:2]
        for roi in rois:
            roi = clamp_roi(roi, w, h)
            
            if not roi:
                continue
            
            x1, y1, x2, y2 = roi

            cropped = img[y1:y2, x1:x2]

            output = ocr.predict(cropped)[0]

            results = [
                {
                    "text": text,
                    "score": float(score),
                    # shift box back to original image coords 😈
                    "box": (box + np.array([x1, y1, x1, y1])).tolist()
                }
                for text, score, box in zip(
                    output["rec_texts"],
                    output["rec_scores"],
                    output["rec_boxes"]
                )
            ]

            all_results.extend(results)

    # 👉 If no ROI → normal full image OCR
    else:
        output = ocr.predict(img)[0]

        all_results = [
            {
                "text": text,
                "score": float(score),
                "box": box.tolist()
            }
            for text, score, box in zip(
                output["rec_texts"],
                output["rec_scores"],
                output["rec_boxes"]
            )
        ]

    if save_result:
        output.save_to_img("test/debug")

    return all_results





@app.post("/ocr")
def ocr_endpoint(req:OCRRequest):
    results = run_ocr(req.img_path, req.save_result, req.rois)

    if results is None:
        return{
            "success" : False,
            "results" : None
        }

    return {
        "success" : True,
        "count" : len(results),
        "results" : results
    }



@app.post("/template")
def template_matching(req:TemplateMatchRequest):
    results = match_template(req.name, req.threshold, req.save_result)

    if results is None:
        return{
            "success" : False,
            "results" : None
        }

    return {
        "success" : True,
        "results" : results
    }



if __name__ == "__main__":
    uvicorn.run(
        "core.ocr:app",
        host="127.0.0.1",
        port=8000
    )




