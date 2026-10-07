from datetime import datetime
from core.voice import speak

PLUGIN = {
    "name": "Time",
    "commands": [
        "time",
        "what time is it"
    ]
}

def run(command):
    now = datetime.now()
    speak(now.strftime("The time is %I:%M %p"))