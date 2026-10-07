from core.voice import speak
from core.config import MEMORY_FILE

PLUGIN = {
    "name": "Remember",
    "commands": [
        "remember",
        "remember that",
        "save this"
    ]
}

def run(command):

    text = command

    for phrase in PLUGIN["commands"]:
        if text.startswith(phrase):
            text = text[len(phrase):].strip()
            break

    if not text:
        speak("What should I remember?")
        return

    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

    speak("I will remember that.")