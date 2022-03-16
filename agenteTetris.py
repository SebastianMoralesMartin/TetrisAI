import pygame


class Event():
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key


counter = 0


def intersecta(game_field, x, y, game_width, game_height, game_figure_image):
    intersection = False
    for i in range(4):
        for j in range(4):
            if i * 4 + j in game_figure_image:
                if i + y > game_height - 1 or \
                        j + x > game_width - 1 or \
                        j + x < 0 or \
                        game_field[i + y][j + x] > 0:
                    intersection = True
    return intersection


def mejor_rotacion_posicion(game_field, game_figure, game_width, game_height):
    mejor_altura = game_height
    mejor_hoyo = game_height * game_width
    mejor_posicion = None
    mejor_rotacion = None

    for rotacion in range(len(game_figure.figures[game_figure.type])):
        fig = game_figure.figures[game_figure.type][rotacion]
        for j in range(-3, game_width):
            if not intersecta(
                    game_field,
                    j,
                    0,
                    game_width,
                    game_height,
                    fig):
                hoyos, height = simular(
                    game_field,
                    j,
                    0,
                    game_width,
                    game_height,
                    fig
                )
                if mejor_posicion is None or mejor_hoyo > hoyos or \
                        mejor_hoyo == hoyos and mejor_altura > height:
                    mejor_altura = height
                    mejor_hoyo = hoyos
                    mejor_posicion = j
                    mejor_rotacion = rotacion
    return mejor_rotacion, mejor_posicion


def ejecutar_Agente(game_field, game_figure, game_width, game_height):
    # Atrasa al agente para visualizar la ejecución.
    global counter
    counter += 1
    if counter < 3:
        return []
    counter = 0
    #--------------------------
    #Funcionalidad del Agente (diagrama de brooks)
    rotacion, posicion = mejor_rotacion_posicion(game_field, game_figure, game_width, game_height)
    if game_figure.rotation != rotacion:
        e = Event(pygame.KEYDOWN, pygame.K_UP)
    elif game_figure.x < posicion:
        e = Event(pygame.KEYDOWN, pygame.K_RIGHT)
    elif game_figure.x > posicion:
        e = Event(pygame.KEYDOWN, pygame.K_LEFT)
    else:
        e = Event(pygame.KEYDOWN, pygame.K_SPACE)
    return [e]


def simular(game_field, x, y, game_width, game_height, game_figure_image):
    while not intersecta(game_field, x, y, game_width, game_height, game_figure_image):
        y += 1
    y -= 1

    altura = game_height
    hoyos = 0
    llenos = []
    breaks = 0
    for i in range(game_height - 1, -1, -1):
        it_is_full = True
        hoyos_anteriores = hoyos
        for j in range(game_width):
            u = '_'
            if game_field[i][j] != 0:
                u = "x"
            for ii in range(4):
                for jj in range(4):
                    if ii * 4 + jj in game_figure_image:
                        if jj + x == j and ii + y == i:
                            u = "x"

            if u == "x" and i < altura:
                altura = i
            if u == "x":
                llenos.append((i, j))
                for k in range(i, game_height):
                    if (k, j) not in llenos:
                        hoyos += 1
                        llenos.append((k, j))
            else:
                it_is_full = False
        if it_is_full:
            breaks += 1
            hoyos = hoyos_anteriores

    return hoyos, game_height - altura - breaks
