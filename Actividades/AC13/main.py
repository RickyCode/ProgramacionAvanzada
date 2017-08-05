__author__ = 'Ricardo Del Río'

from os import listdir, sep, system, getcwd, chdir
from datetime import datetime
from json import dump as jdump
from json import load as jload
from pickle import dump as pdump

class DDChat:
    lista_usuarios = []
    lista_mensajes = []

    @staticmethod
    def cargar_mensajes():
        lista_mensajes = []
        for path in DDChat.archivos('msg'):
            with open(path, 'r', encoding='utf-8') as archivo:
                lista_mensajes.append(Mensaje(**jload(archivo)))
        return lista_mensajes

    @staticmethod
    def cargar_usuarios():
        lista_usuarios = []
        for path in DDChat.archivos('usr'):
            with open(path, 'r', encoding='utf-8') as archivo:
                lista_usuarios.append(Usuario(**jload(archivo)))
        return lista_usuarios

    @staticmethod
    def archivos(subcarpeta):
        return ['db'+sep+subcarpeta+sep+x for x in listdir('db'+sep+subcarpeta)]

    @staticmethod
    def cargar_datos():
        DDChat.lista_usuarios = DDChat.cargar_usuarios()
        DDChat.lista_mensajes = DDChat.cargar_mensajes()

    @staticmethod
    def encontrar_y_anhadir(send_to, send_by):
        for usuario in DDChat.lista_usuarios:
            if usuario.phone_number == send_to:
                usuario.contacts.append(send_by)

    @staticmethod
    def cargar_contactos():
        for mensaje in DDChat.lista_mensajes:
            DDChat.encontrar_y_anhadir(mensaje.send_to, mensaje.send_by)

    @staticmethod
    def crear_directorios():
        path_actual = getcwd()
        if not 'secure_bd' in listdir():
            system('mkdir secure_db')
        chdir('secure_db')
        if not 'msg' in listdir():
            system('mkdir msg')
        if not 'usr' in listdir():
            system('mkdir usr')
        chdir(path_actual)

    @staticmethod
    def guardar_datos():
        DDChat.crear_directorios()
        for usuario in DDChat.lista_usuarios:
            with open('./secure_db/usr/'+str(usuario.phone_number), 'w', encoding='utf-8') as archivo:
                jdump(usuario.__dict__, archivo)
        for mensaje in DDChat.lista_mensajes:
            with open('secure_db'+sep+'usr'+sep+DDChat.nombre_archivo(mensaje.date), 'wb') as archivo:
                pdump(mensaje, archivo)

    @staticmethod
    def caesar_cipher(texto, numero):
        nuevo_texto = ''
        for c in texto:
            nuevo_c = chr((ord(c) + numero) % 26)
            nuevo_texto += nuevo_c
        return nuevo_texto

    @staticmethod
    def nombre_archivo(fecha):
        fecha = str(fecha)
        fecha = fecha.replace(' ','')
        fecha = fecha.replace(':','')
        fecha = fecha.replace('-','')
        return fecha


class Usuario:
    def __init__(self, name, contacts, phone_number):
        self.name = name
        self.contacts = contacts
        self.phone_number = phone_number

class Mensaje:
    def __init__(self, send_to, content, send_by, last_view_date, date):
        self.send_to = send_to
        self.content = content
        self.send_by = send_by
        self.last_view_date = last_view_date
        self.date = date

    def __getstate__(self):
        nuevo = self.__dict__.copy()
        nuevo.update({'content': DDChat.caesar_cipher(self.content,int(self.send_by))})
        return nuevo

    def __setstate__(self, state):
        state.update({'last_view_date': datetime.now()})
        self.__dict__ = state

if __name__ == '__main__':
    DDChat.cargar_datos()
    DDChat.cargar_contactos()
    DDChat.guardar_datos()