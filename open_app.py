import json
import os
import difflib
from pathlib import Path
import subprocess

from core.voice import speak

# ==========================================
# Plugin Information
# ==========================================

PLUGIN = {
    "name": "Open Application",
    "commands": [
        "open",
        "launch",
        "start",
        "run"
    ]
}

# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

APPS_FILE = BASE_DIR / "data" / "apps.json"

# ==========================================
# Aliases
# ==========================================

ALIASES = {

    "chrome": "google chrome",

    "browser": "google chrome",

    "code": "visual studio code",

    "vscode": "visual studio code",

    "vs code": "visual studio code",

    "cmd": "command prompt",

    "terminal": "command prompt",

    "paint": "paint",

    "calc": "calculator"
}

# ==========================================
# Load Applications
# ==========================================

def load_apps():

    if not APPS_FILE.exists():
        speak("Application database not found.")
        return {}

    with open(APPS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

# ==========================================
# Find Best Match
# ==========================================

def find_app(app_name, apps):

    app_name = app_name.lower().strip()

    app_name = ALIASES.get(app_name, app_name)

    names = list(apps.keys())

    matches = difflib.get_close_matches(
        app_name,
        names,
        n=1,
        cutoff=0.35
    )

    if not matches:
        return None

    return matches[0]

# ==========================================
# Launch Application
# ==========================================

def launch_app(app_key, apps):

    app = apps[app_key]

    # Supports both JSON formats
    if isinstance(app, dict):

        path = app.get("path")

        display_name = app.get(
            "display_name",
            app_key
        )

    else:

        path = app

        display_name = app_key

    if not path:

        speak("Shortcut path is missing.")

        return

    if not os.path.exists(path):

        speak("The shortcut no longer exists.")

        return

    try:

        speak(f"Opening {display_name}.")

        subprocess.Popen(
            ["cmd", "/c", "start", "", path],
            shell=True
        )

    except Exception as e:

        print(e)

        speak("Failed to launch the application.")

# ==========================================
# Main Plugin Function
# ==========================================

def run(command):

    apps = load_apps()

    if not apps:
        return

    words = command.split()

    if len(words) < 2:

        speak("Which application should I open?")

        return

    app_name = " ".join(words[1:])

    app_key = find_app(app_name, apps)

    if app_key is None:

        speak(f"I couldn't find {app_name}.")

        return

    launch_app(app_key, apps)