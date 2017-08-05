
from logging import getLogger, DEBUG, WARNING, ERROR, INFO
from loggers import archivo_logs, stream_handler, file_handler

# ------------------------------------------------------------------------------------------------------------- LOGGERS
archivo_logs()
info = getLogger('INFO [{}'.format(__name__))
info.setLevel(INFO)
info.addHandler(stream_handler)
info.addHandler(file_handler)
debug = getLogger('DEBUG [{}'.format(__name__))
debug.setLevel(DEBUG)
debug.addHandler(file_handler)
warning = getLogger('WARNING [{}'.format(__name__))
warning.setLevel(WARNING)
warning.addHandler(file_handler)
error = getLogger('ERROR [{}'.format(__name__))
error.setLevel(ERROR)
error.addHandler(file_handler)
# ------------------------------------------------------------------------------------------------------------- * * *


class Tienda:
    def __init__(self, posicion, sprite_sheet):
        self.posicion = posicion
        self.sprite_sheet = sprite_sheet
        self.lista_objetos = []

    def anhadir_objeto(self, *args):
        objeto = ObjetoTienda(*args)
        self.lista_objetos.append(objeto)

class ObjetoTienda:
    def __init__(self, precio, bonificacion_atributo):
        self.precio = precio
        self.bon_atributo = bonificacion_atributo



