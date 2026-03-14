# core/hand_tracker.py — MediaPipe el algılama
import mediapipe as mp
import cv2

class HandTracker:
    """
    MediaPipe ile el landmark'larını algılar.
    Avuç açık/kapalı tespiti yapar.
    """

    # Parmak ucu landmark indexleri (mediapipe)
    FINGER_TIPS = [8, 12, 16, 20]   # İşaret, orta, yüzük, serçe
    FINGER_PIPS = [6, 10, 14, 18]   # Her parmağın orta eklemi
    THUMB_TIP   = 4
    THUMB_IP    = 3

    def __init__(self, max_hands: int = 2, detection_conf: float = 0.7):
        self.mp_hands = mp.solutions.hands
        self.mp_draw  = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=0.6,
        )

    def process(self, frame):
        """
        BGR frame alır, işlenmiş sonucu döndürür.
        results.multi_hand_landmarks üzerinden landmark'lara erişilir.
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.hands.process(rgb)

    def draw_landmarks(self, frame, results):
        """Elin iskeletini ve noktalarını frame üzerine çizer."""
        if results.multi_hand_landmarks:
            for hand_lm in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand_lm, self.mp_hands.HAND_CONNECTIONS
                )
        return frame

    def is_open(self, hand_landmarks) -> bool:
        """
        Avuç açık mı? 
        4 parmaktan 3'ü açıksa True döner.
        """
        lm = hand_landmarks.landmark
        open_fingers = 0

        # 4 parmak (işaret → serçe)
        for tip, pip in zip(self.FINGER_TIPS, self.FINGER_PIPS):
            if lm[tip].y < lm[pip].y:  # Uç, eklemin üstündeyse açık
                open_fingers += 1

        # Başparmak (x ekseninde karşılaştır)
        if lm[self.THUMB_TIP].x > lm[self.THUMB_IP].x:
            open_fingers += 1

        return open_fingers >= 3

    def get_palm_center(self, hand_landmarks, frame_shape) -> tuple:
        """Avuç merkezini (x, y) piksel koordinatı olarak döndürür."""
        h, w = frame_shape[:2]
        lm = hand_landmarks.landmark
        # 0: bilek, 9: orta parmak tabanı — ikisinin ortası avuç merkezi
        cx = int((lm[0].x + lm[9].x) / 2 * w)
        cy = int((lm[0].y + lm[9].y) / 2 * h)
        return (cx, cy)

    def get_handedness(self, results, index: int) -> str:
        """'Left' veya 'Right' döndürür."""
        if results.multi_handedness and index < len(results.multi_handedness):
            return results.multi_handedness[index].classification[0].label
        return "Unknown"
