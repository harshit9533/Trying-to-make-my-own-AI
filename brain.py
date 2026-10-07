import re
import logging
from dataclasses import dataclass, field
from typing import Dict, Any

logger = logging.getLogger(__name__)


# ===================================================
# Conversation Memory
# ===================================================

MEMORY = {
    "last_application": None,
    "previous_command": None
}


# ===================================================
# Synonyms
# ===================================================

SYNONYMS = {

    "launch": "open",
    "run": "open",
    "execute": "open",
    "start": "open",

    "terminate": "close",
    "kill": "close",
    "quit": "close",
    "shut": "close",

    "turn up": "increase",
    "turn down": "decrease",

    "louder": "increase volume",
    "quieter": "decrease volume"
}


# ===================================================
# Fluff Removal
# ===================================================

FLUFF_REGEX = re.compile(
    r"\b("
    r"jarvis|"
    r"please|"
    r"could you|"
    r"can you|"
    r"would you|"
    r"kindly|"
    r"for me|"
    r"right now"
    r")\b",
    re.IGNORECASE
)


# ===================================================
# Result Object
# ===================================================

@dataclass
class BrainResult:

    cleaned_command: str

    entities: Dict[str, Any] = field(default_factory=dict)


# ===================================================
# Internal Functions
# ===================================================

def _remove_fluff(text):

    text = FLUFF_REGEX.sub("", text)

    return re.sub(r"\s+", " ", text).strip()


def _normalize(text):

    text = text.lower()

    for old, new in SYNONYMS.items():
        text = text.replace(old, new)

    return text


def _resolve_context(text):

    if MEMORY["last_application"]:

        text = re.sub(
            r"\bit\b",
            MEMORY["last_application"],
            text
        )

    return text


def _extract_entities(text):

    entities = {}

    numbers = re.findall(r"\d+", text)

    if numbers:

        entities["numbers"] = [int(n) for n in numbers]

    return entities


def _remember(text):

    MEMORY["previous_command"] = text

    if text.startswith("open "):

        MEMORY["last_application"] = text[5:].strip()


# ===================================================
# Public API
# ===================================================

def think(raw_command):

    logger.debug(raw_command)

    command = raw_command.lower()

    command = _remove_fluff(command)

    command = _normalize(command)

    command = _resolve_context(command)

    entities = _extract_entities(command)

    _remember(command)

    return BrainResult(

        cleaned_command=command,

        entities=entities

    )