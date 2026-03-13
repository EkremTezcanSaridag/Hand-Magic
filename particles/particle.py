# particles/particle.py — Tek parçacık fizik + render
# Faz 2'de doldurulacak
import numpy as np

class Particle:
    """
    Tek bir parçacık.
    Pozisyon, hız, renk, ömür bilgisi taşır.
    """

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 color: tuple, lifespan: int):
        self.x = x
        self.y = y
        self.vx = vx      # x hızı (piksel/frame)
        self.vy = vy      # y hızı (piksel/frame)
        self.color = color  # (B, G, R)
        self.lifespan = lifespan
        self.age = 0

    @property
    def is_alive(self) -> bool:
        return self.age < self.lifespan

    @property
    def alpha(self) -> float:
        """0.0 → 1.0 arası görünürlük (yaşlandıkça solar)."""
        return 1.0 - (self.age / self.lifespan)

    def update(self):
        # TODO: Pozisyonu hıza göre güncelle, yaşı artır
        pass
