import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configurações da tela
WIN_WIDTH = 800
WIN_HEIGHT = 600
tela = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Jet Pack')  # Nome do jogo no título da janela

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)  # Amarelo brilhante

# Frames por segundo
clock = pygame.time.Clock()

# Carregar música do menu e da fase
pygame.mixer.music.load('assets/Menu.mp3')  # Música para o menu
pygame.mixer.music.play(-1)  # Toca a música do menu em loop

# Carregar imagens de fundo
bg_image = pygame.image.load('assets/Background.png')
menu_bg = pygame.image.load('assets/Menubg.png')  # Imagem de fundo do menu

# Classe do jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/Jogador.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (100, WIN_HEIGHT // 2)  # Posição inicial à esquerda
        self.velocidade_y = 0
        self.vidas = 3  # Sempre inicia com 3 vidas

    def update(self):
        self.velocidade_y = 0
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            self.velocidade_y = -5
        if teclas[pygame.K_DOWN]:
            self.velocidade_y = 5

        self.rect.y += self.velocidade_y

        # Impedir que o jogador saia da tela
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT

    def perder_vida(self):
        self.vidas -= 1
        if self.vidas <= 0:
            return True
        return False

    def atirar(self):
        projetil = Projetil(self.rect.right, self.rect.centery)
        todos_sprites.add(projetil)
        projeteis.add(projetil)

# Classe dos projéteis
class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/Projeteis.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 5))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade_x = 10

    def update(self):
        self.rect.x += self.velocidade_x
        if self.rect.left > WIN_WIDTH:
            self.kill()

# Classe dos asteroides
class Asteroide(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/Asteroides.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = WIN_WIDTH
        self.rect.y = random.randint(0, WIN_HEIGHT - self.rect.height)
        self.velocidade_x = random.randint(3, 8)

    def update(self):
        self.rect.x -= self.velocidade_x
        if self.rect.right < 0:
            self.kill()

# Grupos de sprites
todos_sprites = pygame.sprite.Group()
projeteis = pygame.sprite.Group()
asteroides = pygame.sprite.Group()

# Variáveis de jogo
pontuacao = 0
tempo_limite = 60

# Função para gerar asteroides
def gerar_asteroides():
    asteroide = Asteroide()
    todos_sprites.add(asteroide)
    asteroides.add(asteroide)

# Função para tocar a música da fase
def tocar_musica_fase():
    pygame.mixer.music.load('assets/Level.mp3')
    pygame.mixer.music.play(-1)

# Função para exibição da mensagem de derrota
def mostrar_tela_derrota():
    tela.fill(PRETO)
    fonte = pygame.font.Font(None, 74)
    texto_derrota = fonte.render("GAME OVER", True, BRANCO)
    tela.blit(texto_derrota, (250, 200))
    pygame.display.flip()
    pygame.time.wait(2000)
    mostrar_menu()

# Função para exibir a pontuação
def mostrar_pontuacao():
    fonte = pygame.font.Font(None, 36)
    texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, BRANCO)
    tela.blit(texto_pontuacao, (10, 10))

# Função para exibir a quantidade de vidas restantes
def mostrar_vidas(jogador):
    fonte = pygame.font.Font(None, 36)
    texto_vidas = fonte.render(f'Vidas: {jogador.vidas}', True, BRANCO)
    tela.blit(texto_vidas, (WIN_WIDTH - 120, 10))

# Função para exibir o tempo restante
def mostrar_tempo(tempo_restante):
    fonte = pygame.font.Font(None, 36)
    texto_tempo = fonte.render(f'Tempo: {tempo_restante}s', True, BRANCO)
    tela.blit(texto_tempo, (WIN_WIDTH // 2 - 50, 10))

# Função principal do jogo
def main():
    global pontuacao, tempo_limite
    todos_sprites.empty()
    projeteis.empty()
    asteroides.empty()

    jogador = Jogador()
    todos_sprites.add(jogador)

    tempo_inicial = pygame.time.get_ticks()

    rodando = True
    invencivel = False
    tempo_invencivel = 0

    while rodando:
        clock.tick(60)

        # Processamento de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogador.atirar()

        tempo_passado = (pygame.time.get_ticks() - tempo_inicial) // 1000
        tempo_restante = tempo_limite - tempo_passado

        if tempo_restante <= 0:
            mostrar_tela_derrota()
            rodando = False

        # Atualizar invencibilidade
        if invencivel:
            tempo_invencivel -= 1
            if tempo_invencivel <= 0:
                invencivel = False

        todos_sprites.update()

        colisao_projeteis = pygame.sprite.groupcollide(projeteis, asteroides, True, True)
        for _ in colisao_projeteis:
            pontuacao += 1

        if not invencivel:
            colisao_jogador = pygame.sprite.spritecollide(jogador, asteroides, True)
            if colisao_jogador:
                if jogador.perder_vida():
                    mostrar_tela_derrota()
                    rodando = False
                else:
                    jogador.rect.center = (100, WIN_HEIGHT // 2)
                    invencivel = True
                    tempo_invencivel = 60

        if random.random() > 0.98:
            gerar_asteroides()

        tela.fill(PRETO)
        tela.blit(bg_image, (0, 0))
        todos_sprites.draw(tela)
        mostrar_pontuacao()
        mostrar_vidas(jogador)
        mostrar_tempo(tempo_restante)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Função para o menu principal
def mostrar_menu():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('assets/Menu.mp3')
    pygame.mixer.music.play(-1)

    rodando_menu = True
    opcao_selecionada = 0
    while rodando_menu:
        tela.blit(menu_bg, (0, 0))  # Usa Menubg.png como fundo
        fonte = pygame.font.Font(None, 48)
        fonte_titulo = pygame.font.Font(None, 100)  # Fonte maior para o título

        # Título "Jet Pack" maior e com cor brilhante
        texto_titulo = fonte_titulo.render("Jet Pack", True, AMARELO)  # Amarelo brilhante
        texto_new_game = fonte.render("New Game", True, AMARELO if opcao_selecionada == 0 else PRETO)
        texto_quit = fonte.render("Quit", True, AMARELO if opcao_selecionada == 1 else PRETO)

        # Centralizar o título e posicionar as opções
        tela.blit(texto_titulo, (WIN_WIDTH // 2 - texto_titulo.get_width() // 2, 120))  # Ajustado para caber melhor
        tela.blit(texto_new_game, (350, 250))
        tela.blit(texto_quit, (350, 300))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando_menu = False
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % 2
                if evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % 2

                if evento.key == pygame.K_RETURN:
                    if opcao_selecionada == 0:
                        rodando_menu = False
                        pygame.mixer.music.stop()
                        tocar_musica_fase()
                        main()
                    elif opcao_selecionada == 1:
                        rodando_menu = False
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    mostrar_menu()