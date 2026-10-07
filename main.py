import sys

from core import plugin_loader
from core.context import context
from core.executive import Executive
from core.voice import (
    speak,
    listen_wake_word,
    listen_command,
)


def main():

    # ==========================================
    # Load Plugins
    # ==========================================

    plugin_loader.load_plugins()

    # ==========================================
    # Create Executive Brain
    # ==========================================

    executive = Executive()

    print("Jarvis is ready.")

    # ==========================================
    # Main Loop
    # ==========================================

    while True:

        # --------------------------------------
        # Wait for Wake Word
        # --------------------------------------

        if not listen_wake_word():
            continue

        speak("Yes, sir?")

        # --------------------------------------
        # Listen for Command
        # --------------------------------------

        command = listen_command()

        if not command:
            continue

        command = command.strip()

        # --------------------------------------
        # Exit Commands
        # --------------------------------------

        if command.lower() in [
            "exit",
            "quit",
            "shutdown",
            "bye",
            "goodbye",
        ]:

            speak("Goodbye, sir.")
            sys.exit(0)

        # ======================================
        # CONTEXT MANAGER
        # ======================================

        try:

            # Remember every command
            context.remember(command)

            # Store the most recent command
            context.previous_command = command

            print(
                f"[Context] Remembered: {command}"
            )

        except Exception as e:

            print(
                f"[CONTEXT ERROR] {e}"
            )

        # ======================================
        # EXECUTIVE BRAIN
        # ======================================

        try:

            response = executive.process(command)

            # Store AI / Executive response
            if response:

                context.last_response = response

                speak(response)

        except Exception as e:

            print(
                f"[EXECUTIVE ERROR] {e}"
            )

            speak(
                "An internal error occurred."
            )


if __name__ == "__main__":
    main()