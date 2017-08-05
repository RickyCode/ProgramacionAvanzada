# from T05_GUI import *

# COsas que podria usar:
# Progres dialog
# Tabbar
# TabWidget
# whatsthis

from PyQt5 import QtTest
from PyQt5.QtCore import QThread, QThreadPool, QTime
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtWidgets # revisar:

from logging import getLogger, DEBUG, WARNING, ERROR, INFO
from loggers import archivo_logs, stream_handler, file_handler

from edificios_unidades import Campeones, Subditos, Torre, Inhibidor, Nexo
from tienda import Tienda

from os import sep
from math import sqrt


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

class Juego(QThread, QtWidgets.QDialog):
    def __init__(self, tamanho, objetos):
        self.tamanho = tamanho
        self.objetos = objetos
        # self.ui = T05_GUI()
        self.ui.setupUi(self)
        # Elementos del juego:
        self.tienda = None
        # Partida guardada:
        self.partidas_guardadas = []
        self.asesinatos = 0
        self.muertes = 0
        self.uso_habilidad = 0
        self.puntos_obtenidos = 0
        self.puntos_usados = 0

    warning.warning('Sacado del tetris. REVISAR Y MODIFICAR')
    def keyPressEvent(self, event):
        # if not self.isStarted or self.curPiece.shape() == Tetrominoe.NoShape:
        #     super(Board, self).keyPressEvent(event)
        #     return
        key = event.key()
        if key == Qt.Key_P:
            self.pause()
            return
        if self.isPaused:
            return
        elif key == Qt.Key_W:
            pass
            # self.tryMove(self.curPiece, self.curX - 1, self.curY)
        elif key == Qt.Key_A:
            pass
            # self.tryMove(self.curPiece, self.curX + 1, self.curY)
        elif key == Qt.Key_S:
            pass
            # self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)
        elif key == Qt.Key_D:
            pass
            # self.tryMove(self.curPiece.rotateLeft(), self.curX, self.curY)
        else:
            pass
            # super(Board, self).keyPressEvent(event)

    warning.warning('Completar')
    def checkear_colision(self, unidad):
        for objeto in self.objetos:
            if unidad:
                pass

    def checkear_destino(self, coord_destino):
        return coord_destino in [objeto.posicion for objeto in self.objetos]

    def esta_arriba_izq(self, coord1, coord2):
        return (coord1[0] < coord2[0]) or (coord1[1] < coord2[1])


    def checkear_rango(self, unidad, ):
        rango = unidad.rango_ataque
        for objeto in self.objetos:
            distancia = self.distancias_entre_objetos(objeto, unidad)
            if distancia <= rango:
                warning.warning('Completar')
                pass

    def distancias(self, coord1, coord2):
        x1, y1 = coord1.posicion
        x2, y2 = coord2.posicion
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # Base de datos partida --------------------------------------------------------------------------------------------

    def cargar_datos(self):
        # Carga los objetos de la tienda:
        habemus_tienda = False
        with open('INFO'+sep+'tienda.csv', encoding='utf-8') as archivo:
            # Se crea la tienda:
            objetos = (objeto.strip().split(',') for objeto in archivo)
            # Se anhaden los objetos
            for objeto in objetos:
                if objeto[0] == '#':
                    pass
                if objeto[0] == 'tienda' and not habemus_tienda:
                    self.tienda = Tienda(*objeto)
                    habemus_tienda = True
                elif habemus_tienda:
                    self.tienda.anhadir_objeto(*objeto)
        # Carga edificios y unidades:
        debug.debug('En el archivo edificios_unidades.csv no está gusrdado que acción produce la habilidad especial')
        with open('INFO'+sep+'edificios_unidades.csv', encoding='utf-8') as archivo:
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
        with open('INFO'+sep+'partida_guardada.csv', encoding='utf-8') as archivo:
            self.partidas_guardadas = [filter(lambda x: x[0] != '#', (partida.strip().split(',') for partida in archivo))]
            if len(self.partidas_guardadas) > 0:
                self.partidas_guardadas.sort(key=lambda x: x[0])
        info.info('Se han cargado todos los datos del juego')

    def borrar_datos(self):
        with open('INFO'+sep+'partida_guardada.csv', 'w'):
            pass


    # ------------------------------------------------------------------------------------------------------------------


    def agregar_ultima_partida(self):
        debug.debug('Agregar el numero de partida')
        lista = [self.asesinatos, self.muertes, self.uso_habilidad, self.puntos_obtenidos, self.puntos_usados]
        self.partidas_guardadas.append(lista)

    def exportar_partidas(self):
        self.partidas_guardadas.sort()
        with open('INFO'+sep+'partida_guardada.csv', 'w', encoding='utf-8') as archivo:
            archivo.write('# NUMERO PARTIDA(5 la mas antigua), ASESINATOS, MUERTES, ACTIVACION HABILIDAD, PUNTOS OBTENIDOS, PUNTOS USADOS')
            for partida in self.partidas_guardadas:
                archivo.write(','.join(partida))






if __name__ == '__main__':
    pass
    # app = QtWidgets.QApplication(argv)
    # myapp = Juego()
    # myapp.show()
    # exit(app.exec_())
