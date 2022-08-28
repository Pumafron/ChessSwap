class Pieza():
    piezaCaballo = "caballo"
    piezaAlfil = "alfil"
    piezaTorre = "torre"
    def __init__(self,type: str, cordenadas : tuple, live: bool = True, jugador: bool = False):
        self.type = type
        self.cordenadas = cordenadas
        self.live = live
        self.jugador = jugador

    def Revivir(self):
        self.live =True

    def Matar(self):
        self.live =False

    def isDeath(self):
        if(self.live == False):
            return True
        else:
            return False

    # aca es para comprobar partes de el objeto

    def isTower(self):
        if(self.type==self.piezaTorre):
            return True
        return False
    
    def isHorse(self):
        if(self.type==self.piezaCaballo):
            return True
        return False
    
    def isAlfil(self):
        if(self.type==self.piezaAlfil):
            return True
        return False
    #en si es lo mismo que leer live pero esto es para dar una definicion clara de la intencion del codigo
    def isAlive(self):
        return self.live
    
    def isPlayer(self):
        return self.jugador