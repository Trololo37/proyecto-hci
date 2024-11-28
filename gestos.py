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
        self.detector = hand.handDetector(detectionCon=0.7, trackCon=0.7)

    def ejecutar(self):
        prev_time = 0
        prev_value=0
        counter=0
        while True:
            ret, img = self.cap.read()
            if not ret:
                print("Error al capturar el frame")
                break
            img = self.detector.findHands(img)
            lm_list, b_box = self.detector.findPosition(img)
            if lm_list:
                fingers = self.detector.fingersUp()
                if fingers[1] == 1:
                    if fingers[2]==1:
                        if fingers[3]==1:
                            if fingers[4]==1 or fingers[0]==1:
                                counter=0
                                prev_value=0
                                print("Comando no reconocido")
                            elif self.comparator(prev_value, curr_value=3):
                                counter+=1
                                if counter >= 10:
                                    print("\nMáxima intensidad")
                                    return '3'
                            else:
                                counter=0
                                prev_value=3
                        else: 
                            if self.comparator(prev_value, curr_value=2):
                                counter+=1
                                if counter >= 10:
                                    print("\n\nIntensidad media")
                                    return '2'
                            else:
                                counter=0
                                prev_value=2
                    else:
                        if self.comparator(prev_value, curr_value=1):
                            counter+=1
                            if counter >= 10:
                                print("\n\nIntensidad mínima")
                                return '1'
                        else:
                            counter=0
                            prev_value=1
                elif all(num == 1 for num in fingers):
                    if self.comparator(prev_value, curr_value=4):
                        counter+=1
                        if counter >= 15:
                            print("\n\nApagar Foco seleccionado")
                            return '0'
                    else:
                        counter=0
                        prev_value=4
                elif all(num == 0 for num in fingers):
                    if self.comparator(prev_value, curr_value=4):
                        counter+=1
                        if counter >= 20:
                            print("\n\nCANCELAR DETECCION POR GESTOS")
                            break
                    else:
                        counter=0
                        prev_value=4

            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
            prev_time = curr_time

            cv2.putText(img, f"FPS: {int(fps)}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            cv2.imshow("Image", img)

            if cv2.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
        print("Detección por video cancelada")
    
    def comparator(self, prev_value, curr_value):
        if curr_value == prev_value:
            return True
        else:
            return False

if __name__ == '__main__':
    x = gestos()
    x.ejecutar()