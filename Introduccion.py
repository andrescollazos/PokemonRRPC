import pygame
import ConfigParser
import modonormal

NEGRO  = (   0,   0,   0)
BLANCO = ( 255, 255, 255)
VERDE  = (   0, 255,   0)
ROJO   = ( 255,   0,   0)

tamPantalla = [527, 398]

pantalla = pygame.display.set_mode(tamPantalla)
pygame.display.set_caption("POKEMON")

# Cargar matriz que contiene los pokemones
def pokemon_init():
    map = [] # Matriz que va a contener la configuracion
    parser = ConfigParser.ConfigParser()
    parser.read("pokemon/pokemon.cfg")
    # Leer archivo que contiene la configuracion de los pokemones
    map = parser.get("Generacion1", "pokemones").split("\n")
    # La siguiente matriz cuenta con los siguientes campos para cada fila:
    #[Nombre_Pokemon, Nivel_Aparece, Familia, Experiencia_Ganada, Ratio_Captura, Vida, LimVida, Imagen_Frontal, Imagen_Posterior]
    # La vida se calcula con base en: V(Nivel_Aparece) = 5*Nivel_Aparece
    matrizPokemon, cadena = [], ""
    for pokemon in map:
        fila = []
        for i in range(len(pokemon)):
            # No tener en cuenta los espacios
            if not(pokemon[i] == " "):
                cadena += pokemon[i]
                if i + 1 == len(pokemon):
                    fila.append(cadena)
                    cadena = ""
            else:
                if len(cadena):
                    fila.append(cadena)
                cadena = ""
        fila[1], fila[2], fila[3], fila[4], fila[5] = int(fila[1]), int(fila[2]), int(fila[3]), int(fila[4]), int(fila[5])
        fila.append(int(fila[5])) # Agregar limite de vida
        matrizPokemon.append(fila)
    # Calcular experiencia Base: E = 4*(n^3)/5
    for pokemon in matrizPokemon:
        pokemon[3] = (4*(pokemon[1]**3))/5

    # Cargar sprites para cada pokemon (Frontal y posterior)
    for i, pokemon in enumerate (matrizPokemon):
        filename = "img/pokemones/"+str(i+1)+".png"
        image = pygame.image.load(filename)
        imagen_ancho, imagen_alto = image.get_size()
        alto, ancho = 65, 65
        # Recortar imagen, separar imagen frontal e imagen posterior
        for x in range(imagen_ancho/ancho):
            cuadro = (x*ancho, 0, ancho, alto)
            pokemon.append(image.subsurface(cuadro))
    # Ordenar la matriz pokemon de menor a mayor nivel (al aparecer)
    #matrizPokemon = sorted(matrizPokemon, key=lambda pokemon: pokemon[1])
    for i in matrizPokemon:
        print "Cargando Pokemon: {0}\t...\tOk".format(i[0])
    return matrizPokemon

# Funcion para mostrar por pantalla una imagen:
def imagenes(tamano,posicion,ruta):
    imagen = pygame.image.load(ruta)
    imagen = pygame.transform.scale(imagen,tamano)
    pantalla.blit(imagen,posicion)
    pygame.display.flip()


    #CICLO PRESENTACION
    # Se muestra la imagen de dragon con el nombre del juego
    # Despues de contar hasta 200 pasa a la siguiente imagen
    # sale la imagen para oprimir la barra espaciadora y pasar a la introduccion
#'''
def Presentacion():
    reloj = pygame.time.Clock()
    pag,ver_pag, terminar = 1, True, False
    while not terminar and ver_pag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar = True
                return terminar
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pantalla.fill(NEGRO)
                    ver_pag = False
        if pag == 1:
            imagenes(tamPantalla,[0,0],"img/Pinicial/inicial1.jpg")
            reloj.tick(0.5)
        if pag == 2:
            imagenes([527,398],[0,0],"img/Pinicial/inicial2.jpg")
            reloj.tick(0.7)
        if pag == 3:
            imagenes([260,80],[133,310],"img/Pinicial/barespa.png")
        pag += 1
    return False # Para indicar que la presentacion sigue
        #'''
def Introduccion(terminar):
    reloj = pygame.time.Clock()
    pag,ver_pag = 1, True
    while not terminar and ver_pag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar = True
                return terminar
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pag += 1
                    pantalla.fill(NEGRO)
        if pag == 1:
    		imagenes([527,308],[0,0],"img/Introduccion/Oak1.png")
    		imagenes([400,80],[60,310],"img/Introduccion/Introduccion1.png")
    		reloj.tick(0.7)
        imagenes([20,20],[480,330],"img/Teclado/A.png")
        if pag == 2:
            imagenes([527,308],[0,0],"img/Introduccion/OakLab.png")
            imagenes([400,80],[60,310],"img/Introduccion/Introduccion2.png")
            reloj.tick(0.7)
        imagenes([20,20],[480,330],"img/Teclado/A.png")
        if pag == 3:
            imagenes([527,308],[0,0],"img/Introduccion/Oak2.png")
            imagenes([400,80],[60,310],"img/Introduccion/Introduccion3.png")
            reloj.tick(0.7)
        imagenes([20,20],[480,330],"img/Teclado/A.png")
        if pag == 4:
            imagenes([527,308],[0,0],"img/Introduccion/Oak3.png")
            imagenes([400,80],[60,310],"img/Introduccion/Introduccion4.png")
            reloj.tick(0.7)
        imagenes([20,20],[480,330],"img/Teclado/A.png")
        if pag == 5:
            imagenes([527,308],[0,0],"img/Introduccion/Nieto.png")
            imagenes([400,80],[60,310],"img/Introduccion/Introduccion5.png")
            reloj.tick(0.7)
        imagenes([20,20],[480,330],"img/Teclado/A.png")
        if pag == 6:
            imagenes([527,308],[0,0],"img/Introduccion/Blue.png")
            imagenes([400,80],[60,310],"img/Introduccion/Introduccion6.png")
            reloj.tick(0.7)
        imagenes([20,20],[480,330],"img/Teclado/A.png")
        if pag == 7:
            imagenes([527,308],[0,0],"img/Introduccion/Vs.png")
            imagenes([400,80],[60,310],"img/Introduccion/Introduccion7.png")
            reloj.tick(0.7)
        imagenes([20,20],[480,330],"img/Teclado/A.png")
        if pag == 8:
            ver_pag = False
    if terminar:
        return True
    else:
        return False

def Controles(terminar):
    reloj = pygame.time.Clock()
    pag,ver_pag = 1, True
    while not terminar and ver_pag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar = True
                return terminar
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pag += 1
                    pantalla.fill(NEGRO)
        if pag == 1:
            imagenes([527,398],[0,0],"img/Controles/Controles.jpg")
            reloj.tick(0.7)
    	imagenes([20,20],[480,330],"img/Teclado/A.png")
        if pag == 2:
            ver_pag = False
    if terminar:
        return True
    else:
        return False # Indica que el juego va a comenzar

if __name__=='__main__':
    # Paramentros iniciales
    pokemones = pokemon_init() # Cargar pokemones
    pygame.init()
    dim = tamPantalla

    presentacion = Presentacion()
    introduccion = Introduccion(presentacion)
    controles = Controles(introduccion)
    modoN = modonormal.main("maps/interior.map", introduccion, pokemones, False, False, False)
