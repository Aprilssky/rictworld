import pygame
import os
from ui.font import Font
import os
import sys

# 获取项目根目录（假设项目根目录在src上一级）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(f"Project root: {PROJECT_ROOT}")

class Viewer:
    def __init__(self, screen, grid, player, cell_size):
        self.screen = screen
        self.grid = grid
        self.player = player
        self.cell_size = cell_size
        self.font = Font()
        self.image_cache = {}  # 图像缓存字典
    
    def draw_grid(self):
        # 获取玩家位置
        player_i, player_j = self.player.i, self.player.j
        
        # 计算屏幕中心在网格中的位置
        center_i = player_i
        center_j = player_j
        
        # 计算可见网格范围
        screen_width_cells = self.screen.get_width() // self.cell_size
        screen_height_cells = self.screen.get_height() // self.cell_size
        
        start_i = center_i - screen_width_cells // 2
        start_j = center_j - screen_height_cells // 2
        
        end_i = start_i + screen_width_cells + 1
        end_j = start_j + screen_height_cells + 1
        
        # 绘制网格线
        for i in range(start_i, end_i + 1):
            x = (i - start_i) * self.cell_size
            pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, self.screen.get_height()))
        
        for j in range(start_j, end_j + 1):
            y = (j - start_j) * self.cell_size
            pygame.draw.line(self.screen, (50, 50, 50), (0, y), (self.screen.get_width(), y))
    
    def draw_entities(self):
        """绘制所有可见实体"""
        # 获取玩家位置
        player_i, player_j = self.player.i, self.player.j
        
        # 获取屏幕尺寸
        screen_width, screen_height = self.screen.get_size()
        
        # 计算可见区域的网格范围
        cells_x = screen_width // self.cell_size
        cells_y = screen_height // self.cell_size
        
        # 计算矩形区域的左上角和右下角坐标
        top_left_i = player_i - cells_x // 2
        top_left_j = player_j - cells_y // 2
        bottom_right_i = top_left_i + cells_x
        bottom_right_j = top_left_j + cells_y
        
        # 获取可见区域内的实体
        visible_entities = self.grid.get_entities_in_rect(
            top_left_i, top_left_j, bottom_right_i, bottom_right_j
        )
        
        # 绘制实体
        for (i, j), entity in visible_entities.items():
            # 计算屏幕坐标（玩家在屏幕中心）
            screen_x = (i - top_left_i) * self.cell_size
            screen_y = (j - top_left_j) * self.cell_size
            
            # 获取实体图像
            if hasattr(entity, 'image'):
                entity_image = self.get_image(entity.image)
                if entity_image:
                    # 缩放图像到单元格大小
                    scaled_image = pygame.transform.scale(
                        entity_image, 
                        (self.cell_size, self.cell_size)
                    )
                    self.screen.blit(scaled_image, (screen_x, screen_y))
                else:
                    # 如果图像加载失败，绘制彩色矩形作为占位符
                    self.draw_entity_placeholder(entity, screen_x, screen_y)
    
    def draw_entity_placeholder(self, entity, x, y):
        """绘制实体占位符（当图像加载失败时使用）"""
        if isinstance(entity, type(self.player)):
            color = (0, 0, 255)  # 玩家蓝色
        elif hasattr(entity, 'image') and "tree" in entity.image:
            color = (0, 128, 0)  # 树绿色
        elif hasattr(entity, 'image') and "save" in entity.image:
            color = (255, 215, 0)  # 存档点金色
        elif hasattr(entity, 'image') and "pig" in entity.image:
            color = (255, 192, 203)  # 猪粉色
        else:
            color = (128, 128, 128)  # 默认灰色
        
        pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
        
        # 绘制实体类型首字母
        entity_type = type(entity).__name__[0]
        text_surface = self.font.render_text(entity_type, 20, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
        self.screen.blit(text_surface, text_rect)

    def draw_bag(self):
        """在屏幕角落显示玩家背包内容"""
        # 绘制背包背景
        bag_width = 200
        bag_height = 200
        bag_x = 20
        bag_y = 20
        
        pygame.draw.rect(self.screen, (200, 200, 200), (bag_x, bag_y, bag_width, bag_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (bag_x, bag_y, bag_width, bag_height), 2)
        
        # 绘制背包标题
        title_surface = self.font.render_text("背包", 24, (0, 0, 0))
        self.screen.blit(title_surface, (bag_x + 10, bag_y + 10))
        
        # 绘制背包物品
        if hasattr(self.player, 'bag'):
            items = list(self.player.bag.items())
            for i, (item_name, count) in enumerate(items):
                if i < 8:  # 限制显示数量
                    item_y = bag_y + 50 + i * 20
                    item_text = f"{item_name}: {count}"
                    item_surface = self.font.render_text(item_text, 18, (0, 0, 0))
                    self.screen.blit(item_surface, (bag_x + 20, item_y))
    
    def draw_chest(self, chest_entity):
        """当玩家与箱子交互时显示箱子库存"""
        # 绘制箱子界面背景
        chest_width = 300
        chest_height = 300
        chest_x = (self.screen.get_width() - chest_width) // 2
        chest_y = (self.screen.get_height() - chest_height) // 2
        
        pygame.draw.rect(self.screen, (139, 69, 19), (chest_x, chest_y, chest_width, chest_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (chest_x, chest_y, chest_width, chest_height), 2)
        
        # 绘制箱子标题
        title_surface = self.font.render_text("箱子", 24, (255, 255, 255))
        self.screen.blit(title_surface, (chest_x + 10, chest_y + 10))
        
        # 绘制箱子内容
        if hasattr(chest_entity, 'inventory'):
            items = list(chest_entity.inventory.items())
            for i, (item_name, count) in enumerate(items):
                if i < 10:  # 限制显示数量
                    item_y = chest_y + 50 + i * 25
                    item_text = f"{item_name}: {count}"
                    item_surface = self.font.render_text(item_text, 18, (255, 255, 255))
                    self.screen.blit(item_surface, (chest_x + 20, item_y))
    
    def draw_interaction_hint(self):
        """显示与实体交互的提示"""
        # 根据玩家方向计算前方位置
        if self.player.direction == "up":
            target_i, target_j = self.player.i, self.player.j - 1
        elif self.player.direction == "down":
            target_i, target_j = self.player.i, self.player.j + 1
        elif self.player.direction == "left":
            target_i, target_j = self.player.i - 1, self.player.j
        elif self.player.direction == "right":
            target_i, target_j = self.player.i + 1, self.player.j
        else:
            return
        
        # 检查前方是否有可交互实体
        target_entity = self.grid.get_entity_at(target_i, target_j)
        if target_entity is not None:
            # 在屏幕底部显示交互提示
            hint_text = "按空格键交互"
            hint_surface = self.font.render_text(hint_text, 20, (255, 255, 255))
            hint_bg = pygame.Surface((hint_surface.get_width() + 20, hint_surface.get_height() + 10))
            hint_bg.fill((0, 0, 0))
            hint_bg.set_alpha(180)
            
            hint_x = (self.screen.get_width() - hint_bg.get_width()) // 2
            hint_y = self.screen.get_height() - hint_bg.get_height() - 20
            
            self.screen.blit(hint_bg, (hint_x, hint_y))
            self.screen.blit(hint_surface, (hint_x + 10, hint_y + 5))


    
    def draw(self, bag_open=False, chest_entity=None):
        """绘制整个场景"""
        self.screen.fill((255, 255, 255))  # 清空屏幕为白色
        self.draw_grid()
        self.draw_entities()
        
        # 根据游戏状态决定是否绘制背包或箱子界面
        if bag_open:
            self.draw_bag()
        elif chest_entity is not None:
            self.draw_chest(chest_entity)
        else:
            self.draw_interaction_hint()
        
        pygame.display.flip()
    
    def get_image(self, image_path):
        """从图像缓存中获取图像，如果不存在则加载并缓存"""
        if image_path in self.image_cache:
            return self.image_cache[image_path]
        
        # 尝试加载图像
        try:
            abs_image_path = os.path.join(PROJECT_ROOT, image_path)
            if os.path.exists(abs_image_path):
                image = pygame.image.load(abs_image_path).convert_alpha()
                scaled_image = pygame.transform.scale(image, (self.cell_size, self.cell_size))
                self.image_cache[image_path] = scaled_image
                return image
            else:
                return None
        except pygame.error as e:
            return None
    