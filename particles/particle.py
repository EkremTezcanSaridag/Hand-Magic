import random
import math

class Particle:
    def __init__(self, x, y, vx, vy, color, lifespan, size=4):
        self.x        = float(x)
        self.y        = float(y)
        self.vx       = float(vx)
        self.vy       = float(vy)
        self.color    = color
        self.lifespan = lifespan
        self.size     = float(size)
        self.age      = 0

    @property
    def is_alive(self):
        return self.age < self.lifespan

    @property
    def alpha(self):
        t = self.age / self.lifespan
        return max(0.0, 1.0 - t * t)

    def update(self):
        self.x   += self.vx
        self.y   += self.vy
        self.vx  *= 0.94
        self.vy  *= 0.94
        self.age += 1


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add(self, p):
        self.particles.append(p)

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.is_alive]

    def draw(self, frame):
        import cv2
        for p in self.particles:
            a     = p.alpha
            size  = max(1, int(p.size * a))
            faded = tuple(min(255, int(c * a)) for c in p.color)
            cv2.circle(frame, (int(p.x), int(p.y)), size, faded, -1)
        return frame

    def clear(self):
        self.particles.clear()

    def __len__(self):
        return len(self.particles)
