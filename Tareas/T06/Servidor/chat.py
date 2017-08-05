__author__ = 'Ricardo Del Río'

from loggers import MyLogger

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


class Chat:
    def __init__(self):
        self.registro_chats = []

    def recibir_chat(self, hora, contenido, remitente):
        msj_recibido = MensajeChat(hora, contenido, remitente)
        self.registro_chats.append(msj_recibido)




class MensajeChat:
    def __init__(self, hora, contenido, remitente):
        self.hora = hora
        self.contenido = contenido
        self.remitente = remitente

    def __lt__(self, other):
        return self.hora < other.hora

    def __eq__(self, other):
        self.hora == other.hora
