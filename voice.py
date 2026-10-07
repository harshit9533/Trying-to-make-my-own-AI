import asyncio
import edge_tts
import os
import time
import uuid
import pygame
import speech_recognition as sr

from core.config import (
    VOICE,
    WAKE_WORD,
    LISTEN_TIMEOUT,
    PHRASE_TIME_LIMIT,
    AMBIENT_NOISE_DURATION
)

# ==========================================================
# Initialize Audio Engine
# ==========================================================

pygame.mixer.init()

recognizer = sr.Recognizer()

recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.non_speaking_duration = 0.5

microphone = sr.Microphone()

# ==========================================================
# Text To Speech
# ==========================================================

def speak(text: str):

    if not text:
        return

    print(f"Jarvis: {text}")

    filename = f"speech_{uuid.uuid4().hex}.mp3"

    async def generate():

        communicate = edge_tts.Communicate(
            text=text,
            voice=VOICE
        )

        await communicate.save(filename)

    try:

        asyncio.run(generate())

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.05)

        pygame.mixer.music.unload()

    finally:

        if os.path.exists(filename):

            try:
                os.remove(filename)

            except PermissionError:
                pass


# ==========================================================
# Internal Listen
# ==========================================================

def _listen(timeout, phrase_limit):

    with microphone as source:

        recognizer.adjust_for_ambient_noise(
            source,
            duration=AMBIENT_NOISE_DURATION
        )

        try:

            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_limit
            )

        except sr.WaitTimeoutError:

            return ""

    try:

        text = recognizer.recognize_google(audio)

        return text.lower()

    except sr.UnknownValueError:

        return ""

    except sr.RequestError:

        speak("Speech recognition service is unavailable.")

        return ""


# ==========================================================
# Wake Word
# ==========================================================

def listen_wake_word():

    print("Waiting for wake word...")

    text = _listen(
        LISTEN_TIMEOUT,
        PHRASE_TIME_LIMIT
    )

    if not text:
        return False

    print("Heard:", text)

    return WAKE_WORD in text


# ==========================================================
# Command
# ==========================================================

def listen_command():

    print("Listening...")

    command = _listen(
        timeout=5,
        phrase_limit=7
    )

    if command:

        print("You:", command)

    else:

        speak("Sorry, I didn't catch that.")

    return command


# ==========================================================
# Future Offline Hook
# ==========================================================

def recognize_offline(audio):
    """
    Placeholder for Whisper.cpp / Vosk integration.
    """
    pass