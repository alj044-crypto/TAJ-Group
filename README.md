# TAJ-Group Home Assistant with Gesture Recognition

A home assistant application that uses hand gesture recognition for non-verbal commands, with text-to-speech feedback.

## Features

- **Gesture Recognition**: Uses YOLO and template matching to recognize hand gestures (circle, line, zigzag)
- **Text-to-Speech**: Provides audio feedback for detected gestures
- **Web Interface**: Modern home assistant UI with gesture configuration
- **Flask Backend**: REST API for gesture commands and TTS

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- Flask
- pyttsx3
- opencv-python
- ultralytics
- numpy
- requests

### 2. Configure Gesture Templates

Place template images in `CamTrack/Template Images/`:
- `circle.png`
- `line.png`
- `zigzag.png`

### 3. Update Model Path

Edit `CamTrack/TraceFinal.py` and update `MODEL_PATH` to point to your trained YOLO model.

## Usage

### Start the Web Server

```bash
python First_Flask.py
```

The web interface will be available at `http://localhost:5000`

### Start Gesture Recognition

```bash
python CamTrack/TraceFinal.py
```

### Configure Gestures

1. Open the web interface
2. Click the settings button (⚙️)
3. Select "Gestures" from the menu
4. Click "Load Current Commands" to see existing gestures
5. Edit commands and click "Update" for each gesture

## Gesture Commands

Default gestures:
- **Circle**: Turn on lights
- **Line**: Turn off lights
- **Zigzag**: Play music

## API Endpoints

- `GET /`: Main web interface
- `POST /speak`: Trigger text-to-speech
- `POST /gesture_detected`: Notify of detected gesture
- `GET /get_commands`: Get current gesture commands
- `POST /update_command`: Update a gesture command

## Finishing Touches

- [ ] Test TTS functionality
- [ ] Verify gesture recognition accuracy
- [ ] Add more gesture templates
- [ ] Implement actual home automation integration
- [ ] Add user authentication
- [ ] Improve UI responsiveness 
