# config.py

# ===== Voice =====
VOICE = "en-US-GuyNeural"

# ===== Wake Word =====
WAKE_WORD = "jarvis"

# ===== Speech Recognition =====
LISTEN_TIMEOUT = 5
PHRASE_TIME_LIMIT = 7
AMBIENT_NOISE_DURATION = 0.5

# ===== Jarvis =====
JARVIS_NAME = "Jarvis"

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

LOG_FILE = DATA_DIR / "logs.txt"

MEMORY_FILE = DATA_DIR / "memory.txt"