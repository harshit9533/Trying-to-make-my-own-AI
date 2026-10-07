import re

from pycaw.pycaw import AudioUtilities

from core.voice import speak

PLUGIN = {
    "name": "Volume Control",
    "commands": [
        "volume",
        "set volume",
        "current volume",
        "mute",
        "unmute",
        "increase volume",
        "decrease volume",
        "volume up",
        "volume down",
        "raise volume",
        "lower volume",
        "maximum volume",
        "minimum volume"
    ]
}


# --------------------------------------------------
# Internal Helpers
# --------------------------------------------------

def get_interface():

    device = AudioUtilities.GetSpeakers()

    return device.EndpointVolume


def get_volume():

    volume = get_interface()

    return round(
        volume.GetMasterVolumeLevelScalar() * 100
    )


def set_volume(level):

    level = max(0, min(100, level))

    volume = get_interface()

    volume.SetMasterVolumeLevelScalar(
        level / 100,
        None
    )

    speak(f"Volume set to {level} percent.")


def increase_volume(step=10):

    current = get_volume()

    set_volume(current + step)


def decrease_volume(step=10):

    current = get_volume()

    set_volume(current - step)


def mute():

    volume = get_interface()

    volume.SetMute(1, None)

    speak("Volume muted.")


def unmute():

    volume = get_interface()

    volume.SetMute(0, None)

    speak("Volume unmuted.")


# --------------------------------------------------
# Main Plugin
# --------------------------------------------------

def run(command):

    command = command.lower()

    try:

        # ---------- Mute ----------

        if "unmute" in command:

            unmute()

            return

        if "mute" in command:

            mute()

            return

        # ---------- Current Volume ----------

        if (
            "current volume" in command
            or "what is the volume" in command
            or "volume percentage" in command
        ):

            speak(
                f"The current volume is {get_volume()} percent."
            )

            return

        # ---------- Maximum ----------

        if (
            "maximum volume" in command
            or "max volume" in command
            or "full volume" in command
        ):

            set_volume(100)

            return

        # ---------- Minimum ----------

        if (
            "minimum volume" in command
            or "min volume" in command
        ):

            set_volume(0)

            return

        # ---------- Increase ----------

        if (
            "increase volume" in command
            or "volume up" in command
            or "raise volume" in command
            or "make it louder" in command
        ):

            increase_volume()

            return

        # ---------- Decrease ----------

        if (
            "decrease volume" in command
            or "volume down" in command
            or "lower volume" in command
            or "make it quieter" in command
        ):

            decrease_volume()

            return

        # ---------- Set Specific Volume ----------

        numbers = re.findall(r"\d+", command)

        if numbers:

            level = int(numbers[0])

            set_volume(level)

            return

        speak("Please tell me the volume level.")

    except Exception as e:

        print(e)

        speak("Sorry, I couldn't control the volume.")