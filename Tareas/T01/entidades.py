__author__ = 'Ricardo Del Rio'

from usuarios import Usuarios

class Entidad:
    lista_usuarios = None #Objeto de la clase Usuarios

    def __init__(self):
        pass



class ANAF(Entidad,Usuarios):
    def __init__(self):
        Usuarios.__init__(self)


class BrigadaANAF(Entidad,Usuarios):
    def __init__(self):
        Usuarios.__init__(self)
class Bomberos(Entidad,Usuarios):
    def __init__(self):
        Usuarios.__init__(self)

class Pilotos(Entidad,Usuarios):
    def __init__(self):
        Usuarios.__init__(self)