import subprocess
import time
import cv2
import numpy as np
import struct




def get_screenshot(device_id: str = None) -> np.ndarray:
    """
    Захватываем «сырые» кадры RGBA без промежуточных файлов:
      • adb exec-out screencap (raw mode)
      • разбираем 12-байтовый заголовок (width, height, format)
      • получаем w*h*4 байт пикселей RGBA
      • конвертируем в BGR для OpenCV
    """
    # Comment translated to English.
    cmd = ["adb"]
    if device_id:
        cmd += ["-s", device_id]
    cmd += ["exec-out", "screencap"]

    # Comment translated to English.
    raw = subprocess.check_output(cmd)

    # Comment translated to English.
    if len(raw) < 12:
        raise RuntimeError("Unexpected screencap output: too short for header")
    w, h, fmt = struct.unpack("<III", raw[:12])
    if fmt != 1:  # 1 == RGBA_8888
        raise RuntimeError(f"Unsupported format code: {fmt}")

    # Comment translated to English.
    expected = w * h * 4
    body = raw[12:]
    if len(body) < expected:
        raise RuntimeError(f"Screencap truncated: got {len(body)} of {expected} bytes")

    # Comment translated to English.
    img_rgba = np.frombuffer(body[:expected], dtype=np.uint8).reshape((h, w, 4))

    # Comment translated to English.
    img_bgr = cv2.cvtColor(img_rgba, cv2.COLOR_RGBA2BGR)
    return img_bgr








def take_screenshot(device_id="131393852O003802", save=False):
    adb_command = ["adb", "-s", str(device_id), "exec-out", "screencap", "-p"]
    raw = subprocess.check_output(adb_command)

    img_array = np.frombuffer(raw, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        raise RuntimeError("Failed to decode the image")
    elif save:
        os.makedirs("cache", exist_ok=True)
        cv2.imwrite(f"cache/wos-{int(time.time())}.png", img)
    
    return img






t1 = time.time()
take_screenshot()

t2 = time.time()
print(t2-t1)




t1 = time.time()
get_screenshot()
t2 = time.time()
print(t2-t1)