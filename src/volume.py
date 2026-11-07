import cv2
import mediapipe as mp
from pycaw.pycaw import AudioUtilities

mp_hand = mp.solutions.hands.Hands(max_num_hands=1)
draw_util = mp.solutions.drawing_utils

speakers = AudioUtilities.GetSpeakers()
volume = speakers.EndpointVolume

cap = cv2.VideoCapture(0)

finger_counter = 0
last_applied = -1       
candidate = -1         
stable_frames = 0       
STABLE_NEEDED = 5

status_text = 'NO HAND'
status_color = (255, 255, 255)

finger_tips = [8, 12, 16, 20]


def dist(a, b):
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


while True:

    finger_counter = 0
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_hand.process(frameRGB)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:

            landmark = hand.landmark
            draw_util.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)

            
            for tip in finger_tips:
                if landmark[tip].y < landmark[tip - 2].y:
                    finger_counter += 1

            
            if dist(landmark[4], landmark[17]) > dist(landmark[3], landmark[17]) * 1.1:
                finger_counter += 1

        
        if finger_counter == candidate:
            stable_frames += 1
        else:
            candidate = finger_counter
            stable_frames = 0

        if stable_frames >= STABLE_NEEDED and finger_counter != last_applied:

            if finger_counter == 0:
                volume.SetMasterVolumeLevelScalar(0.0, None)
                volume.SetMute(1, None)
                status_text = 'MUTED'
                status_color = (0, 0, 255)
                last_applied = finger_counter

            else:
                volume.SetMute(0, None)
                status_color = (0, 255, 0)

                if finger_counter == 1:
                    volume.SetMasterVolumeLevelScalar(0.30, None)
                    status_text = 'VOLUME 30%'
                    last_applied = finger_counter
                elif finger_counter == 2:
                    volume.SetMasterVolumeLevelScalar(0.60, None)
                    status_text = 'VOLUME 60%'
                    last_applied = finger_counter
                elif finger_counter == 3:
                    volume.SetMasterVolumeLevelScalar(0.90, None)
                    status_text = 'VOLUME 90%'
                    last_applied = finger_counter
                elif finger_counter == 5:
                    volume.SetMasterVolumeLevelScalar(1.0, None)
                    status_text = 'VOLUME 100%'
                    last_applied = finger_counter
    else:
        last_applied = -1
        candidate = -1
        stable_frames = 0
        status_text = 'NO HAND'
        status_color = (255, 255, 255)

    cv2.putText(frame, f'Fingers: {finger_counter}', (50, 60),
                cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 255, 255), 3)

    cv2.putText(frame, status_text, (50, 130),
                cv2.FONT_HERSHEY_COMPLEX, 2, status_color, 3)

    cv2.imshow('WebCam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()