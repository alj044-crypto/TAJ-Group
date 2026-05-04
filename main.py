#!/usr/bin/env python3
"""
Main script to run the Home Assistant with gesture recognition,
Flask server, camera tracker, and voice wake-word commands.
"""

import subprocess
import sys
import os
import threading
import time
import speech_recognition as sr
import pyttsx3
import actions  # separate actions.py file


WAKE_WORDS = ["hey rock", "okay rock"]


def run_flask():
    """Run the Flask web server"""
    flask_script = os.path.join(os.path.dirname(__file__), "First_Flask.py")
    subprocess.run([sys.executable, flask_script])


def run_camera_tracker():
    """Run the camera gesture tracker"""
    time.sleep(2)
    tracker_script = os.path.join(os.path.dirname(__file__), "CamTrack", "TraceFinal.py")
    subprocess.run([sys.executable, tracker_script])


def speak(text):
    """Speak and print assistant responses"""
    print("Rock:", text)
    speaker.say(text)
    speaker.runAndWait()


def listen():
    """Listen to microphone and return recognized text"""
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio).lower()
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("Speech recognition service error.")
        return ""


def handle_command(command):
    """Handle voice commands"""

    if "play music" in command:
        speak("Playing music.")
        actions.play_music()

    elif "turn volume up" in command:
        speak("Turning volume up.")
        actions.volume_up()

    elif "turn volume down" in command:
        speak("Turning volume down.")
        actions.volume_down()

    elif "exit" in command or "quit" in command:
        speak("Shutting down voice commands.")
        return False

    else:
        speak("Command not recognized.")

    return True


def run_voice_assistant():
    """Run wake-word voice assistant"""
    speak("Rock voice assistant is ready.")

    running = True

    while running:
        text = listen()

        if any(wake_word in text for wake_word in WAKE_WORDS):
            speak("Yes?")
            command = listen()
            running = handle_command(command)

        time.sleep(0.2)


if __name__ == "__main__":
    print("Starting Home Assistant with Gesture Recognition...")
    print("Flask server will run on http://localhost:5000")
    print("Camera tracker will start in 2 seconds...")
    print("Voice assistant wake words: Hey Rock, Okay Rock")

    # Initialize voice tools
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    speaker = pyttsx3.init()

    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Start voice assistant in a separate thread
    voice_thread = threading.Thread(target=run_voice_assistant, daemon=True)
    voice_thread.start()

    # Start camera tracker in main thread
    run_camera_tracker()