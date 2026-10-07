import psutil
from core.voice import speak

PLUGIN = {
    "name": "Battery",
    "commands": [
        "battery",
        "battery percentage",
        "battery status",
        "how much battery"
    ]
}

def run(command):

    battery = psutil.sensors_battery()

    if battery is None:
        speak("Battery information is unavailable.")
        return

    charging = "charging" if battery.power_plugged else "not charging"

    speak(f"Battery is {battery.percent} percent and is currently {charging}.")