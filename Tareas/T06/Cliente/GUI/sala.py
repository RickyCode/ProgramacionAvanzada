# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sala.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1022, 718)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 130, 971, 291))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.respuesta1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.respuesta1.setText("")
        self.respuesta1.setObjectName("respuesta1")
        self.gridLayout.addWidget(self.respuesta1, 0, 0, 1, 1)
        self.respuesta2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.respuesta2.setText("")
        self.respuesta2.setObjectName("respuesta2")
        self.gridLayout.addWidget(self.respuesta2, 0, 1, 1, 1)
        self.respuesta3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.respuesta3.setText("")
        self.respuesta3.setObjectName("respuesta3")
        self.gridLayout.addWidget(self.respuesta3, 1, 0, 1, 1)
        self.respuesta4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.respuesta4.setText("")
        self.respuesta4.setObjectName("respuesta4")
        self.gridLayout.addWidget(self.respuesta4, 1, 1, 1, 1)
        self.pushButton_volver = QtWidgets.QPushButton(Dialog)
        self.pushButton_volver.setGeometry(QtCore.QRect(50, 650, 151, 28))
        self.pushButton_volver.setObjectName("pushButton_volver")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(290, 450, 631, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_puntaje1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_puntaje1.setText("")
        self.label_puntaje1.setObjectName("label_puntaje1")
        self.verticalLayout.addWidget(self.label_puntaje1)
        self.label_puntaje2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_puntaje2.setText("")
        self.label_puntaje2.setObjectName("label_puntaje2")
        self.verticalLayout.addWidget(self.label_puntaje2)
        self.label_puntaje3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_puntaje3.setText("")
        self.label_puntaje3.setObjectName("label_puntaje3")
        self.verticalLayout.addWidget(self.label_puntaje3)
        self.label_puntaje4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_puntaje4.setText("")
        self.label_puntaje4.setObjectName("label_puntaje4")
        self.verticalLayout.addWidget(self.label_puntaje4)
        self.label_puntaje5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_puntaje5.setText("")
        self.label_puntaje5.setObjectName("label_puntaje5")
        self.verticalLayout.addWidget(self.label_puntaje5)
        self.label_puntaje6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_puntaje6.setText("")
        self.label_puntaje6.setObjectName("label_puntaje6")
        self.verticalLayout.addWidget(self.label_puntaje6)
        self.label_nombre_sala = QtWidgets.QLabel(Dialog)
        self.label_nombre_sala.setGeometry(QtCore.QRect(50, 40, 441, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_nombre_sala.setFont(font)
        self.label_nombre_sala.setObjectName("label_nombre_sala")
        self.label_tiempo_restante = QtWidgets.QLabel(Dialog)
        self.label_tiempo_restante.setGeometry(QtCore.QRect(640, 50, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_tiempo_restante.setFont(font)
        self.label_tiempo_restante.setObjectName("label_tiempo_restante")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "PrograPop"))
        self.pushButton_volver.setText(_translate("Dialog", "Volver al Inicio"))
        self.label_nombre_sala.setText(_translate("Dialog", "<Nommbre Sala>"))
        self.label_tiempo_restante.setText(_translate("Dialog", "<Tiempo Restante Cancion>"))

