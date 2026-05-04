import os
import random
import subprocess

# Folder where your music lives
MUSIC_FOLDER = "/home/pi/music"  # change this path

# Keep track of current player process
current_process = None


def get_music_files():
    """Return list of mp3 files in folder"""
    return [
        os.path.join(MUSIC_FOLDER, f)
        for f in os.listdir(MUSIC_FOLDER)
        if f.endswith(".mp3")
    ]


def play_music():
    """Play a random MP3 file"""
    global current_process

    music_files = get_music_files()

    if not music_files:
        print("No music files found.")
        return

    # Stop previous song if playing
    if current_process:
        current_process.terminate()

    song = random.choice(music_files)
    print(f"Playing: {song}")

    # Play audio
    current_process = subprocess.Popen(["mpg123", "-q", song])


def volume_up():
    """Increase volume"""
    subprocess.run(["amixer", "sset", "Master", "10%+"])
    print("Volume increased")


def volume_down():
    """Decrease volume"""
    subprocess.run(["amixer", "sset", "Master", "10%-"])
    print("Volume decreased")