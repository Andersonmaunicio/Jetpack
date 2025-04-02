import pygame
import random
from code.player import Player      # Importa Player de code/player.py
from code.asteroid import Asteroid  # Importa Asteroid de code/asteroid.py

class Game:
    def __init__(self, win_width, win_height):
        self.win_width = win_width
        self.win_height = win_height
        self.tela = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption('Jet Pack')
        self.clock = pygame.time.Clock()
        self.bg_image = pygame.image.load('assets/Background.png')
        self.pontuacao = 0
        self.tempo_limite = 60
        self.todos_sprites = pygame.sprite.Group()
        self.projeteis = pygame.sprite.Group()
        self.asteroides = pygame.sprite.Group()
        self.player = Player(win_width, win_height)
        self.todos_sprites.add(self.player)
        self.tempo_inicial = pygame.time.get_ticks()

    def gerar_asteroides(self):
        asteroide = Asteroid(self.win_width, self.win_height)
        self.todos_sprites.add(asteroide)
        self.asteroides.add(asteroide)

    def tocar_musica_fase(self):
        pygame.mixer.music.load('assets/Level.mp3')
        pygame.mixer.music.play(-1)

    def mostrar_pontuacao(self):
        fonte = pygame.font.Font(None, 36)
        texto_pontuacao = fonte.render(f'Pontuação: {self.pontuacao}', True, (255, 255, 255))
        self.tela.blit(texto_pontuacao, (10, 10))

    def mostrar_vidas(self):
        fonte = pygame.font.Font(None, 36)
        texto_vidas = fonte.render(f'Vidas: {self.player.vidas}', True, (255, 255, 255))
        self.tela.blit(texto_vidas, (self.win_width - 120, 10))

    def mostrar_tempo(self, tempo_restante):
        fonte = pygame.font.Font(None, 36)
        texto_tempo = fonte.render(f'Tempo: {tempo_restante}s', True, (255, 255, 255))
        self.tela.blit(texto_tempo, (self.win_width // 2 - 50, 10))

    def mostrar_tela_derrota(self):
        self.tela.fill((0, 0, 0))
        fonte = pygame.font.Font(None, 74)
        texto_derrota = fonte.render("GAME OVER", True, (255, 255, 255))
        self.tela.blit(texto_derrota, (250, 200))
        pygame.display.flip()
        pygame.time.wait(2000)

    def run(self):
        rodando = True
        invencivel = False
        tempo_invencivel = 0

        while rodando:
            self.clock.tick(60)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    projetil = self.player.atirar()
                    self.todos_sprites.add(projetil)
                    self.projeteis.add(projetil)

            tempo_passado = (pygame.time.get_ticks() - self.tempo_inicial) // 1000
            tempo_restante = self.tempo_limite - tempo_passado
            if tempo_restante <= 0:
                self.mostrar_tela_derrota()
                return False

            if invencivel:
                tempo_invencivel -= 1
                if tempo_invencivel <= 0:
                    invencivel = False

            self.todos_sprites.update(self.win_width)

            colisao_projeteis = pygame.sprite.groupcollide(self.projeteis, self.asteroides, True, True)
            for _ in colisao_projeteis:
                self.pontuacao += 1

            if not invencivel and pygame.sprite.spritecollide(self.player, self.asteroides, True):
                if self.player.perder_vida():
                    self.mostrar_tela_derrota()
                    return False
                self.player.rect.center = (100, self.win_height // 2)
                invencivel = True
                tempo_invencivel = 60

            if random.random() > 0.98:
                self.gerar_asteroides()

            self.tela.fill((0, 0, 0))
            self.tela.blit(self.bg_image, (0, 0))
            self.todos_sprites.draw(self.tela)
            self.mostrar_pontuacao()
            self.mostrar_vidas()
            self.mostrar_tempo(tempo_restante)
            pygame.display.flip()

        return True