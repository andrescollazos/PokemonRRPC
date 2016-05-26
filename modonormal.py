# coding=utf-8

import pygame
import ConfigParser
import math

# Constantes
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
tamCuadro = 32 # Tamaño de cada cuadro
tamPantalla = [527, 398]
tamJugador = 48
mapas = ['centropokemon', 'ciudadverde', 'gimnasio', 'interior', 'lab', 'pueblopaleta', 'ruta1', 'tienda']

class Mapa(object):
	def __init__(self, filename):#, jugador):
		# Elementos propios del mapa:
		self.map = [] # Matriz que contiene el mapa
		self.key = {}
		self.parser = ConfigParser.ConfigParser()
		self.parser.read(filename)
        # Cargar mapa codifiado:
		self.map = self.parser.get("level", "map").split("\n")
		for section in self.parser.sections():
			if len(section) == 1:
				desc = dict(self.parser.items(section))
				self.key[section] = desc
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

# MAIN
# def main(filename):
if __name__=='__main__':
	# Parametros iniciales:
	pygame.init()
	pantalla = pygame.display.set_mode(tamPantalla)
	pantalla.fill(NEGRO)

	filename ="maps/interior.map"
	ciudadVerde = Mapa(filename)
	jugador = Jugador("red.png")
	# Posicionar al jugador:
	jugador.ubicar(ciudadVerde)

	# x, y -> Cantidad de ciclos para pintar el mapa a realizar:
	x, y = (tamPantalla[0]*ciudadVerde.scale)/tamCuadro, (tamPantalla[1]*ciudadVerde.scale)/tamCuadro
	left = rigth = up = down = False # Booleanos para saber si el jugador se mueve
	actleft = actrigth = actup = actdown = False # Booleanos para terminar un movimiento
	movleft = movrigth = movup = movdown = 0# Contadores para la animación del movimiento del jugador
	posIant = [False, False] # Conocer la posición de inicio anterior (Cambiar de mapa)

	# Ciclo del juego
	terminar = False
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
		#print "PRUEBA {0}".format(1%2)
		# CAMINAR HACIA ARRIBA:
		if (up and movup < 3) or actup:
			jugador.sprite = jugador.matrizJugador[movup][1]
			# jugador.pos[1] -= 0 #11 - 1*(movup%2) # mov%2 -> 11 + 10 +11 = 32 px
			movup += 1
			# Calcular que tan cerca esta el personaje de los limites del mapa:
			lim = jugador.transfM(ciudadVerde)
			print "Posicion [{0},{1}]".format(lim[0], lim[1])
			# - not(lim[1] <= 6) -> Si esta cerca del borde superior
			# - not([True, False, False, False] == jugador.is_a_wall(ciudadVerde, "up"))
			#   esta condición indica que la pantalla tampoco se desplazara si hay un objeto con el cual chocar
			if not([True, False, False, False] == jugador.is_a_wall(ciudadVerde, "up")):
				print "{0} <= 6: {1}".format(lim[1], lim[1] <= 2)
				if (not(lim[1] <= 2))*bool(ciudadVerde.velocidad):
					ciudadVerde.inicioy -= ciudadVerde.velocidad
				else:
					jugador.pos[1] -= 11 - 1*(movup%2) # mov%2 -> 11 + 10 +11 = 32 px

			#if not(lim[1] <= 6) and not([True, False, False, False] == jugador.is_a_wall(ciudadVerde, "up")):
			#	ciudadVerde.inicioy -= ciudadVerde.velocidad
			# El jugador solo termina el movimiento al soltar la tecla
			if movup == 3: # Reinicia la animación
				print "---------------------------------------------------------"
				movup = 0
				actup = False
				if up == True and ([True, False, False, False] == jugador.is_a_wall(ciudadVerde, "up")):
					up = False

		# CAMINAR HACIA ABAJO:
		if (down and movdown < 3) or actdown:
			jugador.sprite = jugador.matrizJugador[movdown][0]
			#jugador.pos[1] += 0 #11 - 1*(movdown%2) # mov%2 -> 11 + 10 +11 = 32 px
			movdown += 1
			# Calcular que tan cerca esta el personaje de los limites del mapa:
			lim = jugador.transfM(ciudadVerde)
			print "Posicion [{0},{1}]".format(lim[0], lim[1])
			# - not(len(ciudadVerde.map) - lim[1] <= 6) -> Si esta cerca del borde inferior
			# - not([False, True, False, False] == jugador.is_a_wall(ciudadVerde, "down"))
			#   esta condición indica que la pantalla tampoco se desplace si hay un objeto con el cual chocar
			if not([False, True, False, False] == jugador.is_a_wall(ciudadVerde, "down")):
				print "{0} - {1} = {3} <= 6: {2}".format(len(ciudadVerde.map), lim[1], lim[1] <= 60, len(ciudadVerde.map) - lim[1])
				if ((len(ciudadVerde.map) - lim[1] <= len(ciudadVerde.map) - 1)*bool(ciudadVerde.velocidad)):
					ciudadVerde.inicioy += ciudadVerde.velocidad
				else:
					jugador.pos[1] += 11 - 1*(movdown%2) # mov%2 -> 11 + 10 +11 = 32 px
			# El jugador solo termina el movimiento al soltar la tecla
			if movdown == 3: # Reinicia la animación
				print "---------------------------------------------------------"
				movdown = 0
				actdown = False
				if down == True and ([False, True, False, False] == jugador.is_a_wall(ciudadVerde, "down")):
					down = False

		# CAMINAR HACIA LA DERECHA:
		if (rigth and movrigth < 3) or actrigth:
			jugador.sprite = jugador.matrizJugador[movrigth][3]
			#jugador.pos[0] += 0 #11 - 1*(movrigth%2) # mov%2 -> 11 + 10 +11 = 32 px
			movrigth += 1
			# Calcular que tan cerca esta el personaje de los limites del mapa:
			lim = jugador.transfM(ciudadVerde)
			print "Posicion [{0},{1}]".format(lim[0], lim[1])
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
				print "---------------------------------------------------------"
				movrigth = 0
				actrigth = False # Booleano que sirve para terminar la animacion
				# Si el jugador tiene presionada la tecla, pero a su derecha se encuentra
				# un muro, arbol o cerca, no podra continuar caminando
				if rigth == True and ([False, False, False, True] == jugador.is_a_wall(ciudadVerde, "rigth")):
					rigth = False

		# CAMINAR HACIA LA IZQUIERDA:
		if (left and movleft < 3) or actleft:
			jugador.sprite = jugador.matrizJugador[movleft][2]
			#jugador.pos[0] -= 0 # 11 - 1*(movleft%2) # mov%2 -> 11 + 10 +11 = 32 px
			movleft += 1
			# Calcular que tan cerca esta el personaje de los limites del mapa:
			lim = jugador.transfM(ciudadVerde)
			print "Posicion [{0},{1}]".format(lim[0], lim[1])
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
				print "---------------------------------------------------------"
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
		#print "Elemento act: \'{0}\'".format(ciudadVerde.map[posy][posx])

		# Centro de salud pokemon:
		if ciudadVerde.map[posy][posx] == 'S':
			posIant = [posx, posy]
			ciudadVerde.reemplazarElem("I", posIant)
			filename = 'maps/'+ mapas[0] + '.map'
			ciudadVerde = Mapa(filename)
			jugador.ubicar(ciudadVerde)

		# Ciudad Verde:
		elif ciudadVerde.map[posy][posx] == 'C':
			posIant = [posx, posy]
			ciudadVerde.reemplazarElem("I", posIant)
			filename = 'maps/'+ mapas[1] + '.map'
			ciudadVerde = Mapa(filename)
			jugador.ubicar(ciudadVerde)

		# Gimnasio:
		elif ciudadVerde.map[posy][posx] == 'G':
			posIant = [posx, posy]
			ciudadVerde.reemplazarElem("I", posIant)
			filename = 'maps/'+ mapas[2] + '.map'
			ciudadVerde = Mapa(filename)
			jugador.ubicar(ciudadVerde)

		# Interior de la casa:
		elif ciudadVerde.map[posy][posx] == 'i':
			posIant = [posx, posy]
			ciudadVerde.reemplazarElem("I", posIant)
			filename = 'maps/'+ mapas[3] + '.map'
			ciudadVerde = Mapa(filename)
			jugador.ubicar(ciudadVerde)

		# Laboratorio:
		elif ciudadVerde.map[posy][posx] == 'L':
			posIant = [posx, posy]
			ciudadVerde.reemplazarElem("I", posIant)
			filename = 'maps/'+ mapas[4] + '.map'
			ciudadVerde = Mapa(filename)
			jugador.ubicar(ciudadVerde)

		# Pueblo paleta:
		elif ciudadVerde.map[posy][posx] == 'p':
			posIant = [posx, posy]
			ciudadVerde.reemplazarElem("I", posIant)
			filename = 'maps/'+ mapas[5] + '.map'
			ciudadVerde = Mapa(filename)
			jugador.ubicar(ciudadVerde)

		# Ruta 1:
		elif ciudadVerde.map[posy][posx] == '1':
			posIant = [posx, posy]
			ciudadVerde.reemplazarElem("I", posIant)
			filename = 'maps/'+ mapas[6] + '.map'
			ciudadVerde = Mapa(filename)
			jugador.ubicar(ciudadVerde)

		# Tienda:
		elif ciudadVerde.map[posy][posx] == 'T':
			posIant = [posx, posy]
			ciudadVerde.reemplazarElem("I", posIant)
			filename = 'maps/'+ mapas[7] + '.map'
			ciudadVerde = Mapa(filename)
			jugador.ubicar(ciudadVerde)

		# ----------------------------------------------------------------------
		# ENTRAR EN COMBATE:
		elif ciudadVerde.map[posy][posx] == 'P':
			print "HAS ENTRADO A LA BATALLA POKEMON"


		reloj.tick(10)
		jugador.dibujar(pantalla)
		pygame.display.flip()
