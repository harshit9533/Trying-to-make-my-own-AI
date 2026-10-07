import webbrowser
from core.voice import speak

PLUGIN = {
    "name": "YouTube",
    "commands": [
        "youtube",
        "open youtube"
    ]
}

def run(command):
    speak("Opening YouTube.")
    webbrowser.open("https://youtube.com")