import pygame
import random

pygame.init()

# Configurações da janela
LARGURA = 800
ALTURA = 600
TITULO = "Jogo de Física Aprimorado"

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)
clock = pygame.time.Clock()

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
#fonte para texto
fonte = pygame.font.SysFont(None, 36)
# Classe do Jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        
        # Física e Movimentação
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.aceleracao_x = 0.5
        self.desaceleracao = 0.1
        self.velocidade_max = 6
        
        self.gravidade = 0.6
        self.forca_pulo = -12
        self.limite_queda = 15
        
        # Estados
        self.esta_no_chao = False
        self.pulos_restantes = 2

    def atualizar(self, chao, plataformas):
        # Gravidade
        self.velocidade_y += self.gravidade
        if self.velocidade_y > self.limite_queda:
            self.velocidade_y = self.limite_queda

        # Movimento Horizontal com desaceleração
        self.velocidade_x *= (1 - self.desaceleracao)
        self.rect.x += self.velocidade_x

        # Colisão Horizontal
        self.verificar_colisoes_x(plataformas)
        self.verificar_colisoes_x([chao])

        # Movimento Vertical
        self.rect.y += self.velocidade_y

        # Colisão Vertical
        self.esta_no_chao = False
        self.verificar_colisoes_y(plataformas)
        self.verificar_colisoes_y([chao])

        # Limites da tela (paredes)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA

    def pular(self):
        if self.esta_no_chao:
            self.velocidade_y = self.forca_pulo
            self.esta_no_chao = False
        elif self.pulos_restantes > 0: # Pulo duplo
            self.velocidade_y = self.forca_pulo * 0.8 # Pulo duplo um pouco menor
            self.pulos_restantes -= 1

    def verificar_colisoes_x(self, obstaculos):
        for obstaculo in obstaculos:
            if self.rect.colliderect(obstaculo.rect):
                if self.velocidade_x > 0:
                    self.rect.right = obstaculo.rect.left
                elif self.velocidade_x < 0:
                    self.rect.left = obstaculo.rect.right
                self.velocidade_x = 0

    def verificar_colisoes_y(self, obstaculos):
        for obstaculo in obstaculos:
            if self.rect.colliderect(obstaculo.rect):
                if self.velocidade_y > 0: # Caindo
                    self.rect.bottom = obstaculo.rect.top
                    self.velocidade_y = 0
                    self.esta_no_chao = True
                    self.pulos_restantes = 2 # Reseta pulo duplo
                elif self.velocidade_y < 0: # Pulando e batendo a cabeça
                    self.rect.top = obstaculo.rect.bottom
                    self.velocidade_y = 0

# Classe para plataformas
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Classe para coletáveis (moedas/estrelas)
class CartaoAcesso(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(AMARELO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Configurações do jogo
jogador = Jogador()
grupo_jogador = pygame.sprite.GroupSingle(jogador)

chao = Plataforma(0, ALTURA - 40, LARGURA, 40)
grupo_chao = pygame.sprite.GroupSingle(chao)

# Grupo de plataformas
grupo_plataformas = pygame.sprite.Group()
grupo_plataformas.add(Plataforma(250, ALTURA - 120, 150, 20))
grupo_plataformas.add(Plataforma(450, ALTURA - 220, 150, 20))
grupo_plataformas.add(Plataforma(150, ALTURA - 320, 150, 20))

#criar porta
class Porta(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 80))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
#porta no mapa
porta = Porta(700, ALTURA - 120)
grupo_porta = pygame.sprite.GroupSingle(porta)

# Grupo de coletáveis
grupo_coletaveis = pygame.sprite.Group()
for _ in range(5):
    item = CartaoAcesso(random.randint(100, LARGURA - 100), random.randint(100, ALTURA - 150))
    grupo_coletaveis.add(item)

#variaveis de controle
cartoes_coletados = 0
cartoes_necessarios = 5
porta_aberta = False

#função para coletar cartões
def coletar_cartao():
    global cartoes_coletados
    cartoes_coletados += 1
    print(f"Cartões coletados: {cartoes_coletados}")

#função para verificar se a porta pode ser aberta
def encostar_na_porta():
    global porta_aberta
    if cartoes_coletados >= cartoes_necessarios:
        porta_aberta = True
        print("Porta aberta! Você pode passar.")
        porta.image.fill(VERDE) # Muda a cor da porta para indicar que está aberta
    
    else:
        print(f"Você precisa coletar {cartoes_necessarios - cartoes_coletados} cartões para abrir a porta.")
tempo_inicio = pygame.time.get_ticks() # Tempo inicial do jogo
# Loop Principal
venceu = False
rodando = True
while rodando:
    relogio = clock.tick(60)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE or evento.key == pygame.K_UP:
                jogador.pular()

    # Movimento contínuo pelas setas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        jogador.velocidade_x -= jogador.aceleracao_x
        if jogador.velocidade_x < -jogador.velocidade_max:
            jogador.velocidade_x = -jogador.velocidade_max
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        jogador.velocidade_x += jogador.aceleracao_x
        if jogador.velocidade_x > jogador.velocidade_max:
            jogador.velocidade_x = jogador.velocidade_max

    # Atualizações
    jogador.atualizar(chao, grupo_plataformas)
    
    # Coletar itens
    coletados = pygame.sprite.spritecollide(jogador, grupo_coletaveis, True)
    for item in coletados:
        coletar_cartao()
    if pygame.sprite.collide_rect(jogador, porta):
        encostar_na_porta()
        if porta_aberta:
            venceu = True
            print("Parabéns! Você venceu o jogo!")
            rodando = False
            

    # Renderização
    tela.fill(BRANCO)
    grupo_chao.draw(tela)
    grupo_plataformas.draw(tela)
    grupo_coletaveis.draw(tela)
    grupo_jogador.draw(tela)
    grupo_porta.draw(tela)
    texto = fonte.render(
        f"Cartões coletados: {cartoes_coletados}/{cartoes_necessarios}", 
        True, PRETO
    )
    tela.blit(texto, (10, 10))
    if venceu:
        texto_vitoria = fonte.render("Parabéns! Você venceu!", True, AZUL)
        tela.blit(texto_vitoria, (280, 250))
    tempo = (pygame.time.get_ticks() - tempo_inicio) // 1000
    texto_tempo = fonte.render(f"Tempo: {tempo} segundos", True, PRETO)
    tela.blit(texto_tempo, (10, 50))
    pygame.display.flip()
pygame.quit()