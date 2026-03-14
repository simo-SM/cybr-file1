# 🔒 CYBER-FILE v2.7

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.13+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey)

**Real-Time File Monitoring Tool** with Modern GUI, Multi-Alert System, and System Tray Integration.

![image alt](images/cyberFileApp.png)

---

## 🗺️ Application Workflow (Mindmap)

<p align="center">
  <img src="imagesimages/markmap.svg" alt="Cyber-File Workflow" width="800">
</p>

---
---
![image alt](images/cyberTerminale.png)
---
## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Telegram Bot Setup](#-telegram-bot-setup)
- [Usage](#-usage)
- [Admin Mode](#-admin-mode)
- [Build EXE](#-build-exe)
- [Troubleshooting](#-troubleshooting)

---
---
![image alt](images/cyberTerminale2.png)

---
## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Real-Time Monitoring** | Track file creations, deletions, modifications, moves instantly |
| 📱 **Telegram Alerts** | Get notifications on your phone via Telegram Bot |
| 💬 **WhatsApp Alerts** | Alternative alerts via Twilio (optional) |
| 🎨 **Modern GUI** | Dark cyber theme with CustomTkinter |
| 🗕️ **System Tray** | Run in background, minimize to tray |
| 📊 **Live Dashboard** | Real-time statistics and event timeline |
| 🔐 **Admin Mode** | Hidden console with security code |
| 🔊 **Sound Alerts** | Beep on critical events (optional) |

---

## 🚀 Installation

### Step 1: Download Cyber-File

**Option A: Download EXE (Windows)**
- Go to [Releases](https://github.com/simo-SM/cybr-file1/releases)
- Download `Cyber-File_Setup.exe`
- Double-click to run.

**Option B: Run from Python Source**

```bash
# 1. Clone repository
git clone [https://github.com/simo-SM/cybr-file1.git](https://github.com/simo-SM/cybr-file1.git)
cd cybr-file1

# 2. Create virtual environment
python -m venv venv

# 3. Activate environment
# Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run application
python cyberfile_v2.7.py
