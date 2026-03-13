# core/hand_tracker.py — MediaPipe el algılama
# Faz 1'de doldurulacak

class HandTracker:
    """
    MediaPipe ile el landmark'larını algılar.
    Avuç açık/kapalı tespiti yapar.
    """

    def __init__(self, max_hands: int = 2):
        self.max_hands = max_hands
        self.hands = None  # TODO: mp.solutions.hands

    def process(self, frame):
        # TODO: Frame'i işle, HandResult listesi döndür
        pass

    def is_open(self, hand_landmarks) -> bool:
        # TODO: Parmak uçları + eklemlere bakarak avuç açık mı?
        pass

    def get_palm_center(self, hand_landmarks, frame_shape) -> tuple:
        # TODO: Avuç merkezini piksel koordinatı olarak döndür
        pass
