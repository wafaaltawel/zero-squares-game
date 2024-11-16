# display.py

import pygame
import time
import sys
from colors import BACKGROUND_COLOR

class DisplayMessage:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def show(self, message, color, emoji_symbol):
        self.screen.fill(BACKGROUND_COLOR)
        text = self.font.render(message + " " + emoji_symbol, True, color)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        sys.exit()
