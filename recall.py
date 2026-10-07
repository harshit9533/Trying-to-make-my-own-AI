from core.voice import speak
from core.config import MEMORY_FILE

PLUGIN = {
    "name": "Recall",
    "commands": [
        "recall",
        "what do you remember",
        "memory",
        "tell me what you remember"
    ]
}

def run(command):

    try:

        with open(MEMORY_FILE, "r", encoding="utf-8") as f:

            memories = f.readlines()

        if not memories:
            speak("I don't remember anything yet.")
            return

        speak("Here is what I remember.")

        for memory in memories:
            speak(memory.strip())

    except FileNotFoundError:

        speak("I don't remember anything yet.")