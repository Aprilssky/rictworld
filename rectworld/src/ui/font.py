# rictworld/src/ui/font.py
import pygame
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Font:
    def __init__(self):
        self.font_path = PROJECT_ROOT + "/assets/font/华文行楷.ttf"
        try:
            # 尝试加载字体文件
            pygame.font.Font(self.font_path, 12)
        except:
            print(f"字体文件 {self.font_path} 未找到，使用默认字体")
            self.font_path = pygame.font.get_default_font()
    
    def render_text(self, text, size=24, color=(0, 0, 0)):
        font = pygame.font.Font(self.font_path, size)
        return font.render(text, True, color)