# main.py — handmagic Faz 1
import cv2
import time
from core.camera import Camera
from core.hand_tracker import HandTracker

def main():
    print("🪄 handmagic başlatılıyor...")

    camera  = Camera(index=0)
    tracker = HandTracker(max_hands=2)

    camera.start()
    print("✅ Kamera açıldı. Çıkmak için 'q'ya bas.")

    prev_time = time.time()

    while True:
        success, frame = camera.read()
        if not success:
            print("Frame okunamadı, atlanıyor...")
            continue

        # El algıla
        results = tracker.process(frame)

        # İskelet çiz
        frame = tracker.draw_landmarks(frame, results)

        # Her el için avuç durumu + merkez
        if results.multi_hand_landmarks:
            for i, hand_lm in enumerate(results.multi_hand_landmarks):
                cx, cy   = tracker.get_palm_center(hand_lm, frame.shape)
                open_     = tracker.is_open(hand_lm)
                hand_name = tracker.get_handedness(results, i)

                durum = "ACIK" if open_ else "KAPALI"
                renk  = (0, 255, 100) if open_ else (0, 100, 255)

                # Avuç merkezine daire
                cv2.circle(frame, (cx, cy), 12, renk, -1)

                # Durum yazısı
                cv2.putText(frame, f"{hand_name}: {durum}",
                            (cx - 60, cy - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, renk, 2)

        # FPS hesapla
        now = time.time()
        fps = 1.0 / (now - prev_time + 1e-9)
        prev_time = now
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("handmagic", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
    print("👋 Kapatıldı.")

if __name__ == "__main__":
    main()
