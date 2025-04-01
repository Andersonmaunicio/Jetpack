import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configurações da tela
WIN_WIDTH = 800
WIN_HEIGHT = 600
tela = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Jogo Jetpack')

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)

# Frames por segundo
clock = pygame.time.Clock()

# Carregar música do menu e da fase
pygame.mixer.music.load('assets/Menu.mp3')  # Música para o menu
pygame.mixer.music.play(-1)  # Toca a música do menu em loop


# Classe do jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Jogador.png").convert_alpha()  # Carregar imagem do jogador
        self.image = pygame.transform.scale(self.image, (150, 150))  # Ajustar tamanho se necessário
        self.rect = self.image.get_rect()
        self.rect.center = (100, WIN_HEIGHT // 2)
        self.velocidade_y = 0
        self.vidas = 3  # Jogador começa com 3 vidas


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

    def atirar(self):
        projetil = Projetil(self.rect.right, self.rect.centery)
        todos_sprites.add(projetil)
        projeteis.add(projetil)

    def perder_vida(self):
        self.vidas -= 1
        if self.vidas <= 0:
            return True
        return False


# Classe dos projéteis
class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/Projeteis.png").convert_alpha()  # Carregar imagem do projétil
        self.image = pygame.transform.scale(self.image, (40, 20))  # Ajustar tamanho se necessário
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade_x = 10

    def update(self):
        self.rect.x += self.velocidade_x
        if self.rect.left > WIN_WIDTH:
            self.kill()


    def update(self):
        self.rect.x += self.velocidade_x
        if self.rect.left > WIN_WIDTH:
            self.kill()


# Classe dos asteroides
class Asteroide(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Asteroides.png").convert_alpha()  # Carregar imagem do asteroide
        self.image = pygame.transform.scale(self.image, (100, 100))  # Ajustar tamanho se necessário
        self.rect = self.image.get_rect()
        self.rect.x = WIN_WIDTH
        self.rect.y = random.randint(0, WIN_HEIGHT - self.rect.height)
        self.velocidade_x = random.randint(3, 8)

    def update(self):
        self.rect.x -= self.velocidade_x
        if self.rect.right < 0:
            self.kill()


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
vidas_restantes = 3
tempo_limite = 60  # 60 segundos para passar de fase

# Criar o jogador
jogador = Jogador()
todos_sprites.add(jogador)


# Função para gerar asteroides
def gerar_asteroides():
    asteroide = Asteroide()
    todos_sprites.add(asteroide)
    asteroides.add(asteroide)


# Função para tocar a música da fase
def tocar_musica_fase():
    pygame.mixer.music.load('assets/Level1.MP3')  # Música para a fase 1
    pygame.mixer.music.play(-1)  # Toca a música em loop


# Função para exibição da mensagem de derrota
def mostrar_tela_derrota():
    tela.fill(PRETO)
    fonte = pygame.font.Font(None, 74)
    texto_derrota = fonte.render("GAME OVER", True, BRANCO)
    tela.blit(texto_derrota, (250, 200))

    pygame.display.flip()
    pygame.time.wait(2000)  # Aguardar 2 segundos antes de retornar ao menu
    mostrar_menu()  # Retorna ao menu principal


# Função para exibir a mensagem de "Passou de Fase"
def passar_de_fase():
    tela.fill(PRETO)
    fonte = pygame.font.Font(None, 74)
    texto_passar = fonte.render("Fase Concluída!", True, BRANCO)
    tela.blit(texto_passar, (250, 200))

    pygame.display.flip()
    pygame.time.wait(2000)  # Aguardar 2 segundos antes de continuar para a próxima fase
    mostrar_menu()  # Retorna ao menu principal


# Loop principal do jogo
def main():
    global pontuacao, vidas_restantes, tempo_limite
    # Resetar variáveis e reiniciar grupos de sprites
    todos_sprites.empty()
    projeteis.empty()
    asteroides.empty()

    jogador = Jogador()
    todos_sprites.add(jogador)

    # Iniciar o tempo
    tempo_inicial = pygame.time.get_ticks()

    rodando = True
    while rodando:
        clock.tick(60)  # FPS

        # Processamento de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogador.atirar()

        # Calcular o tempo restante
        tempo_passado = (pygame.time.get_ticks() - tempo_inicial) // 1000
        tempo_restante = tempo_limite - tempo_passado

        if tempo_restante <= 0:
            passar_de_fase()
            rodando = False

        # Atualizar sprites
        todos_sprites.update()

        # Verificar colisões entre projéteis e asteroides
        colisao_projeteis = pygame.sprite.groupcollide(projeteis, asteroides, True, True)
        for _ in colisao_projeteis:
            pontuacao += 1  # Aumenta a pontuação a cada asteroide destruído

        # Verificar colisões entre jogador e asteroides
        colisao_jogador = pygame.sprite.spritecollide(jogador, asteroides, False)
        if colisao_jogador:
            if jogador.perder_vida():
                mostrar_tela_derrota()  # Mostrar a tela de derrota
                rodando = False  # Encerra o jogo
            else:
                # Respawn do jogador após perda de vida
                jogador.rect.center = (100, WIN_HEIGHT // 2)
                pygame.time.wait(500)  # Aguardar meio segundo antes de continuar

        # Gerar asteroides periodicamente
        if random.random() > 0.98:
            gerar_asteroides()

        # Desenhar tudo na tela
        tela.fill(PRETO)
        todos_sprites.draw(tela)

        # Exibir pontuação, vidas e tempo
        fonte = pygame.font.Font(None, 36)
        texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, BRANCO)
        tela.blit(texto_pontuacao, (10, 10))

        texto_vidas = fonte.render(f'Vidas: {jogador.vidas}', True, BRANCO)
        tela.blit(texto_vidas, (WIN_WIDTH - 120, 10))

        texto_tempo = fonte.render(f'Tempo: {tempo_restante}s', True, BRANCO)
        tela.blit(texto_tempo, (WIN_WIDTH // 2 - 50, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# Função para o menu principal
def mostrar_menu():
    pygame.mixer.music.stop()  # Parar a música da fase antes de voltar para o menu
    pygame.mixer.music.load('assets/Menu.mp3')  # Carregar música do menu
    pygame.mixer.music.play(-1)  # Tocar música do menu em loop

    rodando_menu = True
    opcao_selecionada = 0  # 0 para "New Game", 1 para "Quit"
    while rodando_menu:
        tela.fill(BRANCO)
        fonte = pygame.font.Font(None, 48)

        # Opções do menu
        texto_new_game = fonte.render("New Game", True, AMARELO if opcao_selecionada == 0 else PRETO)
        texto_quit = fonte.render("Quit", True, AMARELO if opcao_selecionada == 1 else PRETO)

        tela.blit(texto_new_game, (350, 250))
        tela.blit(texto_quit, (350, 300))
        pygame.display.flip()

        # Processamento de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando_menu = False
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % 2  # Alternar entre "New Game" e "Quit"
                if evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % 2  # Alternar entre "Quit" e "New Game"

                if evento.key == pygame.K_RETURN:
                    if opcao_selecionada == 0:
                        rodando_menu = False
                        pygame.mixer.music.stop()  # Parar a música do menu
                        tocar_musica_fase()  # Tocar música da fase 1
                        main()  # Iniciar o jogo
                    elif opcao_selecionada == 1:
                        rodando_menu = False
                        pygame.quit()
                        sys.exit()


if __name__ == "__main__":
    mostrar_menu()
