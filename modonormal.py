# coding=utf-8

import pygame
import ConfigParser

# Constantes
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
tamCuadro = 32 # Tamaño de cada cuadro
tamPantalla = [527, 398]
tamJugador = 56
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
		self.matrizJugador = []
		for x in range(0, 3): # Se requieren tres acciones para un movimiento
			linea = []
			self.matrizJugador.append(linea)
			for y in range(0, 4): # Son cuatro las perspectivas del jugador
				cuadro = (x*tamJugador, y*tamJugador, tamJugador, tamJugador)
				linea.append(self.image.subsurface(cuadro))
		self.pos = [False, False]

	def dibujar(self, pantalla):
		pantalla.blit(self.matrizJugador[1][0], self.pos)

# MAIN
if __name__=='__main__':
	pygame.init()
	pantalla = pygame.display.set_mode(tamPantalla)
	pantalla.fill(NEGRO)

	filename ="maps/tienda.map"
	ciudadVerde = Mapa(filename)

	jugador = Jugador("red.png")

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
	while not terminar:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminar = True
		for j in range(0, y+1):
			for i in range(0, x+1):
				try:
					pantalla.blit(ciudadVerde.matrizMap[i+iniciox][j+inicioy], (i*(tamCuadro/ciudadVerde.scale), j*(tamCuadro/ciudadVerde.scale)))
				except IndexError:
					pass
		jugador.dibujar(pantalla)
		pygame.display.flip()
