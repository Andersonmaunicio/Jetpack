import pygame

class Menu:
    def __init__(self, win_width, win_height):
        self.win_width = win_width
        self.win_height = win_height
        self.tela = pygame.display.set_mode((win_width, win_height))
        self.menu_bg = pygame.image.load('assets/Menubg.png')
        pygame.mixer.music.load('assets/Menu.mp3')
        pygame.mixer.music.play(-1)

    def run(self):
        rodando_menu = True
        opcao_selecionada = 0
        while rodando_menu:
            self.tela.blit(self.menu_bg, (0, 0))
            fonte = pygame.font.Font(None, 48)
            fonte_titulo = pygame.font.Font(None, 100)

            texto_titulo = fonte_titulo.render("Jet Pack", True, (255, 255, 0))
            texto_new_game = fonte.render("New Game", True, (255, 255, 0) if opcao_selecionada == 0 else (0, 0, 0))
            texto_quit = fonte.render("Quit", True, (255, 255, 0) if opcao_selecionada == 1 else (0, 0, 0))

            self.tela.blit(texto_titulo, (self.win_width // 2 - texto_titulo.get_width() // 2, 120))
            self.tela.blit(texto_new_game, (350, 250))
            self.tela.blit(texto_quit, (350, 300))
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "quit"
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_DOWN:
                        opcao_selecionada = (opcao_selecionada + 1) % 2
                    if evento.key == pygame.K_UP:
                        opcao_selecionada = (opcao_selecionada - 1) % 2
                    if evento.key == pygame.K_RETURN:
                        return "start" if opcao_selecionada == 0 else "quit"