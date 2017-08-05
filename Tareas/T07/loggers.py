from logging import (Formatter, StreamHandler, FileHandler, Logger, INFO, ERROR, WARNING, DEBUG)
from datetime import datetime
from os import sep

class MyLogger(Logger):
    levels = {'INFO': INFO, 'ERROR': ERROR, 'DEBUG': DEBUG, 'WARNING': WARNING}
    def __init__(self, module, mylevel='INFO', formatter=None, stream_handler=True, nombre_archivo=None, name=None):
        self.mylevel = mylevel.upper()
        if name:
            super().__init__(name=name)
        else:
            super().__init__(name=str(self.mylevel))
        self.setLevel(MyLogger.levels[self.mylevel])

        if formatter:
            self.formatter = Formatter(formatter)
        else:
            self.formatter = Formatter('%(name)s[{0}, %(lineno)d]:   %(message)s '.format(module))

        if stream_handler:
            self.stream_handler = StreamHandler()
            self.stream_handler.setFormatter(self.formatter)
            self.addHandler(self.stream_handler)

        if nombre_archivo:
            if '.' in nombre_archivo:
                self.n_archivo = nombre_archivo
            else:
                self.n_archivo = nombre_archivo+'.log'
            with open(self.n_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write('------------------------------------------------\n{}\n\n'.format(datetime.now()))
            self.file_handler = FileHandler(self.n_archivo)
            self.file_handler.setFormatter(self.formatter)
            self.addHandler(self.file_handler)


def prueba():
    info = MyLogger(__name__, nombre_archivo='prueba.log')
    info.info('hola')


if __name__ == '__main__':
    funcion = MyLogger(__name__, nombre_archivo='prueba.log')
    funcion.info('bye')

    prueba()
