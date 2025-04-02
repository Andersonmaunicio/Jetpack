import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, win_width, win_height):
        super().__init__()
        self.image = pygame.image.load('assets/Jogador.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (100, win_height // 2)
        self.velocidade_y = 0
        self.vidas = 3
        self.win_height = win_height

    def update(self, *args):  # Deve aceitar *args
        self.velocidade_y = 0
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            self.velocidade_y = -5
        if teclas[pygame.K_DOWN]:
            self.velocidade_y = 5

        self.rect.y += self.velocidade_y

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.win_height:
            self.rect.bottom = self.win_height

    def perder_vida(self):
        self.vidas -= 1
        return self.vidas <= 0

    def atirar(self):
        from code.projectile import Projectile
        projetil = Projectile(self.rect.right, self.rect.centery)
        return projetil