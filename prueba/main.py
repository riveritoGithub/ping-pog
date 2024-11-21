import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir los colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Definir el tamaño de la ventana
ANCHO = 800
ALTO = 600

# Crear la ventana del juego
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pong")

# Clase que representa la paleta (paddle)
class Paleta(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 100))  # Tamaño de la paleta
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 10  # Velocidad de movimiento de la paleta

    def mover(self, direccion):
        if direccion == "arriba" and self.rect.top > 0:
            self.rect.y -= self.velocidad
        elif direccion == "abajo" and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad

# Clase que representa la pelota
class Pelota(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))  # Tamaño de la pelota
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO // 2)
        self.vel_x = 5  # Velocidad horizontal de la pelota
        self.vel_y = 5  # Velocidad vertical de la pelota

    def mover(self, p1, p2):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Rebote en las paredes superior e inferior
        if self.rect.top <= 0 or self.rect.bottom >= ALTO:
            self.vel_y = -self.vel_y

        # Rebote en las paletas
        if self.rect.colliderect(p1.rect) or self.rect.colliderect(p2.rect):
            self.vel_x = -self.vel_x

# Función principal del juego
def main():
    # Crear los objetos del juego
    p1 = Paleta(30, ALTO // 2 - 50)
    p2 = Paleta(ANCHO - 40, ALTO // 2 - 50)
    pelota = Pelota()

    # Crear un grupo de sprites para actualizar
    todos_sprites = pygame.sprite.Group()
    todos_sprites.add(p1, p2, pelota)

    # Controlar la velocidad de los fotogramas
    reloj = pygame.time.Clock()

    # Bucle principal del juego
    while True:
        # Manejar los eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Obtener las teclas presionadas
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]:
            p1.mover("arriba")
        if teclas[pygame.K_s]:
            p1.mover("abajo")
        if teclas[pygame.K_UP]:
            p2.mover("arriba")
        if teclas[pygame.K_DOWN]:
            p2.mover("abajo")

        # Mover la pelota, pasamos las palas como parámetros
        pelota.mover(p1, p2)

        # Verificar si la pelota ha salido de la pantalla (anotación)
        if pelota.rect.left <= 0 or pelota.rect.right >= ANCHO:
            pelota.rect.center = (ANCHO // 2, ALTO // 2)  # Resetear la pelota al centro
            pelota.vel_x = -pelota.vel_x  # Cambiar la dirección de la pelota

        # Dibujar en pantalla
        pantalla.fill(NEGRO)
        todos_sprites.draw(pantalla)

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar la velocidad del juego
        reloj.tick(30)  # 30 FPS

if __name__ == "__main__":
    main()
