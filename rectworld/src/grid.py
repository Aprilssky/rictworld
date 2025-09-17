import json
import os

class Grid:
    def __init__(self):
        # 使用字典存储实体，键为(i,j)网格坐标，值为实体对象
        self.entities = {}
    
    def add_entity(self, entity):
        """添加实体到网格"""
        i, j = entity.i, entity.j
        if not self.is_valid_position(i, j):
            print(f"位置 ({i}, {j}) 已被占用，无法添加实体")
            return False
        
        self.entities[(i, j)] = entity
        return True
    
    def remove_entity(self, entity):
        """从网格中移除实体"""
        # 查找实体所在位置
        positions_to_remove = []
        for pos, ent in self.entities.items():
            if ent == entity:
                positions_to_remove.append(pos)
        
        # 移除实体
        for pos in positions_to_remove:
            del self.entities[pos]
    
    def update(self):
        """更新所有实体状态"""
        # 创建实体位置的临时副本，避免在迭代过程中修改字典
        entities_copy = self.entities.copy()
        
        for pos, entity in entities_copy.items():
            # 保存旧位置
            old_i, old_j = pos
            
            # 更新实体状态
            entity.update()
            
            # 如果位置发生变化，更新字典键
            if (old_i, old_j) != (entity.i, entity.j):
                # 检查新位置是否有效
                if self.is_valid_position(entity.i, entity.j):
                    # 移除旧位置的实体
                    if (old_i, old_j) in self.entities:
                        del self.entities[(old_i, old_j)]
                    # 在新位置添加实体
                    self.entities[(entity.i, entity.j)] = entity
                else:
                    # 如果位置无效，回退到旧位置
                    entity.i, entity.j = old_i, old_j
    
    def is_valid_position(self, i, j):
        """检查位置是否有效（未被占用）"""
        return (i, j) not in self.entities
    
    def get_entity_at(self, i, j):
        """获取指定位置的实体"""
        return self.entities.get((i, j), None)
    
    def get_entities_in_rect(self, top_left_i, top_left_j, bottom_right_i, bottom_right_j):
        """获取指定矩形区域内的所有实体"""
        entities_in_rect = {}
        for (i, j), entity in self.entities.items():
            if (top_left_i <= i <= bottom_right_i and 
                top_left_j <= j <= bottom_right_j):
                entities_in_rect[(i, j)] = entity
        return entities_in_rect
    
    def serialize(self):
        """将网格状态序列化为JSON格式"""
        serialized_data = {
            "entities": []
        }
        
        for (i, j), entity in self.entities.items():
            # 获取实体的基本信息和类型
            entity_data = {
                "type": type(entity).__name__,
                "i": i,
                "j": j
            }
            
            # 特殊处理需要保存额外数据的实体
            if hasattr(entity, 'save_data'):
                entity_data["save_data"] = entity.save_data
            
            serialized_data["entities"].append(entity_data)
        
        return json.dumps(serialized_data)
    
    def deserialize(self, serialized_data):
        """从JSON数据重建网格状态"""
        data = json.loads(serialized_data)
        
        # 清空当前实体
        self.entities.clear()
        
        # 重新创建所有实体
        for entity_data in data["entities"]:
            entity_type = entity_data["type"]
            i = entity_data["i"]
            j = entity_data["j"]
            
            # 根据类型创建实体
            if entity_type == "PlayerEntity":
                from entities.player_entity import PlayerEntity
                entity = PlayerEntity(i, j)
            elif entity_type == "TreeEntity":
                from entities.tree_entity import TreeEntity
                entity = TreeEntity(i, j)
            elif entity_type == "AIEntity":
                from entities.ai_entity import AIEntity
                entity = AIEntity(i, j)
            elif entity_type == "SaveEntity":
                from entities.save_entity import SaveEntity
                entity = SaveEntity(i, j, self)
                # 恢复存档数据
                if "save_data" in entity_data:
                    entity.save_data = entity_data["save_data"]
            else:
                # 默认使用基础实体
                from entities.base_entity import BaseEntity
                entity = BaseEntity(i, j)
            
            # 添加实体到网格
            self.add_entity(entity)