# 🪄 handmagic

Kameradan el hareketlerini algılayıp gerçek zamanlı büyü efektleri yaratan Python uygulaması.

## Efektler
- 🔥 **Ateş** — Avuç açıkken elden alev fışkırır
- 🌊 **Su** — Yumruk yaparken su dalgası yayılır
- Sağ el ve sol el bağımsız çalışır

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

## Proje Yapısı
```
handmagic/
├── main.py              # Ana giriş noktası
├── core/
│   ├── hand_tracker.py  # MediaPipe el algılama
│   └── camera.py        # OpenCV kamera yönetimi
├── effects/
│   ├── base_effect.py   # Soyut efekt sınıfı
│   ├── fire_effect.py   # Ateş efekti
│   └── water_effect.py  # Su efekti
├── particles/
│   └── particle.py      # Parçacık motoru
└── utils/
    └── renderer.py      # Çizim yardımcıları
```

## Fazlar
- [x] Faz 0 — Repo kurulumu
- [ ] Faz 1 — Kamera + el algılama
- [ ] Faz 2 — Parçacık sistemi
- [ ] Faz 3 — Ateş efekti
- [ ] Faz 4 — Su efekti
- [ ] Faz 5 — Polish & glow
