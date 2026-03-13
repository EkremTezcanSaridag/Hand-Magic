# core/camera.py — OpenCV kamera yönetimi
# Faz 1'de doldurulacak

class Camera:
    """Webcam açma, kapama ve frame okuma."""

    def __init__(self, index: int = 0):
        self.index = index
        self.cap = None

    def start(self):
        # TODO: cv2.VideoCapture başlat
        pass

    def read(self):
        # TODO: Frame oku, (frame, başarılı) döndür
        pass

    def release(self):
        # TODO: Kamerayı serbest bırak
        pass
