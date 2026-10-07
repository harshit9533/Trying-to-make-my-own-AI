import psutil

from core.voice import speak

PLUGIN = {
    "name": "Close Application",
    "commands": [
        "close",
        "terminate",
        "kill",
        "stop"
    ]
}

ALIASES = {

    "chrome": "chrome",

    "browser": "chrome",

    "code": "code",

    "vscode": "code",

    "discord": "discord",

    "steam": "steam",

    "spotify": "spotify",

    "edge": "msedge"
}


def run(command):

    app_name = command.lower()

    for trigger in PLUGIN["commands"]:

        if app_name.startswith(trigger):

            app_name = app_name.replace(trigger, "", 1).strip()

            break

    if not app_name:

        speak("Which application should I close?")

        return

    app_name = ALIASES.get(app_name, app_name)

    closed = 0

    for process in psutil.process_iter(["pid", "name"]):

        try:

            process_name = process.info["name"]

            if not process_name:
                continue

            process_name = process_name.lower()

            if app_name in process_name:

                process.terminate()

                try:
                    process.wait(timeout=3)
                except psutil.TimeoutExpired:
                    process.kill()

                closed += 1

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    if closed:

        speak(f"Closed {closed} process{'es' if closed != 1 else ''}.")

    else:

        speak(f"{app_name} is not running.")