# effects/explosion.py — Patlama efekti
import random
import math
import cv2
import numpy as np
from particles.particle import Particle, ParticleSystem

def _explosion_color(ratio):
    """Merkez beyaz, dış kırmızı/duman."""
    if ratio < 0.2:
        return (240, 255, 255)   # beyaz çekirdek
    elif ratio < 0.4:
        return (100, 220, 255)   # parlak sarı
    elif ratio < 0.6:
        return (0,   150, 255)   # turuncu
    elif ratio < 0.8:
        return (0,    40, 220)   # kırmızı
    else:
        return (30,   30,  60)   # koyu duman

class Explosion:
    """Tek bir patlama — ömrü bitince silinir."""

    def __init__(self, x, y, size=85):
        self.x      = x
        self.y      = y
        self.size   = size
        self.system = ParticleSystem()
        self.age    = 0
        self.life   = 45
        self._burst(x, y, size)

    def _burst(self, x, y, size):
        """İlk frame'de tüm parçacıkları fırlat."""
        count = int(120 + size * 1.5)
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1.5, size * 0.18)
            vx    = math.cos(angle) * speed
            vy    = math.sin(angle) * speed

            r     = random.uniform(0, size * 0.5)
            px    = x + math.cos(angle) * r * 0.3
            py    = y + math.sin(angle) * r * 0.3

            ratio = r / max(size * 0.5, 1)
            color = _explosion_color(ratio)

            life  = random.randint(20, 45)
            sz    = random.randint(3, int(6 + size / 15))
            self.system.add(Particle(px, py, vx, vy, color, life, sz))

        # Şok dalgası için büyük yavaş parçacıklar
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(size * 0.12, size * 0.22)
            vx    = math.cos(angle) * speed
            vy    = math.sin(angle) * speed
            color = (0, 60, 180)
            self.system.add(Particle(x, y, vx, vy, color, 18, random.randint(8, 16)))

    @property
    def is_alive(self):
        return self.age < self.life

    def update(self):
        self.system.update()
        self.age += 1

    def draw(self, frame):
        if not self.system.particles:
            return frame

        # Glow katmanı
        glow = np.zeros_like(frame)
        for p in self.system.particles:
            a    = p.alpha
            size = max(1, int(p.size * 3.0 * a))
            col  = tuple(min(255, int(c * a * 0.45)) for c in p.color)
            cv2.circle(glow, (int(p.x), int(p.y)), size, col, -1)
        frame = cv2.add(frame, cv2.GaussianBlur(glow, (45, 45), 0))

        # Orta katman
        mid = np.zeros_like(frame)
        for p in self.system.particles:
            a    = p.alpha
            size = max(1, int(p.size * 1.5 * a))
            col  = tuple(min(255, int(c * a * 0.9)) for c in p.color)
            cv2.circle(mid, (int(p.x), int(p.y)), size, col, -1)
        frame = cv2.add(frame, cv2.GaussianBlur(mid, (13, 13), 0))

        # Keskin parçacıklar
        frame = self.system.draw(frame)
        return frame


class ExplosionManager:
    """Tüm aktif patlamaları yönetir."""

    def __init__(self):
        self.explosions = []

    def trigger(self, x, y, size=85):
        self.explosions.append(Explosion(x, y, size))

    def update(self):
        for e in self.explosions:
            e.update()
        self.explosions = [e for e in self.explosions if e.is_alive]

    def draw(self, frame):
        for e in self.explosions:
            frame = e.draw(frame)
        return frame
