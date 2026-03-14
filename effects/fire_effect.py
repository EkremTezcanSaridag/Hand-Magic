import random
import math
import cv2
import numpy as np
from particles.particle import Particle, ParticleSystem

def flame_color(ratio):
    if ratio < 0.15:
        return (220, 250, 255)
    elif ratio < 0.30:
        return (100, 240, 255)
    elif ratio < 0.50:
        return (20,  180, 255)
    elif ratio < 0.70:
        return (0,   100, 255)
    elif ratio < 0.85:
        return (0,    35, 220)
    else:
        return (0,     0,  80)

MAX_BALL  = 85
GROW_RATE = 3.0

def _render_layers(frame, particles):
    if not particles:
        return frame
    glow = np.zeros_like(frame)
    for p in particles:
        a    = p.alpha
        size = max(1, int(p.size * 3.0 * a))
        col  = tuple(min(255, int(c * a * 0.4)) for c in p.color)
        cv2.circle(glow, (int(p.x), int(p.y)), size, col, -1)
    frame = cv2.add(frame, cv2.GaussianBlur(glow, (41, 41), 0))

    mid = np.zeros_like(frame)
    for p in particles:
        a    = p.alpha
        size = max(1, int(p.size * 1.6 * a))
        col  = tuple(min(255, int(c * a * 0.8)) for c in p.color)
        cv2.circle(mid, (int(p.x), int(p.y)), size, col, -1)
    frame = cv2.add(frame, cv2.GaussianBlur(mid, (13, 13), 0))

    for p in particles:
        a    = p.alpha
        size = max(1, int(p.size * a))
        col  = tuple(min(255, int(c * a)) for c in p.color)
        cv2.circle(frame, (int(p.x), int(p.y)), size, col, -1)
    return frame


class FireEffect:
    def __init__(self):
        self.system    = ParticleSystem()
        self.ball_size = 0.0
        self.fireballs = []
        self.active    = False

    def spawn(self, cx, cy):
        self.active = True
        if self.ball_size < MAX_BALL:
            self.ball_size = min(self.ball_size + GROW_RATE, MAX_BALL)

        count = int(25 + (self.ball_size / MAX_BALL) * 45)
        for _ in range(count):
            angle = random.uniform(math.pi * 0.6, math.pi * 2.4)
            r     = random.uniform(0, self.ball_size * 0.52)
            px    = cx + math.cos(angle) * r
            py    = cy + math.sin(angle) * r * 0.55
            vx    = random.gauss(0, 2.2)
            vy    = random.uniform(-7, -2.0)
            ratio = r / max(self.ball_size * 0.52, 1)
            color = flame_color(ratio)
            if ratio < 0.25:
                life = random.randint(8, 18);  size = random.randint(8, int(14 + self.ball_size / 9))
            elif ratio < 0.55:
                life = random.randint(15, 32); size = random.randint(5, 10)
            else:
                life = random.randint(22, 50); size = random.randint(2, 6)
            self.system.add(Particle(px, py, vx, vy, color, life, size))

    def launch(self, cx, cy, vx, vy):
        if self.ball_size > 10:
            fb = _FlyingFireball(cx, cy, vx, vy, self.ball_size)
            self.fireballs.append(fb)
        self.ball_size = 0.0
        self.system.clear()

    def reset(self):
        self.ball_size = 0.0
        self.active    = False
        self.system.clear()

    def update(self):
        self.system.update()
        for fb in self.fireballs:
            fb.update()
        self.fireballs = [fb for fb in self.fireballs if fb.is_alive]

    def get_explosions(self):
        """Patlayan topların konumlarını döndür, listeyi temizle."""
        hits = [(fb.x, fb.y, fb.size) for fb in self.fireballs if fb.exploded]
        self.fireballs = [fb for fb in self.fireballs if not fb.exploded]
        return hits

    def draw(self, frame):
        if self.system.particles:
            frame = _render_layers(frame, self.system.particles)
        for fb in self.fireballs:
            frame = fb.draw(frame)
        return frame


class _FlyingFireball:
    def __init__(self, x, y, vx, vy, size):
        self.x        = float(x)
        self.y        = float(y)
        self.vx       = float(vx)
        self.vy       = float(vy)
        self.size     = size
        self.system   = ParticleSystem()
        self.age      = 0
        self.life     = 80
        self.exploded = False   # Çarptı mı?

    @property
    def is_alive(self):
        return self.age < self.life and not self.exploded

    @property
    def alpha(self):
        return max(0.0, 1.0 - (self.age / self.life) ** 1.5)

    def check_bounds(self, w, h):
        """Ekran kenarına çarptıysa True döner."""
        margin = 20
        return (self.x < margin or self.x > w - margin or
                self.y < margin or self.y > h - margin)

    def update(self, frame_w=1280, frame_h=720):
        if self.check_bounds(frame_w, frame_h):
            self.exploded = True
            return

        self.x  += self.vx
        self.y  += self.vy
        self.vy += 0.25
        self.vx *= 0.97
        self.age += 1

        shrink = self.alpha
        r      = self.size * 0.5 * shrink
        for _ in range(int(22 * shrink)):
            angle = random.uniform(0, 2 * math.pi)
            dist  = random.uniform(0, r)
            px    = self.x + math.cos(angle) * dist
            py    = self.y + math.sin(angle) * dist * 0.7
            vx    = self.vx * 0.2 + random.gauss(0, 1.8)
            vy    = self.vy * 0.1 + random.uniform(-5, -1)
            ratio = dist / max(r, 1)
            color = flame_color(ratio)
            life  = random.randint(10, 25)
            size  = random.randint(3, int(8 + self.size / 12))
            self.system.add(Particle(px, py, vx, vy, color, life, size))

        self.system.update()

    def draw(self, frame):
        return _render_layers(frame, self.system.particles)
