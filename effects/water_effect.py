# effects/water_effect.py — Gerçekçi su efekti
import random
import math
import cv2
import numpy as np
from particles.particle import Particle, ParticleSystem

def water_color(ratio):
    """Merkez parlak beyaz/cyan, kenar koyu mavi."""
    if ratio < 0.15:
        return (255, 255, 255)   # parlak beyaz damla merkezi
    elif ratio < 0.30:
        return (255, 240, 180)   # açık cyan
    elif ratio < 0.50:
        return (255, 200, 80)    # turkuaz
    elif ratio < 0.70:
        return (220, 150, 20)    # mavi
    elif ratio < 0.85:
        return (180,  90,  5)    # koyu mavi
    else:
        return (120,  40,  0)    # derin mavi

MAX_FLOW  = 80    # maksimum su akış boyutu
GROW_RATE = 2.5
MAX_PARTS = 700

def _render_water(frame, particles):
    if not particles:
        return frame

    # Glow — su parlaması
    glow = np.zeros_like(frame)
    for p in particles:
        a    = p.alpha
        size = max(1, int(p.size * 2.5 * a))
        col  = tuple(min(255, int(c * a * 0.35)) for c in p.color)
        cv2.circle(glow, (int(p.x), int(p.y)), size, col, -1)
    frame = cv2.add(frame, cv2.GaussianBlur(glow, (31, 31), 0))

    # Orta katman
    mid = np.zeros_like(frame)
    for p in particles:
        a    = p.alpha
        size = max(1, int(p.size * 1.4 * a))
        col  = tuple(min(255, int(c * a * 0.8)) for c in p.color)
        cv2.circle(mid, (int(p.x), int(p.y)), size, col, -1)
    frame = cv2.add(frame, cv2.GaussianBlur(mid, (9, 9), 0))

    # Keskin damlalar
    for p in particles:
        a    = p.alpha
        size = max(1, int(p.size * a))
        col  = tuple(min(255, int(c * a)) for c in p.color)
        cv2.circle(frame, (int(p.x), int(p.y)), size, col, -1)

    return frame


class WaterEffect:
    def __init__(self):
        self.system    = ParticleSystem()
        self.flow_size = 0.0
        self.active    = False

    def spawn(self, cx, cy):
        """Avuç açıkken her frame çağrılır."""
        self.active = True
        if self.flow_size < MAX_FLOW:
            self.flow_size = min(self.flow_size + GROW_RATE, MAX_FLOW)

        if len(self.system) >= MAX_PARTS:
            return

        r     = self.flow_size
        count = int(20 + (r / MAX_FLOW) * 40)

        for _ in range(count):
            # Su avuçtan aşağı ve yana fışkırır
            angle = random.uniform(math.pi * 0.3, math.pi * 0.7)  # aşağı yön
            dist  = random.uniform(0, r * 0.5)
            px    = cx + math.cos(angle) * dist
            py    = cy + math.sin(angle) * dist * 0.6

            # Hız: çoğunlukla aşağı + yana saçılma
            vx = random.gauss(0, 2.5)
            vy = random.uniform(1.5, 6.0)   # aşağı

            # Damlacıklar: bazıları yukarı sıçrar
            if random.random() < 0.2:
                vy = random.uniform(-4, -1)
                vx = random.gauss(0, 3.0)

            ratio = dist / max(r * 0.5, 1)
            color = water_color(ratio)

            # İç damlalar büyük, dış ince
            if ratio < 0.3:
                life = random.randint(25, 50)
                size = random.randint(5, int(9 + r / 10))
            elif ratio < 0.6:
                life = random.randint(30, 60)
                size = random.randint(3, 7)
            else:
                life = random.randint(35, 70)
                size = random.randint(1, 4)

            self.system.add(Particle(px, py, vx, vy, color, life, size))

    def reset(self):
        self.flow_size = 0.0
        self.active    = False
        self.system.clear()

    def update(self):
        self.system.update()

    def draw(self, frame):
        if self.system.particles:
            frame = _render_water(frame, self.system.particles)
        return frame

    def __len__(self):
        return len(self.system)
