from pathlib import Path

import cv2
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cmd_program.screen_stream import screen_capture, start_screen_stream, stop_screen_stream


if __name__ == "__main__":
    start_screen_stream(video_device="/dev/video10", width=1080, height=2456)
    try:
        for i in range(5):
            t1 = time.time()
            frame = screen_capture(wait=True, timeout=5.0)
            t2 = time.time()
            print(f"{t2-t1}s")
            if frame is None:
                raise RuntimeError("Timed out waiting for frame")

            save_path = Path("test/test.png")
            save_path.parent.mkdir(parents=True, exist_ok=True)
            if cv2.imwrite(str(save_path), frame):
                print(f"[✓] Saved frame: {save_path}")
            else:
                print("[!] Failed to save frame")
            t2 = time.time()
            print(t2-t1)
    finally:
        stop_screen_stream()
