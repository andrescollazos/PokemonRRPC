import pygame
import ConfigParser
import modonormal

# Constantes
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
tamPantalla = [527, 398]

class EstadoPokemon(object):
    def __init__(self):
        pass

class EstadoEnemigo(object):
    def __init__(self):
        pass

class Cursor(object):
    def __init__(self):
        self.image = pygame.image.load("img/Batalla/cursor.png")
        # Dominio de posiciones validas en las que puede estar el cursor
        self.posicion_validas = {}
        self.posicion_validas["Capturar"] = (388, 304)
        self.posicion_validas["Huir"] = (440, 345)
        self.posicion_validas["Lucha"] = (308, 304)
        self.posicion_validas["Pokemon"] = (308, 345)
        self.posicion_validas["Placaje"] = (10, 302)
        self.posicion = self.posicion_validas["Lucha"] # Posicion inicial (actual)

    def cambiar_pos(self, item):
        try:
            self.posicion = self.posicion_validas[item]
        except KeyError:
            pass
    def mostrar(self, pantalla):
        pantalla.blit(self.image, self.posicion)

# Funcion principal:
# Jugador -> recibe los parametros del jugador: posicion, pokemones.
# matrizPokemon -> Todos los pokemones con sus respectivos sprites
# tipo_combate -> 0: Pokemon salvaje, 1: Entrenador Pokemon
# terminar -> Indica si se termino o no el juego
def main(jugador, matrizPokemon, tipo_combate, terminar):
    # Parametros iniciales:
    pygame.init()
    pantalla = pygame.display.set_mode(tamPantalla)
    pantalla.fill(NEGRO)
    reloj = pygame.time.Clock()

    # Marco del duelo:
    marco = pygame.image.load("img/Batalla/marco_batalla.png")
    # Cursor del menu:
    cursor = Cursor()

    # INTRO BATALLA: JUGADOR LANZANDO POKEBOLA:
    # Recorrido semi parabolico de la pokebola:
    recorrido_pokeball = [(190, 70), (240, 50), (290, 70), (340, 90), (390, 110)]
    # Mostrar al jugador en perspectiva
    intro = pygame.image.load("img/Batalla/intro_red0.png")
    pantalla.blit(intro, (0, 71))
    pantalla.blit(marco, (0, 0))# Mostrar Marco
    cursor.mostrar(pantalla)    # Mostrar cursor
    pygame.display.flip()
    reloj.tick(4) # Esperar para iniciar la animacion
    for i in range(8):
        if not(i >= 5):
            # Despues de terminar la animacion, se queda esperando en la ultilma
            # posicion, mientras la pokebola termian su recorrido
            intro = pygame.image.load("img/Batalla/intro_red"+str(i)+".png")
        else:
            intro = pygame.image.load("img/Batalla/intro_red4.png")
        pantalla.blit(intro, (0, 71))
        if i >= 3: # La pokebola, empieza su animacion cuando el jugador extiende el brazo
            pokeball = pygame.image.load("img/Batalla/pokeball.png")
            pantalla.blit(pokeball, recorrido_pokeball[i-3])

        pygame.display.flip()
        reloj.tick(10)
        # Resetear pantalla
        pantalla.fill(NEGRO)
        pantalla.blit(marco, (0, 0))
        cursor.mostrar(pantalla)
        pygame.display.flip()


    # Ciclo del juego
    reloj = pygame.time.Clock()
    while not terminar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar = True
            if event.type == pygame.KEYDOWN:
                # Desplazarse por las opciones
                if event.key == pygame.K_UP:
                    if cursor.posicion == cursor.posicion_validas["Pokemon"]:
                        cursor.posicion = cursor.posicion_validas["Lucha"]
                    elif cursor.posicion == cursor.posicion_validas["Huir"]:
                        cursor.posicion = cursor.posicion_validas["Capturar"]
                if event.key == pygame.K_DOWN:
                    if cursor.posicion == cursor.posicion_validas["Lucha"]:
                        cursor.posicion = cursor.posicion_validas["Pokemon"]
                    elif cursor.posicion == cursor.posicion_validas["Capturar"]:
                        cursor.posicion = cursor.posicion_validas["Huir"]
                if event.key == pygame.K_LEFT:
                    if cursor.posicion == cursor.posicion_validas["Capturar"]:
                        cursor.posicion = cursor.posicion_validas["Lucha"]
                    elif cursor.posicion == cursor.posicion_validas["Huir"]:
                        cursor.posicion = cursor.posicion_validas["Pokemon"]
                if event.key == pygame.K_RIGHT:
                    if cursor.posicion == cursor.posicion_validas["Lucha"]:
                        cursor.posicion = cursor.posicion_validas["Capturar"]
                    elif cursor.posicion == cursor.posicion_validas["Pokemon"]:
                        cursor.posicion = cursor.posicion_validas["Huir"]
                if event.key == pygame.K_a:
                    # Entrar a las opciones de Lucha
                    if cursor.posicion == cursor.posicion_validas["Lucha"]:
                        cursor.posicion = cursor.posicion_validas["Placaje"]
                    elif cursor.posicion == cursor.posicion_validas["Capturar"]:
                        # TIRAR POKEBOLA  TIRAR POKEBOLA  TIRAR POKEBOLA
                        pass
                    elif cursor.posicion == cursor.posicion_validas["Pokemon"]:
                        # ENTRAR EN MENU POKEMON  ENTRAR EN MENU POKEMON
                        pass
                    elif cursor.posicion == cursor.posicion_validas["Huir"]:
                        # HUIR HUIR HUIR HUIR HUIR HUIR HUIR HUIR HUIR HUIR
                        pass
                    elif cursor.posicion == cursor.posicion_validas["Placaje"]:
                        # ATACAR ATACAR  ATACAR  ATACAR  ATACAR  ATACAR  ATACAR"
                        pass
                if event.key == pygame.K_b:
                    if cursor.posicion == cursor.posicion_validas["Placaje"]:
                        cursor.posicion = cursor.posicion_validas["Lucha"]

        pantalla.blit(marco, (0, 0))
        cursor.mostrar(pantalla)
        pygame.display.flip()


main(True, True, True, False)
