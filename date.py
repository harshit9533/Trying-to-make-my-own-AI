from datetime import datetime
from core.voice import speak

PLUGIN = {
    "name": "Date",
    "commands": [
        "date",
        "today's date"
    ]
}

def run(command):
    today = datetime.now()
    speak(today.strftime("Today is %d %B %Y"))