import cv2
import mediapipe as mp
import numpy as np
import time
import threading
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a,b,c):
    a = np.array(a) #First  
    b = np.array(b) #Second
    c = np.array(c) #Third

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle >180.0:
        angle = 360 - angle

    return angle



cap = cv2.VideoCapture(0)
fps = int(cap.get(cv2.CAP_PROP_FPS))
# Curl counter variables
counter = 0
stage = None
down_frames = 0
up_frames = 0



#Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        #Recolour image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        #Make detections
        results = pose.process(image)

        #Recolour back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        h, w = image.shape[:2]

        #Extract Landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            #Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            #calculate angle
            angle = calculate_angle(shoulder,elbow,wrist)

            #Visualise angle
            cv2.putText(image, str(angle),
                            tuple(np.multiply(elbow, [680, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )
            
            #Curl counter logic
            if angle > 160:
                stage = "down"
                up_frames = 0
                down_frames += 1
            if angle < 30 and stage == "down":
                down_frames = 0
                stage = "up"
                counter += 1
            if angle < 30:
                up_frames += 1
                down_frames = 0


                                    
        except:
            pass


        #Render curl counter
        # Setup status box
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        cv2.rectangle(image, (400,0), (225,73), (245,117,16), -1)


        #Rep data
        cv2.putText(image, 'REPS', (15,12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)    
        cv2.putText(image, str(counter),
                    (10,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        up_time = (1/fps) * up_frames
        down_time = (1/fps) * down_frames
        if up_time > 0:
            time_string_up = 'Up Position Timer: ' + str(round(up_time, 1)) + 's'
            cv2.putText(image, time_string_up, (200,30), cv2.FONT_HERSHEY_SIMPLEX,0.9, (127,255,0), 2 )
        else:
            time_string_down = 'Down Position Timer: ' + str(round(down_time, 1)) + 's'
            cv2.putText(image, time_string_down, (200,30), cv2.FONT_HERSHEY_SIMPLEX,0.9, (50,50,255), 2 )              

        #Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()