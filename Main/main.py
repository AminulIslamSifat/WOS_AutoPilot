import os
import sys
import cv2
import time
import json
import requests
import numpy as np

from cmd_program.screen_action import (
    tap_screen,
    swipe_screen,
    long_press,
    take_screenshot
)

from core.core import (
    req_ocr,
    req_temp_match,
    create_box,
    tap_on_templates_batch,
    tap_on_template
)

from core.exploration import(
    claim_exploration_idle_income,
    continue_exploring
)




res = req_ocr(rois=[[300, 1725, 665, 1830]])
res = [t["text"] for t in res if t["score"] > 0.9]
print(res)