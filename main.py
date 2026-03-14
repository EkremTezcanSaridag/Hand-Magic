# main.py — handmagic: HADOUKEN
import cv2
import time
import math
import numpy as np
from collections import deque
from core.camera import Camera
from core.hand_tracker import HandTracker
from effects.lightning_effect import LightningOrb, LightningBeam

PUSH_SPEED    = 7.0    # hadouken için el hızı eşiği
STACK_DIST    = 200    # eller bu kadar yakınsa "üst üste" sayılır

def is_hands_stacked(lx, ly, rx, ry):
    """İki el birbirine yakın mı? (üst üste veya yan yana)"""
    dist = math.sqrt((rx-lx)**2 + (ry-ly)**2)
    return dist < STACK_DIST

def is_push_pose(hand_landmarks):
    """Tüm parmaklar açık = hadouken pozu."""
    lm = hand_landmarks.landmark
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    open_count = sum(1 for tip, pip in zip(tips, pips) if lm[tip].y < lm[pip].y)
    return open_count >= 3

class HandVelocity:
    def __init__(self, n=6):
        self.hist = deque(maxlen=n)
    def push(self, x, y):
        self.hist.append((x, y))
    def speed(self):
        if len(self.hist) < 3:
            return 0.0
        dx = self.hist[-1][0] - self.hist[0][0]
        dy = self.hist[-1][1] - self.hist[0][1]
        return math.sqrt(dx*dx + dy*dy) / len(self.hist)
    def direction(self):
        if len(self.hist) < 2:
            return 0.0, 1.0
        dx = self.hist[-1][0] - self.hist[0][0]
        dy = self.hist[-1][1] - self.hist[0][1]
        d  = math.sqrt(dx*dx + dy*dy) or 1
        return dx/d, dy/d
    def reset(self):
        self.hist.clear()

def main():
    print("⚡ HADOUKEN modu!")
    print("   🤲  Elleri üst üste getir (yakın tut) → enerji topla")
    print("   💥  İki avucu hızlıca öne it          → HADOUKEN!")

    camera   = Camera(index=0)
    tracker  = HandTracker(max_hands=2)
    orb      = LightningOrb()
    beams    = []
    vel      = {"Left": HandVelocity(), "Right": HandVelocity()}
    cooldown = 0

    camera.start()
    prev_time = time.time()

    while True:
        ok, frame = camera.read()
        if not ok:
            continue

        h, w    = frame.shape[:2]
        results = tracker.process(frame)

        hands = {}
        if results.multi_hand_landmarks:
            for i, lm in enumerate(results.multi_hand_landmarks):
                name   = tracker.get_handedness(results, i)
                cx, cy = tracker.get_palm_center(lm, frame.shape)
                hands[name] = (cx, cy, lm)
                vel[name].push(cx, cy)

        left  = hands.get("Left")
        right = hands.get("Right")

        if cooldown > 0:
            cooldown -= 1

        if left and right:
            lx, ly, llm = left
            rx, ry, rlm = right

            stacked    = is_hands_stacked(lx, ly, rx, ry)
            l_push     = is_push_pose(llm)
            r_push     = is_push_pose(rlm)
            l_speed    = vel["Left"].speed()
            r_speed    = vel["Right"].speed()
            fast_push  = l_speed > PUSH_SPEED and r_speed > PUSH_SPEED

            if fast_push and l_push and r_push and orb.charge > 25 and cooldown <= 0:
                # HADOUKEN — iki elin ortalama hareket yönüne fırlat
                ldx, ldy = vel["Left"].direction()
                rdx, rdy = vel["Right"].direction()
                fx = (ldx + rdx) / 2
                fy = (ldy + rdy) / 2
                fd = math.sqrt(fx*fx + fy*fy) or 1
                beam = LightningBeam(orb.cx, orb.cy, fx/fd, fy/fd, orb.charge)
                beams.append(beam)
                orb.charge = 0.0
                orb.active = False
                orb.system.clear()
                cooldown = 45
                flash = np.ones_like(frame, dtype=np.uint8) * 255
                frame = cv2.addWeighted(frame, 0.2, flash, 0.8, 0)
                print(f"⚡ HADOUKEN! ({fx/fd:.2f}, {fy/fd:.2f})")

            elif stacked and not fast_push:
                # Şarj
                orb.charge_up(lx, ly, rx, ry)
            else:
                orb.reset()

            # El göstergeleri
            for name, (ex, ey, elm) in hands.items():
                push = is_push_pose(elm)
                spd  = vel[name].speed()
                col  = (0, 200, 255) if push else (120, 120, 120)
                cv2.circle(frame, (ex, ey), 10, col, -1)

            # Şarj çizgisi
            if orb.active and orb.charge > 5:
                ov = frame.copy()
                cv2.line(ov, (lx,ly), (rx,ry), (255,200,50), 2)
                frame = cv2.addWeighted(frame, 1 - orb.ratio*0.35,
                                        ov, orb.ratio*0.35, 0)
        else:
            orb.reset()
            for name in vel:
                if name not in hands:
                    vel[name].reset()

        tracker.draw_landmarks(frame, results)

        orb.update()
        lp = (left[0],  left[1])  if left  else (None, None)
        rp = (right[0], right[1]) if right else (None, None)
        frame = orb.draw(frame, lp[0], lp[1], rp[0], rp[1])

        for b in beams:
            b.update()
            frame = b.draw(frame)
        beams = [b for b in beams if b.is_alive]

        now = time.time()
        fps = 1.0 / (now - prev_time + 1e-9)
        prev_time = now
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        cv2.putText(frame,
                    "Elleri ust uste getir=sarj | Avuclari one it=HADOUKEN | Q=cikis",
                    (10, h-15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180,180,180), 1)

        cv2.imshow("handmagic - HADOUKEN", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
