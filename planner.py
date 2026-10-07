from dataclasses import dataclass, field
from typing import List


@dataclass
class Plan:

    goal: str

    steps: List[str] = field(default_factory=list)

    current_step: int = 0


class Planner:

    def __init__(self):
        print("[Planner] Online")

    def create_plan(self, command: str) -> Plan:
        """
        Creates a simple execution plan.

        Examples:
        Open chrome and search google

        becomes

        [
            "open chrome",
            "search google"
        ]
        """

        command = command.lower().strip()

        separators = [
            " and then ",
            " then ",
            " and ",
        ]

        steps = [command]

        for separator in separators:

            if separator in command:

                steps = [
                    s.strip()
                    for s in command.split(separator)
                    if s.strip()
                ]

                break

        return Plan(
            goal=command,
            steps=steps,
        )

    def next_step(self, plan: Plan):

        if plan.current_step >= len(plan.steps):
            return None

        step = plan.steps[plan.current_step]

        plan.current_step += 1

        return step