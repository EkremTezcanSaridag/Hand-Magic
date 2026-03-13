# effects/water_effect.py — Su efekti
# Faz 4'te doldurulacak
from .base_effect import BaseEffect

class WaterEffect(BaseEffect):
    """Yumruk yaparken dışa yayılan su dalgası."""

    def spawn(self, x, y):
        # TODO: Su parçacıkları üret (radyal yön)
        pass

    def update(self):
        # TODO: Dışa doğru yay, sönümle
        pass

    def draw(self, frame):
        # TODO: Mavi→turkuaz renk geçişiyle çiz
        return frame
