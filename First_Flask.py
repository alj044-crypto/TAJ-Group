from flask import Flask, render_template, request, jsonify
import pyttsx3
import threading
import json
import os
import actions

app = Flask(__name__)

tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 150)
tts_engine.setProperty("volume", 0.9)

COMMANDS_FILE = "gesture_commands.json"

gesture_commands = {
    "circle": "Turn on lights",
    "zigzag": "Play music",
    "line_up": "Volume up",
    "line_down": "Volume down"
}


def load_commands():
    global gesture_commands
    if os.path.exists(COMMANDS_FILE):
        with open(COMMANDS_FILE, "r") as f:
            gesture_commands = json.load(f)


def save_commands():
    with open(COMMANDS_FILE, "w") as f:
        json.dump(gesture_commands, f)


load_commands()


def speak_text(text):
    def speak():
        tts_engine.say(text)
        tts_engine.runAndWait()

    thread = threading.Thread(target=speak)
    thread.daemon = True
    thread.start()


# =========================
# DEVICE ACTION FUNCTIONS
# =========================

def volume_up():
    print("Volume up called")
    speak_text("Volume up")
    actions.volume_up()


def volume_down():
    print("Volume down called")
    speak_text("Volume down")
    actions.volume_down()


def light_on():
    print("Light on called")
    speak_text("Turning on lights")
    # Add real light code here later


def play_music():
    print("Play music called")
    speak_text("Playing music")
    actions.play_music()


def no_action():
    print("No valid action found")
    speak_text("No valid action found")


def decide_action(gesture, direction):
    gesture = gesture.lower()
    direction = direction.lower()

    if gesture == "line" and direction == "up":
        return "volume_up"

    if gesture == "line" and direction == "down":
        return "volume_down"

    if gesture == "circle":
        return "light_on"

    if gesture == "zigzag":
        return "play_music"

    return "no_action"


def execute_action(action):
    if action == "volume_up":
        volume_up()
        return "Volume up"

    elif action == "volume_down":
        volume_down()
        return "Volume down"

    elif action == "light_on":
        light_on()
        return "Turn on lights"

    elif action == "play_music":
        play_music()
        return "Play music"

    else:
        no_action()
        return None


@app.route("/")
def home():
    return render_template("homeassistantapp.html")


@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "")

    if text:
        speak_text(text)
        return jsonify({"status": "success"})

    return jsonify({"status": "error", "message": "No text provided"})


@app.route("/gesture_detected", methods=["POST"])
def gesture_detected():
    data = request.get_json()

    gesture = data.get("gesture", "").lower()
    direction = data.get("direction", "").lower()
    score = data.get("score", None)

    # If camera sends action directly, use it.
    action = data.get("action", "").lower()

    # Otherwise decide action from gesture + direction.
    if not action:
        action = decide_action(gesture, direction)

    print("Gesture:", gesture)
    print("Direction:", direction)
    print("Score:", score)
    print("Action:", action)

    command = execute_action(action)

    if command is None:
        return jsonify({
            "status": "error",
            "message": "Unknown gesture or direction",
            "gesture": gesture,
            "direction": direction,
            "action": action,
            "score": score
        })

    return jsonify({
        "status": "success",
        "command": command,
        "gesture": gesture,
        "direction": direction,
        "action": action,
        "score": score
    })


@app.route("/get_commands")
def get_commands():
    return jsonify(gesture_commands)


@app.route("/update_command", methods=["POST"])
def update_command():
    data = request.get_json()

    gesture = data.get("gesture")
    command = data.get("command")

    if gesture and command:
        gesture_commands[gesture] = command
        save_commands()
        return jsonify({"status": "success"})

    return jsonify({"status": "error", "message": "Invalid data"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)