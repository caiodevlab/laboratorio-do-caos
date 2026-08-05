from pathlib import Path
import random
import pygame

pygame.init()

LARGURA = 800
ALTURA = 600

base = Path(__file__).resolve().parent
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Laboratório do Caos")

fundo = pygame.image.load(base / "assets" / "imagens" / "fundo.png")
menu = pygame.image.load(base / "assets" / "imagens" / "menu.png")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
menu = pygame.transform.scale(menu, (LARGURA, ALTURA))
clock = pygame.time.Clock()

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)

fonte = pygame.font.SysFont(None, 36)
fonte_grande = pygame.font.SysFont(None, 60)


class Plataforma:
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)


class Escada:
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)


class Jogador:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, 50, 50)
        self.velx = 0
        self.vely = 0
        self.no_chao = False
        self.pulos = 2
        self.na_escada = False

    def atualizar(self, plataformas):
        if not self.na_escada:
            self.vely += 0.6
        self.vely = min(self.vely, 10)

        self.rect.x += int(self.velx)
        self.rect.y += int(self.vely)

        self.no_chao = False
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.vely > 0:
                    self.rect.bottom = plataforma.rect.top
                    self.vely = 0
                    self.no_chao = True
                    self.pulos = 2
                    break

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA

    def pular(self):
        if self.na_escada:
            return
        if self.no_chao:
            self.vely = -12
        elif self.pulos > 0:
            self.vely = -10
            self.pulos -= 1


def criar_fase():
    jogador = Jogador()

    plataformas = [
        Plataforma(0, 491, 800, 40),
        Plataforma(236, 316, 191, 15),
        Plataforma(466, 255, 228, 15),
        Plataforma(0, 235, 324, 15),
    ]
    escadas = [
        Escada(130, 256, 20, 200),
        Escada(720, 257, 20, 50),
    ]

    cartoes = []
    for _ in range(5):
        cartoes.append(pygame.Rect(random.randint(50, 700), random.randint(80, 500), 20, 20))

    porta = pygame.Rect(634, 399, 75, 80)
    inimigo = pygame.Rect(49, 438, 40, 40)

    return jogador, plataformas, escadas, cartoes, porta, inimigo


estado = "menu"
jogador, plataformas, escadas, cartoes, porta, inimigo = criar_fase()
cartoes_coletados = 0
porta_aberta = False
inicio = pygame.time.get_ticks()
tempo_final = 0
vel_inimigo = 3
rodando = True

while rodando:
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
        elif estado == "menu":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jogador, plataformas, escadas, cartoes, porta, inimigo = criar_fase()
                cartoes_coletados = 0
                porta_aberta = False
                inicio = pygame.time.get_ticks()
                estado = "historia"
        elif estado == "historia":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                estado = "jogo"
        elif estado == "jogo":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                jogador.pular()
        elif estado in {"vitoria", "derrota"}:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                estado = "menu"

    if estado == "jogo":
        teclas = pygame.key.get_pressed()

        jogador.velx = 0
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            jogador.velx = -6
        elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            jogador.velx = 6

        if jogador.na_escada:
            if teclas[pygame.K_w] or teclas[pygame.K_UP]:
                jogador.vely = -4
            elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
                jogador.vely = 4
            else:
                jogador.vely = 0

        jogador.na_escada = False
        for escada in escadas:
            if jogador.rect.colliderect(escada.rect):
                jogador.na_escada = True
                break

        jogador.atualizar(plataformas)

        inimigo.x += vel_inimigo
        if inimigo.left <= 0 or inimigo.right >= LARGURA:
            vel_inimigo *= -1

        for cartao in list(cartoes):
            if jogador.rect.colliderect(cartao):
                cartoes.remove(cartao)
                cartoes_coletados += 1

        if cartoes_coletados >= 5:
            porta_aberta = True

        if jogador.rect.colliderect(inimigo):
            estado = "derrota"

        if porta_aberta and jogador.rect.colliderect(porta):
            tempo_final = (pygame.time.get_ticks() - inicio) // 1000
            estado = "vitoria"

    if estado == "historia":
        tela.fill(BRANCO)
    else:
        tela.blit(fundo, (0, 0))

    if estado == "menu":
        tela.blit(menu, (0, 0))
    elif estado == "historia":
        tela.blit(fonte_grande.render("HISTÓRIA", True, PRETO), (260, 70))
        historia_texto = [
            "Um experimento de Física deu errado!",
            "O cientista está preso no laboratório.",
            "Colete todos os cartões de acesso para escapar.",
            "Aprenda conceitos de Física no percurso.",
        ]
        for indice, linha in enumerate(historia_texto):
            tela.blit(fonte.render(linha, True, PRETO), (50, 150 + indice * 40))
        tela.blit(fonte.render("Pressione ENTER para iniciar a missão.", True, PRETO), (50, ALTURA - 100))
    elif estado == "jogo":
        # As plataformas fazem parte do mapa, mas não precisam aparecer com cor.
        for plataforma in plataformas:
            pass

        # O personagem é desenhado na tela.
        pygame.draw.rect(tela, VERMELHO, jogador.rect)

        # O inimigo também aparece na fase.
        pygame.draw.rect(tela, AZUL, inimigo)

        # Os cartões são mostrados como itens coletáveis.
        for cartao in cartoes:
            pygame.draw.rect(tela, AMARELO, cartao)

        tempo = (pygame.time.get_ticks() - inicio) // 1000
        tela.blit(fonte.render(f"Cartoes: {cartoes_coletados}/5", True, VERDE), (10, 10))
        tela.blit(fonte.render(f"Tempo: {tempo}s", True, VERDE), (10, 45))
    elif estado == "vitoria":
        tempo = (pygame.time.get_ticks() - inicio) // 1000
        tela.blit(fonte_grande.render("VOCE ESCAPOU!", True, VERDE), (180, 220))
        tela.blit(fonte.render(f"Tempo final: {tempo_final}s", True, BRANCO), (300, 300))
        tela.blit(fonte.render("R - Voltar ao menu", True, BRANCO), (260, 350))
    elif estado == "derrota":
        tela.blit(fonte_grande.render("VOCE PERDEU!", True, VERMELHO), (180, 240))
        tela.blit(fonte.render("R - Tentar novamente", True, BRANCO), (250, 320))

    pygame.display.flip()

pygame.quit()
