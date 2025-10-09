import classes as cl

def main():
    
    '''
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
velocidade = 200

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "red", player_pos, 10)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= velocidade * dt
    if keys[pygame.K_s]:
        player_pos.y += velocidade * dt
    if keys[pygame.K_a]:
        player_pos.x -= velocidade * dt
    if keys[pygame.K_d]:
        player_pos.x += velocidade * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
'''
    
    '''
    #TESTE 1
    mapa1 = {
    "A": "NOTA LÁ",
    "B": "NOTA DÓ",
    "C": "NOTA FÁ",
    " ": "TESTE"
    }


    texto1 = cl.LeitorTexto("A B0C ABA0BA CB0A B0ACBA")

    transformada = cl.TransformaMusica(texto1.lista_caracteres, mapa1)

    transformada.converteCaracteres()

    print(transformada.lista_saida)
    '''

    '''
    #TESTE 2
    mapa = cl.MapaCaracteres(['A', 'B', 'C', 'D'], ['NOTA DO', 'NOTA RE', 'NOTA MI', 'NOTA FA'])
    mapa.mostraMapa()
    print("")


    mapa.adicionaCaractere('E', 'NOTA SOL')
    mapa.mostraMapa()
    print("")

    mapa.excluiCaractere('B')
    mapa.mostraMapa()
    print("")

    mapa.excluiCaractere('Z')
    mapa.mostraMapa()
    print("")
    '''

    



if __name__ == "__main__":
    main()