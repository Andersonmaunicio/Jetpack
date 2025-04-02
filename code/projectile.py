import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/Projeteis.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 10))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade_x = 10

    def update(self, win_width):  # Já está correto, usa win_width
        self.rect.x += self.velocidade_x
        if self.rect.left > win_width:
            self.kill()