import webbrowser
from core.voice import speak

PLUGIN = {
    "name": "Google",
    "commands": [
        "google homepage",
        "open google"
    ]
}

def run(command):
    speak("Opening Google.")
    webbrowser.open("https://google.com")