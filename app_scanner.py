import json
from pathlib import Path

# ==========================================
# HARDCODED PATHS (YOUR COMPUTER ONLY)
# ==========================================

SYSTEM_START_MENU = Path(
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
)

USER_START_MENU = Path(
    r"C:\Users\DELL\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
)

OUTPUT_FILE = Path(r"D:\Jarvis\data\apps.json")

# ==========================================
# Scan Applications
# ==========================================

def scan_apps():

    apps = {}

    folders = [
        SYSTEM_START_MENU,
        USER_START_MENU
    ]

    for folder in folders:

        if not folder.exists():
            continue

        for shortcut in folder.rglob("*.lnk"):

            display_name = shortcut.stem.strip()

            app_name = display_name.lower()

            # Ignore duplicates
            if app_name in apps:
                continue

            apps[app_name] = {
                "display_name": display_name,
                "path": str(shortcut)
            }

    return apps


# ==========================================
# Save Database
# ==========================================

def save_apps(apps):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            apps,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Saved {len(apps)} applications.")


# ==========================================
# Load Database
# ==========================================

def load_apps():

    if not OUTPUT_FILE.exists():

        apps = scan_apps()

        save_apps(apps)

        return apps

    with open(
        OUTPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ==========================================
# Refresh Database
# ==========================================

def refresh_apps():

    apps = scan_apps()

    save_apps(apps)

    print("Application database refreshed.")

    return apps


# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    apps = refresh_apps()

    print("\nInstalled Applications\n")

    for app in sorted(apps.values(), key=lambda x: x["display_name"].lower()):

        print(app["display_name"])
        print(app["path"])
        print()