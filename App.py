import gamelib
import random
from Pieza import Pieza as PiezaC
#Solo hay 3 tipos de piezas segun el ejemplo
tipos_de_piezas=[PiezaC.piezaCaballo,PiezaC.piezaAlfil,PiezaC.piezaTorre]

#metodos para manipular piezas
def VerificarMovimiento(mapa: list[list[None or any]],pos: tuple,pos2: tuple) -> bool:
    """
        las reglas son basicas
        en la variable mapa entra una matrix con none o objeto Pieza


        1. que la direccion pos 2 no sea None
        2. que este vivo de acuerdo a una variable este viva con isAlive()
    """
    x,y=pos
    _x,_y=pos2

    if((x>7 or y>7 or x<0 or y<0) or (_x>7 or _y>7 or _x<0 or _y<0) or (mapa[x][y]==None)):
        return False

    pieza : PiezaC=mapa[x][y]

    if(pieza.isHorse()):

        if((_x,_y)==(x,y) or mapa[_x][_y]==None or (not mapa[_x][_y].live)):
            return False
        return ((_x-x)**2+(y-_y)**2)==5
        
    if(pieza.isAlfil()):
        if((_y-y)==0 or (_x-x)==0 or mapa[_x][_y]==None or mapa[_x][_y].live==False or (_x,_y)==(x,y)):
            return False
        #Aca se usa la formula de pendiente para determinar si puede ir en un movimiento diagonal a otra pieza usando la otra cordenada    
        return (_y-y)/(_x-x)==1 or (_y-y)/(_x-x)==-1 and not((_y-y)/(_x-x)==0)

    if(pieza.isTower() and mapa[_x%8][_y%8]!=None and pieza.live):
        _x,_y=pos2
        vive : PiezaC=mapa[_x][_y]
        #reglas en un if
        if(not (x<8 and x>=0 and y<8 and y>=0 and _x<8 and _x>=0 and _y<8 and _y>=0) or ((_x,_y)==(x,y)) or vive.isDeath()):
            return False
        if(_y-y==0 or _x-x==0):
            return True     
    return False
def puedeSpawnear(mapa,pos,pos2):

    """
    Aca las reglas son

    1. que el pos2 sea None
    2. que solo cheque casillas vacias
    """
    cordsX,cordsY=pos
    _x,_y = pos2
    pieza: PiezaC = mapa[cordsX][cordsY]

    #bien aqui es la formula de pendiente pero adaptada a este codigo
    if(pieza.isTower()):
        if(not (cordsX<9 and cordsX>=0 and cordsY<9 and cordsY>=0 and _x<9 and _x>=0 and _y<9 and _y>=0) ):
            return False
        if((_x,_y)==(cordsX,cordsY)):
            return False
        if(_y-cordsY==0 or _x-cordsX==0):
            return True

    if(pieza.isHorse()):

        if(not (cordsX<9 and cordsX>=0 and cordsY<9 and cordsY>=0 and _x<9 and _x>=0 and _y<9 and _y>=0) ):
            return False

        if((_x,_y)==(cordsX,cordsY)):
            return False

        #mediandte la formula de distancia se fabrica el patron del caballo, solo 5 es el unico
        #numero real que es valido
        if(((_x-cordsX)**2+(cordsY-_y)**2)==5):
            return True
        return False
    
    if(pieza.isAlfil()):
        if((_x,_y)==(cordsX,cordsY)):
            return False
        _x,_y=pos2
        if(not (cordsX<9 and cordsX>=0 and cordsY<9 and cordsY>=0 and _x<9 and _x>=0 and _y<9 and _y>=0) ):
            return False


        if((_y-cordsY)==0 or (_x-cordsX)==0):
            return False

        return (_y-cordsY)/(_x-cordsX)==1 or (_y-cordsY)/(_x-cordsX)==-1 and not((_y-cordsY)/(_x-cordsX)==0)

    return False
def generarPieza(mapa,position,type):
    #genera un objeto en esta cordenada de la matix
    x,y=position
    mapa[x][y]=PiezaC(type=type,cordenadas=position)
    return mapa

def cambiareljugador(mapa,PiezaAnterior : PiezaC,NuevaPieza: PiezaC):
    PiezaAnterior.jugador = False
    PiezaAnterior.Matar()
    NuevaPieza.jugador=True
    x,y=PiezaAnterior.cordenadas
    _x,_y=NuevaPieza.cordenadas
    mapa[x][y]=PiezaAnterior
    mapa[_x][_y]=NuevaPieza
    return mapa
    
def juego_mostrar(recuadro=(0,0),player=None,mapa=None,nivel=0):
    #esta sentencia es un if que me indica a mi como programador si me equivoque al usar esta funcion
    if mapa==None:
        print("Error mapa no asignado en render")
        exit()

    gamelib.draw_begin()
    for x in range (0,8):
        #esta variable trash no toma tanta importancia es hacer un patron de tablero de ajedres y toma de referencia el X y le suma 1 
        #asi siempre se asegura que se forme el patron de ajedrez
        _trash=x
        for y in range (0,8):
            if(_trash % 2 == 0):
                gamelib.draw_image('img/floor_gray.gif', x*44, y*44)
            else:
                gamelib.draw_image('img/floor_white.gif', x*44, y*44)
            _trash+=1
    _x,_y=recuadro

    #este ciclo de dos for se encarga de pintar las posiciones donde la ficha jugador puede saltar
    if(player!=None):
            for x in range(0,8):
                for y in range(0,8):
                    Pieza=mapa[x][y]
                    if(VerificarMovimiento(mapa,player,(x,y))):
                        gamelib.draw_image('img/floor_pink.gif', x*44, y*44)
                        gamelib.draw_rectangle(x*44, y*44, (x*44)+44, (y*44)+44, outline='orange', fill=None,width=2)
    #esta funcion renderiza el mapa
    for x in range(0,8):
        for y in range(0,8):
            Pieza : PiezaC =mapa[x][y]
            if(Pieza!=None):

                if(Pieza.isHorse() and Pieza.isAlive()):
                    if(Pieza.isPlayer()):
                        gamelib.draw_image('img/caballo_rojo.gif', x*44, y*44)
                    else:
                        gamelib.draw_image('img/caballo_blanco.gif', x*44, y*44)

                if(Pieza.isAlfil() and Pieza.isAlive()):
                    if(Pieza.isPlayer()):
                        gamelib.draw_image('img/alfil_rojo.gif', x*44, y*44)
                    else:
                        gamelib.draw_image('img/alfil_blanco.gif', x*44, y*44)

                if(Pieza.isTower() and Pieza.isAlive()):
                    if(Pieza.isPlayer()):
                        gamelib.draw_image('img/torre_rojo.gif', x*44, y*44)
                    else:
                        gamelib.draw_image('img/torre_blanco.gif', x*44, y*44)

    #Esta parte dibuja en pantalla las opciones usando un texto basico
    gamelib.draw_text(f'--r: reset  --s: save --Q: QUIT ',110,360)
    gamelib.draw_text(f'--n:nueva partida --F:rehacernivel', 125,380)
    gamelib.draw_text(f'Nivel: {nivel}', 300,380)
    gamelib.draw_end()

def GenerarNivel(mapa,N_nivel):
    #esta funcion se encarga de generar un nivel apartir de un algoritmo aleatorio
    #en donde crea una pieza inicial y si se puede mover a la pieza futura la pone en la lista y toma su lugar de inicial
    #asi la cadena de cumple con una probabilidad de 1/2 de colorcarse o no haciendo el mapa
    N=1
    generando=True
    bucle=0
    x,y=random.randint(0,7),random.randint(0,7)
    mapa=generarPieza(mapa,position=(x,y),type=tipos_de_piezas[random.randint(0,len(tipos_de_piezas)-1)])
    # print(mapa[x][y])
    while generando:
        for new_x in range(0,8):
            for new_y in range(0,8):
                if(puedeSpawnear(mapa,(x,y),(new_x,new_y)) and random.choice([True, False, False])):

                    mapa=generarPieza(mapa,position=(new_x,new_y),type=tipos_de_piezas[random.randint(0,len(tipos_de_piezas)-1)])
                    #print(mapa[new_x][new_y])
                    N+=1
                    #print("creando")
                    x = new_x
                    y = new_y

                    #debugcoment borrar
                    piezanueva : PiezaC= mapa[x][y]
                    if(piezanueva.isAlfil()):
                        debug=3


                    if(N==N_nivel):
                        return mapa
            bucle += 1
            if bucle > 6000:
                debug= 3
        
        #La funcion de este fragmento de codigo es identificar si el mapa llega a estar completo de piezas, donde aclara al inicio
        #una afirmacion y el for se encarga de refutarla, si es refutada una sola vez sigue el proceso pero si es cierta
        #retorna al mapa al no ser refutada porque esta llena y eso provocaria un bucle infinito
        
        LLeno=True
        for new_x in range(0,8):
            for new_y in range(0,8):
                if(mapa[new_x][new_y]==None):
                    LLeno=False
        if(LLeno):
            return mapa
            
def save(level):
    #esta funcion escribe un nuevo valor numerico que define el progreso
    f = open('LevelData.dat','w')
    f.write(str(level))
    f.close()

def load():
    #La funcion que cumple este fragmento de codigo leer el archivo LevelData.dat, el cual retorna un valor Int que significa el nivel
    f = open('LevelData.dat','r')
    nivel = str(f.read())
    return nivel
def ClearMapa():
    return [[None for x in range(8)] for y in range(8)]
def LevelEnd(mapa):
    numeroDePiezasVivas=0
    for x in range(0,8):
        for y in range(0,8):
            if(mapa[x][y]!=None):
                pieza : PiezaC = mapa[x][y]
                if(pieza.live):
                    numeroDePiezasVivas+=1
    if(numeroDePiezasVivas<2):
        return True
    return False
def main():
    #TODO: este es el metodo principal
    try:
        Nivel=int(load())
    except:
        gamelib.say("Archivo no creado creando nivel nuevo")
        Nivel=1
        save(1)

    mapa=[[None for x in range(8)] for y in range(8)]
    player_selected=False
    gamelib.title("Shape Shifter Chess")
    gamelib.resize(352, 390)
    mapa = GenerarNivel(mapa=mapa,N_nivel=Nivel+2)
    player=None
    #________________
    juego_mostrar(mapa=mapa)
    while gamelib.is_alive():
        if(LevelEnd(mapa)):

            #aca se resetean las variables y se regenera el mapa
            Nivel+=1
            mapa = ClearMapa()
            player = None
            player_selected=False
            mapa = GenerarNivel(mapa=mapa,N_nivel=Nivel+2)
        #OPTIMIZE: the code
        ev = gamelib.wait()
        if not ev:
            break
        if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1:

            if(player_selected):
                juego_mostrar(mapa=mapa,recuadro=(int(ev.x/44), int(ev.y/44)),player=player,nivel=Nivel)
            else:
                juego_mostrar(mapa=mapa,recuadro=(int(ev.x/44), int(ev.y/44)),nivel=Nivel)
            #print(f'se ha presionado el botón del mouse: {int(ev.x/44)} {int(ev.y/44)}')

            
            #_____________--
            recuadro=ev.x,ev.y
            if(int(ev.x/44)<8 and int(ev.y/44)<8):
                if(player_selected==False and mapa[int(ev.x/44)][int(ev.y/44)] != None):
                    player = int(ev.x/44),int(ev.y/44)
                    if(player!=None and mapa[int(ev.x/44)][int(ev.y/44)] != None and player_selected == False):
                        Pieza: PiezaC = mapa[int(ev.x/44)][int(ev.y/44)]
                        Pieza.jugador = True
                        
                        player_selected = True
                        mapa[int(ev.x/44)][int(ev.y/44)]=Pieza
                        print('jugador seleccionado')

                        # juego_mostrar(mapa=mapa,recuadro=(int(ev.x/44), int(ev.y/44)),nivel=Nivel)
                        juego_mostrar(mapa=mapa,recuadro=(int(ev.x/44), int(ev.y/44)),nivel=Nivel,player=player)
            if(player_selected and VerificarMovimiento(mapa,player,(int(ev.x/44),int(ev.y/44)))):
                """
                Aca en esta instruccion el jugador deja de ser jugador y la ficha muere , no se borra del todo por si se quiere hacer un reset del nivel y volver a revivir
                a las fichas en proximos cambios
                """
                xp,yp=player
                cambiareljugador(mapa,mapa[xp][yp],mapa[int(ev.x/44)][int(ev.y/44)]) 
                player=int(ev.x/44),int(ev.y/44)

        #HACK: XD
        elif ev.type == gamelib.EventType.KeyPress:
            #print(f'se ha presionado la tecla: {ev.key}')
            
            # con q se quita 
            if(ev.key == 'q' or ev.key == 'Q'):
                exit()
            if(ev.key == 'n' or ev.key == 'N'):
                #aqui se da el valor de 1 al archivo
                f = open('LevelData.dat','w')
                f.write(str(1))
                f.close()
                Nivel=1
                mapa = ClearMapa()
                player = None
                player_selected=False
                mapa = GenerarNivel(mapa=mapa,N_nivel=Nivel+2)
            # con r se resetea
            if(ev.key == 'r' or ev.key == 'R'):
                player=None
                player_selected=False
                for x in range(0,8):
                    for y in range(0,8):
                        if(mapa[x][y]!=None):
                            pieza : PiezaC = mapa[x][y]
                            pieza.jugador = False
                            pieza.Revivir()
                            mapa[x][y] = pieza
                juego_mostrar(mapa=mapa,recuadro=(int(ev.x/44), int(ev.y/44)),nivel=Nivel)
            if(ev.key == 's' or ev.key == 'S'):
                save(Nivel)
                gamelib.say("se ha guardado nivel")
            if(ev.key == 'f' or ev.key == 'F'):
                mapa = ClearMapa()
                player = None
                player_selected=False
                mapa = GenerarNivel(mapa=mapa,N_nivel=Nivel+2)
        juego_mostrar(mapa=mapa,recuadro=(int(ev.x/44), int(ev.y/44)),nivel=Nivel,player=player)
        
if __name__ == "__main__":
    gamelib.init(main)