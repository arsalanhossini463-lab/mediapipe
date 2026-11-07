# Hand Gesture Recognition

Python scripts that use your webcam to recognize hand gestures in real time with OpenCV and MediaPipe. They count raised fingers, recognize a fist, an open hand and the victory sign, and one script controls the Windows system volume with your fingers.

Everything runs locally. No video is uploaded or saved (except the screenshot taken by `Victory.py`).

## Files

| File | Description |
|------|-------------|
| `app.py` | Counts the raised fingers of up to 4 hands and shows the total on the video. |
| `app_2.py` | Tracks one hand and shows a label: `Baz` (open hand), `Four`, `Three`, `Two`, `One` or `Mosht` (fist). |
| `app_3.py` | Same as `app_2.py` with the `Two` label fixed. |
| `Victory.py` | Detects the victory sign, shows `VICTORY` / `NOT VICTORY` and saves a screenshot as `screen.png`. |
| `volume.py` | Controls the Windows master volume with your fingers. Windows only. |

### Volume control (`volume.py`)

| Fingers | Action |
|---------|--------|
| 0 (fist) | Mute |
| 1 | Volume 30% |
| 2 | Volume 60% |
| 3 | Volume 90% |
| 5 (open hand) | Volume 100% |

## Requirements

- Python 3
- A webcam
- The packages in `requirements.txt`: `opencv-python`, `mediapipe`, and `pycaw` (only for `volume.py`, Windows only)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
python app_3.py
python Victory.py
python volume.py
```

A window called **WebCam** opens. Show your hand to the camera and press **q** to quit.

## Notes

- Detection works best with good lighting and your palm facing the camera. The thumb is the least reliable finger.
- `Victory.py` overwrites `screen.png` every time the sign is detected.
- If the camera does not open, change `cv2.VideoCapture(0)` to `1`.
