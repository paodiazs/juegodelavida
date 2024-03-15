import pygame #para juegos
import time, os
import numpy as np #matematicas y manejo de matrices
import time #para el delay 

#para que se centre la ventana
os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init() #crear la pantalla del juego


#titulo de la ventana
pygame.display.set_caption("Juego de la vida - paodiazs")

width, height = 1000, 1000 #ancho y  largo
#creación de la pantalla
screen = pygame.display.set_mode((height, width)) 
bg = 25,25,25 #color de fondo, intensidad de 25
#se pinta el fondo con el color elegido
screen.fill(bg)
#numero de celdas, en el eje X y eje Y
nxC, nyC = 60,60

#dimensiones de la celda, (cuadritos medidas)
dimCW = width / nxC
dimCH = height / nyC

#estado de las celdas. VIVAS = 1, MUERTAS = 0
#matriz del tamaño igual al numero de celdas
gameState = np.zeros((nxC, nyC))

#Autómata movil
gameState[21,21] = 1
gameState[22,22] = 1
gameState[22,23] = 1
gameState[21,23] = 1
gameState[20,23] = 1

#automata palo
gameState[5,3] = 1
gameState[5,4] = 1
gameState[5,5] = 1
gameState[5,6] = 1
gameState[5,7] = 1



pauseRun = False
running = True

#para que la pantalla se muestre de manera infinita
while running : 

    newGameState = np.copy(gameState) # en cada itereacion, realizamos una copia del estado actual del juego
    #se guarda en la copia cada una de las actualizaciones del juego
    #Limpiamos la pantalla para que cada estado no se vaya superponiendo
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        if event.type == pygame.KEYDOWN:
          pauseRun = not pauseRun
        
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
          posX, posY = pygame.mouse.get_pos()
          celX, celY = int(np.floor(posX/dimCW)), int(np.floor(posY/dimCH))
          newGameState[celX, celY] = not mouseClick[2]
          
    screen.fill(bg)


    for y in range(0 , nxC):
      for x in range (0 , nyC):
        if not pauseRun:
            #ESTRATEGIA TOROIDAL para los bordes - se hace como un infinito, la izquierda al "salir", vas llegando a la derecha, para eso usamos la operacion modulo
            #calculamos el numero de vecinos cercanos:
            n_neigh = (
                    gameState[(x - 1) % nxC, (y - 1) % nyC]
                    + gameState[x % nxC, (y - 1) % nyC]
                    + gameState[(x + 1) % nxC, (y - 1) % nyC]
                    + gameState[(x - 1) % nxC, y % nyC]
                    + gameState[(x + 1) % nxC, y % nyC]
                    + gameState[(x - 1) % nxC, (y + 1) % nyC]
                    + gameState[x % nxC, (y + 1) % nyC]
                    + gameState[(x + 1) % nxC, (y + 1) % nyC]
                )
            #REGLA 1: una celcula muerta, con 3 celulas vecinas vivas, revive
            if gameState[x, y] == 0 and n_neigh == 3:
              newGameState[x, y] = 1 #"revive" -> cambia de 0 a 1
            #REGLA 2: Una celula viva con menos de 2 o más de 3 vivas, muere
            elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh >3):
              newGameState[x, y] = 0 
        #creamos el poligono de cada celda a dibujar, COORDENADAS DE NUESTROS RECTANGULOS
        poly = [
                (int(x * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int((y + 1) * dimCH)),
                (int(x * dimCW), int((y + 1) * dimCH)),
        ]
      
        #Dibujamos la celda para cada par de x y y ,  dibujamos el poligono
        if newGameState[x, y] == 0 : 
          pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
        else:
          # Con el juego ejecutándose pinto de blanco las celdas
          pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    #Actualizamos el estado del juego
    gameState = np.copy(newGameState)
     #Delay 
    time.sleep(0.1)
    #ACtualizamos la pantalla  
    pygame.display.flip()
