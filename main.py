from logging import DEBUG

import pygame
import random

pygame.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Laboratório do Caos")

fundo = pygame.image.load('assets/imagens/fundo.png')
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
clock = pygame.time.Clock()

BRANCO=(255,255,255)
PRETO=(0,0,0)
VERMELHO=(255,0,0)
VERDE=(0,255,0)
AZUL=(0,0,255)
AMARELO=(255,255,0)
CINZA=(120,120,120)

fonte = pygame.font.SysFont(None,36)
fonte_grande = pygame.font.SysFont(None,60)

class Plataforma:
    def __init__(self,x,y,w,h):
        self.rect = pygame.Rect(x,y,w,h)

class Jogador:
    def __init__(self):
        self.rect = pygame.Rect(100,100,50,50)
        self.velx = 0
        self.vely = 0
        self.no_chao = False
        self.pulos = 2

    def atualizar(self, plataformas):
        self.vely += 0.6
        if self.vely > 10:
            self.vely = 10

        self.rect.x += int(self.velx)

        self.rect.y += int(self.vely)

        self.no_chao = False
        for p in plataformas:
            if self.rect.colliderect(p.rect):
                if self.vely > 0:
                    self.rect.bottom = p.rect.top
                    self.vely = 0
                    self.no_chao = True
                    self.pulos = 2

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA

    def pular(self):
        if self.no_chao:
            self.vely = -12
        elif self.pulos > 0:
            self.vely = -10
            self.pulos -= 1

def criar_fase():
    jogador = Jogador()

    plataformas = [
        Plataforma(0,491,800,40),
        Plataforma(236,316,191,15),
        Plataforma(466,255,228,15),
        Plataforma(0,235,324,15)    
    ]

    cartoes = []
    for _ in range(5):
        cartoes.append(pygame.Rect(random.randint(50,700), random.randint(80,500), 20, 20))

    porta = pygame.Rect(700,480,60,80)
    inimigo = pygame.Rect(300,520,40,40)

    return jogador, plataformas, cartoes, porta, inimigo

estado = "menu"
escadas = [
    pygame.Rect(300,316,20,175),
    pygame.Rect(500,255,20,235)
]
em_escada = False
jogador, plataformas, cartoes, porta, inimigo = criar_fase()
cartoes_coletados = 0
porta_aberta = False
inicio = pygame.time.get_ticks()
vel_inimigo = 3
tempo_final = 0
#bug de plataforma
DEBUG = False
#loop principal
rodando = True

while rodando:
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if estado == "menu":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    jogador, plataformas, cartoes, porta, inimigo = criar_fase()
                    cartoes_coletados = 0
                    porta_aberta = False
                    inicio = pygame.time.get_ticks()
                    estado = "jogo"

        elif estado == "jogo":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogador.pular()

        elif estado in ["vitoria","derrota"]:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                estado = "menu"

    if estado == "jogo":
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            jogador.velx = -6
        elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            jogador.velx = 6
        else:
            jogador.velx = 0

        jogador.atualizar(plataformas)

        inimigo.x += vel_inimigo
        if inimigo.left <= 0 or inimigo.right >= LARGURA:
            vel_inimigo *= -1

        for c in cartoes[:]:
            if jogador.rect.colliderect(c):
                cartoes.remove(c)
                cartoes_coletados += 1

        if cartoes_coletados >= 5:
            porta_aberta = True

        if jogador.rect.colliderect(inimigo):
            estado = "derrota"

        if porta_aberta and jogador.rect.colliderect(porta):
            tempo_final = (pygame.time.get_ticks()-inicio)//1000
            estado = "vitoria"

    tela.blit(fundo, (0, 0))

    if estado == "menu":
        titulo = fonte_grande.render("LABORATORIO DO CAOS", True, PRETO)
        iniciar = fonte.render("ENTER - Iniciar", True, PRETO)
        tela.blit(titulo,(160,200))
        tela.blit(iniciar,(300,320))

    elif estado == "jogo":
        for p in plataformas:
            #pygame.draw.rect(tela,CINZA,p.rect)
            pygame.draw.rect(tela,VERMELHO,jogador.rect)
            pygame.draw.rect(tela,AZUL,inimigo)
  
        for c in cartoes:
            pygame.draw.rect(tela,AMARELO,c)

        pygame.draw.rect(tela, VERDE if porta_aberta else AZUL, porta)

        tempo = (pygame.time.get_ticks()-inicio)//1000

        tela.blit(fonte.render(f"Cartoes: {cartoes_coletados}/5",True,PRETO),(10,10))
        tela.blit(fonte.render(f"Tempo: {tempo}s",True,PRETO),(10,45))

    elif estado == "vitoria":
        tempo = (pygame.time.get_ticks()-inicio)//1000
        tela.blit(fonte_grande.render("VOCE ESCAPOU!",True,VERDE),(180,220))
        tela.blit(fonte.render(f"Tempo final: {tempo_final}s",True,PRETO),(300,300))
        tela.blit(fonte.render("R - Voltar ao menu",True,PRETO),(260,350))

    elif estado == "derrota":
        tela.blit(fonte_grande.render("VOCE PERDEU!",True,VERMELHO),(180,240))
        tela.blit(fonte.render("R - Tentar novamente",True,PRETO),(250,320))
    #escadas
    for escada in escadas:
        if jogador.rect.colliderect(escada):
            em_escada = True
    if DEBUG:
        for p in plataformas:
            pygame.draw.rect(tela,(255,0,255),p.rect,2)

    pygame.display.flip()

pygame.quit()