import numpy as np
import handDetector as hand
import time
import cv2

#url = "http://192.168.1.74" #esta es la ip en la que esta la transmisión de video
#cap = cv2.VideoCapture(url)
cap = cv2.VideoCapture(0)
detector = hand.handDetector()

while True:
    cap.open(url)
    ret,img = cap.read()
    if ret:
        img = detector.findHands(img)
        lm_list,b_box = detector.findPosition(img)
        if len(lm_list) != 0:
            fingers = detector.fingersUp()
            if all(num==0 for num in fingers):
                print("Mano cerrada")
            elif all(num==1 for num in fingers):
                print("Mano abierta")
            elif fingers[0]==1:
                print("Pulgar arriba")
            elif fingers[1]==1:
                print("Indice arriba")
            elif fingers[2]==1:
                print("Medio arriba")
            elif fingers[3]==1:
                print("Anular arriba")
            elif fingers[4]==1:
                print("Meñique arriba")
        cv2.imshow("Image", img)
    if cv2.waitKey(1)==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()