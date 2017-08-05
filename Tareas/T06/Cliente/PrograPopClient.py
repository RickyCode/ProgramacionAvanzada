__author__ = 'Ricardo Del Río'


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   AQUI SE SE DEFINEN EL HOST Y EL PORT   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
HOST = None
PORT = 8000
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Propios:
from loggers import MyLogger
from Cliente.cliente import Cliente
# GUI
from PyQt5.QtWidgets import (QWidget, QApplication, QDialog, QPushButton, QHBoxLayout, QVBoxLayout)
from PyQt5.QtMultimedia import QSound
# GUI Propios
from Cliente.GUI.inicio_cliente import Ui_Dialog_inicio_cliente as Ui_Inicio
from Cliente.GUI.pantalla_inicio import Ui_PantallaInicio
from Cliente.GUI.sala import Ui_Dialog

from threading import Thread
from time import sleep
import sys

# -------------------------------------------------------------------------------------------------------------- LOGGERS


log_i = MyLogger(__name__, name='CLIENTE',
                 formatter='%(name)s[{0}]:   %(message)s'.format(__name__))
log_w = MyLogger(__name__, name='CLIENTE',
                 nombre_archivo='cliente.log', stream_handler=False,
                 mylevel='warning')
log_e = MyLogger(__name__, name='CLIENTE',
                 nombre_archivo='cliente.log', stream_handler=False,
                 mylevel='error')
log_d = MyLogger(__name__, name='CLIENTE',
                 nombre_archivo='cliente.log', stream_handler=False,
                 mylevel='debug')
space = MyLogger(__name__, formatter='%(message)s')



class PrograPopClient:
    def __init__(self):
        self.cliente = Cliente(HOST, PORT)
        self.inicio = Inicio()
        self.pantalla_inicio = PantallaInicio()


    def mostrar_inicio(self):
        self.inicio.ui.lineEdit_host.setText(self.cliente.HOST)
        self.inicio.ui.lineEdit_port.setText(str(self.cliente.PORT))
        self.inicio.ui.pushButton_conectar.clicked.connect(self.conectar_al_servidor)
        self.inicio.show()

    def mostrar_pantalla_inicio(self):
        self.pantalla_inicio.ui.label_nombre_usuario.setText(self.cliente.nombre_usuario)
        self.pantalla_inicio.ui.label_puntaje.setText(str(self.cliente.puntaje_total))
        self.pantalla_inicio.show()

    def conectar_al_servidor(self):
        if not self.cliente.funcionando:
            self.cliente.HOST = self.inicio.ui.lineEdit_host.text()
            self.cliente.PORT = int(self.inicio.ui.lineEdit_port.text())
            nombre_usuario = self.inicio.ui.lineEdit_nombre_usuario.text()
            if len(nombre_usuario) > 20:
                self.mostrar_mensajes_inicio('El nombre es demasiado largo. no debe superar los 20 cacacteres')
            elif len(nombre_usuario) < 1:
                self.mostrar_mensajes_inicio('Debes ingresar un nombre.')
            else:
                self.cliente.nombre_usuario = nombre_usuario
                self.cliente.conectar_servidor()
                self.mostrar_mensajes_inicio()
                sleep(1)
                self.mostrar_mensajes_inicio()
                if self.cliente.funcionando:
                    sleep(2)
                    self.inicio.hide()
                    self.creacion_salas()
                    self.mostrar_pantalla_inicio()
        else:
            self.mostrar_mensajes_inicio('Ya estas conectado al servidor')

    def creacion_salas(self):
        self.pantalla_inicio.crear_visualizacion_salas(self.cliente.info_salas)

    def solicitar_cancion_servidor(self):
        pass



    def mostrar_mensajes_inicio(self, mensaje=None):
        if mensaje:
            nuevo_mensaje = ''
            contador = 1
            for c in mensaje:
                if contador % 50 == 0:
                    nuevo_mensaje += '\n'
                nuevo_mensaje += c
                contador += 1
            self.inicio.definir_mensaje(nuevo_mensaje)
        else:
            for mensaje in self.cliente.mensajes:
                nuevo_mensaje = ''
                contador = 1
                for c in mensaje:
                    if contador%50 == 0:
                        nuevo_mensaje += '\n'
                    nuevo_mensaje += c
                    contador += 1
                self.inicio.definir_mensaje(nuevo_mensaje)
                self.cliente.mensajes.remove(mensaje)
                sleep(0.5)







class Inicio(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Inicio()
        self.ui.setupUi(self)

    # def def_host_port(self, host, port):
    #     self.ui.lineEdit_host.setText(host)
    #     self.ui.lineEdit_port.setText(port)
    #     self.show()
    #     return self.ui.lineEdit_host.text(), self.ui.lineEdit_port.text(), self.ui.lineEdit_nombre_usuario.text()

    def definir_mensaje(self, mensaje):
        self.ui.label_status.setText(mensaje)

class PantallaInicio(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self,parent)
        self.ui = Ui_PantallaInicio()
        self.ui.setupUi(self)
        self.salas = []
        # self.funcion = funcion

    def crear_visualizacion_salas(self,info_salas):
        labels_salas = {1: [self.ui.label_s1, self.ui.label_e1, self.ui.label_21],
                        2: [self.ui.label_s2, self.ui.label_e2, self.ui.label_22],
                        3: [self.ui.label_s3, self.ui.label_e3, self.ui.label_23],
                        4: [self.ui.label_s4, self.ui.label_e4, self.ui.label_24],
                        5: [self.ui.label_s5, self.ui.label_e5, self.ui.label_25],
                        6: [self.ui.label_s6, self.ui.label_e6, self.ui.label_26]}
        botones_salas = {1: [self.ui.pushButton_s1, self.ui.pushButton_e1, self.ui.pushButton_21],
                        2: [self.ui.pushButton_s2, self.ui.pushButton_e2, self.ui.pushButton_22],
                        3: [self.ui.pushButton_s3, self.ui.pushButton_e3, self.ui.pushButton_23],
                        4: [self.ui.pushButton_s4, self.ui.pushButton_e4, self.ui.pushButton_24],
                        5: [self.ui.pushButton_s5, self.ui.pushButton_e5, self.ui.pushButton_25],
                        6: [self.ui.pushButton_s6, self.ui.pushButton_e6, self.ui.pushButton_26]}
        n = 1
        for sala in info_salas:
            labels_salas[n][0].setText(sala.upper())
            sala_musica = Sala(sala.upper())
            botones_salas[n][0].clicked.connect(lambda: self.mostrar_sala(sala_musica))
            sala_musica.ui.pushButton_volver.clicked.connect(lambda: self.volver_pantalla_inicio(sala_musica))
            self.salas.append(sala_musica)

            labels_salas[n][1].setText(sala.upper()+' - Ecualizador'.upper())
            sala_musica = Sala(sala.upper()+' - Ecualizador'.upper())
            botones_salas[n][1].clicked.connect(lambda: self.mostrar_sala(sala_musica))
            sala_musica.ui.pushButton_volver.clicked.connect(lambda: self.volver_pantalla_inicio(sala_musica))
            self.salas.append(sala_musica)

            labels_salas[n][2].setText(sala.upper()+' - 2x Canción.'.upper())
            sala_musica = Sala(sala.upper() + ' - Ecualizador'.upper())
            botones_salas[n][2].clicked.connect(lambda: self.mostrar_sala(sala_musica))
            sala_musica.ui.pushButton_volver.clicked.connect(lambda: self.volver_pantalla_inicio(sala_musica))
            self.salas.append(sala_musica)

            n += 1

    def mostrar_sala(self, sala):
        self.hide()
        sala.show()

    def volver_pantalla_inicio(self,sala):
        sala.hide()
        self.show()


class Sala(QDialog):
    def __init__(self, nombre, parent=None):
        QWidget.__init__(self,parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.label_nombre_sala.setText(nombre)







if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)

    sys.__excepthook__ = hook

    app = QApplication(sys.argv)
    juego = PrograPopClient()
    juego.mostrar_inicio()
    sys.exit(app.exec_())