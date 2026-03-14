import random
import math
import cv2
import numpy as np
from particles.particle import Particle, ParticleSystem

def bolt_color(ratio):
    if ratio < 0.15:
        return (255, 255, 255)
    elif ratio < 0.35:
        return (255, 240, 160)
    elif ratio < 0.55:
        return (255, 160, 40)
    elif ratio < 0.75:
        return (220, 80,  10)
    else:
        return (150, 20,   0)

MAX_CHARGE     = 100.0
CHARGE_RATE    = 1.5
FIRE_THRESHOLD = 75.0

def _draw_lightning(frame, x1, y1, x2, y2, color=(255,220,100), width=2, splits=6):
    pts = [(int(x1), int(y1))]
    for i in range(1, splits):
        t  = i / splits
        mx = x1 + (x2-x1)*t + random.randint(-20, 20)
        my = y1 + (y2-y1)*t + random.randint(-20, 20)
        pts.append((int(mx), int(my)))
    pts.append((int(x2), int(y2)))
    for i in range(len(pts)-1):
        cv2.line(frame, pts[i], pts[i+1], color, width, cv2.LINE_AA)

def _render_layers(frame, particles, b1=35, b2=11):
    if not particles:
        return frame
    glow = np.zeros_like(frame)
    for p in particles:
        a = p.alpha
        s = max(1, int(p.size * 3.0 * a))
        c = tuple(min(255, int(ch * a * 0.4)) for ch in p.color)
        cv2.circle(glow, (int(p.x), int(p.y)), s, c, -1)
    frame = cv2.add(frame, cv2.GaussianBlur(glow, (b1|1, b1|1), 0))
    mid = np.zeros_like(frame)
    for p in particles:
        a = p.alpha
        s = max(1, int(p.size * 1.5 * a))
        c = tuple(min(255, int(ch * a * 0.9)) for ch in p.color)
        cv2.circle(mid, (int(p.x), int(p.y)), s, c, -1)
    frame = cv2.add(frame, cv2.GaussianBlur(mid, (b2|1, b2|1), 0))
    for p in particles:
        a = p.alpha
        s = max(1, int(p.size * a))
        c = tuple(min(255, int(ch * a)) for ch in p.color)
        cv2.circle(frame, (int(p.x), int(p.y)), s, c, -1)
    return frame


class LightningOrb:
    """
    İki avuç arasında dönen enerji topu.
    Eller üst üste (dikey yakın, yatay yakın) olunca şarj başlar.
    """
    def __init__(self):
        self.system   = ParticleSystem()
        self.charge   = 0.0
        self.active   = False
        self.cx       = 0
        self.cy       = 0
        self._angle   = 0.0   # dönen parçacıklar için

    @property
    def is_ready(self):
        return self.charge >= FIRE_THRESHOLD

    @property
    def ratio(self):
        return min(self.charge / MAX_CHARGE, 1.0)

    def charge_up(self, lx, ly, rx, ry):
        self.active = True
        self.cx = int((lx + rx) / 2)
        self.cy = int((ly + ry) / 2)
        self._angle += 0.15

        if self.charge < MAX_CHARGE:
            self.charge = min(self.charge + CHARGE_RATE, MAX_CHARGE)

        cx, cy = self.cx, self.cy
        r      = 20 + self.ratio * 65   # top büyür

        # Dönen spiral parçacıklar — top hissi
        count = int(18 + self.ratio * 32)
        for i in range(count):
            # Sarmal: parçacıklar dışarıdan içe doğru spiral çizer
            base_angle = self._angle + (i / count) * 2 * math.pi
            dist       = r * random.uniform(0.3, 1.0)
            px = cx + math.cos(base_angle) * dist
            py = cy + math.sin(base_angle) * dist * 0.7  # hafif yassı

            # Merkeze doğru çekilirken döner
            to_center_angle = base_angle + math.pi / 2
            speed = random.uniform(2.0, 5.0)
            vx    = math.cos(to_center_angle) * speed * 0.4 - (px - cx) * 0.04
            vy    = math.sin(to_center_angle) * speed * 0.4 - (py - cy) * 0.04

            ratio = dist / max(r, 1)
            color = bolt_color(ratio * 0.8)
            life  = random.randint(6, 14)
            size  = max(2, int(3 + self.ratio * 5))
            self.system.add(Particle(px, py, vx, vy, color, life, size))

        # Top içinde çakıl şimşekler
        if random.random() < 0.55:
            for _ in range(2):
                a1 = random.uniform(0, 2*math.pi)
                a2 = a1 + math.pi + random.uniform(-0.5, 0.5)
                x1 = int(cx + math.cos(a1) * r * 0.75)
                y1 = int(cy + math.sin(a1) * r * 0.75)
                x2 = int(cx + math.cos(a2) * r * 0.75)
                y2 = int(cy + math.sin(a2) * r * 0.75)
                _draw_lightning(self.__dict__.setdefault('_tmp', np.zeros((1,1,3), np.uint8)),
                                0, 0, 1, 1)  # dummy, asıl çizim draw()'da

    def reset(self):
        self.charge = max(0.0, self.charge - 2.0)
        if self.charge <= 0:
            self.active = False
            self.system.clear()

    def update(self):
        self.system.update()

    def draw(self, frame, lx=None, ly=None, rx=None, ry=None):
        if not self.active or self.charge <= 0:
            return frame

        frame = _render_layers(frame, self.system.particles)
        cx, cy = self.cx, self.cy
        r      = int(20 + self.ratio * 65)

        # Dış halkalar
        ring_col = (int(255*self.ratio), int(180*self.ratio), 30)
        cv2.circle(frame, (cx, cy), r,     ring_col, 2, cv2.LINE_AA)
        cv2.circle(frame, (cx, cy), r - 6, (180, 140, 20), 1, cv2.LINE_AA)

        # Top içi şimşekler
        if random.random() < 0.6:
            for _ in range(3):
                a1 = random.uniform(0, 2*math.pi)
                a2 = a1 + math.pi + random.uniform(-0.5, 0.5)
                x1 = int(cx + math.cos(a1) * r * 0.8)
                y1 = int(cy + math.sin(a1) * r * 0.8)
                x2 = int(cx + math.cos(a2) * r * 0.8)
                y2 = int(cy + math.sin(a2) * r * 0.8)
                _draw_lightning(frame, x1, y1, x2, y2,
                                color=(255, 230, 100), width=1, splits=4)

        # El → top şimşekleri
        if lx is not None and random.random() < 0.5:
            _draw_lightning(frame, lx, ly, cx, cy, (180,180,255), 2, 5)
        if rx is not None and random.random() < 0.5:
            _draw_lightning(frame, rx, ry, cx, cy, (180,180,255), 2, 5)

        # Şarj çubuğu
        bw = 160; bh = 14
        bx = cx - bw//2
        by = cy - r - 38
        cv2.rectangle(frame, (bx, by), (bx+bw, by+bh), (30,30,30), -1)
        fill    = int(bw * self.ratio)
        bar_col = (0, 200, 255) if not self.is_ready else (0, 60, 255)
        cv2.rectangle(frame, (bx, by), (bx+fill, by+bh), bar_col, -1)
        cv2.rectangle(frame, (bx, by), (bx+bw,   by+bh), (160,160,160), 1)

        lbl = ">>> HADOUKEN! <<<" if self.is_ready else f"Sarj: {int(self.charge)}%"
        col = (0, 80, 255) if self.is_ready else (200, 230, 255)
        cv2.putText(frame, lbl, (bx - 10, by - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, col, 2)
        return frame


class LightningBeam:
    """Hadouken — yön vektörü boyunca patlayan enerji huzmesi."""
    def __init__(self, cx, cy, direction_x, direction_y, charge):
        self.cx     = cx
        self.cy     = cy
        self.dx     = direction_x
        self.dy     = direction_y
        self.system = ParticleSystem()
        self.age    = 0
        self.life   = 55
        self._burst(charge)

    def _burst(self, charge):
        cx, cy = self.cx, self.cy

        # Ana huzme — ileri yönde geniş saçılım
        for i in range(260):
            t      = i / 260
            spread = random.gauss(0, 10 + t * 25)
            px = cx + self.dx * t * 1000 + (-self.dy) * spread
            py = cy + self.dy * t * 1000 + ( self.dx) * spread
            spd = random.uniform(14, 24)
            vx  = self.dx * spd + random.gauss(0, 2)
            vy  = self.dy * spd + random.gauss(0, 2)
            color = bolt_color(min(t, 1.0))
            life  = random.randint(15, 38)
            # HATA DÜZELTİLDİ: max ile alt sınır garantilendi
            size  = max(3, int(14 * (1 - t) + 3))
            self.system.add(Particle(px, py, vx, vy, color, life, size))

        # Merkez patlaması
        for _ in range(120):
            angle = random.uniform(0, 2*math.pi)
            speed = random.uniform(4, 20)
            vx    = math.cos(angle) * speed
            vy    = math.sin(angle) * speed
            color = bolt_color(random.random() * 0.4)
            life  = random.randint(10, 28)
            size  = random.randint(4, 14)
            self.system.add(Particle(cx, cy, vx, vy, color, life, size))

    @property
    def is_alive(self):
        return self.age < self.life

    def update(self):
        self.system.update()
        self.age += 1

    def draw(self, frame):
        return _render_layers(frame, self.system.particles, b1=45, b2=15)
