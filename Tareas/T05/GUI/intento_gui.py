#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Ricardo Del Rio'

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QIcon, QPixmap

from PyQt5.QtWidgets import (QMainWindow, QFrame, QDesktopWidget, QApplication, QProgressBar, QPushButton, QLabel, QDialog)
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import qApp

from sys import exit, __excepthook__
from os import sep, chdir, getcwd
from time import sleep

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *




class LeagueofProgra(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusbar = self.statusBar()

        # self.carga_juego = CargaJuego(self)
        # self.menu_inicio = MenuInicio(self)
        # self.juego = PantallaJuego(self)
        # self.tienda = Tienda(self)

        # Caracteristicas invariantes:
        self.centrar()
        self.setWindowTitle('League of Progra')
        logo = QPixmap('..\IMGS\logo.png')
        icono_ventana = logo.scaled(15,15)
        icon = QIcon()
        icon.addPixmap(icono_ventana)
        self.setWindowIcon(icon)

        self.show()

    def centrar(self):
        pantalla = QDesktopWidget().screenGeometry()
        tamanho = self.geometry()
        self.move((pantalla.width() - tamanho.width()) / 2,
                  (pantalla.height() - tamanho.height()) / 2)

    def mostrar_progreso_carga(self):
        self.carga_juego = CargaJuego(self)
        self.setCentralWidget(self.carga_juego)
        self.carga_juego.mensaje_status_bar[str].connect(self.statusbar.showMessage)
        self.carga_juego.start()
        self.carga_juego.show()
        self.centrar()

    def mostrar_menu_inicio(self):
        self.menu_inicio = MenuInicio(self)
        self.setCentralWidget(self.menu_inicio)
        self.menu_inicio.mensaje_status_bar[str].connect(self.statusbar.showMessage)
        self.menu_inicio.start()
        self.menu_inicio.show()
        self.centrar()

    def mostrar_pantalla_juego(self):
        self.juego = PantallaJuego(self)
        self.setCentralWidget(self.juego)
        self.juego.show()
        self.centrar()

    def mostrar_tienda(self):
        self.tienda = Tienda(self)
        self. setCentralWidget(self.tienda)
        self.centrar()



class CargaJuego(QFrame):
    mensaje_status_bar = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_carga_juego()

    def init_carga_juego(self):

        # Barra de progreso:
        self.barra = QProgressBar()
        self.barra.setRange(0, 100)
        self.barra.setValue(50)

        # Mensaje:
        self.mensaje = QLabel()
        self.mensaje.setText('Cargando juego...')

        # Layouts:
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.mensaje)
        vbox.addWidget(self.barra)
        vbox.addStretch(1)
        self.setLayout(vbox)


        # for count in range(self.barra.minimum(), self.barra.maximum() + 1):
        #     self.barra.setValue(count)
        #     qApp.processEvents()
        #     sleep(0.05)

    def start(self):
        self.mensaje_status_bar.emit('Se esta cargando el juego')


class MenuInicio(QFrame):
    mensaje_status_bar = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initMenuInicio()

    def initMenuInicio(self):
        # Imagenes:
        logo = QPixmap('D:\Archivos\[Git] Progra Avanzada (N1)\Trabajando-En-Tareas\T05\IMGS\logo.png')

        # Boton Iniciar Partida:
        self.b_iniciar_partida = QPushButton(self)
        self.b_iniciar_partida.setText('Iniciar Partida')
        # self.b_iniciar_partida.setFixedSize(100,30)

        # Boton Borrar Historial Partidas:
        self.b_borrar_historial = QPushButton(self)
        self.b_borrar_historial.setText('Borrar Historial de Partidas')
        # self.b_borrar_historial.setFixedSize(200,30)

        # Lista Seleccionar Campeon:

        # Imagen Central:
        imagen_central = QLabel()
        imagen_central.setPixmap(logo)

        # Cuandro de información:
        cuadro_informacion = QLabel()
        cuadro_informacion.setText('Bienvenido Jugador'
                                   '\nA League of Progra')

        # Layouts:
        lado_izquierdo = QFrame()
        lado_izquierdo.setFrameShape(QFrame.Box)
        vbox = QVBoxLayout()
        vbox.addWidget(cuadro_informacion)
        vbox.addWidget(self.b_iniciar_partida)
        vbox.addWidget(self.b_borrar_historial)
        lado_izquierdo.setLayout(vbox)

        hbox = QHBoxLayout()
        hbox.addWidget(lado_izquierdo)
        hbox.addWidget(imagen_central)
        self.setLayout(hbox)

    def start(self):
        self.mensaje_status_bar.emit('Menu de Inicio')


class PantallaJuego(QFrame):
    mensaje_status_bar = pyqtSignal(str)
    medida_largo = 500
    medida_alto = 500

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initPantallaJuego()

    def initPantallaJuego(self):
        # Fondo de pantalla:
        imagen_fondo = QPixmap('D:\\Archivos\\[Git] Progra Avanzada (N1)\\Trabajando-En-Tareas\\T05\\IMGS\\fondo_verde.jpg')
        fondo = QLabel()
        fondo.setPixmap(imagen_fondo)



class Tienda(QFrame):
    mensaje_status_bar = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_tienda

    def init_tienda(self):
        pass



if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    __excepthook__ = hook

    app = QApplication([])
    juego = LeagueofProgra()
    juego.mostrar_progreso_carga()
    print('Se muestra el cuadro de progreso')
    sleep(10)
    juego.mostrar_menu_inicio()
    print('se muestra el menu de inicio')
    sleep(10)
    juego.mostrar_pantalla_juego()
    print('se muestrala pantalla del juego')6


    exit(app.exec_())



