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


class EdificiosUnidades:
    def __init__(self, vida, ubicacion, sprite_sheet, team, largo):
        self.vida = vida
        self.__ubicacion = ubicacion
        self.sprite_sheet = sprite_sheet
        self.team = team
        self.largo = largo

        self.__ur = None
        self.__ll = None
        self.__lr = None

    @property
    def ul(self):
        return self.__ubicacion

    @property
    def ur(self):
        x, y = self.__ubicacion
        return x + self.largo, y

    @property
    def ll(self):
        x, y = self.__ubicacion
        return x, y + self.largo

    @property
    def lr(self):
        x, y = self.__ubicacion
        return x + self.largo, y + self.largo


class Unidades(EdificiosUnidades):
    def __init__(self, vida, ubicacion, sprite_sheet, vel_mov, danho, vel_ataque, rango_ataque, orientacion, ts_ataque):
        super().__init__(vida, ubicacion, sprite_sheet)
        self.vel_mov = vel_mov
        self.danho = danho
        self.vel_ataque = vel_ataque
        self.rango_ataque = rango_ataque
        self.orientacion = orientacion
        self.ts_ataque = ts_ataque

class Campeones(Unidades):
    dic_campeones = {}
    def __init__(self, vida, ubicacion, sprite_sheet, vel_mov, danho, vel_ataque, rango_ataque, nombre, habilidad_unica, enfriamiento_hab):
        super().__init__(vida, ubicacion, vel_mov, danho, vel_ataque, rango_ataque, sprite_sheet)
        self.nombre = nombre
        self.habilidad_unica = habilidad_unica
        self.enfriamiento_hab = enfriamiento_hab
        self.muertes = None
        self.ts_habilidad = None
        self.personalidad = None
        self.puntos = None
        self.gastados = None
        self.kills = None
        self.destino = None

class Subditos(Unidades):
    dic_subditos = {}
    def __init__(self, vida, ubicacion, sprite_sheet, vel_mov, danho, vel_ataque, rango_ataque, tipo):
        super().__init__(vida, ubicacion, sprite_sheet, vel_mov, danho, vel_ataque, rango_ataque)
        self.tipo = tipo
        self.destino = None

class Torre(EdificiosUnidades):
    formato_torre = []
    def __init__(self, vida, ubicacion, sprite_sheet, danho, vel_ataque, rango_ataque):
        super().__init__(vida, ubicacion, sprite_sheet)
        self.danho = danho
        self.vel_ataque = vel_ataque
        self.rango_ataque = rango_ataque

class Inhibidor(EdificiosUnidades):
    formato_inhibidor = []
    def __init__(self, vida, ubicacion, sprite_sheet):
        super().__init__(vida, ubicacion, sprite_sheet)

class Nexo(EdificiosUnidades):
    formato_nexo = []
    def __init__(self, vida, ubicacion, sprite_sheet):
        super().__init__(vida, ubicacion, sprite_sheet)







