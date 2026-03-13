# effects/fire_effect.py — Ateş efekti
# Faz 3'te doldurulacak
from .base_effect import BaseEffect

class FireEffect(BaseEffect):
    """Avuç açıkken elden yukarı fışkıran ateş."""

    def spawn(self, x, y):
        # TODO: Ateş parçacıkları üret
        pass

    def update(self):
        # TODO: Yukarı yükselt, sönümle, ömrü bitenleri sil
        pass

    def draw(self, frame):
        # TODO: Sarı→turuncu→kırmızı renk geçişiyle çiz
        return frame
