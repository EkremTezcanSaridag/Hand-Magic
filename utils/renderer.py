# utils/renderer.py — Çizim yardımcıları
import cv2
import numpy as np
import time

class FPSCounter:
    def __init__(self):
        self._prev = time.time()
        self.fps   = 0.0

    def tick(self):
        now       = time.time()
        self.fps  = 1.0 / (now - self._prev + 1e-9)
        self._prev = now

def draw_fps(frame: np.ndarray, fps: float) -> np.ndarray:
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return frame

def draw_hand_info(frame: np.ndarray, cx: int, cy: int,
                   hand_label: str, is_open: bool) -> np.ndarray:
    """Avuç merkezine daire + durum yazısı çiz."""
    state  = "ACIK" if is_open else "KAPALI"
    emoji  = "🔥" if is_open else "🌊"
    color  = (0, 100, 255) if is_open else (255, 100, 0)

    cv2.circle(frame, (cx, cy), 12, color, -1)
    cv2.circle(frame, (cx, cy), 14, (255, 255, 255), 2)

    label = f"{hand_label} | {state}"
    cv2.putText(frame, label, (cx - 60, cy - 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    return frame

def apply_glow(frame: np.ndarray, intensity: int = 15) -> np.ndarray:
    """Faz 5'te aktifleşecek — şimdilik orijinali döndürür."""
    return frame
