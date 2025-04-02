import pygame
import random

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, win_width, win_height):
        super().__init__()
        self.image = pygame.image.load('assets/Asteroides.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = win_width
        self.rect.y = random.randint(0, win_height - self.rect.height)
        self.velocidade_x = random.randint(3, 8)

    def update(self, *args):  # Corrige aceitando argumentos opcionais
        self.rect.x -= self.velocidade_x
        if self.rect.right < 0:
            self.kill()