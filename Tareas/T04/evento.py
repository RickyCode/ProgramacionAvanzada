__author__ = 'Ricardo Del Rio'

from contenidos import Contenido
from random import random, randint
from logging import getLogger, DEBUG, StreamHandler, Formatter

logger = getLogger(__name__)
logger.setLevel(DEBUG)
formatter = Formatter(
    '%(levelname)s[%(name)s, linea %(lineno)d]:   %(message)s ')
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class Evento:
    '''
    Esta clase representa los eventos que se llevaran a cabo en la simulacion.
    '''
    lista_eventos = []
    eventos_ocurridos = []
    evento_actual = None
    tipos = {1: 'Actividad',
             2: 'Tarea',
             3: 'Control',
             4: 'Examen',
             5: 'Ayudantia',
             6: 'Catedra',
             7: 'Entrega de Notas Coordinador',
             8: 'Reunion Ayudantes Docencia',
             9: 'Reunion Ayudantes Tarea',
             10: 'Renuncia de Ramos',
             11: 'Fiesta',
             12: 'Partido de Fútbol',
             13: 'Corte de Agua',
             14: 'Publicación de Notas',
             15: 'Reunion Profesor',
             16: 'Entrega Tarea'}

    def __init__(self, tipo, tiempo):
        self.tiempo = tiempo
        self.tipo = tipo
        try:
            self.numero_tipo = next(contadores[self.tipo])
        except:
            pass
        self.__numero = None
        # revisar: ¿Se añaden os eventos tipo evaluaciones y entrega de notas?
        Evento.lista_eventos.append(self)

    @property
    def numero(self):
        '''
        Retorna el valor de la variable '__numero'
        SI aún no se le asigna un numero al evento levanta un error.
        :return int:
        '''
        if self.__numero:
            return self.__numero
        else:
            raise ValueError('No se ha asignado un numero a este evento.')

    @numero.setter
    def numero(self, valor):
        '''
        Se le asigna el valor 'valor' a la variable '__numero'
        :param valor:
        :return:
        '''
        self.__numero = valor

    @staticmethod
    def creacion_primeros_eventos():
        '''
        Se crean los eventos que pueden crearse al comienzo de la simulación.
        :return:
        '''
        # Actividades:
        fecha = 4  # Considerando la primera actividad el primer jueves
        contenido = Contenido.lista_contenidos[1]
        Evaluacion(1, fecha, contenido)

        # Controles:
        c_controles = 0
        fecha = 11  # Considerando el primer control el segundo jueves
        fechas_controles = []
        while (c_controles < 5) and semana(fecha) < 12:
            if (fecha - 7) in fechas_controles:
                pass
            else:
                num = random()
                if num <= 0.7:
                    Evaluacion(
                        3, fecha, Contenido.lista_contenidos[semana(fecha)])
                    c_controles += 1
            fecha += 7
        # Si es que no se distribuyeron los 5 controles en el maximo de tiempo
        # posible.
        if c_controles < 5:
            fecha = 11
            while c_controles < 5:
                if (fecha - 7) in fechas_controles:
                    pass
                else:
                    Evaluacion(
                        3, fecha, Contenido.lista_contenidos[semana(fecha)])
                    c_controles += 1
                fecha += 7

        # Tarea (Entrega de enunciado)
        fecha = 1
        Evaluacion(2, fecha, Contenido.lista_contenidos[semana(fecha)])

        # Ayudantias:
        fecha = 2  # La primera ayudantia es el primer martes
        Evento(5, fecha)

        # Catedra:
        fecha = 4  # La primera catedra es el primer jueves
        Evento(6, fecha)

    def __le__(self, other):
        '''
        Se compara que evento es menor o igual que otro en base al tiempo en el que deben ejecutarse.
        :param other:
        :return bool:
        '''
        return self.tiempo <= other.tiempo

    def __lt__(self, other):
        return self.tiempo < other.tiempo

    @staticmethod
    def seleccionar_evento():
        '''
        Se ordena la lista segun el tiempo en el que debe producirse un evento.
        Se selecciona el proximo evento que debe ocurrir.
        Se le asigna un numero al evente, que representa el numero de evento en ser ejecutado
        :return:
        '''
        Evento.lista_eventos.sort()
        Evento.evento_actual = Evento.lista_eventos.pop(0)
        Evento.evento_actual.numero = next(num_evento)
        Evento.eventos_ocurridos.append(Evento.evento_actual)

    @staticmethod
    def ejecutar_evento():
        for funcion in Evento.evento_actual.funciones:
            funcion()


class Evaluacion(Evento):
    def __init__(self, tipo, tiempo, contenido):
        super().__init__(tipo, tiempo)
        self.exigencia = 7 + (randint(1, 5) / contenido.dificultad)
        self.cont_a_evaluar = contenido

class PublicacionNotas(
        Evento):
    publicaciones = []

    def __init__(self, tipo, tiempo, *args):
        '''
        Este metodo crea los objetos de la clase PublicacionNotas.
        Si ya hay una publicación de notas programada para para el mismo, día, no se crea una nueva,
        sino que a la existente se le agregan las evaluaciones que serán entregadas en dicha fecha.
        :param tipo:
        :param tiempo:
        :param args:
        '''
        si_estaba = False
        for publicacion in PublicacionNotas.publicaciones:
            if publicacion.tiempo == tiempo:
                publicacion.agregar_evaluacion(*args)
                si_estaba = True

        if not si_estaba:
            super().__init__(tipo, tiempo)
            # args debe ser una tupla de tuplas: (tipo evaluacion, numero
            # tipo evaluacion) Ej: (actividad, 3)
            self.lista_entregas = list(args)
            PublicacionNotas.publicaciones.append(self)

    def agregar_evaluacion(self, tupla):
        self.lista_entregas.append(tupla)


class EntregaNotasCoord(Evento):
    def __init__(self, tipo, tiempo, *args):
        super().__init__(tipo, tiempo)
        self.lista_ev_recibidas = args


# ----------------------------------------------------------------------------------------------------------------------

def gen_numero():
    '''
    Esta funcion es un generador de numeros para los eventos.
    A cada evento solo se le debe asignar un numero en el momento en el que se realiza dicho evento.
    Este numero esta pensado para que las properties puedan verificar si su valor se encuentra actualizado.
    También se usa para que cada evaluacion y cada tipo de evento tenga su propia secueciade numeros.
    :return int:
    '''
    numero = 0
    while True:
        numero += 1
        yield numero


def semana(dia):
    '''
    Esta función calcula a que semana pertenece cierto día.
    Usada para ver que contenido se está viendo.
    :param dia:
    :return:
    '''
    return (dia // 7) + 1


num_evento = gen_numero()
num_actividad = gen_numero()
num_tarea = gen_numero()
num_control = gen_numero()
num_ayudantia = gen_numero()
num_catedra = gen_numero()
num_entrega_de_notas_coord = gen_numero()
num_reunion_docencios = gen_numero()
num_reunion_tareos = gen_numero()
num_fiesta = gen_numero()
num_partido = gen_numero()
num_corte_agua = gen_numero()
num_publicacion_notas = gen_numero()

contadores = {1: num_actividad,
              2: num_tarea,
              3: num_control,
              4: 1,
              5: num_ayudantia,
              6: num_catedra,
              7: num_entrega_de_notas_coord,
              8: num_reunion_docencios,
              9: num_reunion_tareos,
              10: 1,
              11: num_fiesta,
              12: num_partido,
              13: num_corte_agua,
              14: num_publicacion_notas}


if __name__ == '__main__':
    print(next(num_evento))
    print(next(num_actividad))
    print(next(num_tarea))
    print(next(num_control))
    print(next(num_ayudantia))
    print(next(num_catedra))
    print(next(num_entrega_de_notas_coord))
    print(next(num_reunion_docencios))
    print(next(num_reunion_tareos))
    print(next(num_fiesta))
    print(next(num_partido))
    print(next(num_corte_agua))
    print(next(num_publicacion_notas))
    print()
    print(next(num_evento))
    print(next(num_actividad))
    print(next(num_tarea))
    print(next(num_control))
    print(next(num_ayudantia))
    print(next(num_catedra))
    print(next(num_entrega_de_notas_coord))
    print(next(num_reunion_docencios))
    print(next(num_reunion_tareos))
    print(next(num_fiesta))
    print(next(num_partido))
    print(next(num_corte_agua))
    print(next(num_publicacion_notas))
