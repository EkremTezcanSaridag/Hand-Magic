# utils/renderer.py — Çizim yardımcıları
# Faz 5'te glow + blur eklenecek
import cv2
import numpy as np

def draw_fps(frame: np.ndarray, fps: float) -> np.ndarray:
    """Sol üst köşeye FPS yaz."""
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    return frame

def apply_glow(frame: np.ndarray, intensity: int = 15) -> np.ndarray:
    """Faz 5'te doldurulacak — Gaussian blur ile glow efekti."""
    # TODO: Parlaklık katmanı üret, orijinalle birleştir
    return frame
