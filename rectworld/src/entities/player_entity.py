from entities.base_entity import BaseEntity

class PlayerEntity(BaseEntity):
    def __init__(self, i, j):
        super().__init__(i, j, auto_move=False)
        self.direction = ""  # 方向属性初始值为空
        self.image = "assets/images/player.png"  # 玩家专用图像
        self.bag = {}  # 初始化背包为空字典
        self.bag_capacity = 10  # 设置背包容量限制
    
    def store_item(self, entity):
        """将实体添加到背包"""
        if len(self.bag) >= self.bag_capacity:
            print("背包已满")
            return False
        
        # 获取实体类型作为物品标识符
        item_type = type(entity).__name__
        
        # 更新背包物品计数
        if item_type in self.bag:
            self.bag[item_type] += 1
        else:
            self.bag[item_type] = 1
        
        # 从网格中移除被存储的实体
        # 注意：这里需要网格引用，但PlayerEntity通常不直接持有网格引用
        # 这个功能应该在交互时由外部处理
        
        return True
    
    def take_item(self, item_type):
        """从背包中取出物品"""
        if item_type in self.bag and self.bag[item_type] > 0:
            self.bag[item_type] -= 1
            
            # 如果数量为0，从背包中移除该物品
            if self.bag[item_type] == 0:
                del self.bag[item_type]
            
            # 创建物品实体并放置到玩家当前位置或相邻位置
            # 这个功能需要在外部实现，因为需要网格引用
            
            return True
        return False
    
    def interact(self, grid):
        """与玩家朝向方向的实体进行交互"""
        # 根据当前方向计算相邻位置的网格坐标
        if self.direction == "up":
            target_i, target_j = self.i, self.j - 1
        elif self.direction == "down":
            target_i, target_j = self.i, self.j + 1
        elif self.direction == "left":
            target_i, target_j = self.i - 1, self.j
        elif self.direction == "right":
            target_i, target_j = self.i + 1, self.j
        else:
            # 如果方向未设置，不进行交互
            return
        
        # 通过网格的get_entity_at方法获取该位置的实体
        target_entity = grid.get_entity_at(target_i, target_j)
        
        # 如果存在实体则调用该实体的interact方法
        if target_entity is not None:
            target_entity.interact(self)
    
    def serialize_bag(self):
        """序列化背包状态"""
        return self.bag.copy()
    
    def deserialize_bag(self, bag_data):
        """从序列化数据恢复背包状态"""
        self.bag = bag_data.copy()