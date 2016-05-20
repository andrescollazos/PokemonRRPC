import pygame
import ConfigParser

# Constantes
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
tamPantalla = [527, 398]

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
		ancho = 32/self.scale
		alto = 32/self.scale
		for fondo_x in range(0, imagen_ancho/ancho):
			linea = []
			self.matrizMap.append(linea)
			for fondo_y in range(0, imagen_alto/alto):
				cuadro = (fondo_x*ancho, fondo_y*alto, ancho, alto)
				linea.append(self.image.subsurface(cuadro))

	def get_tile(self, x, y):
		try:
			char = self.map[y][x]
		except IndexError:
			return {}
		try:
			return self.key[char]
		except KeyError:
			return {}

# MAIN
if __name__=='__main__':
	pygame.init()
	pantalla = pygame.display.set_mode(tamPantalla)
	pantalla.fill(NEGRO)

	filename ="maps/ruta1.map"
	ciudadVerde = Mapa(filename)

	print "--------------------------------------------------------------------"
	print "MAPA"
	print "--------------------------------------------------------------------"
	for x in ciudadVerde.map:
		for y in x:
			print y,
		print ""

	# Ciclo del juego
	terminar = False
	x, y = ciudadVerde.image.get_size()
	x, y = x/32, y/32
	while not terminar:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminar = True
		for j in range(0, y):
			for i in range(0, x):
				pantalla.blit(ciudadVerde.matrizMap[i][j], (i*(32/ciudadVerde.scale), j*(32/ciudadVerde.scale)))

		pygame.display.flip()
