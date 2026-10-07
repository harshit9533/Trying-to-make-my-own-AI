from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class Intent:

    name: str

    target: Optional[str] = None

    confidence: float = 0.0

    original: str = ""


# --------------------------
# Intent Rules
# --------------------------

RULES = {

    "open_app": [
        "open",
        "launch",
        "start",
        "run"
    ],

    "battery": [
        "battery",
        "charge",
        "power"
    ],

    "time": [
        "time",
        "clock"
    ],

    "date": [
        "date",
        "today",
        "day"
    ],

    "calculator": [
        "calculate",
        "solve",
        "evaluate"
    ]

}


def detect(command: str) -> Intent:

    text = command.lower().strip()

    # -------------------------
    # Rule Detection
    # -------------------------

    for intent_name, keywords in RULES.items():

        for keyword in keywords:

            if keyword in text:

                target = None

                if intent_name == "open_app":

                    target = re.sub(
                        r"^(open|launch|start|run)\s+",
                        "",
                        text
                    )

                return Intent(

                    name=intent_name,

                    target=target,

                    confidence=0.95,

                    original=command

                )

    return Intent(

        name="chat",

        confidence=0.0,

        original=command

    )


# --------------------------
# Local Test
# --------------------------

if __name__ == "__main__":

    while True:

        q = input(">>> ")

        if q == "exit":
            break

        print(detect(q))