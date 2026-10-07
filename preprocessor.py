import re
from .context import ConversationContext

# ==========================================================
# Pre-compiled Regular Expressions
# ==========================================================

FLUFF_REGEX = re.compile(
    r"\b("
    r"jarvis|"
    r"please|"
    r"could you please|"
    r"can you please|"
    r"could you|"
    r"can you|"
    r"would you|"
    r"would you mind|"
    r"kindly|"
    r"for me|"
    r"right now|"
    r"just|"
    r"actually"
    r")\b",
    re.IGNORECASE
)

MULTISPACE_REGEX = re.compile(r"\s+")

# ==========================================================
# Phrase Synonyms
# (Longest phrases first)
# ==========================================================

SYNONYMS = {

    # Open
    "launch": "open",
    "run": "open",
    "execute": "open",
    "fire up": "open",

    # Close
    "terminate": "close",
    "kill": "close",
    "quit": "close",
    "shut down": "close",
    "shut": "close",

    # Volume
    "turn up": "increase",
    "turn down": "decrease",

    "volume up": "increase volume",
    "volume down": "decrease volume",

    "louder": "increase volume",
    "quieter": "decrease volume",

    # Brightness
    "brighten": "increase brightness",
    "dim": "decrease brightness",

    # Screenshot
    "capture screen": "take screenshot",
    "capture the screen": "take screenshot",

    # Media
    "skip song": "next song",
    "skip track": "next track",

    "go back": "previous track"
}

# ==========================================================
# Cleaning
# ==========================================================

def clean(text: str) -> str:

    text = text.lower().strip()

    text = FLUFF_REGEX.sub("", text)

    text = MULTISPACE_REGEX.sub(" ", text)

    return text.strip()

# ==========================================================
# Phrase Normalization
# ==========================================================

def normalize(text: str) -> str:

    # Replace longest phrases first
    for phrase in sorted(
        SYNONYMS.keys(),
        key=len,
        reverse=True
    ):
        text = text.replace(
            phrase,
            SYNONYMS[phrase]
        )

    return text

# ==========================================================
# Final Preprocessor
# ==========================================================

def preprocess(
    text: str,
    context: ConversationContext
) -> str:

    text = clean(text)

    text = normalize(text)

    text = context.resolve_pronouns(text)

    return text