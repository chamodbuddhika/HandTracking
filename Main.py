import cv2
import time
import math
import numpy as np
import HandTrackingModule as htm
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Constants for hand gesture control
W_CAM, H_CAM = 640, 480
H_MIN, H_MAX = 50, 200
MIN_VOL = -63
COLOR = (0, 215, 255)
tip_ids = [4, 8, 12, 16, 20]  # Tip IDs for fingers

# Initialize hand detector
detector = htm.handDetector(maxHands=1, detectionCon=0.85, trackCon=0.8)

# Initialize audio control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()
max_vol = vol_range[1]

# Initialize variables
p_time = time.time()  # Initialize p_time here
vol_bar = 400
vol_per = 0
mode = 'N'  # Initialize mode to 'N'
active = 0

# Disable pyautogui fail-safe
pyautogui.FAILSAFE = False

def putText(img, mode, loc=(250, 450), color=(0, 255, 255)):
    cv2.putText(img, str(mode), loc, cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, color, 3)

def main():
    global mode, active, p_time  # Declare mode, active, and p_time as global to modify within function

    # Initialize camera
    cap = cv2.VideoCapture(0)  # Change to 1 if you have multiple cameras
    
    if not cap.isOpened():
        print("Error: Camera not found.")
        return
    
    print("Camera initialized successfully. Press 'q' to quit.")

    while True:
        success, img = cap.read()
        
        if not success:
            print("Error: Failed to capture image.")
            break
        
        img = detector.findHands(img)
        lm_list = detector.findPosition(img, draw=False)
        fingers = []

        if lm_list:
            # Thumb
            thumb_up = lm_list[4][1] > lm_list[3][1]
            fingers.append(1 if thumb_up else 0)

            # Other fingers
            for id in range(1, 5):
                if lm_list[tip_ids[id]][2] < lm_list[tip_ids[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Mode detection
            if fingers == [0, 0, 0, 0, 0] and active == 0:
                mode = 'N'
            elif (fingers == [0, 1, 0, 0, 0] or fingers == [0, 1, 1, 0, 0]) and active == 0:
                mode = 'Scroll'
                active = 1
            elif fingers == [1, 1, 0, 0, 0] and active == 0:
                mode = 'Volume'
                active = 1
            elif fingers == [1, 1, 1, 1, 1] and active == 0:
                mode = 'Cursor'
                active = 1

        # Scroll
        if mode == 'Scroll':
            active = 1
            putText(img, mode)
            cv2.rectangle(img, (200, 410), (245, 460), (255, 255, 255), cv2.FILLED)
            if fingers == [0, 1, 0, 0, 0]:
                putText(img, 'U', (200, 455), (0, 255, 0))
                pyautogui.scroll(300)
            elif fingers == [0, 1, 1, 0, 0]:
                putText(img, 'D', (200, 455), (0, 0, 255))
                pyautogui.scroll(-300)
            elif fingers == [0, 0, 0, 0, 0]:
                active = 0
                mode = 'N'

        # Volume
        if mode == 'Volume':
            active = 1
            putText(img, mode)
            if fingers[-1] == 1:
                active = 0
                mode = 'N'
            else:
                x1, y1 = lm_list[4][1], lm_list[4][2]
                x2, y2 = lm_list[8][1], lm_list[8][2] 
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                length = math.hypot(x2 - x1, y2 - y1)

                vol = np.interp(length, [H_MIN, H_MAX], [MIN_VOL, max_vol])
                vol_bar = np.interp(vol, [MIN_VOL, max_vol], [400, 150])
                vol_per = np.interp(vol, [MIN_VOL, max_vol], [0, 100])

                volume.SetMasterVolumeLevel(vol, None)

                if length < 50:
                    cv2.circle(img, (cx, cy), 11, (0, 0, 255), cv2.FILLED)

                cv2.rectangle(img, (30, 150), (55, 400), (209, 206, 0), 3)
                cv2.rectangle(img, (30, int(vol_bar)), (55, 400), (215, 255, 127), cv2.FILLED)
                cv2.putText(img, f'{int(vol_per)}%', (25, 430), cv2.FONT_HERSHEY_COMPLEX, 0.9, (209, 206, 0), 3)

        # Cursor
        if mode == 'Cursor':
            active = 1
            putText(img, mode)
            cv2.rectangle(img, (110, 20), (620, 350), (255, 255, 255), 3)
            if fingers[1:] == [0, 0, 0, 0]:
                active = 0
                mode = 'N'
            else:
                if lm_list:
                    x1, y1 = lm_list[8][1], lm_list[8][2]
                    w, h = pyautogui.size()
                    x = int(np.interp(x1, [110, 620], [0, w - 1]))
                    y = int(np.interp(y1, [20, 350], [0, h - 1]))

                    pyautogui.moveTo(x, y)

                    if fingers[0] == 0:
                        cv2.circle(img, (lm_list[4][1], lm_list[4][2]), 10, (0, 0, 255), cv2.FILLED)
                        pyautogui.click()

        # Calculate FPS
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        cv2.putText(img, f'FPS:{int(fps)}', (480, 50), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)
        cv2.imshow('Hand LiveFeed', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
