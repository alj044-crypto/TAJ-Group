#!/usr/bin/env python3
"""
Main script to run the Home Assistant with gesture recognition.
This script starts the Flask web server and the camera gesture tracker.
"""

import subprocess
import sys
import os
import threading
import time

def run_flask():
    """Run the Flask web server"""
    flask_script = os.path.join(os.path.dirname(__file__), 'First_Flask.py')
    subprocess.run([sys.executable, flask_script])

def run_camera_tracker():
    """Run the camera gesture tracker"""
    time.sleep(2)  # Wait for Flask to start
    tracker_script = os.path.join(os.path.dirname(__file__), 'CamTrack', 'TraceFinal.py')
    subprocess.run([sys.executable, tracker_script])

if __name__ == "__main__":
    print("Starting Home Assistant with Gesture Recognition...")
    print("Flask server will run on http://localhost:5000")
    print("Camera tracker will start in 2 seconds...")
    
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Start camera tracker
    run_camera_tracker()