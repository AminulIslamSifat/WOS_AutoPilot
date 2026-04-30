# ❄️ Whiteout Survival Autopilot (WOS-Bot)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-blueviolet?style=flat-square)

**A high-performance, intelligent automation suite for Whiteout Survival**

Built with Python, OpenCV, and PaddleOCR • FastAPI OCR Server • Real-time Screen Mirroring

[Features](#-features--use-cases) • [Quick Start](#-quickstart-arch-linux) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

> **💡 Platform Note:** High-speed streaming mode is optimized for **Linux** environments using `v4l2loopback`. Windows users can fall back to standard ADB screen capture with standard performance.

---

## 📋 Table of Contents

- [How It Works](#-the-bot-brain-how-it-works)
- [⚠️ Resolution Requirements](#-attention-resolution-lock-)
- [Quick Start](#-quickstart-arch-linux)
- [Features](#-features--use-cases)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Platform Support](#-linux-vs-windows-support)
- [Roadmap](#-roadmap)
- [License & Disclaimer](#-disclaimer)

---

## 🧠 The Bot Brain: How it Works

The bot operates on a **Research → Strategy → Execution** loop:

1. **Vision Engine** 👁️  
   Instead of simple coordinate clicking, the bot "sees" the game using a hybrid approach of **PaddleOCR** (for reading text) and **OpenCV Template Matching** (for identifying icons).

2. **Fuzzy Logic** 🎯  
   Uses `rapidfuzz` to handle OCR misreads (e.g., reading '0' as 'O'), ensuring actions don't fail due to tiny text variations.

3. **Local OCR Server** ⚡  
   A dedicated FastAPI server handles heavy lifting for image processing, allowing the main bot logic to remain lightweight and fast.

4. **FSM Navigation** 🗺️  
   (In development) A navigation graph that calculates the shortest path between game screens (e.g., jumping from "World Map" directly to "Alliance Tech").


## ⚠️ ATTENTION: Resolution Lock ⚠️

> **🔴 CRITICAL:** This bot is hardcoded for **1080×2460 resolution**.

**If your device uses a different resolution:**
- ❌ ROI detection will fail
- ❌ Clicks will land in incorrect locations  
- ❌ The bot may perform unintended actions

### 📝 Planned Solution

An **Auto-Calibration Suite** is under development. In a future release, the bot will:
- ✅ Auto-detect your device resolution on first run
- ✅ Execute a guided "World Tour" of all game screens
- ✅ Dynamically generate resolution-specific coordinates in `references/TextArea/`

**Status:** Coming soon

---

## 🚀 Quickstart (Arch Linux)

### Prerequisites

- Android device/emulator with Whiteout Survival installed
- Arch Linux system (or equivalent distro with `pacman`)
- ADB enabled on your Android device
- USB cable (if using physical device)

### 1️⃣ Install System Dependencies

```bash
sudo pacman -Syu scrcpy v4l2loopback-dkms v4l2loopback-utils android-tools uv
```

**What this installs:**
- `scrcpy` — High-speed screen mirroring
- `v4l2loopback` — Virtual video device driver
- `uv` — Fast Python package manager
- `android-tools` — ADB utilities

### 2️⃣ Initialize V4L2 Loopback (Recommended)

Enable the virtual video device for high-speed OCR streaming:

```bash
sudo modprobe v4l2loopback video_nr=10 card_label="scrcpy" exclusive_caps=1
```

> **💡 Tip:** Add this to `/etc/modules-load.d/v4l2loopback.conf` to auto-load on boot.

### 3️⃣ Start the OCR Server

In a dedicated terminal window:

```bash
cd ~/wos
uv run core/ocr.py
```

This installs dependencies and launches the FastAPI OCR server on `localhost:8000`.

### 4️⃣ Launch the Bot

In a separate terminal window:

```bash
cd ~/wos
python Main/main.py
```

The bot will:
- ✅ Auto-detect your device via ADB
- ✅ Launch Whiteout Survival if not already running
- ✅ Initialize your player profile
- ✅ Begin running daily tasks

---

## 📋 Configuration

### Account Setup

Edit `db/account.json` to configure your accounts:

```json
{
  "your_email@gmail.com": {
    "priority": 1,
    "player": [
      {
        "id": "12345678",
        "name": "Chief Name"
      }
    ]
  }
}
```

**Key Settings:**
- `priority` — Order to process accounts (lower = earlier)
- `id` — Player ID (found in-game via Chief Profile)
- `name` — Character name for account switching

### Task Scheduling

Modify `run_task()` in [Main/main.py](Main/main.py) to customize which daily tasks run:

```python
def run_task(current_player_id):
    collect_vip_rewards()        # VIP reward collection
    claim_exploration_idle_income()  # Exploration income
    train()                      # Troop training
    # Add or remove tasks as needed
```

---

## 🛠️ Features & Use Cases

The bot is feature-complete for daily maintenance automation:

### 🌍 World Operations
- **Gathering** — Intelligent resource search (Meat/Wood/Coal/Iron) with troop equalization and recall logic
- **Healing** — Auto-heal wounded troops with optimal item usage

### 🏰 Alliance Management
- **Tech Contribution** — Contribute to tech trees automatically
- **Help Members** — Provide help to alliance members in need
- **Chests** — Collect alliance chests on cooldown
- **Rallies** — Auto-join war rallies and contribute
- **Triumph Collection** — Harvest alliance triumph rewards

### ⚔️ Combat & Exploration
- **Arena Battles** — Daily automated arena fights
- **Labyrinth Runs** — Complete labyrinth dungeons
- **Intel Missions** — Auto-complete Beast hunts, Survivor rescues, Exploration intel

### 🎖️ Growth & Progression
- **Troop Training** — Auto-train Infantry, Lancers, and Marksmen
- **Pet Exploration** — Auto-start pet expeditions and claim rewards
- **Chief Order** — Activate and track chief order progression

### 💰 Rewards
- **VIP Rewards** — Collect daily VIP bonuses and auto-buy VIP time when profitable
- **Mail** — Auto-collect all mail rewards
- **Missions** — Collect mission rewards
- **Life Essence** — Harvest life essence drops
- **Events** — Collect event-specific rewards

---

## 📁 Project Structure

```
wos/
├── Main/
│   ├── main.py                 # Entry point & account switching
│   └── main.py                 # Daily task scheduler
├── core/
│   ├── ocr.py                  # FastAPI OCR server
│   ├── core.py                 # Vision engine (template matching, OCR)
│   ├── change_player.py        # Account/character switching
│   ├── recalibrate.py          # Auto-calibration tools
│   └── backup/                 # Legacy versions
├── cmd_program/
│   ├── screen_action.py        # ADB touch/swipe actions
│   ├── screen_stream.py        # scrcpy streaming setup
│   └── scrcpy_config.json      # Stream configuration
├── usecases/                   # Feature modules
│   ├── gather.py               # Resource gathering
│   ├── alliance.py             # Alliance tasks
│   ├── arena.py                # Arena battles
│   ├── exploration.py          # Exploration intel
│   ├── labyrinth.py            # Labyrinth runs
│   ├── pet.py                  # Pet mechanics
│   └── [other features].py
├── db/
│   ├── account.json            # Account/player configuration
│   ├── completion_log.txt      # Daily task completion tracking
│   └── players/                # Per-player data
├── references/
│   ├── icon/                   # PNG templates for icon matching
│   │   ├── alliance/
│   │   ├── arena/
│   │   └── [other categories]/
│   └── TextArea/               # JSON ROI definitions
│       ├── Home.json
│       ├── Home.Alliance.json
│       └── [all screen definitions].json
└── test/                       # Debug & testing utilities
```

---

## �️ Linux vs Windows Support

| Feature | Linux | Windows |
| :--- | :--- | :--- |
| ADB Support | ✅ | ✅ |
| Standard Screencap | ✅ | ✅ |
| **High-Speed Scrcpy Stream** | ✅ **Native** | ❌ *Requires WSL2 + v4l2* |
| V4L2 Direct Streaming | ✅ **Native** | ❌ Not Available |
| Performance | 🚀 **Ultra Fast** | 🐢 Standard |
| Setup Complexity | ⭐ Straightforward | ⭐⭐ Extra steps needed |

**Recommended:** Linux (native full support)  
**Fallback:** Windows with ADB only (slower performance)

---

## �️ Troubleshooting

### OCR Server Won't Start

**Error:** `ModuleNotFoundError` or port already in use

```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill existing process if needed
kill -9 <PID>

# Reinstall dependencies
cd ~/wos
uv sync
uv run core/ocr.py
```

### Bot Clicks in Wrong Locations

**Cause:** Resolution mismatch (not 1080×2460)

**Solutions:**
1. Verify device resolution: `adb shell wm size`
2. If different, await Auto-Calibration Suite (in development)
3. Manually update ROI coordinates in `references/TextArea/` (advanced)

### ADB Connection Issues

```bash
# Restart ADB daemon
adb kill-server
adb start-server

# List connected devices
adb devices

# Enable USB debugging on device settings
```

### V4L2 Loopback Not Detected

```bash
# Check if module is loaded
lsmod | grep v4l2loopback

# If not loaded, reinstall
sudo dkms remove v4l2loopback/0.12.7 --all
sudo pacman -S v4l2loopback-dkms

# Reload module
sudo modprobe -r v4l2loopback
sudo modprobe v4l2loopback video_nr=10 card_label="scrcpy" exclusive_caps=1
```

---

## 🚀 Roadmap

### Phase 1 (Current)
- ✅ Core daily task automation
- ✅ Multi-account support
- ⏳ Auto-calibration suite

### Phase 2 (Planned)
- 📋 Advanced FSM navigation (Dijkstra-based pathfinding)
- 📋 Event-specific strategies (Tundra Adventure, Sunfire Castle)
- 📋 Enhanced anti-detection (human-like click patterns)

### Phase 3 (Future)
- 🔮 Multi-device simultaneous control
- 🔮 Web dashboard for monitoring
- 🔮 Community script marketplace

---

## 📦 Dependencies

**Core Requirements:**
- Python 3.9+
- OpenCV (`cv2`)
- PaddleOCR
- FastAPI & Uvicorn
- RapidFuzz
- Requests
- Rich (CLI output)

See `requirements.txt` or `pyproject.toml` for the complete dependency list.

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create a feature branch:** `git checkout -b feature/your-feature-name`
3. **Make your changes** and test thoroughly
4. **Submit a Pull Request** with a clear description

### Code Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Test with multiple accounts if applicable
- Document any new game modules

---

## 📄 License & Disclaimer

### License
This project is released under the **MIT License**. See LICENSE file for details.

### ⚠️ Disclaimer

**Use this bot at your own risk.** 

This project is **for educational purposes only**. Using automation tools may violate the **Terms of Service** of Whiteout Survival. The authors are **not responsible for**:
- Account suspension or bans
- In-game penalties
- Loss of progress or items
- Violation of game terms

**Always read the game's ToS before using automation tools.**

---

## 📞 Support

- **Issues:** Report bugs via GitHub Issues
- **Discussions:** Share ideas in GitHub Discussions
- **Documentation:** Check the wiki for advanced topics

---

<div align="center">

Made with ❄️ by the WOS Bot community

⭐ Star this repo if you find it useful!

</div>
