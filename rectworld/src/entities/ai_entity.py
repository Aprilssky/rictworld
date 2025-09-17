# rictworld/src/entities/ai_entity.py
from entities.base_entity import BaseEntity

class AIEntity(BaseEntity):
    def __init__(self, i, j):
        super().__init__(i, j, auto_move=True)
        self.image = "assets/images/pig.png"  # Pig 专用图像