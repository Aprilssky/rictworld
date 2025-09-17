# rictworld/src/main.py
import pygame
import sys
import time
from grid import Grid
from ui.viewer import Viewer
from entities.player_entity import PlayerEntity
from entities.tree_entity import TreeEntity
from entities.ai_entity import AIEntity
from entities.save_entity import SaveEntity

# Pygame 初始化
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RictWorld")

# Grid 初始化
grid = Grid()

# 实体添加
player = PlayerEntity(0, 0)
grid.add_entity(player)

# 添加一些树
tree1 = TreeEntity(3, 3)
tree2 = TreeEntity(7, 7)
tree3 = TreeEntity(10, 5)
grid.add_entity(tree1)
grid.add_entity(tree2)
grid.add_entity(tree3)

# 添加一些猪
pig1 = AIEntity(8, 8)
pig2 = AIEntity(12, 3)
grid.add_entity(pig1)
grid.add_entity(pig2)

# 在实体添加部分添加存档实体
save_point = SaveEntity(5, 5, grid)
grid.add_entity(save_point)

# Viewer 初始化
CELL_SIZE = 40
viewer = Viewer(screen, grid, player, CELL_SIZE)

# 游戏循环
clock = pygame.time.Clock()
last_update_time = time.time()

# 背包状态
bag_open = False

running = True
while running:
    current_time = time.time()
    
    # 事件监听
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 键盘事件处理
        elif event.type == pygame.KEYDOWN:
            if not bag_open:  # 背包关闭状态下的输入映射
                if event.key == pygame.K_UP:
                    player.move(0, -1)
                    player.direction = "up"
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1)
                    player.direction = "down"
                elif event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                    player.direction = "left"
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0)
                    player.direction = "right"
                elif event.key == pygame.K_SPACE:
                    player.interact(grid)
                elif event.key == pygame.K_b:  # 打开/关闭背包
                    bag_open = not bag_open
            else:  # 背包打开状态下的输入映射
                if event.key == pygame.K_b:  # 关闭背包
                    bag_open = not bag_open
                # 可以添加背包内的物品选择逻辑
                elif event.key == pygame.K_1:
                    selected_bag_index = 0
                elif event.key == pygame.K_2:
                    selected_bag_index = 1
                elif event.key == pygame.K_3:
                    selected_bag_index = 2
                elif event.key == pygame.K_4:
                    selected_bag_index = 3
                elif event.key == pygame.K_5:
                    selected_bag_index = 4
                elif event.key == pygame.K_6:
                    selected_bag_index = 5
                elif event.key == pygame.K_7:
                    selected_bag_index = 6
                elif event.key == pygame.K_8:
                    selected_bag_index = 7
                elif event.key == pygame.K_9:
                    selected_bag_index = 8
                elif event.key == pygame.K_0:
                    selected_bag_index = 9
    
    # 定时更新
    if current_time - last_update_time > 0.5:
        grid.update()
        last_update_time = current_time
    
    # 屏幕刷新
    viewer.draw(bag_open=bag_open)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()