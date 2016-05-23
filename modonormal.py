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
mapas = {"interior", "pueblopaleta","lab", "ruta1", "ciudadverde", "centropokemon", "tienda", "gimnasio",}

class Mapa(object):
	def __init__(self, filename):#, jugador):
		# Elementos propios del mapa:
		self.map = [] # Matriz que contiene el mapa
		self.key = {}
		parser = ConfigParser.ConfigParser()
		parser.read(filename)
        # Cargar mapa codifiado:
		self.map = parser.get("level", "map").split("\n")
		for section in parser.sections():
			if len(section) == 1:
				desc = dict(parser.items(section))
				self.key[section] = desc
		self.width = len(self.map[0])
		self.height = len(self.map)
		#-----------------------------------------------------------------------
		# Imagen del mapa:
		self.tileset = parser.get("level", "tileset")
		self.image = pygame.image.load(self.tileset)#.convert_alpha()
		# Obtener dimensiones del mapa
		imagen_ancho, imagen_alto = self.image.get_size()
		self.matrizMap = [] # Matriz que relaciona el mapa con la imagen
		self.scale = int(parser.get("level", "scale")) # Saber el tamanyo de cada elemento
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
		self.iniciox = int(parser.get("level", "iniciox"))
		self.inicioy = int(parser.get("level", "inicioy"))

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

	# MOSTRAR EN PANTALLA EL JUGADOR
	def dibujar(self, pantalla):
		pantalla.blit(self.sprite, self.pos)

# MAIN
if __name__=='__main__':
	pygame.init()
	pantalla = pygame.display.set_mode(tamPantalla)
	pantalla.fill(NEGRO)

	filename ="maps/pueblopaleta.map"
	ciudadVerde = Mapa(filename)

	jugador = Jugador("red.png")
	#jugador.matrizMap = ciudadVerde.map

	# Ciclo del juego
	terminar = False
	x, y = (tamPantalla[0]*ciudadVerde.scale)/tamCuadro, (tamPantalla[1]*ciudadVerde.scale)/tamCuadro
	# Ajustar pantalla:
	iniciox = ciudadVerde.iniciox
	inicioy = ciudadVerde.inicioy
	# Posicionar al jugador:
	pos = [False, False]
	cont = 0
	for lst in ciudadVerde.map:
		try:
			print cont
			pos[0] = lst.index('I')
			break
		except ValueError:
			pass
			cont += 1
	pos[1] = cont
	# Calcular la posición del jugador en la pantalla:
	pos[0] = (pos[0]*ciudadVerde.scale - iniciox)*(32/ciudadVerde.scale)
	pos[1] = (pos[1]*ciudadVerde.scale - inicioy)*(32/ciudadVerde.scale) - (tamJugador-32)
	jugador.pos = pos

	#print "POSICION DEL JUGADOR: ", jugador.pos
	#print "Posicion pantalla:\t{0},{1}".format(jugador.pos[0]/16, jugador.pos[1]/16)
	#print "Posicion matriz:\t{0},{1}".format((jugador.pos[0]/(32/ciudadVerde.scale)+iniciox)/ciudadVerde.scale, (jugador.pos[1]/(32/ciudadVerde.scale)+inicioy)/ciudadVerde.scale)

	left = rigth = up = down = False # Booleanos para saber si el jugador se mueve
	actleft = actrigth = actup = actdown = False # Booleanos para terminar un movimiento
	movleft = movrigth = movup = movdown = 0# Contadores para la animación del movimiento del jugador
	# reloj
	reloj = pygame.time.Clock()
	total = 0
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
					up = True
					actup = True
				# Mover abajo:
				if event.key == pygame.K_DOWN:
					down = True
					actdown = True
				# Mover a la derecha:
				if event.key == pygame.K_RIGHT:
					rigth = True
					actrigth = True
				# Mover a la leftuierda:
				if event.key == pygame.K_LEFT:
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
		for j in range(0, y+1):
			for i in range(0, x+1):
				try:
					pantalla.blit(ciudadVerde.matrizMap[i+iniciox][j+inicioy], (i*(tamCuadro/ciudadVerde.scale), j*(tamCuadro/ciudadVerde.scale)))
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
			jugador.pos[1] -= 11 - 1*(movup%2) # mov%2 -> 11 + 10 +11 = 32 px
			movup += 1
			# El jugador solo termina el movimiento al soltar la tecla
			if movup == 3: # Reinicia la animación
				movup = 0
				actup = False
		# CAMINAR HACIA ABAJO:
		if (down and movdown < 3) or actdown:
			jugador.sprite = jugador.matrizJugador[movdown][0]
			jugador.pos[1] += 11 - 1*(movdown%2) # mov%2 -> 11 + 10 +11 = 32 px
			movdown += 1
			# El jugador solo termina el movimiento al soltar la tecla
			if movdown == 3: # Reinicia la animación
				movdown = 0
				actdown = False
		# CAMINAR HACIA LA DERECHA:
		if (rigth and movrigth < 3) or actrigth:
			jugador.sprite = jugador.matrizJugador[movrigth][3]
			jugador.pos[0] += 11 - 1*(movrigth%2) # mov%2 -> 11 + 10 +11 = 32 px
			movrigth += 1
			# El jugador solo termina el movimiento al soltar la tecla
			if movrigth == 3: # Reinicia la animación
				movrigth = 0
				actrigth = False
		# CAMINAR HACIA LA IZQUIERDA:
		if (left and movleft < 3) or actleft:
			jugador.sprite = jugador.matrizJugador[movleft][2]
			jugador.pos[0] -= 11 - 1*(movleft%2) # mov%2 -> 11 + 10 +11 = 32 px
			movleft += 1
			# El jugador solo terminar el movimiento al soltar la tecla
			if movleft == 3: # Reinicia la animación
				movleft = 0
				actleft = False
		#-----------------------------------------------------------------------


		reloj.tick(10)
		jugador.dibujar(pantalla)
		pygame.display.flip()
