import os
import time
from datetime import datetime

import pyautogui

from core.voice import speak


PLUGIN = {
    "name": "Screenshot",
    "commands": [
        "take a screenshot",
        "capture the screen",
        "screenshot",
        "capture screen"
    ]
}


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_DIR = os.path.join(BASE_DIR, "data", "screenshots")


def ensure_directory():
    os.makedirs(SAVE_DIR, exist_ok=True)


def get_filename():

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    return os.path.join(
        SAVE_DIR,
        f"{timestamp}.png"
    )


def take_screenshot():

    ensure_directory()

    filepath = get_filename()

    # Small delay so future GUI/overlay can disappear
    time.sleep(0.5)

    pyautogui.screenshot(filepath)

    return filepath


def run(command):

    try:

        speak("Taking screenshot.")

        filepath = take_screenshot()

        filename = os.path.basename(filepath)

        speak(f"Screenshot saved as {filename}.")

    except Exception as e:

        print(e)

        speak("Sorry, I couldn't take the screenshot.")