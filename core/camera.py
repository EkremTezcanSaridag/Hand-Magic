# core/camera.py — OpenCV kamera yönetimi
import cv2

class Camera:
    """Webcam açma, kapama ve frame okuma."""

    def __init__(self, index: int = 0, width: int = 1280, height: int = 720):
        self.index = index
        self.width = width
        self.height = height
        self.cap = None

    def start(self):
        self.cap = cv2.VideoCapture(self.index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        if not self.cap.isOpened():
            raise RuntimeError("Kamera açılamadı! İndex doğru mu?")

    def read(self):
        """(success, frame) döndürür. Frame aynalı gelir."""
        success, frame = self.cap.read()
        if success:
            frame = cv2.flip(frame, 1)  # Ayna efekti
        return success, frame

    def release(self):
        if self.cap:
            self.cap.release()
