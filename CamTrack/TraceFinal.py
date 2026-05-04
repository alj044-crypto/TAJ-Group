gesture_name = best_template["name"].lower()

action = "no_action"

if gesture_name == "line" and direction == "up":
    action = "volume_up"

elif gesture_name == "line" and direction == "down":
    action = "volume_down"

elif gesture_name == "circle":
    action = "light_on"

elif gesture_name == "zigzag":
    action = "play_music"

print(f"Sending action to Flask: {action}")

try:
    response = requests.post(
        FLASK_URL,
        json={
            "gesture": gesture_name,
            "direction": direction,
            "score": best_score,
            "action": action,
            "result": best_template["result"]
        },
        timeout=1
    )

    if response.status_code == 200:
        print("Flask notified successfully")
        print(response.json())
    else:
        print(f"Flask error: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Failed to contact Flask: {e}")