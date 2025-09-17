from entities.base_entity import BaseEntity

class ChestEntity(BaseEntity):
    def __init__(self, i, j):
        super().__init__(i, j, auto_move=False)
        self.image = "assets/images/chest.png"  # 箱子图像
        self.inventory = {}  # 初始化箱子库存为空字典
        self.capacity = 20  # 设置箱子容量限制
    
    def interact(self, interactor):
        """当玩家与箱子交互时，打开箱子库存界面"""
        # 这里可以触发UI显示箱子内容
        # 在实际实现中，可能需要通过回调或事件通知UI层
        print("箱子被打开")
        # 返回箱子自身，以便UI层知道要显示哪个箱子
        return self
    
    def add_item(self, item_entity):
        """向箱子添加物品"""
        if len(self.inventory) >= self.capacity:
            print("箱子已满")
            return False
        
        # 获取物品类型作为标识符
        item_type = type(item_entity).__name__
        
        # 更新箱子物品计数
        if item_type in self.inventory:
            self.inventory[item_type] += 1
        else:
            self.inventory[item_type] = 1
        
        return True
    
    def remove_item(self, item_type):
        """从箱子移除物品"""
        if item_type in self.inventory and self.inventory[item_type] > 0:
            self.inventory[item_type] -= 1
            
            # 如果数量为0，从箱子中移除该物品
            if self.inventory[item_type] == 0:
                del self.inventory[item_type]
            
            return True
        return False
    
    def get_inventory(self):
        """返回箱子当前库存"""
        return self.inventory.copy()
    
    def serialize(self):
        """序列化箱子状态"""
        return {
            "inventory": self.inventory,
            "capacity": self.capacity
        }
    
    def deserialize(self, data):
        """从序列化数据恢复箱子状态"""
        self.inventory = data.get("inventory", {})
        self.capacity = data.get("capacity", 20)