import webbrowser
from core.voice import speak

PLUGIN = {
    "name": "ChatGPT",
    "commands": [
        "chatgpt",
        "open chatgpt"
    ]
}

def run(command):
    speak("Opening ChatGPT.")
    webbrowser.open("https://chat.openai.com")