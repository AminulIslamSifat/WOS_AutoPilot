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
    create_box
)























t1 = time.time()
response = req_temp_match("assets/global/reconnect.jpg")
t2 = time.time()
if response:
    print(response)
print(f"Time taken: {t2-t1} seconds")

