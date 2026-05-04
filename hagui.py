
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import threading
import time
import subprocess
app = Flask(__name__)

CORS(app)

###############################
#alarm section
###############################

alarms = []
triggered_alarm = None

@app.route("/set_alarm", methods=["POST"])
def set_alarm():
    data = request.json
    alarm_time = data.get("time")
    
    if alarm_time:
        if alarm_time in alarms:
            pass
        else:
            alarms.append(alarm_time)
            print(f"[INFO] Alarm set for {alarm_time}")

    return jsonify({
        "status": "ok",
        "alarms": list(alarms)
    })

@app.route("/check_alarm", methods=["GET"])
def check_alarm():
    global triggered_alarm

    if triggered_alarm:
        alarm_time = triggered_alarm
        triggered_alarm = None

        return jsonify({
            "trigger": True,
            "time": alarm_time
        })
    return jsonify({
        "trigger": False
    })

def alarm_checker():
    global triggered_alarm

    while True:
        now = datetime.now().strftime("%H:%M")
        
        if now in alarms:
            print("Alarm triggered!", now)
            triggered_alarm = now

            alarms.remove(now)
        
        time.sleep(1)

@app.route("/alarms", methods=["GET"])
def get_alarms():
    return jsonify({
        "alarms": list(alarms)
    })

def delete_alarm(time):
    global alarms

    if time in alarms:
        alarms.remove(time)
        return True
    return False

@app.route("/delete_alarm", methods=["POST"])
def delete_alarm_route():
    data = request.get_json()
    time = data.get("time")

    success = delete_alarm(time)

    return jsonify({
        "success": success,
        "alarms": alarms
    })

##################################
#timer section
###################################

timer_state = {
    "running": False,
    "remaining": 0,
    "start_time": None
}

@app.route("/start_timer", methods=["POST"])
def start_timer():
    data = request.json
    hours = int(data.get("hours", 0))
    minutes = int(data.get("minutes", 0))
    seconds = int(data.get("seconds", 0))

    total = hours * 3600 + minutes * 60 + seconds

    timer_state["running"] = True
    timer_state["remaining"] = total

    return jsonify({"status": "started", "remaining": total})

@app.route("/pause_timer", methods=["POST"])
def pause_timer():
    timer_state["running"] = False
    return jsonify({"status": "paused", "remaining": timer_state["remaining"]})

@app.route("/cancel_timer", methods=["POST"])
def cancel_timer():
    timer_state["running"] = False
    timer_state["remaining"] = 0
    return jsonify({"status": "cancelled"})

@app.route("/timer_status", methods=["GET"])
def timer_status():
    return jsonify(timer_state)

def timer_loop():
    while True:
        time.sleep(1)

        if not timer_state["running"]:
            continue

        if timer_state["remaining"] > 0:
            timer_state["remaining"] -= 1

            if timer_state["remaining"] <= 0:
                timer_state["remaining"] = 0
                timer_state["running"] = False

#############################
#stopwatch section
#############################

@app.route("/start_stopwatch", methods=["POST"])
def start_stopwatch():
    return jsonify({"ok": True})

@app.route("/pause_stopwatch", methods=["POST"])
def pause_stopwatch():
    return jsonify({"ok": True})

@app.route("/reset_stopwatch", methods=["POST"])
def reset_stopwatch():
    return jsonify({"ok": True})

#################################
#Audio Section
#################################

def set_volume(level):
    try:
        subprocess.run(
            f"pactl set-sink-volume @DEFAULT_SINK@ {level}%",
            shell=True
        )
    except Exception as e:
        print("[AUDIO FAIL]", e)

def toggle_mute():
    try:
        subprocess.run(
            "pactl set-sink-mute @DEFAULT_SINK@ toggle",
            shell=True
        )
    except Exception as e:
        print("[MUTE FAIL]")

@app.route("/audio_volume", methods=["POST"])
def audio_volume():
    data = request.json
    level = int(data.get("level", 50))

    set_volume(level)

    return jsonify({
        "ok": True,
        "volume": level
    })

@app.route("/audio_mute", methods=["POST"])
def audio_mute():
    toggle_mute()

    return jsonify({
        "ok": True
    })

if __name__ == "__main__":
    threading.Thread(target=alarm_checker, daemon=True).start()
    threading.Thread(target=timer_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=False)