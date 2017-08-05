__author__ = 'Ricardo Del Río'

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   AQUI SE SE DEFINEN EL HOST Y EL PORT   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
HOST = None
PORT = 8000
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# -------------------------------------------------------------------------------------------------------------- IMPORTS

# Propios:
from loggers import MyLogger
from Servidor.clientes_usuarios import ClienteUsuario
from Servidor.salas_canciones import Salas
from Servidor.chat import Chat
# Networking:
from socket import gethostname, gethostbyname, AF_INET, SOCK_STREAM, socket
# Treading
from threading import Thread, Lock
# Serialización:
from pickle import dumps
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



# ------------------------------------------------------------------------------------------------------------- SERVIDOR

class Servidor:
    def __init__(self, HOST, PORT):
        space.info('')
        log_i.info('Iniciando servidor...')
        space.info('')
        if HOST:
            self.HOST = HOST
        else:
            self.HOST = gethostbyname(gethostname())
        self.PORT = PORT
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.funcionando = True
        # Ejecución de funciones:
        Salas.crear_salas()
        self.bind_and_listen()
        self.aceptar_conexiones()
        self.recibir_comandos_consola()
        # Diccionario de comandos:
        self.comandos = {# Ingresados por calquier medio:
                              'terminar_servidor': [self.finalizar_servidor, 'Finaliza la ejecución del servidor.', False],
                              'lista_comandos': [self.lista_comandos, 'Muestra los comandos validos.', False],
                              'mostrar_conectados': [ClienteUsuario.mostrar_conectados,
                              'Muestra a todos los usuarios conectados al servidor', False],
                              'enviar_archivo': [self.enviar_archivo_a_todos, 'Envia el archivo especificado a todos los clientes', False],
                              # Ingresados por el cliente:
                              'desconectarme': [ClienteUsuario.desconectar_usuario, 'Desconecta al cliente del servidor.', True],
                              'desconectar': [ClienteUsuario.desconectar_usuario, 'Desconecta al cliente del servidor.', False],
                              'chat': [self.chat, 'Recibe un mensaje de chat y lo reeenvía a todos los usuarios', True]
                             }


        space.info('')
        log_i.info('HOST:       {}'.format(self.HOST))
        log_i.info('PORT:       {}'.format(self.PORT))
        log_i.info('UBICACIÓN:  {}'.format(getcwd()))
        space.info('')
        log_i.info('Servidor iniciado: {}'.format(dt.now()))
        log_i.info('Escuchando ...')
        space.info('')
        space.info('-'*100)
        space.info('')

    def bind_and_listen(self):
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen(10)

    def enviar_mensaje(self, valor, socket):
        valor_str = str(valor)
        bytes_msj = valor_str.encode('utf-8')
        bytes_tipo = 'msj'.encode('utf-8')
        largo_msj = (len(bytes_msj) + 3).to_bytes(4, byteorder='big')
        socket.send(largo_msj + bytes_tipo + bytes_msj)

    def enviar_archivo(self, tipo, path, socket, reprodccion=0):
        if tipo == 'wav':
            with open(path, 'rb') as archivo:
                bytes_archivo = archivo.read()
                tamano = len(bytes_archivo) + 5 # 3 bytes del tipo y 2 del segundo de reproducción
                bytes_tamano = tamano.to_bytes(4, byteorder='big')
                bytes_tipo = tipo.encode('utf-8')
                bytes_reproduccion = reprodccion.to_bytes(2, byteorder='big')
                socket.send(bytes_tamano + bytes_tipo + bytes_reproduccion + bytes_archivo)

    def enviar_pickle(self,serial, socket):
        tamano = len(serial) +3 # 3 del tipo
        bytes_tamano = tamano.to_bytes(4, byteorder='big')
        bytes_tipo = 'pkl'.encode('utf-8')
        socket.send(bytes_tamano + bytes_tipo + serial)

    def enviar_archivo_a_todos(self, tipo, path, reproduccion=0):
        al_verre = path[::-1]
        nombre_archivo_al_verre = al_verre[:al_verre.find('\\')]
        nombre_archivo = nombre_archivo_al_verre[::-1]
        log_i.info('Se esta enviando el archivo {} a todos los usuarios conectados.'.format(nombre_archivo))
        for cliente in ClienteUsuario.usuarios_conectados:
            self.enviar_archivo(tipo, path, cliente.socket, reproduccion)
        log_i.info('Archivo enviado!')


    def thread_escuchar_cliente(self, cliente):
        while self.funcionando and cliente.conectado:
            try:
                recibido = self.recibir_mensaje(cliente.socket)
                if recibido != '':
                    respuesta = self.procesar_comando(recibido, cliente)
                    self.enviar_mensaje(respuesta, cliente.socket)
            except:
                with ClienteUsuario.lock:
                    ClienteUsuario.desconectar_usuario(cliente.nombre)

    def recibir_mensaje(self, socket_cliente):
        try:
            bytes_largo_respuesta = socket_cliente.recv(4)
            largo_respuesta = int.from_bytes(bytes_largo_respuesta, byteorder='big')
            respuesta = b''
            while len(respuesta) < largo_respuesta:
                respuesta += socket_cliente.recv(256)
            return respuesta.decode('utf-8')
        except:
            pass


    def thread_aceptar_conexiones(self):
        while self.funcionando:
            try:
                socket_cliente, direccion = self.socket.accept()
                nombre_usuario = self.recibir_mensaje(socket_cliente)
                nombre_usuario = nombre_usuario.replace(' ','')
                log_i.info('"{}" intentando conectarse desde {} ...'.format(nombre_usuario, direccion))
                with ClienteUsuario.lock:
                    if ClienteUsuario.es_usuario_nuevo(nombre_usuario):
                        usuario = ClienteUsuario(socket_cliente, direccion, nombre_usuario)
                        mensaje = '0001 CONEXIÓN ACEPTADA: Se creó el usuario "{}"'.format(nombre_usuario)
                        self.enviar_mensaje(mensaje, socket_cliente)
                        log_i.info('CONEXIÓN ACEPTADA: Se creó el usuario "{}". Conectado desde IP: {} PUERTO: {}'.format(nombre_usuario, direccion[0],direccion[1]))
                        thread_escucha = Thread(target=self.thread_escuchar_cliente,
                                                args=(usuario,))
                        thread_escucha.start()
                        self.enviar_pickle(Salas.info_cliente, socket_cliente)
                    else:
                        if ClienteUsuario.ya_conectado(nombre_usuario):
                            log_i.info('CONEXIÓN RECHAZADA. El usuario "{}" ya está activo'.format(nombre_usuario))
                            mensaje = '0002 CONEXIÓN RECHAZADA: El usuario "{}" ya está activo'.format(nombre_usuario)
                            self.enviar_mensaje(mensaje, socket_cliente)
                            socket_cliente.close()
                        else:
                            usuario = ClienteUsuario.conectar_usuario(socket_cliente, direccion, nombre_usuario)
                            mensaje = '0003 CONEXIÓN ACEPTADA: Usuario existente. "{}" está ahora conectado'.format(nombre_usuario)
                            self.enviar_mensaje(mensaje, socket_cliente)
                            log_i.info('CONEXIÓN ACEPTADA: Unuario existente. "{}" Conectado desde IP: {} PUERTO: {}'.format(
                                nombre_usuario, direccion[0], direccion[1]))
                            thread_escucha = Thread(target=self.thread_escuchar_cliente,
                                                    args=(usuario,))
                            thread_escucha.start()
                            self.enviar_pickle(Salas.info_cliente, socket_cliente)
            except:
                log_i.info('Conexión terminada.')

    def aceptar_conexiones(self):
        thread_conexiones = Thread(target=self.thread_aceptar_conexiones)
        thread_conexiones.start()

    def finalizar_servidor(self):
        log_d.debug('Agregar un código')
        mensaje = 'Se ha dado la orden de termnar la ejecución del servidor. Todos los usuarios serán desconecados'
        log_i.info('Terminando servidor...')
        self.funcionando = False
        with ClienteUsuario.lock:
            for cliente in ClienteUsuario.usuarios_conectados:
                self.enviar_mensaje(mensaje, cliente.socket)
                ClienteUsuario.desconectar_usuario(cliente.nombre)
        space.info('-' * 100)
        self.socket.close()
        sleep(0.01)
        return 'Servidor finalizado.'

    def thread_recibir_cmds_consola(self):
        while self.funcionando:
            sleep(0.01)
            comando = input()
            if comando:
                mensaje = self.procesar_comando(input())
            if mensaje:
                log_i.info(mensaje)

    def recibir_comandos_consola(self):
        thread_comandos_consola = Thread(target=self.thread_recibir_cmds_consola, )
        thread_comandos_consola.start()

    def lista_comandos(self):
        mensaje = '\n\n'
        for comando in self.comandos:
            mensaje += (
            '{0} {1}\n'.format('\t' + comando, '.' * (20 - len(comando)) + ' ' + self.comandos[comando][1]))
        return mensaje


    def procesar_comando(self, comando, cliente=None):
        lista = comando.split('::')
        if cliente:
            log_i.info('"{}" a solicitado ejecutar el comando: {}'.format(cliente.nombre, lista[0]))

        if lista[0] in self.comandos:
            if self.comandos[lista[0]][2]:
                return self.comandos[lista[0]][0](*lista[1:], cliente.nombre)
            else:
                return self.comandos[lista[0]][0](*lista[1:])
        else:
            return 'Comando "{}" no existe'.format(lista[0])


    def chat(self, mensaje, usuario):
        for cliente in ClienteUsuario.usuarios_conectados:
            self.enviar_mensaje('chat {}: {}'.format(usuario.nombre,mensaje), cliente.socket)



if __name__ == '__main__':
    Servidor(HOST, PORT)
