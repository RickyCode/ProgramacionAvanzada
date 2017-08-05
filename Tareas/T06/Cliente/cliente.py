__author__ = 'Ricardo Del Río'

# Propios:
from loggers import MyLogger
# Networking:
from socket import gethostname, gethostbyname, AF_INET, SOCK_STREAM, socket
# Treading
from threading import Thread
# Serialización:
from pickle import loads
# Reproducción audio:
from PyQt5.QtMultimedia import QSound
# Otros
from datetime import datetime as dt
from os import listdir, getcwd, chdir, sep, mkdir
from time import sleep

# -------------------------------------------------------------------------------------------------------------- LOGGERS


log_i = MyLogger(__name__, name='SERVIDOR',
                 formatter='%(name)s[{0}]:   %(message)s'.format(__name__))
log_w = MyLogger(__name__, name='SERVIDOR',
                 nombre_archivo='servidor.log', stream_handler=False,
                 mylevel='warning')
log_e = MyLogger(__name__, name='SERVIDOR',
                 nombre_archivo='servidor.log', stream_handler=False,
                 mylevel='error')
log_d = MyLogger(__name__, name='SERVIDOR',
                 nombre_archivo='servidor.log', stream_handler=False,
                 mylevel='debug')
space = MyLogger(__name__, formatter='%(message)s')


class Cliente:
    def __init__(self, HOST, PORT):
        log_i.info('Inicializando cliente...')
        if HOST:
            self.HOST = HOST
        else:
            self.HOST = gethostbyname(gethostname())
        self.PORT = PORT
        self.nombre_usuario = None
        self.funcionando = False
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.info_salas = None
        self.mensajes = []
        self.puntaje_total = 0

    def definir_nombre_usuario(self, nombre):
        if len(nombre) > 20:
            self.mensajes.append('EL nombre de usuario no debe tener más de 20 caracteres')
            raise ValueError('El nombre de usuario no debe tener más de 20 caracteres')
        self.nombre_usuario = nombre


    def conectar_servidor(self):
        try:
            self.socket.connect((self.HOST, self.PORT))
            primer_mensaje = self.nombre_usuario
            self.enviar_mensaje(primer_mensaje)
            tipo, respuesta = self.recibir()
            mensaje = 'MENSAJE SERVIDOR: {}'.format(respuesta)
            log_i.info(mensaje)
            self.mensajes.append('MENSAJE SERVIDOR: {}'.format(respuesta))
            print(int(respuesta[:4]))
            if int(respuesta[:4]) == 1 or int(respuesta[:4]) == 3:
                self.funcionando = True
                self.escucha()
            else:
                self.socket.close()
                self.socket = socket(AF_INET, SOCK_STREAM)


        except ConnectionRefusedError:
            mensaje = 'El servidor indicado no se encuentra conectado.'
            log_i.info(mensaje)
            self.mensajes.append(mensaje)
            self.funcionando = False
            self.socket.close()
            self.socket = socket(AF_INET, SOCK_STREAM)

        except OSError:
            mensaje = 'Se solicito conexion en un socket ya conectado'
            self.mensajes.append(mensaje)


    def thread_escucha(self):
        gen_num_archivo = gen()
        while self.funcionando:
            tipo, recibido = self.recibir() # Retorna None, None si se desconecto el servidor
            if tipo == 'msj':
                mensaje = 'MENSAJE SERVIDOR: {}'.format(recibido)
                log_i.info(mensaje)
                self.mensajes.append(mensaje)
            elif tipo == 'wav':
                mensaje = 'Se esta recbiendo un archivo...'
                log_i.info(mensaje)
                self.mensajes.append(mensaje)
                str_numero = str(next(gen_num_archivo))
                nombre_archivo = '0'*(10-len(str_numero))+str_numero
                if not 'temp' in listdir():
                    mkdir('temp')
                with open('temp\\{}.wav'.format(nombre_archivo), 'wb') as archivo:
                    archivo.write(recibido[2:])
                    log_d.debug('Falta revisar el tiempo en que debe reproducirse')
                mensaje = 'Se recibió un archivo wav. Guardado con nombre {}'.format(nombre_archivo)
                log_i.info(mensaje)
                self.mensajes.append(mensaje)
            elif tipo == 'pkl':
                mensaje = 'Se está recibiendo infomación de las salas del servidor...'
                log_i.info(mensaje)
                self.mensajes.append(mensaje)
                self.info_salas = recibido
                mensaje = 'Información recibida, hay {} salas en el servidor'.format(len(self.info_salas)*3)
                log_i.info(mensaje)
                self.mensajes.append(mensaje)



    def escucha(self):
        thread_escucha = Thread(target=self.thread_escucha)
        thread_escucha.start()

    def enviar_mensaje(self, msj):
        bytes_msj = msj.encode('utf-8')
        largo_msj = len(bytes_msj).to_bytes(4, byteorder='big')
        self.socket.send(largo_msj + bytes_msj)

    def recibir(self):
        try:
            bytes_largo_respuesta = self.socket.recv(4)
            largo_respuesta = int.from_bytes(bytes_largo_respuesta, byteorder='big')
            respuesta = b''
            while len(respuesta) < largo_respuesta:
                respuesta += self.socket.recv(256)
            tipo_respuesta = respuesta[:3].decode('utf-8')
            if tipo_respuesta == 'msj':
                return tipo_respuesta, respuesta[3:].decode('utf-8')
            elif tipo_respuesta == 'wav':
                return tipo_respuesta, respuesta[3:]
            elif tipo_respuesta == 'pkl':
                return tipo_respuesta, loads(respuesta[3:])
            else:
                raise ValueError('Este programa no puede recibir cosas de tipo: {}'.format(tipo_respuesta))
        except:
            self.funcionando = False
            log_i.info('Se terminó la conexión con el sevidor')
            return None,None

# ------------------------------------------------------------------------------------------------------------- COMANDOS

class ProcesadorComandos:
    def __init__(self, servidor):
        self.servidor = servidor
        self.funcionando = True
        self.comandos = {'desconectar': [None, 'Desconecta al cliente del servidor.'],
                         'lista_comandos': [self.lista_comandos, 'Muestra los comandos validos.'],
                         'chat': [None,'Recibe un mensaje de chat y lo reeenvía a todos los usuarios']}
        self.recibir_comandos_consola()



    def __call__(self, comando):
        return self.procesar_comando(comando)

    def thread_recibir_comandos_consola(self):
        while self.funcionando:
            sleep(0.01)
            mensaje = self.procesar_comando(input('>>> '))
            log_i.info(mensaje)


    def recibir_comandos_consola(self):
        thread_comandos_consola = Thread(target=self.thread_recibir_comandos_consola,)
        thread_comandos_consola.start()

    def procesar_comando(self, comando):
        lista = comando.split(' ')
        if lista[0] in self.comandos:
            return self.comandos[lista[0]][0](*lista[1:])
        else:
            return 'Comando "{}" no existe'.format(lista[0])


    def lista_comandos(self):
        mensaje = '\n\n'
        for comando in self.comandos:
            mensaje += ('{0} {1}\n'.format(' '*22+comando, '.'*(20-len(comando))+' '+self.comandos[comando][1]))
        return mensaje

# ------------------------------------------------------------------------------------------------------ GENERADOR

def gen():
    contador = 1
    while True:
        yield contador
        contador += 1



if __name__ == '__main__':
    cliente = Cliente(None, 8000)
    cliente.definir_nombre_usuario('Ricardo')
    cliente.conectar_servidor()

