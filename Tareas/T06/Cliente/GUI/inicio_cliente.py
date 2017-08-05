# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inicio_cliente.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_inicio_cliente(object):
    def setupUi(self, Dialog_inicio_cliente):
        Dialog_inicio_cliente.setObjectName("Dialog_inicio_cliente")
        Dialog_inicio_cliente.resize(400, 272)
        self.pushButton_conectar = QtWidgets.QPushButton(Dialog_inicio_cliente)
        self.pushButton_conectar.setGeometry(QtCore.QRect(270, 220, 93, 31))
        self.pushButton_conectar.setObjectName("pushButton_conectar")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog_inicio_cliente)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 20, 261, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_nombre_usuario = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_nombre_usuario.setObjectName("label_nombre_usuario")
        self.horizontalLayout_2.addWidget(self.label_nombre_usuario)
        self.lineEdit_nombre_usuario = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_nombre_usuario.setText("")
        self.lineEdit_nombre_usuario.setObjectName("lineEdit_nombre_usuario")
        self.horizontalLayout_2.addWidget(self.lineEdit_nombre_usuario)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_host = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_host.setObjectName("label_host")
        self.horizontalLayout.addWidget(self.label_host)
        self.lineEdit_host = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_host.setText("")
        self.lineEdit_host.setObjectName("lineEdit_host")
        self.horizontalLayout.addWidget(self.lineEdit_host)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_port = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_port.setObjectName("label_port")
        self.horizontalLayout_3.addWidget(self.label_port)
        self.lineEdit_port = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_port.setText("")
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.horizontalLayout_3.addWidget(self.lineEdit_port)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label_status = QtWidgets.QLabel(Dialog_inicio_cliente)
        self.label_status.setGeometry(QtCore.QRect(30, 160, 331, 41))
        self.label_status.setText("")
        self.label_status.setObjectName("label_status")

        self.retranslateUi(Dialog_inicio_cliente)
        QtCore.QMetaObject.connectSlotsByName(Dialog_inicio_cliente)

    def retranslateUi(self, Dialog_inicio_cliente):
        _translate = QtCore.QCoreApplication.translate
        Dialog_inicio_cliente.setWindowTitle(_translate("Dialog_inicio_cliente", "Iniciar Cliente"))
        self.pushButton_conectar.setText(_translate("Dialog_inicio_cliente", "Conectar"))
        self.label_nombre_usuario.setText(_translate("Dialog_inicio_cliente", "Nombre Usuario: "))
        self.label_host.setText(_translate("Dialog_inicio_cliente", "HOST"))
        self.label_port.setText(_translate("Dialog_inicio_cliente", "PORT"))

