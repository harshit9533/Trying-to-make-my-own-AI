from core import plugin_loader
from core import ai_router
from core.context import context
from core.planner import Planner


class Executive:

    def __init__(self):

        print("[Executive] Online")

        self.planner = Planner()

    def process(self, command: str):

        print(f"\n[Executive] Goal -> {command}")

        # ==========================================
        # CONTEXT
        # ==========================================

        context.previous_command = command

        # ==========================================
        # CREATE EXECUTION PLAN
        # ==========================================

        plan = self.planner.create_plan(command)

        print(
            f"[Planner] {len(plan.steps)} step(s) created."
        )

        last_ai_response = None

        # ==========================================
        # EXECUTE EVERY STEP
        # ==========================================

        while True:

            step = self.planner.next_step(plan)

            if step is None:
                break

            print(
                f"[Planner] Executing -> {step}"
            )

            # --------------------------------------
            # Save current task
            # --------------------------------------

            context.set(
                "current_step",
                step
            )

            # --------------------------------------
            # Find Plugin
            # --------------------------------------

            plugin = plugin_loader.get_plugin(step)

            if plugin:

                print(
                    f"[Executive] Plugin -> "
                    f"{plugin.__name__}"
                )

                # Remember active plugin
                context.active_plugin = plugin.__name__

                # Remember action
                context.last_action = step

                try:

                    plugin.run(step)

                    # --------------------------------
                    # Update application context
                    # --------------------------------

                    if plugin.__name__ == "plugins.open_app":

                        words = step.split()

                        if len(words) > 1:

                            application = " ".join(
                                words[1:]
                            )

                            context.update_application(
                                application
                            )

                    # --------------------------------
                    # Store successful step
                    # --------------------------------

                    context.set(
                        "last_successful_step",
                        step
                    )

                except Exception as e:

                    print(
                        f"[PLUGIN ERROR] {e}"
                    )

                    context.set(
                        "last_error",
                        str(e)
                    )

            else:

                # --------------------------------------
                # No Plugin → AI
                # --------------------------------------

                print(
                    "[Executive] Using AI"
                )

                try:

                    last_ai_response = (
                        ai_router.ask(step)
                    )

                    # Save AI response
                    context.last_response = (
                        last_ai_response
                    )

                    context.set(
                        "last_ai_step",
                        step
                    )

                except Exception as e:

                    print(
                        f"[AI ERROR] {e}"
                    )

                    context.set(
                        "last_error",
                        str(e)
                    )

        # ==========================================
        # TASK COMPLETE
        # ==========================================

        context.current_task = command

        return last_ai_response


# ==============================================
# Local Test
# ==============================================

if __name__ == "__main__":

    plugin_loader.load_plugins()

    executive = Executive()

    while True:

        command = input(
            "EXECUTIVE >>> "
        ).strip()

        if command.lower() in (
            "exit",
            "quit"
        ):

            break

        print()

        result = executive.process(
            command
        )

        if result:

            print(result)

        print()

        print(
            "[Context]",
            context.get("current_step")
        )