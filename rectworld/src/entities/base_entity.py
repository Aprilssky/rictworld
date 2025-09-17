# rictworld/src/entities/base_entity.py
import random

class BaseEntity:
    def __init__(self, i, j, auto_move=False):
        self.i = i  # 网格坐标 i
        self.j = j  # 网格坐标 j
        self.auto_move = auto_move
        self.image = "assets/images/default.png"  # 默认图像路径
    
    def update(self):
        if self.auto_move:
            # 随机选择一个方向
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            dx, dy = random.choice(directions)
            self.move(dx, dy)
    
    def move(self, dx, dy):
        self.i += dx
        self.j += dy
    
    def interact(self, interactor):
        # 默认交互行为为空
        pass