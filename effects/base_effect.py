# effects/base_effect.py — Soyut efekt sınıfı
from abc import ABC, abstractmethod
import numpy as np

class BaseEffect(ABC):
    """Tüm efektlerin miras aldığı temel sınıf."""

    @abstractmethod
    def spawn(self, x: int, y: int):
        """Verilen konumda parçacık üret."""
        pass

    @abstractmethod
    def update(self):
        """Parçacıkları bir adım ilerlet."""
        pass

    @abstractmethod
    def draw(self, frame: np.ndarray) -> np.ndarray:
        """Parçacıkları frame üzerine çiz."""
        pass
