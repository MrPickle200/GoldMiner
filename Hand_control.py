# hand_control.py
import cv2
import mediapipe as mp
import threading
import numpy as np
import time


class HandTracker:
    def __init__(self, show_cam=False):
        # We don't use self.show_cam for cv2.imshow anymore.
        # It's kept here, but the display logic is moved to Pygame.
        self.gesture = -1
        self.running = True

        # New: Stores the latest processed frame as a NumPy array for Pygame
        self.frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self.lock = threading.Lock()  # Use a lock for safe access to self.frame

        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        mp_hands = mp.solutions.hands
        # Configure hands to process the video frame
        hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        mp_draw = mp.solutions.drawing_utils

        cap = cv2.VideoCapture(0)

        # Camera settings
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        cap.set(cv2.CAP_PROP_EXPOSURE, -5)
        cap.set(cv2.CAP_PROP_AUTO_WB, 0)
        cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4500)

        while self.running:
            success, frame = cap.read()
            if not success:
                time.sleep(0.01)  # Avoid busy waiting if camera fails
                continue

            frame = cv2.flip(frame, 1)
            # Convert to RGB only for MediaPipe processing
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            gesture = -1

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
                    landmarks = handLms.landmark

                    fingers_up = 0
                    tips = [8, 12, 16, 20]
                    bases = [6, 10, 14, 18]

                    # Simple gesture logic
                    for tip, base in zip(tips, bases):
                        if landmarks[tip].y < landmarks[base].y:  # Finger is up
                            fingers_up += 1

                    gesture = 0 if fingers_up >= 3 else 1

                    cv2.putText(frame, f'Gesture: {"Open" if gesture == 0 else "Closed"}',
                                (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # --- Key Change: Store frame and gesture ---
            self.gesture = gesture

            # Convert the final annotated BGR frame to RGB for Pygame
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Safely update the frame accessible by the main thread
            with self.lock:
                self.frame = rgb_frame
            # --- End Key Change ---

        cap.release()

    def stop(self):
        self.running = False
        self.thread.join()

    # New: Method for the main thread to safely get the latest frame
    def get_frame(self):
        with self.lock:
            return self.frame.copy()