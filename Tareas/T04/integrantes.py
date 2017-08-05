__author__ = 'Ricardo Del Rio'

from random import choice, random, randint, uniform, triangular
from contenidos import Contenido
from evento import Evento, semana
from logging import getLogger, DEBUG, StreamHandler, Formatter

logger = getLogger(__name__)
logger.setLevel(DEBUG)
formatter = Formatter(
    '%(levelname)s[%(name)s, linea %(lineno)d]:   %(message)s ')
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

'''
COMENTARIOS
-Prefijos Usados:
    act = actualizar
    det = determinar
    calc = calcular
'''

# ----------------------------------------------------------------------------------------------------------------------


class Integrante():
    '''
    Esta clase representa a todos los integrantes del ramo 'Avanzación Programada'.
    '''

    def __init__(self, nombre, seccion=None):
        self.nombre = nombre
        self.seccion = seccion

# ----------------------------------------------------------------------------------------------------------------------


class Alumno(Integrante):
    '''
    Esta clase representa a los alumnos del curso.
    '''
    lista_alumnos = []
    personalidades = {1: 'eficiente', 2: 'artistico', 3: 'teorico'}
    alumnos_botaron_ramo = 0

    def __init__(self, nombre, seccion=None):
        Integrante.__init__(self, nombre, seccion)
        # Parametros que se fijan una sola vez:
        self.numero_lista = None
        self.cant_creditos = 0
        self.det_cant_creditos()
        self.personalidad = Alumno.personalidades[randint(1, 3)]
        # Cada lista mas interna es: [nota_esperada, nota_final] y el numero de
        # la evaluacion ee la posicion +1
        self.notas_actividades = [
            [
                None, None], [
                None, None], [
                None, None], [
                    None, None], [
                        None, None], [
                            None, None], [
                                None, None], [
                                    None, None], [
                                        None, None], [
                                            None, None], [
                                                None, None], [
                                                    None, None]]
        self.notas_tareas = [
            [
                None, None], [
                None, None], [
                None, None], [
                    None, None], [
                        None, None], [
                            None, None]]
        self.notas_controles = [[None, None], [None, None], [
            None, None], [None, None], [None, None]]
        self.nota_examen = [None, None]
        self.boto_ramo = False
        # notas = {Actividad: {1: [esperada, final], 2: }, Tarea: {}, Control:
        # {}, Examen {}}      }

        # PROPERTIES QUE SE MODIFICAN CONSTANTEMENTE:
        # Tienen la forma: [valor, ultimo tiempo en que se modificó]
        self.__horas_estudio = [None, 0]
        self.__confianza = [uniform(2, 12), 0]  # [valor, numero evento]
        self.__manejo_de_contenidos = [None, 0]
        self.__nivel_de_programacion = [
            uniform(2, 10), 0]  # Se calcula semanalmente
        self.__nota_esperada = [None, 0]
        # OTROS VALORES QUE CAMBIAN CONSTANTEMENTE
        self.escucho_tips_clase = [False, 0]
        # revisar: No puede visitar al profesor dos semanas seguidas
        self.reunion_profesor = [False, 0]
        self.fiesta = [False, 0]
        # Se anade al alumno a la lista de alumnos:
        Alumno.lista_alumnos.append(self)

    @property
    def horas_semana(self):
        '''
        Determina la cantidad de horas que el estudiante dedicará al curso en la semana actual
        Devulve el valor correspondiente cada vez que se llama a horas_semana
        :return:
        '''
        if actualizado_semana(self.__horas_estudio[1]):
            return self.__horas_estudio[0]
        else:
            if self.cant_creditos == 40:
                self.__horas_estudio[0] = randint(10, 25)
            elif self.cant_creditos == 50:
                self.__horas_estudio[0] = randint(10, 15)
            elif self.cant_creditos == 55:
                self.__horas_estudio[0] = randint(5, 15)
            elif self.cant_creditos == 60:
                self.__horas_estudio[0] = randint(5, 10)
            # Actualizamos el tiempo de la ultima modificacion
            self.__horas_estudio[1] = Evento.evento_actual.tiempo

            return self.__horas_estudio[0]

    @property
    def confianza(self):
        '''
        Esta property mantiene actualizado el valor de la confianza cada verz que hay una entrega de notas
        :return:
        '''
        # Revisa si el valor esta actualizado, sino, lo actualiza:
        n_evento = Evento.evento_actual.numero
        evento_ult_act = self.__confianza[1]
        # revisar: Asegurarse que siempre que hay un evento 'entrega de notas'
        # se llame a la property 'confianza'
        if (evento_ult_act <
                n_evento) and Evento.evento_actual.tipo == 7:  # Es una entrega de notas
            self.__confianza += self.__act_confianza()
            # Ultimo evento que modifico la variable:
            self.__confianza[1] = Evento.evento_actual.numero
        return self.__confianza[0]

    @property
    def manejo_contenidos(self):
        if esta_actualizado(self.__manejo_de_contenidos[1]):
            return self.__manejo_de_contenidos[0]
        else:
            dificultad = Contenido.lista_contenidos[semana(
                Evento.evento_actual.tiempo)].dificultad
            self.__manejo_de_contenidos[0] = (
                1 / dificultad) * self.horas_semana
            self.__manejo_de_contenidos[1] = Evento.evento_actual.tiempo
            return self.__manejo_de_contenidos[0]

    @property
    def nivel_programacion(self):
        '''
        Actualiza la variable 'nivel_de_programacion' en base a los casos y la formula dada.
        :return float:
        '''
        if actualizado_semana(self.__nivel_de_programacion[1]):
            return self.__nivel_de_programacion[1]
        else:
            # Se define la variable 'v':
            if self.reunion_profesor:
                v = 0.08
            else:
                v = 0
            # Se define la variable 'w':
            if self.fiesta:
                w = 0.15
            else:
                w = 0
            # Se define la formula:
            self.__nivel_de_programacion[0] = 1.05 * \
                (1 + v + w) * self.__nivel_de_programacion[0]
            self.__nivel_de_programacion[1] = Evento.evento_actual.tiempo
            return self.__nivel_de_programacion[0]

    @property
    def nota_esperada(self):
        '''
        Esta property revisa cual es el contenido que se esta pasando actualmente llamando a la variable
        'contenido_actual' de la clase Contenido.
        Llama a la función del objeto 'Contenido' que permite calcular la nota esperada del alumno en base a la cantidad
        de horas que dedico al estudio de la materia. Se actualiza la variable 'nota_esperada' con el retorno de dicha
        funcion.
        :return:
        '''
        # Revisa si el valor esta actualizado, sino, lo actualiza:
        n_evento = Evento.evento_actual.numero
        evento_ult_act = self.__confianza[1]
        eventos_evaluaciones = [1, 2, 3, 4]
        # revisar: Asegurarse que siempre que hay un evento 'evaluacion' se
        # llame a la property 'nota esperada'
        if (evento_ult_act < n_evento) and (
                Evento.evento_actual.tipo in eventos_evaluaciones):  # Es una evaluacion
            n_contenido = semana(Evento.evento_actual.tiempo)
            contenido = Contenido.lista_contenidos[n_contenido]
            dia_de_la_semana = Evento.evento_actual.tiempo % 7
            horas_hasta_dia = (self.horas_semana / 7) * dia_de_la_semana
            if horas_hasta_dia <= int(contenido.rango1[-1]):
                self.__nota_esperada[0] = round(uniform(1, 3.9), 2)
            elif horas_hasta_dia <= int(contenido.rango2[-1]):
                self.__nota_esperada[0] = round(uniform(4, 5.9), 2)
            elif horas_hasta_dia <= int(contenido.rango3[-1]):
                self.__nota_esperada[0] = round(uniform(6, 6.9), 2)
            elif horas_hasta_dia >= int(contenido.rango4[-1]):
                self.__nota_esperada[0] = 7
            self.__nota_esperada[1] = Evento.evento_actual.numero
        return self.__nota_esperada[0]

    # Progresos tareas

    @property
    def progreso_act_actual(self):
        __PEP8 = (0.7 * self.manejo_contenidos) + \
            (0.2 * self.nivel_programacion) + (0.1 * self.confianza)
        __funcionalidad = (0.3 * self.manejo_contenidos) + \
            (0.7 * self.nivel_programacion) + (0.1 * self.confianza)
        __contenidos = (0.7 * self.manejo_contenidos) + \
            (0.2 * self.nivel_programacion) + (0.1 * self.confianza)
        return (0.2 * __PEP8) + (0.4 * __funcionalidad) + (0.4 * __contenidos)

    @property
    def progreso_tarea_actual(self):
        __horas = self.horas_estudio * 0.7
        __PEP8 = (0.5 * __horas) + (0.2 * self.nivel_programacion)
        __contenido = (0.7 * self.manejo_contenidos) + \
            (0.1 * self.nivel_programacion) + (0.2 * __horas)
        __funcionalidad = (0.5 * self.manejo_contenidos) + \
            (0.1 * self.nivel_programacion) + (0.4 * __horas)
        return (0.2 * __PEP8) + (0.4 * __contenido) + (0.4 * __funcionalidad)

    @property
    def progreso_control_actual(self):
        __contenidos = (0.7 * self.manejo_contenidos) + (0.05 * \
                        self.nivel_programacion) + (0.25 * self.confianza)
        __funcionalidad = (0.3 * self.manejo_contenidos) + \
            (0.2 * self.nivel_programacion) + (0.5 * self.confianza)
        return (0.7 * __contenidos) + (0.3 * __funcionalidad)

    @property
    def progreso_examen(self):
        # revisar: falta implementar, recordar que el progreso es por pregunta.
        __contenidos = 0
        __funcionalidad = 0
        return (0.7 * __contenidos) + (0.3 * __funcionalidad)

    def det_cant_creditos(self):
        '''
        Este asigna una cantidad de creditos a un estudiante en base a la probabilidad dada.
        Se debe utilizar solamente cuando se crea un nuevo objeto 'Alumno'.
        :return:
        '''
        num = random()
        if num <= 0.1:
            self.cant_creditos = 40
        elif num <= 0.8:
            self.cant_creditos = 50
        elif num <= 0.95:
            self.cant_creditos = 55
        elif num <= 1:
            self.cant_creditos = 55

    def __act_confianza(self):
        '''
        Actualiza el nivel de confanza del alumno según la formula dada.
        :return:
        '''
        # Definicion de variables
        for tupla in Evento.evento_actual.lista_entregas:
            if tupla[0] == 1:  # actividad
                # Nota final actividad
                Naf = self.notas_actividades[tupla[1] - 1][1]
                # Nota esperada actividad
                Nae = self.notas_actividades[tupla[1] - 1][0]
            elif tupla[0] == 2:  # tarea
                Ntf = self.notas_actividades[tupla[1] - 1][1]
                Nte = self.notas_actividades[tupla[1] - 1][0]
            elif tupla[0] == 3:  # control
                Ncf = self.notas_actividades[tupla[1] - 1][1]
                Nce = self.notas_actividades[tupla[1] - 1][0]
        # Deiniendo x:
        if Naf:
            x = 1
        else:
            x = 0
        # Definiendo y:
        if Ntf:
            y = 1
        else:
            y = 0
        # Definiendo z:
        if Ncf:
            z = 1
        else:
            z = 0
        # Calculando y modificando:
        confianza_notas = 3 * x * (Naf - Nae) + 5 * \
            y * (Ntf - Nte) + z * (Ncf - Nce)
        return confianza_notas

    def duda_catedra(self):
        '''
        Este metodo selecciona a uno de los tres ayudantes de la seccion que estan en la catedra.
        Si el ayudante ya resolvio 200 dudas, seleccionara al siguiente y así hasta haber seleccionado a los 3 o haber
        resuelto la duda.
        Si un ayudante resuelve una duda, el manejo de contenidos del estudiante aumenta un 1%
        :return:
        '''
        resuelto = False
        n = 1
        while n <= 3 and not resuelto:
            ayudante = AyudanteDocencia.ayudantes_secciones[self.seccion][n]
            try:
                ayudante.resolver_dudas()
                self.__manejo_de_contenidos *= 1.1  # Aumenta el manejo de contenidos en un 1%
                resuelto = True
            except BaseException:
                pass
            n += 1

    def calc_nota_actividad(self, numero):
        # revisar: en caso de que exista la posibilidad de que hayan más
        # evaluaciones que la cantidad que se fijaron en un ptrincipio, el
        # programa deberá agregarlas haciendo append[nota esperada, nota final]
        num = semana(Evento.evento_actual.tiempo)
        exigencia = 7 + (randint(1, 5) /
                         Contenido.lista_contenidos[num].dificultad)
        self.notas_actividades[numero -
                               1][1] = round(max((self.progreso_act_actual /
                                                  exigencia) *
                                                 7, 1), 2)

    def calc_nota_tarea(self, numero):
        num = semana(Evento.evento_actual.tiempo)
        exigencia = 7 + (randint(1, 5) /
                         Contenido.lista_contenidos[num].dificultad)
        self.notas_tareas[numero -
                          1][1] = round(max((self.progreso_act_actual /
                                             exigencia) *
                                            7, 1), 2)

    def calc_nota_control(self, numero):
        num = semana(Evento.evento_actual.tiempo)
        exigencia = 7 + (randint(1, 5) /
                         Contenido.lista_contenidos[num].dificultad)
        self.notas_controles[numero -
                             1][1] = round(max((self.progreso_control_actual /
                                                exigencia) *
                                               7, 1), 2)

    def calc_nota_examen(self, numero):
        self.nota_examen[1] = 4  # revisar: esto esta mal, solo para probar

    def entrega_tarea(self):
        pass

    def catedra(self):
        '''
        Este metodo define cuantas veces el estudiante pedirá ayuda durante la catedra.
        Llama a la función que hace que el estudiante resuelva sus dudas la cantidad de veces que se establecen.
        :return:
        '''
        solicitud_de_ayuda = triangular(1, 10, 3)
        for i in range(solicitud_de_ayuda):
            self.duda_catedra()

    def evaluar_botar_ramo(self):
        sum_notas = 0
        for notas in self.notas_actividades:
            if notas[1]:
                sum_notas += notas[1]
        for notas in self.notas_tareas:
            if notas[1]:
                sum_notas += notas[1]
        for notas in self.notas_controles:
            if notas[1]:
                sum_notas += notas[1]
        s = (self.confianza * 0.8) + (sum_notas * 0.2)
        if s < 20:
            self.boto_ramo = True
            Alumno.alumnos_botaron_ramo += 1

        s = (self.confianza * 0.8) + (sum_notas*0.2)

    def __le__(self, other):
        return self.nombre <= other.nombre


# ----------------------------------------------------------------------------------------------------------------------

class Profesor(Integrante):
    dict_profesores = {}
    '''
    Esta clase representa a los profesores del curso.
    '''

    def __init__(self, nombre, seccion=None):
        Integrante.__init__(self, nombre, seccion)
        self.dia_consultas_alumnos = None
        self.alumnos_quieren_reunion = []
        self.alumnos_semana = []
        Profesor.dict_profesores[seccion] = self

    def elegir_estudiantes(self):
        self.alumnos_semana = []
        if len(self.alumnos_quieren_reunion) > 10:
            while len(self.alumnos_semana) < 10:
                self.alumnos_semana.append(self.alumnos_quieren_reunion.pop(
                    randint(0, len(self.alumnos_quieren_reunion) - 1)))
        else:
            self.alumnos_semana = self.alumnos_quieren_reunion

    def atender_alumnos(self):
        for alumno in self.alumnos_semana:
            alumno.reunion_profesor = True


# ----------------------------------------------------------------------------------------------------------------------

class AyudanteTarea(Integrante):
    '''
    Esta clase representa a los ayudantes de tareas del curso.
    '''
    ayudantes_tareas = []

    def __init__(self, nombre, seccion=None):
        Integrante.__init__(self, nombre, seccion)
        AyudanteTarea.ayudantes_tareas.append(self)


class AyudanteDocencia(Integrante):
    '''
    Esta clase representa a los ayudantes de docencia del curso.
    '''
    ayudantes_docencia = []
    ayudantia = []
    ayudantes_secciones = {}

    def __init__(self, nombre, seccion=None):
        Integrante.__init__(self, nombre, seccion)
        AyudanteDocencia.ayudantes_docencia.append(self)
        self.__ayudados = 0
        self.__dudas_resueltas = 0
        self.contenidos_destacados = []

    @staticmethod
    def quien_hara_ayudantia():
        '''Este metodo selecciona a los ayudantesque haran la ayudantía de la semana'''
        # Se limpia la lista
        AyudanteDocencia.ayudantia = []
        # Se selecciona al primer ayudante
        AyudanteDocencia.ayudantia.append(
            choice(AyudanteDocencia.ayudantes_docencia))
        # Se selecciona al segundo:
        stop = False
        while not stop:
            ayudante = choice(AyudanteDocencia.ayudantes_docencia)
            if ayudante not in AyudanteDocencia.ayudantia:
                AyudanteDocencia.ayudantia.append(ayudante)
                stop = True

    @staticmethod
    def ayudantes_por_seccion():
        '''Este metodo selecciona a los ayudantes que iran a cada seccion de la catedra'''
        seleccionados = []
        AyudanteDocencia.ayudantes_secciones.clear()
        AyudanteDocencia.ayudantes_secciones[1] = []
        AyudanteDocencia.ayudantes_secciones[2] = []
        AyudanteDocencia.ayudantes_secciones[3] = []
        while len(seleccionados) < 9:
            ayudante = choice(AyudanteDocencia.ayudantes_docencia)
            if ayudante not in seleccionados:
                seleccionados.append(ayudante)
        for i in range(3):
            AyudanteDocencia.ayudantes_secciones[1].append(seleccionados.pop())
            AyudanteDocencia.ayudantes_secciones[2].append(seleccionados.pop())
            AyudanteDocencia.ayudantes_secciones[3].append(seleccionados.pop())

    @property
    def dudas_resueltas(self):
        '''
        Esta property representa la cantidad de veces que el ayudante ha resueto dudas.
        :return:
        '''
        return self.__dudas_resueltas

    def resolver_dudas(self):
        '''
        Se evita que el ayudante resuelva más dudas que el maximo permitido.
        :return:
        '''
        if self.__dudas_resueltas < 200:
            self.__dudas_resueltas += 1
        else:
            raise ValueError('Se han resuelto el máximo de dudas')

    def selec_contenidos_destacados(self):
        '''
        Se seleccionan los 3 contenidos que el ayudante domina mejor.
        :return:
        '''
        while len(self.contenidos_destacados) < 3:
            contenido = choice(Contenido.lista_contenidos)
            if contenido in self.contenidos_destacados:
                pass
            else:
                self.contenidos_destacados.append(contenido)


class Coordinador(Integrante):
    '''
    Esta clase representa al ayudante coordinador del curso.
    '''
    coordinador = None

    def __init__(self, nombre, seccion=None):
        Integrante.__init__(self, nombre, seccion)
        self.c_descuentos = 0
        self.fecha_ultimo_descuento = None
        Coordinador.coordinador = self

    @property
    def atrasar_notas(self):
        num = random()
        if num <= 0.1:
            return True
        return False

    @property
    def descontar_notas(self):
        if self.c_descuentos == 3:
            return False
        # Debe revisar que no vuelva a pasar en menos de un mes (revisar:)
        # if self.fecha_ultimo_descuento - fecha_actual > 1 mes:
        #     pass
        num = random()
        if num <= 0.5:
            self.c_descuentos += 1
            return True
        return False

    def recibir_notas(self):
        evento = Evento.evento_actual
        if self.descontar_notas:
            for alumno in Alumno.lista_alumnos:
                for notas in evento.lista_ev_recibidas:
                    if notas[0] == 1:
                        alumno.notas_actividades[notas[1] - 1][1] -= 0.5
                    elif notas[0] == 2:
                        alumno.notas_tareas[notas[1] - 1][1] -= 0.5
                    elif notas[0] == 3:
                        alumno.notas_controles[notas[1] - 1][1] -= 0.5
                    return True
        return False


# ----------------------------------------------------------------------------------------------------------------------

def esta_actualizado(tiempo):
    t_actual = Evento.evento_actual.tiempo
    if tiempo < t_actual:
        return False
    return True


def actualizado_semana(tiempo):
    if tiempo == 0:
        return False
    t_actual = Evento.evento_actual.tiempo
    s_actual = (t_actual // 7) + 1
    s_ultima_act = (tiempo // 7) + 1
    if s_ultima_act < s_actual:
        return False
    return True
