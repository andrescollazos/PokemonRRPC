# coding=utf-8

import pygame
import ConfigParser
import math
import random
#import Batalla

# Constantes
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
tamCuadro = 32 # Tamaño de cada cuadro
tamPantalla = [527, 398]
tamJugador = 48

class Mapa(object):
	def __init__(self, filename):#, jugador):
		# Elementos propios del mapa:
		self.map = [] # Matriz que contiene el mapa
		self.key = {}
		self.parser = ConfigParser.ConfigParser()
		self.parser.read(filename)
        # Cargar mapa codifiado:
		self.map = self.parser.get("level", "map").split("\n")
		#for section in self.parser.sections():
		#	if len(section) == 1:
		#		desc = dict(self.parser.items(section))
		#		self.key[section] = desc
		self.width = len(self.map[0])
		self.height = len(self.map)
		#-----------------------------------------------------------------------
		# Imagen del mapa:
		self.tileset = self.parser.get("level", "tileset")
		self.image = pygame.image.load(self.tileset)#.convert_alpha()
		# Obtener dimensiones del mapa
		imagen_ancho, imagen_alto = self.image.get_size()
		self.matrizMap = [] # Matriz que relaciona el mapa con la imagen
		self.scale = int(self.parser.get("level", "scale")) # Saber el tamanyo de cada elemento
		# Escalar la imagen:
		self.image = pygame.transform.scale(self.image, (imagen_ancho*self.scale, imagen_alto*self.scale))
		imagen_ancho, imagen_alto = self.image.get_size()
		ancho = tamCuadro/self.scale
		alto = tamCuadro/self.scale
		for fondo_x in range(0, imagen_ancho/ancho):
			linea = []
			self.matrizMap.append(linea)
			for fondo_y in range(0, imagen_alto/alto):
				cuadro = (fondo_x*ancho, fondo_y*alto, ancho, alto)
				linea.append(self.image.subsurface(cuadro))
		# Inicio: Donde se ubica el juador al entrar en el mapa:
		self.iniciox = int(self.parser.get("level", "iniciox"))
		self.inicioy = int(self.parser.get("level", "inicioy"))
		# Velocidad de la pantalla:
		self.velocidad = int(self.parser.get("level", "velocidad"))

	# Funcion que permite buscar una letra en la matriz del mapa:
	def buscarL(self, letra):
		cont, pos = 0, [False, False]
		for lst in self.map:
			try:
				pos[0] = lst.index(letra)
				break
			except ValueError:
				cont += 1
		pos[1] = cont
		return pos

	# Reemplazar un elemento por otro en la matriz del mapa:
	def reemplazarElem(self, letra, pos, letrai='.'):
		pos_vieja = self.buscarL(letra)
		# Se crea variable temporal para poder modificar la cadena (fila de la matriz)
		tempLst = self.map[pos_vieja[1]]
		tempLst = list(tempLst) # Se convierte la cadena en lista
		tempLst[pos_vieja[0]] = letrai # Se modifica elemento de la lista
		tempLst = ''.join(tempLst) # Se convierte la lista a cadena
		self.map[pos_vieja[1]] = tempLst # Y se asigna la cadena a su respectiva fila

		# Se crea variable temporal para poder modificar la cadena (fila de la matriz)
		tempLst = self.map[pos[0]]
		tempLst = list(tempLst) # Se convierte la cadena en lista
		tempLst[pos[1]] = letra # Se modifica elemento de la lista
		tempLst = ''.join(tempLst) # Se convierte la lista a cadena
		self.map[pos[0]] = tempLst # Y se asigna la cadena a su respectiva fila

		# Se modifica el mapa:
		self.parser.set("level", "map", self.map)

class Jugador(object):
	def __init__(self, imagen):
		self.image = pygame.image.load(imagen).convert_alpha()
		self.rect = self.image.get_rect()
		self.image = pygame.transform.scale(self.image, (tamJugador*3, tamJugador*4))
		imagen_ancho, imagen_alto = self.image.get_size()
		self.matrizJugador = [] # MATRIZ QUE CONTIENE LOS SPRITES DEL JUGADOR
		#self.matrizMap = [] # MATRIZ DEL MAPA, PARA EVITAR QUE CRUCE ELEMENTOS
		for x in range(0, 3): # Se requieren tres acciones para un movimiento
			linea = []
			self.matrizJugador.append(linea)
			for y in range(0, 4): # Son cuatro las perspectivas del jugador
				cuadro = (x*tamJugador, y*tamJugador, tamJugador, tamJugador)
				linea.append(self.image.subsurface(cuadro))
		self.pos = [False, False]
		self.sprite = self.matrizJugador[1][0]
		self.pokemones = []
		self.seleccionar_pokemon = True # Seleccionar primer pokemon
		self.aviso_sin_pokemon = False # Por si el jugador intenta salir del pueblo sin pokemon

	# UBICAR JUGADOR EN LA PANTALLA:
	def ubicar(self, city):
		pos = city.buscarL('I')
		# Calcular la posición del jugador en la pantalla:
		pos[0] = (pos[0]*city.scale - city.iniciox)*(32/city.scale)
		pos[1] = (pos[1]*city.scale - city.inicioy)*(32/city.scale) - (tamJugador-32)
		self.pos = pos

	# MOSTRAR EN PANTALLA EL JUGADOR
	def dibujar(self, pantalla):
		pantalla.blit(self.sprite, self.pos)

	# SABER SI HAY UN MURO O ALGUN OBJETO QUE NO PERMITA CAMINAR AL JUGADOR:
	# retorna vector de booleanos -> [Up, Down, Left, Rigth]
	def is_a_wall(self, city, direc):
		# Transformar posicion de la pantalla, en posicion de la matriz del mapa
		posx = (((self.pos[0]*city.scale)/32) + city.iniciox)/city.scale
		posy = ((((self.pos[1] + (tamJugador-32))*city.scale)/32) + city.inicioy)/city.scale
		# Izquierda y derecha:
		try:
			if (city.map[posy][posx - 1] == "#" or city.map[posy][posx - 1] == "A" or city.map[posy][posx - 1] == "c" or city.map[posy][posx - 1] == "W") and direc == "left":
				return [False, False, True, False]
		except IndexError:
			pass
		try:
			if (city.map[posy][posx + 1] == "#" or city.map[posy][posx + 1] == "A" or city.map[posy][posx + 1] == "c" or city.map[posy][posx + 1] == "W") and direc == "rigth":
				return [False, False, False, True]
		except IndexError:
			pass
		try:
			if (city.map[posy - 1][posx] == "#" or city.map[posy - 1][posx] == "A" or city.map[posy - 1][posx] == "c" or city.map[posy - 1][posx] == "W") and direc == "up":
				return [True, False, False, False]
		except IndexError:
			pass
		try:
			if (city.map[posy + 1][posx] == "#" or city.map[posy + 1][posx] == "A" or city.map[posy + 1][posx] == "c" or city.map[posy + 1][posx] == "W") and direc == "down":
				return [False, True, False, False]
		except IndexError:
			pass
		return [False, False, False, False]

	def transfM(self, city):
		posx = (((self.pos[0]*city.scale)/32) + city.iniciox)/city.scale
		posy = ((((self.pos[1] + (tamJugador-32))*city.scale)/32) + city.inicioy)/city.scale
		return posx, posy

class Enemigo(object):
	def __init__(self, imagen):
		self.image = pygame.image.load(imagen)
		self.rect = self.image.get_rect()
		self.image = pygame.transform.scale(self.image, (tamJugador, tamJugador))
		self.pokemones = []
		self.dialogo = False

# MAIN
#if __name__=='__main__':
def main(filename, terminar, matrizPokemon, posicion = False):
	# Parametros iniciales:
	pygame.init()
	pantalla = pygame.display.set_mode(tamPantalla)
	pantalla.fill(NEGRO)
	accion = False # Boton de false
	# Mapas iniciales:
	centropokemon = Mapa("maps/centropokemon.map")
	ciudadverde = Mapa("maps/ciudadverde.map")
	gimnasio = Mapa("maps/gimnasio.map")
	interior = Mapa("maps/interior.map")
	laboratorio = Mapa("maps/lab.map")
	pueblopaleta = Mapa("maps/pueblopaleta.map")
	ruta1 = Mapa("maps/ruta1.map")
	tienda = Mapa("maps/tienda.map")
	# Ciudad verde es una variable que contiene el mapa actual
	ciudadVerde = Mapa(filename)
	if posicion:
		ciudadVerde.iniciox = posicion[0]
		ciudadVerde.inicioy = posicion[1]
	# JUGADOR:
	jugador = Jugador("red.png")
	jugador.ubicar(ciudadVerde) # Posicionar al jugador:

	# ENEMIGOS
	# Matriz de pokemones de Blue
	blue = Enemigo("img/enemigos/Blue.png")
	blue.pokemones = [matrizPokemon[15]] # Pidgey
	blue.pokemones[0][1] = 5 # El pokemon de Blue es nivel 5
	# Matriz de pokemones de Brock
	Brock = Enemigo("img/enemigos/brock.png")
	Brock.pokemones = [matrizPokemon[73], matrizPokemon[94]]
	Brock.pokemones[0][1] = 14 # Geodude nivel 14
	Brock.pokemones[1][1] = 20 # Onix nivel 20

	# PROFESOR OAK (NPC's)
	oak_conversacion = True # Booleano que informa si se ha hablado con OAk

	# x, y -> Cantidad de ciclos para pintar el mapa a realizar:
	x, y = (tamPantalla[0]*ciudadVerde.scale)/tamCuadro, (tamPantalla[1]*ciudadVerde.scale)/tamCuadro
	left = rigth = up = down = False # Booleanos para saber si el jugador se mueve
	actleft = actrigth = actup = actdown = False # Booleanos para terminar un movimiento
	movleft = movrigth = movup = movdown = 0# Contadores para la animación del movimiento del jugador
	posIant = [False, False] # Conocer la posición de inicio anterior (Cambiar de mapa)

	# Ciclo del juego
	#terminar = False
	# reloj
	reloj = pygame.time.Clock()
	while not terminar:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminar = True
			# CONTROLES CUANDO EL JUGADOR PRESIONA UNA TECLA
			if event.type == pygame.KEYDOWN:
				# Pausar:
				if event.type == pygame.K_p:
					pass
				# MOVIMIENTOS DEL JUGADOR CON EL TECLADO:
				# Mover arriba:
				if event.key == pygame.K_UP:
					if not([True, False, False, False] == jugador.is_a_wall(ciudadVerde, "up")):
						up = True
						actup = True
				# Mover abajo:
				if event.key == pygame.K_DOWN:
					if not([False, True, False, False] == jugador.is_a_wall(ciudadVerde, "down")):
						down = True
						actdown = True
				# Mover a la derecha:
				if event.key == pygame.K_RIGHT:
					if not([False, False, False, True] == jugador.is_a_wall(ciudadVerde, "rigth")):
						rigth = True
						actrigth = True
				# Mover a la leftuierda:
				if event.key == pygame.K_LEFT:
					if not([False, False, True, False] == jugador.is_a_wall(ciudadVerde, "left")):
						left = True
						actleft = True
				# Empezar una acción:
				if event.key == pygame.K_a:
					posx, posy = jugador.transfM(ciudadVerde)
					# SELECCIONAR EL POKEMON INCIAL
					if not(oak_conversacion) and jugador.seleccionar_pokemon:
						if ciudadVerde.map[posy][posx] == 's':
							# Seleccionar a squirtle:
							jugador.pokemones.append(matrizPokemon[6])
							jugador.seleccionar_pokemon = False
							jugador.aviso_sin_pokemon = False
							aviso = pygame.image.load("img/avisos/squirtle_seleccionado.jpg")
							pantalla.blit(aviso, (0, 0))
							pygame.display.flip()
							reloj.tick(0.3)
							#print "SQUIRTLE SELECCIONADO: \n POKEMONES: {0}".format(jugador.pokemones)
						elif ciudadVerde.map[posy][posx] == 'r':
							# Seleccionar a charmander
							jugador.pokemones.append(matrizPokemon[3])
							jugador.seleccionar_pokemon = False
							jugador.aviso_sin_pokemon = False
							aviso = pygame.image.load("img/avisos/charmander_seleccionado.jpg")
							pantalla.blit(aviso, (0, 0))
							pygame.display.flip()
							reloj.tick(0.3)
							#print "CHARMANDER SELECCIONADO: \n POKEMONES: {0}".format(jugador.pokemones)
						elif ciudadVerde.map[posy][posx] == 'b':
							# Seleccionar a bulbasaur:
							jugador.pokemones.append(matrizPokemon[0])
							jugador.seleccionar_pokemon = False
							jugador.aviso_sin_pokemon = False
							aviso = pygame.image.load("img/avisos/bulbasaur_seleccionado.jpg")
							pantalla.blit(aviso, (0, 0))
							pygame.display.flip()
							reloj.tick(0.3)
							#print "BULBASAUR SELECCIONADO: \n POKEMONES: {0}".format(jugador.pokemones)

			# CONTROLES CUANDO EL JUGADOR SUELTA UNA TECLA
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					up = False
					jugador.sprite = jugador.matrizJugador[1][1]
				if event.key == pygame.K_DOWN:
					down = False
					jugador.sprite = jugador.matrizJugador[1][0]
				if event.key == pygame.K_RIGHT:
					rigth = False
					jugador.sprite = jugador.matrizJugador[1][3]
				if event.key == pygame.K_LEFT:
					left = False
					jugador.sprite = jugador.matrizJugador[1][2]

		#-----------------------------------------------------------------------
		# MOSTRAR MAPA EN PANTALLA:
		x, y = (tamPantalla[0]*ciudadVerde.scale)/tamCuadro, (tamPantalla[1]*ciudadVerde.scale)/tamCuadro
		pantalla.fill(NEGRO)
		for j in range(0, y+1):
			for i in range(0, x+1):
				try:
					pantalla.blit(ciudadVerde.matrizMap[i+ciudadVerde.iniciox][j+ciudadVerde.inicioy], (i*(tamCuadro/ciudadVerde.scale), j*(tamCuadro/ciudadVerde.scale)))
				except IndexError:
					pass
		#-----------------------------------------------------------------------

		#-----------------------------------------------------------------------
		# ANIMACION DEL JUGADOR AL CAMINAR
		#-----------------------------------------------------------------------
		# CAMINAR HACIA ARRIBA:
		if (up and movup < 3) or actup:
			jugador.sprite = jugador.matrizJugador[movup][1]
			movup += 1
			# Calcular que tan cerca esta el personaje de los limites del mapa:
			lim = jugador.transfM(ciudadVerde)
			# - not(lim[1] <= 6) -> Si esta cerca del borde superior
			# - not([True, False, False, False] == jugador.is_a_wall(ciudadVerde, "up"))
			#   esta condición indica que la pantalla tampoco se desplazara si hay un objeto con el cual chocar
			if not([True, False, False, False] == jugador.is_a_wall(ciudadVerde, "up")):
				if (not(lim[1] <= 2))*bool(ciudadVerde.velocidad):
					ciudadVerde.inicioy -= ciudadVerde.velocidad
				else:
					jugador.pos[1] -= 11 - 1*(movup%2) # mov%2 -> 11 + 10 +11 = 32 px
			# El jugador solo termina el movimiento al soltar la tecla
			if movup == 3: # Reinicia la animación
				movup = 0
				actup = False
				if up == True and ([True, False, False, False] == jugador.is_a_wall(ciudadVerde, "up")):
					up = False

		# CAMINAR HACIA ABAJO:
		if (down and movdown < 3) or actdown:
			jugador.sprite = jugador.matrizJugador[movdown][0]
			movdown += 1
			# Calcular que tan cerca esta el personaje de los limites del mapa:
			lim = jugador.transfM(ciudadVerde)
			# - not(len(ciudadVerde.map) - lim[1] <= 6) -> Si esta cerca del borde inferior
			# - not([False, True, False, False] == jugador.is_a_wall(ciudadVerde, "down"))
			#   esta condición indica que la pantalla tampoco se desplace si hay un objeto con el cual chocar
			if not([False, True, False, False] == jugador.is_a_wall(ciudadVerde, "down")):
				if ((len(ciudadVerde.map) - lim[1] <= len(ciudadVerde.map) - 1)*bool(ciudadVerde.velocidad)):
					ciudadVerde.inicioy += ciudadVerde.velocidad
				else:
					jugador.pos[1] += 11 - 1*(movdown%2) # mov%2 -> 11 + 10 +11 = 32 px
			# El jugador solo termina el movimiento al soltar la tecla
			if movdown == 3: # Reinicia la animación
				movdown = 0
				actdown = False
				if down == True and ([False, True, False, False] == jugador.is_a_wall(ciudadVerde, "down")):
					down = False

		# CAMINAR HACIA LA DERECHA:
		if (rigth and movrigth < 3) or actrigth:
			jugador.sprite = jugador.matrizJugador[movrigth][3]
			movrigth += 1
			# Calcular que tan cerca esta el personaje de los limites del mapa:
			lim = jugador.transfM(ciudadVerde)
			# - not(len(ciudadVerde.map[0]) - lim[0] <= 6) -> Si esta cerca del borde derecho
			# - not([False, False, False, True] == jugador.is_a_wall(ciudadVerde, "rigth"))
			#   esta condición indica que la pantalla tampoco se desplace si hay un objeto con el cual chocar
			if not([False, False, False, True] == jugador.is_a_wall(ciudadVerde, "rigth")):
				if (not(len(ciudadVerde.map[0]) - lim[0] <= 6))*bool(ciudadVerde.velocidad):
					ciudadVerde.iniciox += ciudadVerde.velocidad - 1*(movrigth%2)*bool(ciudadVerde.velocidad)
				else:
					jugador.pos[0] += 11 - 1*(movrigth%2) # mov%2 -> 11 + 10 +11 = 32 px
			# El jugador solo termina el movimiento al soltar la tecla
			if movrigth == 3: # Reinicia la animación
				movrigth = 0
				actrigth = False # Booleano que sirve para terminar la animacion
				# Si el jugador tiene presionada la tecla, pero a su derecha se encuentra
				# un muro, arbol o cerca, no podra continuar caminando
				if rigth == True and ([False, False, False, True] == jugador.is_a_wall(ciudadVerde, "rigth")):
					rigth = False

		# CAMINAR HACIA LA IZQUIERDA:
		if (left and movleft < 3) or actleft:
			jugador.sprite = jugador.matrizJugador[movleft][2]
			movleft += 1
			# Calcular que tan cerca esta el personaje de los limites del mapa:
			lim = jugador.transfM(ciudadVerde)
			# - not(lim[0] <= 6) -> Si esta cerca del limite izquierdo del mapa
			# - not([False, False, True, False] == jugador.is_a_wall(ciudadVerde, "left"))
			#   esta condición indica que la pantalla no se desplace si hay un objeto con el cual chocar
			if not([False, False, True, False] == jugador.is_a_wall(ciudadVerde, "left")):
				if (not(lim[0] <= 6))*bool(ciudadVerde.velocidad):
					ciudadVerde.iniciox -= ciudadVerde.velocidad - 1*(movleft%2)*bool(ciudadVerde.velocidad)
				else:
					jugador.pos[0] -= 11 - 1*(movleft%2) # mov%2 -> 11 + 10 +11 = 32 px
			# El jugador solo terminar el movimiento al soltar la tecla
			if movleft == 3: # Reinicia la animación
				movleft = 0
				actleft = False # Booleano que sirve para terminar la animacion
				# Si el jugador tiene presionada la tecla, pero a su izquierda se encuentra
				# un muro, arbol o cerca, no podra continuar caminando
				if left == True and ([False, False, True, False] == jugador.is_a_wall(ciudadVerde, "left")):
					left = False
		#-----------------------------------------------------------------------

		#-----------------------------------------------------------------------
		# CAMBIAR DE MAPA O ENTRAR A COMBATE: <orden alfabetico>
		#-----------------------------------------------------------------------
		posx, posy = jugador.transfM(ciudadVerde)

		# Centro de salud pokemon:
		if ciudadVerde.map[posy][posx] == 'S':
			posIant = [posy+1, posx]
			ciudadverde.reemplazarElem("I", posIant)
			ciudadVerde = centropokemon #Mapa(filename)
			jugador.ubicar(ciudadVerde)

		# Ciudad Verde:
		elif ciudadVerde.map[posy][posx] == 'C':
			posIant = [posy+1, posx]
			if ciudadVerde.tileset == "maps/ruta1.png":
				ruta1.reemplazarElem("I", posIant)
			ciudadVerde = ciudadverde # Mapa(filename)
			jugador.ubicar(ciudadVerde)

		# Gimnasio:
		elif ciudadVerde.map[posy][posx] == 'G':
			posIant = [posy+1, posx]
			ciudadverde.reemplazarElem("I", posIant)
			ciudadVerde = gimnasio #Mapa(filename)
			jugador.ubicar(ciudadVerde)

		# Interior de la casa:
		elif ciudadVerde.map[posy][posx] == 'i':
			posIant = [posy+1, posx]
			pueblopaleta.reemplazarElem("I", posIant)
			ciudadVerde = interior #Mapa(filename)
			jugador.ubicar(ciudadVerde)

		# Laboratorio:
		elif ciudadVerde.map[posy][posx] == 'L':
			posIant = [posy+1, posx]
			pueblopaleta.reemplazarElem("I", posIant)
			ciudadVerde = laboratorio #Mapa(filename)
			jugador.ubicar(ciudadVerde)

		# Pueblo paleta:
		elif ciudadVerde.map[posy][posx] == 'p':
			posIant = [posy, posx]
			if ciudadVerde.tileset == "maps/interior.png":
				posIant[0] -= 1
				interior.reemplazarElem("I", posIant)
			elif ciudadVerde.tileset == "maps/ruta1.png":
				posIant = [posy, posx]
				posIant[0] -= 1
				ruta1.reemplazarElem("I", posIant)
			ciudadVerde = pueblopaleta #Mapa(filename)
			jugador.ubicar(ciudadVerde)

		# Ruta 1:
		elif ciudadVerde.map[posy][posx] == '1':
			if not(len(jugador.pokemones) == 0):
				posIant = [posy, posx]
				if ciudadVerde.tileset == "maps/ciudadverde.png":
					posIant[0] -= 1
					ciudadverde.reemplazarElem("I", posIant)
				elif ciudadVerde.tileset == "maps/pueblopaleta.png":
					posIant[0] += 1
					pueblopaleta.reemplazarElem("I", posIant)
				ciudadVerde = ruta1 #Mapa(filename)
				jugador.ubicar(ciudadVerde)
			else:
				# EN EL CASO DE NO TENER NINGUN POKEMON, MOSTRAR AVISO
				jugador.aviso_sin_pokemon = True


		# Tienda:
		elif ciudadVerde.map[posy][posx] == 'T':
			posIant = [posy+1, posx]
			ciudadverde.reemplazarElem("I", posIant)
			ciudadVerde = tienda #Mapa(filename)
			jugador.ubicar(ciudadVerde)

		# ----------------------------------------------------------------------
		# ENTRAR EN COMBATE:
		elif ciudadVerde.map[posy][posx] == 'P':
			# Probabilidad de entrar en batalla -> 25%
			# Si se detiene sobre un lugar, tiene posibilidad de entrar en batalla
			if not bool(random.randrange(0, 4)):
				pass
				#terminar = True # Terminar solo esta pantalla
				#Batalla.main((posx, posy), not(terminar))
				# print "HAS ENTRADO A LA BATALLA POKEMON"

		reloj.tick(10)
		jugador.dibujar(pantalla)

		#----------------------------------------------------------------------
		# AVISOS

		# En caso de que el jugador intente salir del pueblo paleta sin un pokemon:
		if jugador.aviso_sin_pokemon:
			aviso = pygame.image.load("img/avisos/sin_pokemon.png")
			pantalla.blit(aviso, (0, 0))
			jugador.aviso_sin_pokemon = False

		# Avisos dentro del laboratorio
		if ciudadVerde.tileset == "maps/laboratorio.png":
			posx, posy = jugador.transfM(ciudadVerde)
			# Conversacion con el profesor OAK (solo se tiene una vez)
			if ciudadVerde.map[posy][posx] == 'o' and oak_conversacion:
				aviso = pygame.image.load("img/avisos/entregar_pokemon.png")
				aviso2 = pygame.image.load("img/avisos/entregar_pokemon2.png")
				pantalla.blit(aviso, (0, 0))
				pygame.display.flip()
				reloj.tick(0.1)
				pantalla.blit(aviso2, (0, 0))
				pygame.display.flip()
				reloj.tick(0.1)
				oak_conversacion = False
			# Seleccionar pokemon inicial:
			if not(oak_conversacion):
				if ciudadVerde.map[posy][posx] == 's' and jugador.seleccionar_pokemon:
					aviso = pygame.image.load("img/avisos/seleccionar_squirtle.png")
					pantalla.blit(aviso, (354, 16))
					pygame.display.flip()
				elif ciudadVerde.map[posy][posx] == 'r' and jugador.seleccionar_pokemon:
					aviso = pygame.image.load("img/avisos/seleccionar_charmander.png")
					pantalla.blit(aviso, (354, 16))
					pygame.display.flip()
				elif ciudadVerde.map[posy][posx] == 'b' and jugador.seleccionar_pokemon:
					aviso = pygame.image.load("img/avisos/seleccionar_bulbasaur.png")
					pantalla.blit(aviso, (354, 16))
					pygame.display.flip()
			if blue.dialogo:
				aviso = pygame.image.load("img/avisos/duelo_Blue.png")
				pantalla.blit(aviso, (0, 0))
				reloj.tick(0.2)

		# Teclas de accion:

		pygame.display.flip()
