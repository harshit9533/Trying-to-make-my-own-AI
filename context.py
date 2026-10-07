"""
context.py

Stores conversation state, previous commands,
plugin context, and short-term memory.
"""

import re
import time
from dataclasses import dataclass, field
from collections import deque
from typing import Optional, Dict, Any


@dataclass
class ConversationContext:

    # =====================================================
    # Conversation History
    # =====================================================

    history: deque = field(
        default_factory=lambda: deque(maxlen=100)
    )

    # =====================================================
    # Previous Intent Cache
    # =====================================================

    last_application: Optional[str] = None
    last_intent: Optional[str] = None
    last_action: Optional[str] = None
    last_entities: Dict[str, Any] = field(default_factory=dict)

    previous_command: Optional[str] = None

    # =====================================================
    # Frequently Used Context
    # =====================================================

    last_search: Optional[str] = None
    last_url: Optional[str] = None

    last_timer_id: Optional[int] = None
    last_volume: Optional[int] = None
    last_brightness: Optional[int] = None

    active_plugin: Optional[str] = None

    # =====================================================
    # Shared Variables
    # =====================================================

    shared: Dict[str, Any] = field(default_factory=dict)

    # =====================================================
    # History
    # =====================================================

    def add_to_history(self, record: dict):
        """Append command record to rolling history."""

        record.setdefault("timestamp", time.time())

        self.history.append(record)

    def remember(self, command: str):
        """Remember a command and add it to conversation history."""

        self.previous_command = command

        self.add_to_history({
            "command": command
        })

    # =====================================================
    # Context Updates
    # =====================================================

    def update_application(self, app: str):
        self.last_application = app

    def update_intent(
        self,
        intent: str,
        action: str = None,
        entities: dict = None
    ):
        self.last_intent = intent
        self.last_action = action
        self.last_entities = entities or {}

    # =====================================================
    # Shared Variables
    # =====================================================

    def set(self, key: str, value: Any):
        """Store arbitrary information in shared context."""

        self.shared[key] = value

    def get(self, key: str, default=None):
        """Retrieve arbitrary information from shared context."""

        return self.shared.get(key, default)

    # =====================================================
    # Pronoun Resolution
    # =====================================================

    def resolve_pronouns(self, text: str) -> str:

        replacements = {
            "it": self.last_application,
            "that": self.last_application,
            "app": self.last_application
        }

        for word, replacement in replacements.items():

            if replacement:

                text = re.sub(
                    rf"\b{word}\b",
                    replacement,
                    text,
                    flags=re.IGNORECASE
                )

        return text

    # =====================================================
    # Query Helpers
    # =====================================================

    def get_last_command(self):

        if not self.history:
            return None

        return self.history[-1]

    # =====================================================
    # Clear Context
    # =====================================================

    def clear(self):
        """Reset conversational state."""

        self.history.clear()

        self.last_application = None
        self.last_intent = None
        self.last_action = None
        self.last_entities = {}

        self.previous_command = None

        self.last_search = None
        self.last_url = None

        self.last_timer_id = None
        self.last_volume = None
        self.last_brightness = None

        self.active_plugin = None

        self.shared.clear()


# =========================================================
# Global Context Instance
# =========================================================

context = ConversationContext()


# =========================================================
# Local Test
# =========================================================

if __name__ == "__main__":

    context.remember("open chrome")
    context.remember("search python")

    context.update_application("Google Chrome")

    context.update_intent(
        "open_app",
        action="open",
        entities={
            "application": "Google Chrome"
        }
    )

    context.set("test_value", 123)

    print("Context test successful.")
    print()
    print("Last application:", context.last_application)
    print("Last intent:", context.last_intent)
    print("Last command:", context.get_last_command())
    print("Shared test value:", context.get("test_value"))
    print("History:")

    for item in context.history:
        print(item)