import pygame
pygame.init()
# Configurações da janela
pygame.display.set_caption('Jogo de física')
altura = 600
largura = 800
tela = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock()
# Loop principal do jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    tela.fill((255, 255, 255))
    pygame.display.update()
    clock.tick(60)

pygame.quit()