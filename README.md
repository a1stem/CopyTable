# CopyTable
CopyTable is a play on words, CoffeeTable, but when run, CopyTable is a Linux Copyboard History App. A lightweight, **text-only** clipboard history manager for Linux — built with security in mind.

## What It Does
CopyTable quietly runs in your system tray, monitoring your clipboard and keeping a local history of text you've copied. No cloud. No sync. No tracking. Everything stays on your machine.

## Features
- 🔒 **Text only** — images, files, and binary data are intentionally ignored
- 📋 **Clipboard history** — automatically captures new text entries
- 🔍 **Search/filter** — quickly find a previous entry
- 1️⃣ **One-click copy** — double-click any entry to copy it back
- 🗑️ **Delete entries** — remove individual items or clear all
- 🖥️ **System tray** — runs silently in the background, never in your way

## Security Philosophy
CopyTable is designed with privacy first:
- All clipboard data is stored **in memory only** — nothing is written to disk
- No network calls, no telemetry, no logging
- Closing the window keeps it in the tray — **quitting fully clears all history**

## Requirements
- Linux Mint / Ubuntu / Debian
- Python 3
- PyQt5

## Install & Run
```bash
sudo apt install python3-pyqt5
python3 main.py
```

## Running CopyTable - Best Practice from /OPT/ using run and deploy scripts

Once deployed, you can launch CopyTable from any terminal with:
```bash
copytable
```

This runs the clipboard app directly without needing to navigate to the install directory.

## Deployment

To deploy or update CopyTable to `/opt/clipboard-app/`:
```bash
./deploy.sh
```

The deploy script copies all necessary files, excluding `.git`, `__pycache__`, and `*.pyc` files.

## Usage
| Action | Result |
|---|---|
| Copy any text | Automatically captured |
| Double-click entry | Copies it back to clipboard |
| Search box | Filters history in real time |
| Delete Selected | Removes one entry |
| Clear All | Wipes entire history |
| Close window | Minimizes to system tray |
| Tray → Quit | Exits and clears all history |

## License
MIT — free to use and modify.
