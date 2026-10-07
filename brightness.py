import re
import screen_brightness_control as sbc

from core.voice import speak


PLUGIN = {
    "name": "Brightness Control",
    "commands": [
        "brightness",
        "set brightness",
        "increase brightness",
        "decrease brightness",
        "brightness up",
        "brightness down",
        "brighten screen",
        "dim screen",
        "maximum brightness",
        "minimum brightness",
        "current brightness"
    ]
}


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def get_brightness():

    try:
        return sbc.get_brightness(display=0)[0]

    except Exception:

        return sbc.get_brightness()[0]


def set_brightness(level):

    level = max(1, min(100, level))

    sbc.set_brightness(level)

    speak(f"Brightness set to {level} percent.")


def increase_brightness(step=10):

    current = get_brightness()

    set_brightness(current + step)


def decrease_brightness(step=10):

    current = get_brightness()

    set_brightness(current - step)


# --------------------------------------------------
# Main Plugin
# --------------------------------------------------

def run(command):

    command = command.lower()

    try:

        # ---------- Current ----------

        if (
            "current brightness" in command
            or "what is the brightness" in command
        ):

            speak(
                f"The current brightness is {get_brightness()} percent."
            )

            return

        # ---------- Maximum ----------

        if (
            "maximum brightness" in command
            or "max brightness" in command
        ):

            set_brightness(100)

            return

        # ---------- Minimum ----------

        if (
            "minimum brightness" in command
            or "lowest brightness" in command
            or "min brightness" in command
        ):

            set_brightness(0)

            return

        # ---------- Increase ----------

        if (
            "increase brightness" in command
            or "brightness up" in command
            or "brighten screen" in command
            or "make it brighter" in command
        ):

            increase_brightness()

            return

        # ---------- Decrease ----------

        if (
            "decrease brightness" in command
            or "brightness down" in command
            or "dim screen" in command
            or "make it darker" in command
        ):

            decrease_brightness()

            return

        # ---------- Set Specific ----------

        numbers = re.findall(r"\d+", command)

        if numbers:

            level = int(numbers[0])

            set_brightness(level)

            return

        speak("Please tell me the brightness level.")

    except Exception as e:

        print(e)

        speak("Sorry, I couldn't control the brightness.")