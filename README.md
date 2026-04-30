# ❄️ Whiteout Survival Autopilot (WOS-Bot)

A high-performance, intelligent automation suite for **Whiteout Survival**, built with Python, OpenCV, and PaddleOCR. This bot is designed for efficiency, utilizing a local OCR server and high-speed screen streaming via `scrcpy` and `v4l2loopback`.

> **Note:** High-speed streaming mode is optimized for **Linux** environments. Windows users may fall back to standard ADB screen capture.

---

## 🧠 The Bot Brain: How it Works
The bot operates on a **Research -> Strategy -> Execution** loop:
1.  **Vision Engine:** Instead of simple coordinate clicking, the bot "sees" the game using a hybrid approach of **PaddleOCR** (for reading text) and **OpenCV Template Matching** (for identifying icons).
2.  **Fuzzy Logic:** Uses `rapidfuzz` to handle OCR misreads (e.g., reading '0' as 'O'), ensuring actions don't fail due to tiny text variations.
3.  **Local OCR Server:** A dedicated FastAPI server handles heavy lifting for image processing, allowing the main bot logic to remain lightweight and fast.
4.  **FSM (Finite State Machine):** (In development) A navigation graph that allows the bot to calculate the shortest path between game screens (e.g., jumping from "World Map" directly to "Alliance Tech").

---

## 🚀 Quickstart (Linux)

### 1. System Dependencies
Install the required tools for high-speed screen mirroring:
```bash
sudo apt update
sudo apt install scrcpy v4l2loopback-dkms v4l2loopback-utils adb
```

### 2. Setup V4L2 Loopback
To enable the high-speed stream into the OCR engine, you must initialize the virtual video device:
```bash
sudo modprobe v4l2loopback video_nr=10 card_label="scrcpy" exclusive_caps=1
```

### 3. Environment Setup
We recommend using `uv` for lightning-fast dependency management:
```bash
# Install dependencies
pip install -r requirements.txt

# Start the OCR Server (In a separate terminal)
python core/ocr.py

# Run the Bot
python Main/main.py
```

---

## 🛠️ Features & Use Cases
The bot is feature-complete for daily maintenance tasks:

*   **Gathering:** Intelligent resource search (Meat/Wood/Coal/Iron) with troop equalization and recall logic.
*   **Alliance Management:** Auto-contribute to Tech, help all members, collect alliance chests, and auto-join rallies.
*   **Intel Missions:** Automatically completes Beast hunts, Survivor rescues, and Exploration intel.
*   **Hero Growth:** Daily training of Infantry, Lancers, and Marksmen.
*   **Rewards:** Automated collection of VIP rewards, Mail, Missions, and Life Essence.
*   **Competitive:** Automated Arena battles and Labyrinth runs.

---

## 📁 Project Structure
```text
/home/sifat/wos/
├── Main/               # Entry point and account switching logic
├── core/               # The "Heart": OCR, FSM, and Template Matching logic
├── cmd_program/        # ADB actions, scrcpy config, and V4L2 streaming
├── usecases/           # Individual game modules (Gather, Alliance, Intel, etc.)
├── db/                 # Account data, logs, and completion records
├── references/         # Vision data
│   ├── icon/           # PNG templates for icons
│   └── TextArea/       # JSON definitions for text regions
└── cache/              # Temporary screen captures for debugging
```

---

## 🛠️ Linux vs Windows Support
| Feature | Linux | Windows |
| :--- | :--- | :--- |
| ADB Support | ✅ Yes | ✅ Yes |
| Standard Screencap | ✅ Yes | ✅ Yes |
| **High-Speed Scrcpy Stream** | ✅ **Yes** | ❌ No (`v4l2` required) |
| Performance | 🚀 Ultra Fast | 🐢 Standard |

---

## 🛣️ Future Roadmap
*   **Advanced FSM:** Full implementation of the Dijkstra-based navigation system.
*   **Event Handling:** Specialized logic for Tundra Adventure and Sunfire Castle.
*   **Anti-Detection:** Randomized click-jitter and more "human-like" swipe patterns.
*   **Multi-Device:** Simultaneous control of multiple Android instances.

---

## ⚠️ Disclaimer
This project is for educational purposes only. Using bots can violate game Terms of Service. Use at your own risk.
