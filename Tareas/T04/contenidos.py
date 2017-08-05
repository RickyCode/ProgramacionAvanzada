__author__ = 'Ricardo Del Rio'

from random import random, randint, uniform
from os import sep
from logging import getLogger, DEBUG, StreamHandler, Formatter

logger = getLogger(__name__)
logger.setLevel(DEBUG)
formatter = Formatter(
    '%(levelname)s[%(name)s, linea %(lineno)d]:   %(message)s ')
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class Contenido:
    '''
    Cada objeto de esta clase representa uno de los contenidos que se ven en el curso 'Avanzacion Programada'
    '''
    lista_contenidos = []

    def __init__(
            self,
            numero,
            nombre,
            dificultad,
            rango1,
            rango2,
            rango3,
            rango4):
        self.numero = numero
        self.nombre = nombre
        self.dificultad = dificultad
        self.rango1 = rango1
        self.rango2 = rango2
        self.rango3 = rango3
        self.rango4 = rango4
        Contenido.lista_contenidos.append(self)

    @staticmethod
    def importar_info_contenidos():
        '''
        Esta funcion obtiene los datos de los contenidos del curso.
        Cada linea del archivo 'contenidos.dsap' contiene una materia del curso con su informacion.
        Se crean los onjetos de la clase COntenido.
        '''
        with open('info' + sep + 'contenidos.dsap', 'r', encoding='utf-8') as archivo:
            contenidos = (linea.strip().split(',') for linea in archivo)
            for contenido in contenidos:
                if contenido[0][0] != '#':
                    Contenido(int(contenido[0].strip()),
                              contenido[1].strip(),
                              int(contenido[2].strip()),
                              contenido[3].strip(),
                              contenido[4].strip(),
                              contenido[5].strip(),
                              contenido[6].strip())
        Contenido.lista_contenidos.sort()

    def __str__(self):
        return '{} {} {} {} {} {} {}'.format(self.numero,
                                             self.nombre,
                                             self.dificultad,
                                             self.rango1,
                                             self.rango2,
                                             self.rango3,
                                             self.rango4)

    def __le__(self, otro):
        return self.numero <= otro.numero

    def __lt__(self, otro):
        return self.numero < otro.numero


if __name__ == '__main__':

    Contenido.importar_info_contenidos()
    print(len(Contenido.lista_contenidos))
    for contenido in Contenido.lista_contenidos:
        print(contenido)
