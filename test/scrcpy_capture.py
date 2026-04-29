import subprocess
import time
from pathlib import Path
from datetime import datetime
import cv2
import threading
import numpy as np
import os


def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")



latest_frame = None
lock = threading.Lock()




def start_ffmpeg_stream(mkv_path):
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-i", str(mkv_path),
        "-f", "rawvideo",
        "-pix_fmt", "bgr24",
        "pipe:1",
    ]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**8)


def stop_process(proc):
    if proc is None or proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=2)

out_dir = "frames"

out_dir = Path(out_dir)
out_dir.mkdir(parents=True, exist_ok=True)



mkv = Path("/home/sifat/wos/cache") / "screen.mkv"

scrcpy_cmd = [
    "scrcpy",
    "--turn-screen-off",
    "--no-audio",
    "--max-size", "0",
    "--record", str(mkv),
    "--record-format=mkv",
    "--video-bit-rate", "200000000"
]

print("[*] Starting scrcpy...")
scrcpy_proc = subprocess.Popen(scrcpy_cmd)

# wait for recording to start
while not mkv.exists() or mkv.stat().st_size < 8000:
    if scrcpy_proc.poll() is not None:
        print("[!] scrcpy exited early")
        raise RuntimeError("No mkv")
    time.sleep(0.3)

print("[✓] Recording started\n")

ffmpeg_proc = start_ffmpeg_stream(mkv)







def reader(proc, stop_event, width=1080, height=2456):
    global latest_frame
    frame_size = width * height * 3

    while not stop_event.is_set():
        raw = proc.stdout.read(frame_size)

        if not raw:
            if proc.poll() is not None:
                break
            continue

        if len(raw) < frame_size:
            if proc.poll() is not None:
                break
            continue

        frame = np.frombuffer(raw, np.uint8).reshape((height, width, 3))

        with lock:
            latest_frame = frame


stop_event = threading.Event()
reader_thread = threading.Thread(target=reader, args=(ffmpeg_proc, stop_event), daemon=True)
reader_thread.start()

def screen_capture():
    with lock:
        if latest_frame is None:
            return None
        else:
            return latest_frame.copy()
        
try:
    while True:
        frame = screen_capture()
        if frame is not None:
            break
        if scrcpy_proc.poll() is not None:
            raise RuntimeError("scrcpy exited before a frame was available")
        if ffmpeg_proc.poll() is not None:
            raise RuntimeError("ffmpeg exited before a frame was available")
        time.sleep(0.01)

    save_path = "test/test.png"
    saved = cv2.imwrite(str(save_path), frame)
    if saved:
        print(f"[✓] Saved frame: {save_path}")
    else:
        print("[!] Failed to save frame")
finally:
    stop_event.set()
    stop_process(ffmpeg_proc)
    stop_process(scrcpy_proc)
    reader_thread.join(timeout=1.0)

    if mkv.exists():
        try:
            mkv.unlink()
        except OSError as exc:
            print(f"[!] Could not delete {mkv}: {exc}")