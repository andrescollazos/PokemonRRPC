# coding=utf-8
import pygame
import ConfigParser
import modonormal
import random

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
        self.nombre = list(self.pokemon[0].upper())
        self.posi_nombre = posN
        for i in range(len(self.nombre)): # Convertir cadena en vector de imagenes:
            self.nombre[i] = [convertLI(self.nombre[i]), (self.posi_nombre[0]+i*10, self.posi_nombre[1])]
        # Nivel del pokemon:
        self.nivel = list(str(self.pokemon[1]))
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
        vida = self.pokemon[5]
        limvida = self.pokemon[6]
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

class Pokemon(object):
    def __init__(self, pokemones, sentido=True):
        self.pokemones = pokemones # Matriz de Pokemones
        self.pokemon = pokemones[0] # Pokemon inicial
        self.contPok = 0 # Contador Pokemon
        image_ancho, imagen_alto = self.pokemon[7].get_size()
        # Imagen frontal
        self.imageF = pygame.transform.scale(self.pokemon[7], (image_ancho*2, imagen_alto*2))
        self.posF = (319, 36)
        # Imagen Trasera
        self.imageP =  pygame.transform.scale(self.pokemon[8], (image_ancho*2, imagen_alto*2))
        self.posP = (76, 133)
        self.sentido = sentido
        if self.sentido:
            self.image = self.imageP
            self.pos = self.posP
        else:
            self.image = self.imageF
            self.pos = self.posF
        self.terminar_duelo = False

    def mostrar(self, pantalla):
        pantalla.blit(self.image, self.pos)

    def cambiar_Pokemon(self):
        image_ancho, imagen_alto = self.pokemon[7].get_size()
        # Imagen frontal
        self.imageF = pygame.transform.scale(self.pokemon[7], (image_ancho*2, imagen_alto*2))
        # Imagen Trasera
        self.imageP =  pygame.transform.scale(self.pokemon[8], (image_ancho*2, imagen_alto*2))
        if self.sentido:
            self.image = self.imageP
        else:
            self.image = self.imageF

    def subir_nivel(self):
        # Calcular nivel en función de la experiencia:
        n = ((self.pokemon[3]*5.0)/4)**(1.0/3)
        print int(n)

    # D = 0.01*E*V*(((0.2*N + 1)*P)/25 + 2)
    # E -> Efectividad: {1, 2, 4}
    # V -> Variacion: Valores discretos: 85-100
    # N -> Nivel del pokemon atacante
    # P -> Poder del ataque (Placaje) (35)
    def atacar(self, enemigo, tipo_combate = 0):#, pantalla):
        e = [0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 4]# Dominio de efectividad
        # Variables para el calculo del daño
        E = e[random.randrange(0, 10)]      # Efectividad del ataque
        V = random.randrange(85, 101)       # Variacion del daño
        P = 50                              # Potencia del Placaje
        N = self.pokemon[1]                 # Nivel del pokemon atacante
        # DAÑO CAUSADO AL OPONENTE:
        D = 0.01*E*V*(2 + ((0.2*N + 1)*P)/25)
        enemigo.pokemon[5] -= D

        # Calcular Experiencia ganada (Cuando el pokemon enemigo es derrotado)
        # EXP = (E*L*C)/7
        # E -> Experiencia Base del rival
        # L -> Nivel del oponente
        # C -> Tipo de combate: {1: Pokemon salvaje, 1.5: Entrenador}
        if enemigo.pokemon[5] <= 0:
            if not(tipo_combate):
                C = 1 # Pokemon Salvaje
            else:
                C = 1.5 # Entrenador Pokemon
            exp = (enemigo.pokemon[3]*enemigo.pokemon[1]*C)/7
            self.pokemon[3] += exp # Subir experiencia
            self.subir_nivel() # Verificar si aumenta de nivel

            # Si el contador pokemon es igual a la longitud de los pokemones
            # enemigos, quiere decir que fue completamente derrotado
            if enemigo.contPok == len(enemigo.pokemones) - 1:
                self.terminar_duelo = True
            # Enemigo cambia de pokemon
            if len(enemigo.pokemones) > 1 and not(self.terminar_duelo):
                enemigo.contPok += 1
                enemigo.pokemon = enemigo.pokemones[enemigo.contPok]
                enemigo.cambiar_Pokemon()

# Funcion principal:
# Jugador -> recibe los parametros del jugador: posicion, pokemones.
# Enemigo -> recibe la lista de los pokemones enemigos
# tipo_combate -> 0: Pokemon salvaje, 1: Entrenador Pokemon
# terminar -> Indica si se termino o no el juego
def main(jugador, enemigo, tipo_combate, terminar, matrizPokemon):
    # Parametros iniciales:
    pygame.init()
    pantalla = pygame.display.set_mode(tamPantalla)
    pantalla.fill(NEGRO)
    reloj = pygame.time.Clock()
    turno_enemigo = False

    # Marco del duelo:
    marco = pygame.image.load("img/Batalla/marco_batalla.png")
    # Estado del pokemon del jugador:
    pokemon_jug = Pokemon(jugador.pokemones) # Pokemon Actual (Default)
    estado = Estado(pokemon_jug.pokemon, (315, 187), (350, 202), (500, 202), (412, 221))
    # Estado del pokemo enemigo:
    pokemon_ene = Pokemon(enemigo, False) # Pokemon Actual del enemigo
    estadoEnemigo = Estado(pokemon_ene.pokemon, (5, 6), (42, 21), (189, 21), (102, 40))
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
                        if tipo_combate == 0: # Contra pokemon salvaje:
                            # Animacion: Red tirando pokebola
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
                                pokemon_ene.mostrar(pantalla)
                                pygame.display.flip()
                            # Calcular Variable, que permite saber si un pokemon es capturado o no
                            # A = ((3*Psmax - 2*Psact)*Rc)/(3*Psmax)
                            # Psmax -> Puntos de vida maximos de un pokemon
                            # Psact -> Puntos de vida actuales
                            # Rc -> Ratio de Captura del pokemon
                            psmax = pokemon_ene.pokemon[6]
                            psact = pokemon_ene.pokemon[5]
                            rc = pokemon_ene.pokemon[4]
                            A = ((3*psmax -2*psact)*rc)/(3*psmax)
                            if random.randrange(0, 256) <= A:
                                # Pokemon Capturado:
                                jugador.pokemones.append(pokemon_ene.pokemon)
                                aviso = pygame.image.load("img/avisos/pokemon_capturado.png")
                                pantalla.blit(aviso, (0, 0))
                                pygame.display.flip()
                                reloj.tick(0.7)
                                terminar = True
                                print "POKEMONES: "
                                for pokemon in jugador.pokemones:
                                    print "Nombre: {0}  Vida: {1}  Exp:{2}".format(pokemon[0], pokemon[5], pokemon[3])
                                modonormal.main(jugador.city.filename, not(terminar), matrizPokemon, jugador, (jugador.city.iniciox, jugador.city.inicioy))
                                break
                            else:
                                # Pokemon NO capturado:
                                aviso = pygame.image.load("img/avisos/pokemon_no_capturado.png")
                                pantalla.blit(aviso, (0, 0))
                                pygame.display.flip()
                                reloj.tick(0.7)
                                turno_enemigo = True

                        # TIRAR POKEBOLA  TIRAR POKEBOLA  TIRAR POKEBOLA
                        #pass
                    elif cursor.posicion == cursor.posicion_validas["Pokemon"]:
                        # ENTRAR EN MENU POKEMON  ENTRAR EN MENU POKEMON
                        pass
                    elif cursor.posicion == cursor.posicion_validas["Huir"]:
                        terminar = True
                        # Mostrar aviso de huida:
                        aviso = pygame.image.load("img/avisos/huir.png")
                        pantalla.fill(NEGRO)
                        pantalla.blit(aviso, (0,0))
                        pygame.display.flip()
                        reloj.tick(0.8)
                        modonormal.main(jugador.city.filename, not(terminar), matrizPokemon, jugador, (jugador.city.iniciox, jugador.city.inicioy))
                        break
                    elif cursor.posicion == cursor.posicion_validas["Placaje"]:
                        pokemon_jug.atacar(pokemon_ene) # Atacar Pokemon Enemigo
                        estadoEnemigo.pokemon = pokemon_ene.pokemon # En caso de cambiar de pokemon
                        estadoEnemigo.calc_ps() # Calcular Ps del enemigo
                        # Saber si el pokemon del jugador gano el duelo:
                        if pokemon_jug.terminar_duelo:
                            print "GANAS EL DUELO!"
                            #print "TU VIDA: {0} ENEMIGO: {1}".format(pokemon_jug.pokemon[5], pokemon_ene.pokemon[5])
                            terminar = True
                            modonormal.main(jugador.city.filename, not(terminar), matrizPokemon, jugador, (jugador.city.iniciox, jugador.city.inicioy))
                            break
                        turno_enemigo = True
                if event.key == pygame.K_b:
                    if cursor.posicion == cursor.posicion_validas["Placaje"]:
                        cursor.posicion = cursor.posicion_validas["Lucha"]

        pantalla.blit(marco, (0, 0))
        cursor.mostrar(pantalla)
        estado.mostrar(pantalla)
        estadoEnemigo.mostrar(pantalla)
        pokemon_jug.mostrar(pantalla)
        pokemon_ene.mostrar(pantalla)
        pygame.display.flip()

        # TURNO DEL POKEMON ENEMIGO:
        if turno_enemigo:
            reloj.tick(0.45) # Esperar
            reloj.tick(1)
            pokemon_ene.atacar(pokemon_jug)
            estado.calc_ps()
            turno_enemigo = False
            if pokemon_ene.terminar_duelo:
                print "PERDISTE LOCA"
                print "TU VIDA: {0} ENEMIGO: {1}".format(pokemon_jug.pokemon[5], pokemon_ene.pokemon[5])
                terminar = True

#n = EstadoPokemon(True)
#main(True, True, True, False)
