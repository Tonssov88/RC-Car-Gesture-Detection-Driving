import os
import cv2
import mediapipe as mp
from gpiozero import AngularServo
from time import sleep
from collections import Counter
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Right Motor
in3= 22
in4 = 23
en_b = 18
#SERVO
serv=4

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en_b,GPIO.OUT)
GPIO.setup(serv, GPIO.OUT)

s=GPIO.PWM(serv,50)
p=GPIO.PWM(en_b,100)
p.start(30)
s.start(0)

GPIO.output(in4,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)

servo = AngularServo(4, min_pulse_width=0.0006, max_pulse_width=0.0023)

mpHands = mp.solutions.hands
mpDrawing = mp.solutions.drawing_utils
webcam = cv2.VideoCapture(0)
hands = mpHands.Hands(max_num_hands = 2)
tip=[8,12,16,20]
tipname=[8,12,16,20]
fingers=[]
finger=[]

while webcam.isOpened():
    ret, frame = webcam.read()
    frame = cv2.resize(frame, (320,240))
    #applying hand tracking model
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert to RGB to use mpHands
    results = hands.process(frame)
#     frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) # convert back to GBR to work with OpenCV

    #draw annotations on frame
    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            mpDrawing.draw_landmarks(frame, handLandmarks, mpHands.HAND_CONNECTIONS)
            for point in mpHands.HandLandmark:
                normalizedLandmark = handLandmarks.landmark[point]
                pixelCoordinatesLandmark = mpDrawing._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, 320, 240)
                list=[]
            for id, pt in enumerate (handLandmarks.landmark):
                x = int(pt.x * 320)
                y = int(pt.y * 240)
                list.append([id,x,y])
            if len(list)!=0:
                finger=[]
                if list[0][1:] < list[4][1:]: 
                   finger.append(1)
                else:
                    finger.append(0)
                
                fingers = []
                for id in range (0,4):
                    if list[tip[id]][2:] < list[tip[id]-2][2:]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
           

    x=fingers + finger
    c=Counter(x)
    up=c[1]
    down=c[0]
    print('This many fingers are up - ', up)
    print('This many fingers are down - ', down)
    
    if up == 3:
        servo.max()
    elif up == 4:
        servo.mid()
    elif up == 5:
        servo.min()
    elif up == 1:
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
    elif up == 2:
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
     
    cv2.imshow("Gestures", frame)
    if cv2.waitKey(5) == ord("q"):
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        break

webcam.release()
cv2.destroyAllWindows()