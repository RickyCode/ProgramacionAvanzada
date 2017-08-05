__author__ = 'Ricado Del Río'

from loggers import MyLogger
from time import sleep
from threading import Thread

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

# ------------------------------------------------------------------------------------------------------------- COMANDOS

class ProcesadorComandosConsola:
    def __init__(self, servidor):
        self.servidor = servidor
        self.funcionando = True
        self.comandos = {'desconectar': [None, 'Desconecta al cliente del servidor.'],
                         'terminar_servidor': [self.terminar_servidor, 'Finaliza la ejecución del servidor.'],
                         'usuario': [None, 'Solicita la incorporación de un usuario.'],
                         'lista_comandos': [self.lista_comandos, 'Muestra los comandos validos.'],
                         'chat': [None, 'Recibe un mensaje de chat y lo reeenvía a todos los usuarios'],
                         'mostrar_conectados': [self.mostrar_conectados,
                                                'Muestra a todos los usuarios conectados al servidor']}
        self.recibir_comandos_consola()

    def __call__(self, comando):
        return self.procesar_comando(comando)

    def thread_recibir_comandos_consola(self):
        while self.funcionando:
            sleep(0.01)
            mensaje = self.procesar_comando(input())
            log_i.info(mensaje)

    def recibir_comandos_consola(self):
        thread_comandos_consola = Thread(target=self.thread_recibir_comandos_consola, )
        thread_comandos_consola.start()

    def procesar_comando(self, comando):
        lista = comando.split(' ')
        if lista[0] in self.comandos:
            return self.comandos[lista[0]][0](*lista[1:])
        else:
            return 'Comando "{}" no existe'.format(lista[0])

    def

    # def terminar_servidor(self):
    #     self.servidor.finalizar_servidor()
    #     self.funcionando = False
    #     return 'Servidor finalizado.'

    def mostrar_conectador(self):
        for ClienteUsuario


