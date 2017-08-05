from edificios_unidades import Campeones, Subditos, Torre, Inhibidor, Nexo
from tienda import Tienda

from os import sep
from math import sqrt

from logging import getLogger, DEBUG, WARNING, ERROR, INFO
from loggers import archivo_logs, stream_handler, file_handler


# ------------------------------------------------------------------------------------------------------------- LOGGERS
archivo_logs()
info = getLogger('INFO [{}'.format(__name__))
info.setLevel(INFO)
info.addHandler(stream_handler)
info.addHandler(file_handler)
debug = getLogger('DEBUG [{}'.format(__name__))
debug.setLevel(DEBUG)
debug.addHandler(file_handler)
warning = getLogger('WARNING [{}'.format(__name__))
warning.setLevel(WARNING)
warning.addHandler(file_handler)
error = getLogger('ERROR [{}'.format(__name__))
error.setLevel(ERROR)
error.addHandler(file_handler)
# ------------------------------------------------------------------------------------------------------------- * * *

class ManejoDatos():

    # Base de datos partida --------------------------------------------------------------------------------------------

    def cargar_datos():
        # Carga los objetos de la tienda:
        habemus_tienda = False
        with open('INFO' + sep + 'tienda.csv', encoding='utf-8') as archivo:
            # Se crea la tienda:
            objetos = (objeto.strip().split(',') for objeto in archivo)
            # Se anhaden los objetos
            for objeto in objetos:
                if objeto[0] == '#':
                    pass
                if objeto[0] == 'tienda' and not habemus_tienda:
                    tienda = Tienda(*objeto)
                    habemus_tienda = True
                elif habemus_tienda:
                    tienda.anhadir_objeto(*objeto)
        # Carga edificios y unidades:
        debug.debug('En el archivo edificios_unidades.csv no está gusrdado que acción produce la habilidad especial')
        with open('INFO' + sep + 'edificios_unidades.csv', encoding='utf-8') as archivo:
            edificios_unidades = (ed_un.strip().split(',') for ed_un in archivo)
            for ed_un in edificios_unidades:
                # Carga campeones:
                if ed_un[0] == 'campeon':
                    Campeones.dic_campeones[ed_un[8]] = ed_un
                # Carga subditos:
                if ed_un[0] == 'subdito':
                    Subditos.dic_subditos[ed_un[8]] = ed_un
                # Carga torre:
                if ed_un[0] == 'torre':
                    Torre.formato_torre = ed_un
                # Carga inhibidor:
                if ed_un[0] == 'inhibidor':
                    Inhibidor.formato_inhibidor = ed_un
                # Carga nexo:
                if ed_un[0] == 'nexo':
                    Nexo.formato_nexo = ed_un
        # Carga partidas anteriores:
        with open('INFO' + sep + 'partida_guardada.csv', encoding='utf-8') as archivo:
            partidas_guardadas = [filter(lambda x: x[0] != '#', (partida.strip().split(',') for partida in archivo))]
            if len(partidas_guardadas) > 0:
                partidas_guardadas.sort(key=lambda x: x[0])
        info.info('Se han cargado todos los datos del juego')


    def borrar_datos():
        with open('INFO' + sep + 'partida_guardada.csv', 'w'):
            pass


    # ------------------------------------------------------------------------------------------------------------------


    def agregar_ultima_partida():
        debug.debug('Agregar el numero de partida')
        lista = [asesinatos, muertes, uso_habilidad, puntos_obtenidos, puntos_usados]
        partidas_guardadas.append(lista)


    def exportar_partidas():
        partidas_guardadas.sort()
        with open('INFO' + sep + 'partida_guardada.csv', 'w', encoding='utf-8') as archivo:
            archivo.write(
                '# NUMERO PARTIDA(5 la mas antigua), ASESINATOS, MUERTES, ACTIVACION HABILIDAD, PUNTOS OBTENIDOS, PUNTOS USADOS')
            for partida in partidas_guardadas:
                archivo.write(','.join(partida))