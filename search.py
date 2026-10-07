import webbrowser
from urllib.parse import quote_plus
from core.voice import speak

PLUGIN = {
    "name": "Google Search",
    "commands": [
        "search",
        "google find",
        "google search",
        "search for"
    ]
}


def run(command):

    query = command.lower()

    # Remove trigger words
    for phrase in PLUGIN["commands"]:
        if query.startswith(phrase):
            query = query[len(phrase):].strip()
            break

    if not query:
        speak("What would you like me to search for?")
        return

    speak(f"Searching Google for {query}")

    url = f"https://www.google.com/search?q={quote_plus(query)}"

    webbrowser.open(url)