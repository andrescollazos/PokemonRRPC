import pygame
import ConfigParser
import modonormal

# Constantes
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
tamPantalla = [527, 398]

# Convertir Letra a una Imagen:
def convertLI(letra):
    return "img/Batalla/"+letra+".png"

class Estado(object):
    # Pokemon -> Objeto Pokemon
    # posM -> Posicion del marco
    # posN -> Posicion del nombre
    # posL -> Posicion del nivel (level)
    # posB -> Posicion de la barra de vida
    def __init__(self, pokemon, posM, posN, posL, posB):
        # Marco
        self.marco = pygame.image.load("img/Batalla/estado_pokemon.png")
        self.marco_pos = posM
        # Datos del pokemon
        self.pokemon = pokemon
        # Nombre del pokemon:
        self.nombre = list('Bulbasaur'.upper()) #list(self.pokemon[0].upper())
        self.posi_nombre = posN
        for i in range(len(self.nombre)): # Convertir cadena en vector de imagenes:
            self.nombre[i] = [convertLI(self.nombre[i]), (self.posi_nombre[0]+i*10, self.posi_nombre[1])]
        # Nivel del pokemon:
        self.nivel = list(str(10)) # list(str(self.pokemon[1]))
        self.posi_nivel = posL
        for i in range(len(self.nivel)): # Convertir cadena en vector de imagenes:
            self.nivel[i] = [convertLI(self.nivel[i]), (self.posi_nivel[0]+i*6, self.posi_nivel[1])]

        # Barra de salud
        self.ps_barra = pygame.image.load("img/Batalla/ps_barra.png")
        self.ps_vacio = pygame.image.load("img/Batalla/ps_vacio.png")
        self.status = []
        for i in range(10): # La barra se divide en 10 secciones:
            self.status.append([self.ps_barra, (posB[0]+i*9, posB[1])])
    # Mostrar por pantalla el marco y la barra de vida:
    def mostrar(self, pantalla):
        pantalla.blit(self.marco, self.marco_pos)
        for barrita in self.status:
            pantalla.blit(barrita[0], barrita[1])
        for letra in self.nombre:
            img = pygame.image.load(letra[0])
            pantalla.blit(img, letra[1])
        for numero in self.nivel:
            img = pygame.image.load(numero[0])
            pantalla.blit(img, numero[1])

    def calc_ps(self):
        vida = 10 #self.pokemon[4]
        limvida = 20 #self.pokemon[5]
        porcion = limvida/10.0
        for i in range(len(self.status)):
            if vida > porcion*(i):
                self.status[i][0] = self.ps_barra
            else:
                self.status[i][0] = self.ps_vacio


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
    # Estado del pokemon del jugador:
    estado = Estado(True, (315, 187), (350, 202), (500, 202), (412, 221))
    # Estado del pokemo enemigo:
    estadoEnemigo = Estado(True, (5, 6), (42, 21), (189, 21), (102, 40))
    # Cursor del menu:
    cursor = Cursor()

    # INTRO BATALLA: JUGADOR LANZANDO POKEBOLA:
    # Recorrido semi parabolico de la pokebola:
    recorrido_pokeball = [(190, 70), (240, 50), (290, 70), (340, 90), (390, 110)]
    # Mostrar al jugador en perspectiva
    intro = pygame.image.load("img/Batalla/intro_red0.png")
    pantalla.blit(intro, (0, 71))
    pantalla.blit(marco, (0, 0))    # Mostrar Marco
    estado.mostrar(pantalla)        # Mostrar estado Jugador
    estadoEnemigo.mostrar(pantalla) # Mostrar estado Enemigo
    cursor.mostrar(pantalla)        # Mostrar cursor
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
        estado.mostrar(pantalla)
        estadoEnemigo.mostrar(pantalla)
        cursor.mostrar(pantalla)
        pygame.display.flip()

    estado.calc_ps()
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
        estado.mostrar(pantalla)
        estadoEnemigo.mostrar(pantalla)
        pygame.display.flip()

#n = EstadoPokemon(True)
main(True, True, True, False)
