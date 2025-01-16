import pygame
import numpy as np

# Clase principal del juego
class Game(object):

    def __init__(self, ancho_juego, alto_juego):
        # Inicializa la ventana del juego
        pygame.display.set_caption('Snake')
        self.ancho_juego = ancho_juego
        self.alto_juego = alto_juego
        self.display_juego = pygame.display.set_mode((ancho_juego, alto_juego + 100))  # +100 para mostrar el puntaje
        self.fondo = pygame.image.load('img/fondo.png')  # Carga el fondo del juego
        self.colision = False  # Indica si ha ocurrido una colisión
        self.score = 0  # Puntaje inicial
        self.font = pygame.font.SysFont('Ubuntu', 20)  # Fuente para mostrar el puntaje

    def display_ui(self, record):
        # Actualiza la interfaz del usuario (UI)
        self.display_juego.fill((255, 255, 255))  # Rellena el fondo de blanco
        score_txt = self.font.render('PUNTAJE: ', True, (0, 0, 0))
        score_num = self.font.render(str(self.score), True, (0, 0, 0))
        record_txt = self.font.render('MEJOR: ', True, (0, 0, 0))
        record_num = self.font.render(str(record), True, (0, 0, 0))

        pygame.draw.rect(self.display_juego, (156, 204, 101), (0, self.alto_juego, self.alto_juego, 100))  # Rectángulo gris para la UI

        self.display_juego.blit(score_txt, (45, 480))
        self.display_juego.blit(score_num, (170, 480))
        self.display_juego.blit(record_txt, (270, 480))
        self.display_juego.blit(record_num, (350, 480))
        self.display_juego.blit(self.fondo, (0, 0))  # Dibuja el fondo del juego

    def obtener_record(self, score, record):
        # Devuelve el puntaje más alto entre el actual y el record anterior
        return score if score >= record else record

# Clase del jugador (serpiente)
class Player(object):

    def __init__(self):
        self.x = 100  # Posición inicial en x
        self.y = 100  # Posición inicial en y
        self.posicion = []  # Lista de segmentos de la serpiente
        self.posicion.append([self.x, self.y])  # Añade la posición inicial
        self.n_manzanas = 1  # Número inicial de segmentos de la serpiente
        self.comida = False  # Indica si la serpiente ha comido
        self.imagen = pygame.image.load('img/cuerpo_serpiente.png')  # Carga la imagen del segmento de la serpiente
        self.cambio_x = 20  # Cambio en x (velocidad)
        self.cambio_y = 0  # Cambio en y (velocidad)
        self.direccion = [1, 0]  # Dirección inicial (derecha)

    def refrescar_posicion(self, x, y):
        # Actualiza la posición de la serpiente
        if self.posicion[-1][0] != x or self.posicion[-1][1] != y:
            if self.n_manzanas > 1:
                for i in range(self.n_manzanas - 1):
                    self.posicion[i][0], self.posicion[i][1] = self.posicion[i + 1]

            self.posicion[-1][0] = x
            self.posicion[-1][1] = y

    def hacer_movimiento(self, x, y, game, food):
        # Maneja el movimiento de la serpiente
        array_m = [self.cambio_x, self.cambio_y]

        # Si la serpiente ha comido, añade un segmento
        if self.comida:
            self.posicion.append([self.x, self.y])
            self.comida = False
            self.n_manzanas += 1

        # Maneja los eventos de teclado
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT and self.direccion != [1, 0]:
                    array_m = [-20, 0]
                    self.direccion = [-1, 0]
                elif e.key == pygame.K_RIGHT and self.direccion != [-1, 0]:
                    array_m = [20, 0]
                    self.direccion = [1, 0]
                elif e.key == pygame.K_UP and self.direccion != [0, -1]:
                    array_m = [0, -20]
                    self.direccion = [0, 1]
                elif e.key == pygame.K_DOWN and self.direccion != [0, 1]:
                    array_m = [0, 20]
                    self.direccion = [0, -1]

        # Actualiza la posición de la serpiente
        self.cambio_x, self.cambio_y = array_m
        self.x = x + self.cambio_x
        self.y = y + self.cambio_y

        # Verifica si hay colisión con los bordes o con sí misma
        if self.x < 0 or self.x > game.ancho_juego - 20 \
                or self.y < 0 or self.y > game.alto_juego - 20 \
                or [self.x, self.y] in self.posicion:
            game.colision = True

        # Verifica si ha comido la comida
        food.comer(self, game)
        self.refrescar_posicion(self.x, self.y)

    def display_jugador(self, x, y, game):
        # Dibuja la serpiente en la pantalla
        self.posicion[-1][0] = x
        self.posicion[-1][1] = y

        if not game.colision:
            for i in range(self.n_manzanas):
                x_temp, y_temp = self.posicion[len(self.posicion) - 1 - i]
                game.display_juego.blit(self.imagen, (x_temp, y_temp))

# Clase de la comida
class Food(object):

    def __init__(self):
        self.x_food = 200  # Posición inicial en x
        self.y_food = 200  # Posición inicial en y
        self.imagen = pygame.image.load('img/comida.png')  # Carga la imagen de la comida

    def comida_coor(self, game, player):
        # Genera nuevas coordenadas para la comida
        x_rand = np.random.choice(list(range(0, game.ancho_juego, 20)))
        self.x_food = x_rand
        y_rand = np.random.choice(list(range(0, game.alto_juego, 20)))
        self.y_food = y_rand

    def display_comida(self, x, y, game):
        # Dibuja la comida en la pantalla
        game.display_juego.blit(self.imagen, (x, y))

    def comer(self, player, game):
        # Verifica si la serpiente ha comido la comida
        if player.x == self.x_food and player.y == self.y_food:
            self.comida_coor(game, player)
            player.comida = True
            game.score += 1  # Incrementa el puntaje

def run():
    # Función principal para ejecutar el juego
    pygame.init()
    record = 0  # Record inicial
    clock = pygame.time.Clock()
    while True:
        game = Game(420, 420)  # Inicializa el juego con dimensiones 420x420
        player = Player()  # Inicializa el jugador (serpiente)
        food = Food()  # Inicializa la comida

        game.display_ui(record)  # Muestra la UI inicial
        player.display_jugador(player.x, player.y, game)  # Dibuja la serpiente
        food.display_comida(food.x_food, food.y_food, game)  # Dibuja la comida
        pygame.display.update()

        while not game.colision:
            player.hacer_movimiento(player.x, player.y, game, food)  # Mueve la serpiente
            record = game.obtener_record(game.score, record)  # Actualiza el record si es necesario
            game.display_ui(record)  # Actualiza la UI
            player.display_jugador(player.x, player.y, game)  # Dibuja la serpiente
            food.display_comida(food.x_food, food.y_food, game)  # Dibuja la comida
            pygame.display.update()
            clock.tick(10)  # Controla la velocidad del juego

if __name__ == '__main__':
    run()  # Ejecuta el juego

