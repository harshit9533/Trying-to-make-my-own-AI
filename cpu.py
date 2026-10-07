import psutil
from core.voice import speak

PLUGIN = {
    "name": "CPU",
    "commands": [
        "cpu",
        "cpu usage",
        "processor usage",
        "how much cpu"
    ]
}

def run(command):

    usage = psutil.cpu_percent(interval=1)

    speak(f"CPU usage is {usage} percent.")