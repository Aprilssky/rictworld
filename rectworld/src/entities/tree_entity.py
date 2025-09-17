# rictworld/src/entities/tree_entity.py
from entities.base_entity import BaseEntity

class TreeEntity(BaseEntity):
    def __init__(self, i, j):
        super().__init__(i, j, auto_move=False)
        self.image = "assets/images/tree.png"  # 树专用图像
    
    def interact(self, interactor):
        print(f"{type(interactor).__name__} 与树交互了")
        # 这里可以实现采集资源等特定交互行为
        
        # 背包功能预留接口
        # 存档功能预留接口