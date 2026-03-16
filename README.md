# ⚡ handmagic

Kameradan el hareketlerini algılayıp gerçek zamanlı yıldırım efekti yaratan Python uygulaması.

## Demo

```
🤲 İki eli üst üste getir  →  Aralarında yıldırım topu birikir
💥 İki eli hızlıca öne it  →  HADOUKEN!
```

## Kurulum

```bash
git clone https://github.com/kullanici/handmagic.git
cd handmagic
pip install -r requirements.txt
python main.py
```

## Gereksinimler

- Python 3.9+
- Webcam
- `opencv-python`, `mediapipe`, `numpy`

## Nasıl Kullanılır

### ⚡ Enerji Toplama
İki eli **üst üste** getir — avuçlar birbirine baksın, aynı hizada dursun.  
Eller yaklaştıkça aralarında yıldırım topu büyür ve şarj çubuğu dolar.

### 💥 Hadouken
Şarj dolunca iki eli **hızlıca öne doğru** it.  
Enerji topu o yöne patlar.

### ✋ İptal
Elleri birbirinden uzaklaştır — top yavaşça söner.

## Proje Yapısı

```
handmagic/
├── main.py                        # Ana giriş noktası
├── core/
│   ├── camera.py                  # OpenCV kamera yönetimi
│   └── hand_tracker.py            # MediaPipe el algılama
├── effects/
│   ├── lightning_effect.py        # Yıldırım topu + hadouken huzmesi
│   └── explosion.py               # Patlama efekti
├── particles/
│   └── particle.py                # Parçacık motoru
└── utils/
    └── renderer.py                # Yardımcı çizim fonksiyonları
```

## Fazlar

- [x] Faz 0 — Repo kurulumu
- [x] Faz 1 — Kamera + el algılama
- [x] Faz 2 — Parçacık sistemi
- [x] Faz 3 — Yıldırım topu + Hadouken
- [ ] Faz 4 — Çoklu efekt modu
- [ ] Faz 5 — Ses efektleri
