import os
import random
import subprocess
import platform

MUSIC_FOLDER = r"C:\Users\ajaxs\Music"

current_process = None


def get_music_files():
    if not os.path.exists(MUSIC_FOLDER):
        print("Music folder does not exist:", MUSIC_FOLDER)
        return []

    return [
        os.path.join(MUSIC_FOLDER, f)
        for f in os.listdir(MUSIC_FOLDER)
        if f.lower().endswith(".mp3")
    ]


def play_music():
    global current_process

    music_files = get_music_files()

    if not music_files:
        print("No music files found.")
        return

    song = random.choice(music_files)
    print(f"Playing: {song}")

    system = platform.system()

    if system == "Windows":
        os.startfile(song)

    elif system == "Linux":
        current_process = subprocess.Popen(["mpg123", "-q", song])

    else:
        print("Unsupported OS for music playback")


def volume_up():
    system = platform.system()

    if system == "Linux":
        subprocess.run(["amixer", "sset", "Master", "10%+"])
    elif system == "Windows":
        print("Windows volume up placeholder")
        # Add pycaw later if needed

    print("Volume increased")


def volume_down():
    system = platform.system()

    if system == "Linux":
        subprocess.run(["amixer", "sset", "Master", "10%-"])
    elif system == "Windows":
        print("Windows volume down placeholder")
        # Add pycaw later if needed

    print("Volume decreased")