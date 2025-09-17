from entities.base_entity import BaseEntity

class SaveEntity(BaseEntity):
    def __init__(self, i, j, grid):
        super().__init__(i, j, auto_move=False)
        self.image = "assets/images/save_point.png"  # 存档实体专用图像
        self.grid = grid  # 保存grid引用
        self.save_data = None  # 初始化存档数据为空
    
    def interact(self, interactor):
        # 获取交互者相对于存档实体的位置
        if interactor.j < self.j:  # 交互者在存档实体上方
            self.serialize()
            print("游戏状态已保存")
        elif interactor.j > self.j and self.save_data is not None:  # 交互者在存档实体下方且有存档数据
            self.deserialize()
            print("游戏状态已恢复")
        # 其他方向不做操作
    
    def serialize(self):
        # 调用grid的serialize方法获取当前游戏状态的序列化数据
        self.save_data = self.grid.serialize()
    
    def deserialize(self):
        # 如果存档数据不为空，调用grid的deserialize方法恢复游戏状态
        if self.save_data is not None:
            self.grid.deserialize(self.save_data)
    
    def has_save_data(self):
        # 返回布尔值，表示是否有存储的存档数据
        return self.save_data is not None
    
    def clear_save_data(self):
        # 清空存档数据
        self.save_data = None