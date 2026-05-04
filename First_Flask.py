from flask import Flask, render_template, request, jsonify
import pyttsx3
import threading
import json
import os

app = Flask(__name__)

# Global TTS engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 0.9)

# Gesture commands configuration
gesture_commands = {
    "circle": "Turn on lights",
    "line": "Turn off lights",
    "ZigZag": "Play music"
}

# File to store gesture commands
COMMANDS_FILE = 'gesture_commands.json'

def load_commands():
    global gesture_commands
    if os.path.exists(COMMANDS_FILE):
        with open(COMMANDS_FILE, 'r') as f:
            gesture_commands = json.load(f)

def save_commands():
    with open(COMMANDS_FILE, 'w') as f:
        json.dump(gesture_commands, f)

load_commands()

def speak_text(text):
    """Function to speak text in a separate thread"""
    def speak():
        tts_engine.say(text)
        tts_engine.runAndWait()
    
    thread = threading.Thread(target=speak)
    thread.daemon = True
    thread.start()

@app.route("/")
def home():
    return render_template('homeassistantapp.html')

@app.route("/speak", methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get('text', '')
    if text:
        speak_text(text)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'No text provided'})

@app.route("/gesture_detected", methods=['POST'])
def gesture_detected():
    data = request.get_json()
    gesture = data.get('gesture', '')
    if gesture in gesture_commands:
        command = gesture_commands[gesture]
        speak_text(f"Executing: {command}")
        # Here you could add actual home automation logic
        return jsonify({'status': 'success', 'command': command})
    return jsonify({'status': 'error', 'message': 'Unknown gesture'})

@app.route("/get_commands")
def get_commands():
    return jsonify(gesture_commands)

@app.route("/update_command", methods=['POST'])
def update_command():
    data = request.get_json()
    gesture = data.get('gesture')
    command = data.get('command')
    if gesture and command:
        gesture_commands[gesture] = command
        save_commands()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Invalid data'})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)





