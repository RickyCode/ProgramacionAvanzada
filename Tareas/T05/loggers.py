from logging import Formatter, StreamHandler, FileHandler
from datetime import datetime
from os import sep

def archivo_logs():
    with open('INFO'+sep+'LeagueOfProgra.log', 'w', encoding='utf-8') as archivo:
        archivo.write('\n ------------------------------------------------\n {}\n\n'.format(datetime.now()))

archivo = 'INFO'+sep+'LeagueOfProgra.log'
formatter = Formatter('%(name)s, linea %(lineno)d]:   %(message)s ')
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)
file_handler = FileHandler(archivo)
file_handler.setFormatter(formatter)
