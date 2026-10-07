from core.voice import speak
from core.media import (
    play_pause,
    next_track,
    previous_track,
    mute,
    unmute,
)

PLUGIN = {
    "name": "Media",
    "commands": [
        "play",
        "pause",
        "resume",
        "next",
        "previous"
    ]
}


def run(command):

    command = command.lower()

    if "next" in command:
        next_track()
        speak("Playing next track.")

    elif "previous" in command:
        previous_track()
        speak("Playing previous track.")

    elif "mute" in command and "unmute" not in command:
        mute()
        speak("Muted.")

    elif "unmute" in command:
        unmute()
        speak("Unmuted.")

    else:
        play_pause()
        speak("Done.")