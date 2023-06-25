import cv2
import mediapipe as md

md_drawing = md.solutions.drawing_utils
md_drawing_styles = md.solutions.drawing_styles
md_pose = md.solutions.pose

count = 0

pull_position = None
push_position = None
situp_position = None
cap = cv2.VideoCapture(0)

with md_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            print("empty camera")
            break

        img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        res = pose.process(img)

        pos = []

        if res.pose_landmarks:
            md_drawing.draw_landmarks(img, res.pose_landmarks, md_pose.POSE_CONNECTIONS)
        for i, j in enumerate(res.pose_landmarks.landmark):
            h, w, _ = img.shape
            X,Y = int(j.x * w), int(j.y * h)
            pos.append([i, X, Y])
        if len(pos) != 0:

            if (pos[12][2] and pos[11][2] >= pos[14][2] and pos[13][2]) and (pos[5][2] and pos[0][2] <= pos[20][2] and pos[19][2]):
                push_position = "push_down"
            if((pos[12][2] and pos[11][2] <= pos[14][2] and pos[13][2]) and push_position == "push_down") and (pos[5][2] and pos[0][2] <= pos[20][2] and pos[19][2]):
                push_position = "push_up"
                print("PUSHUP")

            if(pos[5][2] and pos[0][2] >= pos[20][2] and pos[19][2]):
                pull_position ="pull_down"
            if(pos[5][2] and pos[0][2] <= pos[20][2] and pos[19][2]) and pull_position == "pull_down":
                pull_position = "pull_up"
                print("PULLUP")

            if (pos[24][2] and pos[23][2] >= pos[26][2] and pos[25][2]):
                situp_position = "pull_down"
            if (pos[24][2] and pos[23][2] <= pos[26][2] and pos[25][2]) and situp_position == "pull_down":
                situp_position = "pull_up"
                print("SITUP")

            cv2.imshow("Push-up and Pull-up", cv2.flip(img, 1))
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

cap.release()