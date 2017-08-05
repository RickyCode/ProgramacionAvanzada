__author__ = 'Ricardo Del Río'

from loggers import MyLogger
from threading import Lock


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

# ------------------------------------------------------------------------------------------------------------- CLIENTES


class ClienteUsuario:
    usuarios = []
    usuarios_conectados = []
    lock = Lock()

    def __init__(self, socket, direccion, nombre):
        self.socket = socket
        self.direccion = direccion
        self.nombre = nombre
        self.conectado = True
        ClienteUsuario.usuarios.append(self)
        ClienteUsuario.usuarios_conectados.append(self)

    @staticmethod
    def ya_conectado(nombre_usuario):
        '''Verifica si el usuario ya inicio sesión'''
        for cliente in ClienteUsuario.usuarios_conectados:
            if cliente.nombre == nombre_usuario:
                return True
        return False

    @staticmethod
    def es_usuario_nuevo(nombre_usuario):
        for cliente in ClienteUsuario.usuarios:
            if cliente.nombre == nombre_usuario:
                return False
        return True

    @staticmethod
    def desconectar_usuario(nombre_cliente=None):
        for usuario in ClienteUsuario.usuarios_conectados:
            if usuario.nombre == nombre_cliente:
                ClienteUsuario.usuarios_conectados.remove(usuario)
                usuario.conectado = False
                usuario.socket.close()
                log_i.info('Se ha desconectado "{}" en {}'.format(usuario.nombre, usuario.direccion))

            else:
                raise ValueError('El usuario "{}" no existe'.format(nombre_cliente))




    @staticmethod
    def conectar_usuario(socket, direccion, nombre_usuario):
        for cliente in ClienteUsuario.usuarios:
            if cliente.nombre == nombre_usuario:
                ClienteUsuario.usuarios_conectados.append(cliente)
                cliente.conectado = True
                cliente.socket = socket
                cliente.direccion = direccion
                return cliente
        raise ValueError('No existe un  usuario con ese nombre.')

    @staticmethod
    def mostrar_conectados():
        texto_conectados = '\n\n'
        contador = 1
        if len(ClienteUsuario.usuarios_conectados) == 0:
            texto_conectados = '\tNo hay usuarios conectados.'
        else:
            for usuario in ClienteUsuario.usuarios_conectados:
                texto_conectados += str('\t {}. {}'.format(contador,usuario))
                contador += 1
        texto_conectados += '\n'
        return texto_conectados


    def __str__(self):
        return 'NOMBRE: {} , IP: {} , PORT: {}'.format(self.nombre, self.direccion[0], self.direccion[1])





