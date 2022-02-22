import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

from array import array
from socket import *

size = 33
marks = array('f',range(size*4))

HOST = '127.0.0.1'
PORT = 9000
#BUFSIZ = 1024
ADDRESS = (HOST, PORT)

udpClientSocket = socket(AF_INET, SOCK_DGRAM)


# For static images:

# For webcam input:
cap = cv2.VideoCapture(0)

frameno = 0

#file_handle=open('1.txt',mode='w')

#cap = cv2.VideoCapture("test.mp4")
with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      break
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = holistic.process(image)

    # Draw landmark annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.face_landmarks,
        mp_holistic.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles
        .get_default_face_mesh_contours_style())
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles
        .get_default_pose_landmarks_style())

    landmarks = results.pose_landmarks

    for i in range(0,size):
          marks[i*4+0] = landmarks.landmark[i].x
          marks[i*4+1] = landmarks.landmark[i].y
          marks[i*4+2] = landmarks.landmark[i].z
          marks[i*4+3] = landmarks.landmark[i].visibility
          print(i)
          print(landmarks)
    udpClientSocket.sendto(marks.tobytes(), ADDRESS)
    #print(i)
    #print(landmarks)

    #print (type(results.pose_landmarks))
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Holistic', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
    print(frameno)

    #file_handle.write(landmarks)

    #file_handle.write("@")
    #file_handle.write("\n")

    #file_handle.write(str(landmarks))
    #file_handle.write("\n")


    frameno = frameno+1
cap.release()

#file_handle.close()