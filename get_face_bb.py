import cv2
import sys

def get_face_bb():
    ''' get the boubding box of the face
        detects a face, saves the face as a png file, return true
        returns false if no face face is found'''
    faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    video_capture = cv2.VideoCapture(0)
    flag = 0
    while True:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.1,
            minNeighbors = 5,
            minSize = (100, 100),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
        if len(faces) > 0:
            x, y, w, h = faces[0]
            cv2.imwrite('detected_face.png', frame[y-50:y+h+50, x-50: x+w+50])
            flag = 1
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if flag:
        return True
    else:
        return False