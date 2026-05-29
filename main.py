import pygame
pygame.init()
# Configurações da janela
pygame.display.set_caption('Jogo de física')
altura = 600
largura = 800
tela = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock()
# variaveis do jogador
posição_x = 350
posição_y = 200
largura_player = 100
altura_player = 100
velocidade = 5
#velocidade do jogador e gravidade
velocidade_x = 0
velocidade_y = 0
gravidade = 0.5
#cor do jogador
cor_jogador = (255, 0, 0)
# Loop principal do jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    # Aplicar gravidade
    velocidade_y += gravidade
    # Movimentação do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        posição_x -= velocidade
    if teclas[pygame.K_RIGHT]:
        posição_x += velocidade
    if teclas[pygame.K_SPACE]:
        velocidade_y = -10#pular
    #aplicar gravidade
    velocidade_y += gravidade
    posição_y += velocidade_y
    #impedir que o jogador saia da tela
    if posição_x < 0:
        posição_x = 0
    if posição_x > largura - largura_player:
        posição_x = largura - largura_player
    if posição_y < 0:
        posição_y = 0
    if posição_y > altura - altura_player:
        posição_y = altura - altura_player
        velocidade_y = 0
    tela.fill((255, 255, 255))
    #colisão com o chão
    if posição_y > altura - altura_player:
        posição_y = altura - altura_player
        velocidade_y = 0
    # Desenhar o jogador
    pygame.draw.rect(tela, cor_jogador, (posição_x, posição_y, largura_player, altura_player))
    pygame.display.update()
    clock.tick(60)

pygame.quit()