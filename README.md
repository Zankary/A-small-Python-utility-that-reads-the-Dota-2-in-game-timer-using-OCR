from pathlib import Path

readme = """# Dota 2 OCR Timer

A small Python utility that reads the Dota 2 in-game timer using OCR and triggers audio notifications for scheduled game events.

## Features

- Captures the timer area from the screen.
- Uses Tesseract OCR to read the `MM:SS` game timer.
- Converts the detected timer into seconds.
- Calculates scheduled event times.
- Plays asynchronous `.wav` alerts.
- Uses a notification cooldown to reduce repeated alerts.
- Runs continuously while the game is being monitored.

## Events

The current version includes notifications for:

- Stack timing
- Bounty Rune
- Power Rune
- XP Rune
- Lotus Pool

The event timings are defined directly in `get_event_times()` and can be adjusted if game mechanics or personal preferences change.

## Requirements

- Windows
- Python 3.x
- Tesseract OCR
- Python packages listed in `requirements.txt`

The project uses `winsound`, which is included with standard Python installations on Windows.

## Installation

### 1. Install Python

Install Python 3.x and make sure Python is available from the command line.

### 2. Install Tesseract OCR

Install Tesseract OCR and verify that the executable exists at:

```text
C:\\Program Files\\Tesseract-OCR\\tesseract.exe
