import numpy as np
import handDetector as hand
import time
import cv2

#url = "http://192.168.1.74" #esta es la ip en la que esta la transmisión de video
#cap = cv2.VideoCapture(url)
#cap = cv2.VideoCapture(0)
#detector = hand.handDetector()

class gestos:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.detector = hand(detectionCon=0.7, trackCon=0.7)

    def ejecutar(self):
        prev_time = 0
        while True:
            ret, img = self.cap.read()
            if not ret:
                print("Error al capturar el frame")
                break
            img = self.detector.findHands(img)
            lm_list, b_box = self.detector.findPosition(img)
            if lm_list:
                fingers = self.detector.fingersUp()
                if all(num == 0 for num in fingers):
                    print("Mano cerrada")
                elif all(num == 1 for num in fingers):
                    print("Mano abierta")
                elif fingers[0] == 1:
                    print("Pulgar arriba")
                elif fingers[1] == 1:
                    print("Índice arriba")
                elif fingers[2] == 1:
                    print("Medio arriba")
                elif fingers[3] == 1:
                    print("Anular arriba")
                elif fingers[4] == 1:
                    print("Meñique arriba")
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
            prev_time = curr_time
            cv2.putText(img, f"FPS: {int(fps)}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow("Image", img)
            if cv2.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
        print("Detección por video cancelada")

if __name__ == '__main__':
    x = gestos()
    x.ejecutar()