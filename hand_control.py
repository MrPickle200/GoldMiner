# hand_control.py
import cv2
import mediapipe as mp
import threading

class HandTracker:
    def __init__(self, show_cam=False):
        self.gesture = -1
        self.running = True
        self.show_cam = show_cam
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        mp_draw = mp.solutions.drawing_utils

        cap = cv2.VideoCapture(0)

        # Manual exposure (try values -7 to -2 depending on brightness)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        cap.set(cv2.CAP_PROP_EXPOSURE, -5)

        # Manual white balance (optional, may not be supported)
        cap.set(cv2.CAP_PROP_AUTO_WB, 0)
        cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4500)

        while self.running:
            success, frame = cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            gesture = -1

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
                    landmarks = handLms.landmark
                    h, w, _ = frame.shape

                    fingers_up = 0
                    tips = [8, 12, 16, 20]
                    bases = [6, 10, 14, 18]

                    for tip, base in zip(tips, bases):
                        if landmarks[tip].y < landmarks[base].y:  # Finger is up
                            fingers_up += 1

                    gesture = 0 if fingers_up >= 3 else 1

                    cv2.putText(frame, f'Gesture: {"Open" if gesture == 0 else "Closed"}',
                                (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            self.gesture = gesture

            if self.show_cam:
                cv2.imshow("Hand Camera", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False
                    break

        if self.show_cam:
            cv2.destroyAllWindows()
        cap.release()

    def stop(self):
        self.running = False
        self.thread.join()
