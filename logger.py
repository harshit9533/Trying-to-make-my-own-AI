from datetime import datetime
from config import LOG_FILE


def log(user_text, jarvis_text):

    with open(LOG_FILE, "a", encoding="utf-8") as f:

        f.write("\n")
        f.write("=" * 60 + "\n")
        f.write(f"Time   : {datetime.now()}\n")
        f.write(f"User   : {user_text}\n")
        f.write(f"Jarvis : {jarvis_text}\n")