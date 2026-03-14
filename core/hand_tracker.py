# core/hand_tracker.py
import mediapipe as mp
import cv2
import math

class HandTracker:
    FINGER_TIPS = [8, 12, 16, 20]
    FINGER_PIPS = [6, 10, 14, 18]
    THUMB_TIP   = 4
    THUMB_IP    = 3

    def __init__(self, max_hands=2, detection_conf=0.7):
        self.mp_hands = mp.solutions.hands
        self.mp_draw  = mp.solutions.drawing_utils
        self.hands    = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=0.6,
        )
        self._gun_cooldown = {}

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.hands.process(rgb)

    def draw_landmarks(self, frame, results):
        if results.multi_hand_landmarks:
            for lm in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, lm, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def is_open(self, hand_landmarks) -> bool:
        lm = hand_landmarks.landmark
        open_fingers = 0
        for tip, pip in zip(self.FINGER_TIPS, self.FINGER_PIPS):
            if lm[tip].y < lm[pip].y:
                open_fingers += 1
        if lm[self.THUMB_TIP].x > lm[self.THUMB_IP].x:
            open_fingers += 1
        return open_fingers >= 3

    def get_finger_states(self, hand_landmarks) -> dict:
        """
        Her parmağın açık/kapalı durumunu döndürür.
        Debug ve esnek algılama için kullanılır.
        """
        lm = hand_landmarks.landmark
        return {
            "index":  lm[8].y  < lm[6].y,   # işaret
            "middle": lm[12].y < lm[10].y,  # orta
            "ring":   lm[16].y < lm[14].y,  # yüzük
            "pinky":  lm[20].y < lm[18].y,  # serçe
            "thumb":  lm[4].x  > lm[3].x,   # başparmak
        }

    def is_gun_pose(self, hand_landmarks) -> bool:
        """
        Tabanca pozu: işaret açık, diğerleri kapalı.
        Gevşetilmiş versiyon: serçe açık olsa da geçer.
        """
        s = self.get_finger_states(hand_landmarks)
        index_open   = s["index"]
        middle_closed = not s["middle"]
        ring_closed   = not s["ring"]
        # Serçeyi ignore et — çoğu insan tam kapatamıyor
        return index_open and middle_closed and ring_closed

    def detect_gun_trigger(self, hand_landmarks, hand_id: str) -> bool:
        """
        Tabanca pozundayken işaret parmağı kapanınca ateş et.
        """
        lm       = hand_landmarks.landmark
        cooldown = self._gun_cooldown.get(hand_id, 0)

        if cooldown > 0:
            self._gun_cooldown[hand_id] = cooldown - 1
            return False

        index_closed = lm[8].y > lm[6].y
        if index_closed:
            self._gun_cooldown[hand_id] = 15
            return True
        return False

    def get_palm_center(self, hand_landmarks, frame_shape) -> tuple:
        h, w = frame_shape[:2]
        lm   = hand_landmarks.landmark
        cx   = int((lm[0].x + lm[9].x) / 2 * w)
        cy   = int((lm[0].y + lm[9].y) / 2 * h)
        return cx, cy

    def get_index_tip(self, hand_landmarks, frame_shape) -> tuple:
        h, w = frame_shape[:2]
        lm   = hand_landmarks.landmark
        return int(lm[8].x * w), int(lm[8].y * h)

    def get_index_direction(self, hand_landmarks, frame_shape) -> tuple:
        h, w = frame_shape[:2]
        lm   = hand_landmarks.landmark
        bx = lm[5].x * w;  by = lm[5].y * h   # işaret tabanı
        tx = lm[8].x * w;  ty = lm[8].y * h   # işaret ucu
        dx, dy = tx - bx, ty - by
        length = math.sqrt(dx**2 + dy**2) or 1
        return dx / length, dy / length

    def get_handedness(self, results, index: int) -> str:
        if results.multi_handedness and index < len(results.multi_handedness):
            return results.multi_handedness[index].classification[0].label
        return "Unknown"

    def draw_debug(self, frame, hand_landmarks, frame_shape):
        """Parmak durumlarını ekranda göster — sorun giderme için."""
        s   = self.get_finger_states(hand_landmarks)
        cx, cy = self.get_palm_center(hand_landmarks, frame_shape)
        labels = [
            ("I", s["index"]),
            ("M", s["middle"]),
            ("R", s["ring"]),
            ("P", s["pinky"]),
            ("T", s["thumb"]),
        ]
        for j, (label, state) in enumerate(labels):
            col = (0, 255, 80) if state else (0, 60, 220)
            cv2.putText(frame, label, (cx - 50 + j * 22, cy + 55),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, col, 2)
        return frame
