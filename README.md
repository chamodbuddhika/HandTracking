# Hand Tracking System

This is a Python-based hand gesture control system using computer vision and machine learning libraries, allowing you to control your PC with hand gestures. The system is designed to enable gesture-based actions such as scrolling, adjusting the volume, and cursor movement.

## Features

- **Scroll Control:** Scroll up or down using specific hand gestures.
- **Volume Control:** Adjust the system volume by pinching your thumb and index finger.
- **Cursor Control:** Move the cursor and click by controlling hand movements.
  
## Requirements

- Python 3.x
- OpenCV
- MediaPipe
- PyAutoGUI
- PyCaw (for audio control)
- NumPy
- comtypes

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/chamodbuddhika/HandTracking.git
    cd HandTracking
    ```

2. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the main Python file:
    ```bash
    python Main.py
    ```

## Usage

1. Make sure your camera is connected and working.
2. Run the program, and the camera feed will open, detecting your hand gestures.
3. Use the following hand gestures:
   - **Scroll:** Raise your index finger and scroll up or down.
   - **Volume Control:** Pinch your thumb and index finger, and the distance between them will control the volume.
   - **Cursor Control:** Use all fingers open to control the cursor.

## Troubleshooting

- If your camera does not initialize, ensure that it is correctly connected and that the video device is set correctly.
- Ensure that all required libraries are installed, and there are no version conflicts.

## Credits

This project uses:
- [OpenCV](https://opencv.org/) for computer vision.
- [MediaPipe](https://mediapipe.dev/) for hand tracking.
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) for automation.
- [PyCaw](https://github.com/AndreMiras/pycaw) for audio control.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
