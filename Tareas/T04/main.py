__author__ = 'Rcardo Del Rio'

from random import randint, choice

from integrantes import Alumno, Profesor, AyudanteDocencia, AyudanteTarea, Coordinador
from evento import Evento, Evaluacion, semana, PublicacionNotas, EntregaNotasCoord
from contenidos import Contenido
from logging import getLogger, INFO, DEBUG, StreamHandler, Formatter

sim_logger = getLogger('SIMULACION')
sim_logger.setLevel(INFO)
formatter = Formatter('%(name)s %(message)s')
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)
sim_logger.addHandler(stream_handler)

logger = getLogger(__name__)
logger.setLevel(DEBUG)
formatter = Formatter(
    '%(levelname)s[%(name)s, linea %(lineno)d]:   %(message)s ')
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# sim_logger.info('[Día 1]: hola')
# sim_logger.info('[Día 2]: chao')


'''
COMENTARIOS
Archivos de datos = '.dsap' (Datos Simulacion Avanzacion Programada)
'''


class Simulacion:
    '''
    Esta clase es la encargada de llevar todos los procesos de la simulación.
    Lleva la linea temporal de está y ejecuta en orden los eventos correspondientes.
    '''

    def __init__(self):
        self.funciones = {1: self.actividad,
                          2: self.tarea,
                          3: self.control,
                          4: self.examen,
                          5: self.ayudantia,
                          6: self.catedra,
                          7: self.entrega_notas,
                          8: self.reunion_a_docencia,
                          9: self.reunion_a_tarea,
                          10: self.renuncia_ramos,
                          11: self.fiesta,
                          12: self.partido,
                          13: self.corte_agua,
                          14: self.publicacion_notas}

    def cargar_integrantes(self):
        '''
        Este método lee el archivo 'integrantes.csv' y crea un objeto de cada integrante en su clase correspondiente,
        el cual es almacenado en una lista de la clase (no de la instancia)
        '''
        with open('integrantes.csv', encoding='utf-8') as archivo:
            # Carga los alumnos
            alumnos = (
                filter(
                    lambda x: x[1] == 'Alumno',
                    (integrante.strip().split(',') for integrante in archivo)))
            for alumno in alumnos:
                Alumno(alumno[0], alumno[2])
            # Vuelve a la posicion inicial
            archivo.seek(0)
            # Carga los profesores
            profesores = (
                filter(
                    lambda x: x[1] == 'Profesor',
                    (integrante.strip().split(',') for integrante in archivo)))
            for profesor in profesores:
                Profesor(profesor[0], profesor[2])
            # Vuelve a la posicion inicial
            archivo.seek(0)
            # Carga los ayudantes
            ayudantes = (
                filter(
                    lambda x: (
                        (x[1] == 'Coordinación') or (
                            x[1] == 'Docencia') or (
                            x[1] == 'Tareas')),
                    (integrante.strip().split(',') for integrante in archivo)))
            for ayudante in ayudantes:
                if ayudante[1] == 'Coordinación':
                    Coordinador(ayudante[0], ayudante[2])
                elif ayudante[1] == 'Docencia':
                    AyudanteDocencia(ayudante[0], ayudante[2])
                elif ayudante[1] == 'Tareas':
                    AyudanteTarea(ayudante[0], ayudante[2])

    def run(self):
        self.cargar_integrantes()
        Contenido.importar_info_contenidos()
        Evento.creacion_primeros_eventos()
        while Evento.lista_eventos:
            Evento.seleccionar_evento()
            self.funciones[Evento.evento_actual.tipo]()
        examen = Evaluacion(4, Evento.evento_actual.tiempo + 5, choice(Contenido.lista_contenidos)) #Solo para mostrar, mal implemenado
        Evento.evento_actual = examen
        self.funciones[examen.tipo]()
        entrega_examen = EntregaNotasCoord(7, examen.tiempo + 14, (4,1))
        Evento.evento_actual = entrega_examen
        self.funciones[entrega_examen.tipo]()
        publicacion_examen = PublicacionNotas(14, entrega_examen.tiempo, (4, 1))
        Evento.evento_actual = publicacion_examen
        Evento.evento_actual.numero = 1000000
        self.funciones[publicacion_examen.tipo]()

    # AGRUPACIONES DE FUNCIONES DE CADA EVENTO: ------------------------------

    def actividad(self):
        '''
        Esta función desencadena todas las funciones que deben ejecutarse cuando se reliza una actividad.
        Define cuando serán los eventos de las proximas evaluaciones y de las entrega de notas de esta actividad.
        :return:
        '''
        evento = Evento.evento_actual
        # Ejecucion de funciones:
        for alumno in Alumno.lista_alumnos:
            alumno.calc_nota_actividad(evento.numero_tipo)
        # Creacion de proxima actividad:
        try:
            prox_fecha = evento.tiempo + 7
            prox_contenido = Contenido.lista_contenidos[semana(prox_fecha)]
            Evaluacion(1, prox_fecha, prox_contenido)
            # Creacion entrega notas actividad:
            fecha = evento.tiempo + 14
            EntregaNotasCoord(7, fecha, (1, evento.numero_tipo))
            # Logging
            sim_logger.info(
                '[Día {dia}]: Se realizó la actividad {numero}.'.format(
                    numero=evento.numero_tipo,
                    dia=evento.tiempo))
        except BaseException:
            pass

    def tarea(self):  # Entrega enunciado.
        '''
        Este metodo desencadena todas las funciones asociadas a la entrega del enunciado de la tarea.
        Se crean los futuros eventos que dependen de este.
        :return:
        '''
        # revisar: Pendiente considerar las dos semanas
        evento = Evento.evento_actual
        # Ejecucion de funciones:
        for alumno in Alumno.lista_alumnos:
            alumno.calc_nota_tarea(evento.numero_tipo)
        # Creación de entrega tarea: revisar:

        # Creacion de entrega proximo enunciado:
        try:
            prox_fecha = evento.tiempo + 14
            prox_contenido = Contenido.lista_contenidos[semana(prox_fecha)]
            Evaluacion(2, prox_fecha, prox_contenido)
            # Creación entrega de notas tarea:
            fecha = evento.tiempo + 14
            EntregaNotasCoord(7, fecha, (2, evento.numero_tipo))
            sim_logger.info(
                '[Día {dia}]: Se entregó el enunciado de la tarea {numero}.'.format(
                    numero=evento.numero_tipo, dia=evento.tiempo))
        except BaseException:
            pass

    def control(self):
        '''
        Este metodo desencadena todas las funciones asociadas a la entrega del enunciado del control.
        Se crean los futuros eventos que dependen de este.
        :return:
        '''
        evento = Evento.evento_actual

        # Ejecucion de funciones:
        for alumno in Alumno.lista_alumnos:
            alumno.calc_nota_control(evento.numero_tipo)
        # Creación entrega de notas control:
        fecha = evento.tiempo + 14
        EntregaNotasCoord(7, fecha, (3, evento.numero_tipo))
        sim_logger.info(
            '[Día {dia}]: Se realizó el control {numero}.'.format(
                numero=evento.numero_tipo,
                dia=evento.tiempo))

    def examen(self):
        '''
        Este metodo desencadena todas las funciones asociadas a la entrega del enunciado del examen.
        Se crean los futuros eventos que dependen de este.
        :return:
        '''
        evento = Evento.evento_actual
        # Ejecucion de funciones:
        for alumno in Alumno.lista_alumnos:
            alumno.calc_nota_examen(1)
        # Creacion entrega de notas examen:
        fecha = evento.tiempo + 14
        EntregaNotasCoord(7, fecha, (4, 1))
        sim_logger.info(
            '[Día {dia}]: Se realizó el exámen.'.format(
                dia=evento.tiempo))

    def ayudantia(self):
        '''
        Este metodo desencadena todas las funciones asociadas a la realizaciond e la ayudantía.
        Se crean los futuros eventos que dependen de este.
        :return:
        '''
        evento = Evento.evento_actual
        # Ejecucion de funciones:

        # Creacion proxima ayudantía:
        try:
            fecha = evento.tiempo + 7
            sim_logger.info('[Día {dia}]: Se realizo la ayudantía {numero}, acerca de {materia}.'.format(
                materia=Contenido.lista_contenidos[semana(evento.tiempo)].nombre, dia=evento.tiempo, numero=evento.numero_tipo))
            Evento(5, fecha)
        except BaseException:
            pass

    def catedra(self):
        '''
        Este metodo desencadena todas las funciones asociadas a la realizaciond e la catedra.
        Se crean los futuros eventos que dependen de este.
        :return:
        '''
        evento = Evento.evento_actual

        # Creacion proxima catedra:
        try:
            fecha = evento.tiempo + 7
            sim_logger.info('[Día {dia}]: Se realizó la catedra {numero}, acerca de {materia}.'.format(
                materia=Contenido.lista_contenidos[semana(evento.tiempo)].nombre, dia=evento.tiempo, numero=evento.numero_tipo))
            Evento(6, fecha)
        except BaseException:
            pass

    def entrega_notas(self):
        '''
        Este metodo desencadena todas las funciones asociadas a la entrega de notas.
        Se crean los futuros eventos que dependen de este.
        :return:
        '''
        evento = Evento.evento_actual
        # Ejecucion de funciones:
        se_descuenta = Coordinador.coordinador.recibir_notas()
        # Programar entrega de notas:
        if Coordinador.atrasar_notas:  # ojo: es una property, cada vez que se llama cambia su valor
            atraso = randint(2, 5)
            fecha = evento.tiempo + atraso
            PublicacionNotas(14, fecha, *evento.lista_ev_recibidas)
            msj_atraso = 'La entrega de notas se atrasa {} dias.'.format(
                atraso)
        else:
            PublicacionNotas(14, evento.tiempo, *evento.lista_ev_recibidas)
            msj_atraso = 'No se atrasa la entrega de notas.'
        if se_descuenta:
            msj_descuento = 'Se descontaron 5 decimas a todas las notas de esta entrega.'
        else:
            msj_descuento = 'No se descontó puntaje.'

        if evento.lista_ev_recibidas[0][0] == 4:
            msj_atraso = ''
            msj_descuento = ''

        evaluaciones = ''
        for notas in evento.lista_ev_recibidas:
            evaluaciones += '{} {}, '.format(Evento.tipos[notas[0]], notas[1])
        evaluaciones = evaluaciones[:-2]
        sim_logger.info(
            '[Día {dia}]: Se entregaron al coordinador las notas de {evaluacion}. {atraso} {descuento}'.format(
                evaluacion=evaluaciones,
                dia=evento.tiempo,
                atraso=msj_atraso,
                descuento=msj_descuento))

    def reunion_a_docencia(self):
        '''
        Este metodo desencadena todas las funciones asociadas a la reunion de los ayudantes de docencia.
        Se crean los futuros eventos que dependen de este.
        :return:
        '''
        evento = Evento.evento_actual

        # Proxima reunion:
        fecha = evento.tiempo + 7
        Evento(8, fecha)
        sim_logger.info(
            '[Día {dia}]: Reunión de ayudantes de docencia.'.format(
                dia=evento.tiempo))

    def reunion_a_tarea(self):
        '''
        Este metodo desencadena todas las funciones asociadas a la reunion de los ayudantes de tarea.
        Se crean los futuros eventos que dependen de este.
        :return:
        '''
        evento = Evento.evento_actual
        sim_logger.info(
            '[Día {dia}]: Raunión de ayudantes de tareas.'.format(
                dia=evento.tiempo))

    def renuncia_ramos(self):
        '''
        Este metodo desencadena todas las funciones asociadas a la renuncia de ramos.
        Se crean los futuros eventos que dependen de este.
        :return:
        '''
        evento = Evento.evento_actual
        for alumno in Alumno.lista_alumnos:
            alumno.evaluar_botar_ramo()
        sim_logger.info(
            '[Día {dia}]: Día de renuncia de ramos. {c_alumnos} estudiantes botaron Avazación Programada.'.format(
                dia=evento.tiempo, c_alumnos=Alumno.alumnos_botaron_ramo))

    def fiesta(self):
        evento = Evento.evento_actual
        sim_logger.info(
            '[Día {dia}]: Hubo una fiesta, asistieron 50 estudiantes.'.format(
                dia=evento.tiempo))

    def partido(self):
        evento = Evento.evento_actual
        sim_logger.info(
            '[Día {dia}]: Hubo un partido de fútbol.'.format(
                numero=evento.numero_tarea,
                dia=evento.tiempo))

    def corte_agua(self):
        evento = Evento.evento_actual
        sim_logger.info(
            '[Día {dia}]: Hoy hubo corte de agua.'.format(
                dia=evento.tiempo))

    def publicacion_notas(self):
        evento = Evento.evento_actual
        str_publicacion = ''
        for alumno in Alumno.lista_alumnos:
            confianza = alumno.confianza
        for tupla in Evento.evento_actual.lista_entregas:
            if tupla[0] == 1 and tupla[1] == 4:
                # Se programa la bota de ramos:
                Evento(10, evento.tiempo)
            str_publicacion += '{tipo_ev} {num}, '.format(tipo_ev=Evento.tipos[tupla[0]], num=tupla[1])

        str_publicacion = str_publicacion[:-2]
        sim_logger.info(
            '[Día {dia}]: Se publicaron las notas de: {evaluaciones}'.format(evaluaciones=str_publicacion, dia=evento.tiempo))


if __name__ == '__main__':
    s = Simulacion()
    s.run()
