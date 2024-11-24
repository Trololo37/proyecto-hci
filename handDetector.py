import mediapipe as mp
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
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            b_box = (min(x_list), min(y_list), max(x_list), max(y_list))
            if draw and b_box:
                cv2.rectangle(img, (b_box[0], b_box[1]), (b_box[2], b_box[3]), (0, 255, 0), 2)
        return lm_list, b_box

    def fingersUp(self):
        fingers = []
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                # Aquí definimos una lógica básica basada en posiciones relativas.
                # Puedes mejorar esto con los índices específicos de MediaPipe.
                pass  # Aquí puedes agregar reglas específicas.
        return fingers
