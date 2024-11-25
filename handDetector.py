import mediapipe as mp
import math
import cv2

class handDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = bool(mode)  # Booleano
        self.maxHands = int(maxHands)  # Entero
        self.detectionCon = float(detectionCon)  # Flotante
        self.trackCon = float(trackCon)  # Flotante

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tip = [4,8,12,16,20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lm_list = []
        b_box = None
        self.list = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            x_list = []
            y_list = []
            for id, lm in enumerate(myHand.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                x_list.append(cx)
                y_list.append(cy)
                lm_list.append([id, cx, cy])
                self.list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            b_box = (min(x_list), min(y_list), max(x_list), max(y_list))
            if draw and b_box:
                cv2.rectangle(img, (b_box[0], b_box[1]), (b_box[2], b_box[3]), (0, 255, 0), 2)
        return lm_list, b_box

    def fingersUp(self):
        fingers = []
        if self.list[self.tip[0]][1] > self.list[self.tip[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range (1,5):
            if self.list[self.tip[id]][2] < self.list[self.tip[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                pass 
        return fingers

    def distance(self, p1, p2, img, draw=True, r=15, t=3):
        x1,y1 = self.lista[p1][1:]
        x2,y2 = self.lista[p2][1:]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        if draw:
            cv2.line(img, (x1,y1), (x2,y2), (0,0,255), t)
            cv2.circle(img, (x1,y1), r, (255,0,0), cv2.FILLED)
            cv2.circle(img, (x2,y2), r, (255,0,0), cv2.FILLED)
            cv2.circle(img, (cx,cy), r, (255,0,0), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)
        return length, img, [x1,y1,x2,y2,cx,cy]