__author__ = 'Ricardo Del Río'

# Librerías propias:
from loggers import MyLogger
# Librerías de terceros:
from os import chdir, mkdir, listdir, getcwd, sep
from random import uniform, randint
from datetime import datetime as dt
from pickle import dumps, dump, load

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

# ---------------------------------------------------------------------------------------------------------------- SALAS

class Salas:
    salas = []
    path = None
    path_20_seg = None
    path_ecualizador = None
    path_2x = None
    info_cliente = None

    def __init__(self, nombre, path, p_20_seg, p_ecual, p_2x):
        self.nombre = nombre
        self.path = path
        self.path_20_seg = p_20_seg
        self.path_ecualizador = p_ecual
        self.path_2x = p_2x
        # Atributos a obtener:
        self.nom_canciones = []
        self.artistas = []
        self.canciones = []
        # Ejecutar métodos:
        self.identificar_modificar_canciones()
        Salas.salas.append(self)


    @staticmethod
    def crear_salas():
        log_i.info('Se estan creando las salas...')
        Salas.crear_directorios_ppals()
        chdir(Salas.path)
        directorios = listdir()
        if directorios:
            Salas.cargar_base_datos()
            for nom_carpeta in listdir():
                if (nom_carpeta != '__SalasPrograPop__') and (not '.ppop' in nom_carpeta) and (not '.log' in nom_carpeta):
                    if not nom_carpeta+'.ppop' in listdir():
                        print(nom_carpeta)
                        Salas.directorios_secundarios(nom_carpeta)
                        path_sala = '{}{}{}'.format(Salas.path,sep,nom_carpeta)
                        path_20_seg = '{}{}{}'.format(Salas.path_20_seg,sep,nom_carpeta)
                        path_ecual = '{}{}{} - Ecualizador'.format(Salas.path_ecualizador,sep,nom_carpeta)
                        path_2x = '{}{}{} - 2x Cancion'.format(Salas.path_2x,sep,nom_carpeta)
                        Salas(nom_carpeta, path_sala, path_20_seg, path_ecual, path_2x)
            log_i.info('Se crearon {} salas.'.format(len(Salas.salas)*3))
        else:
            log_i.info('No hay salas para agregar. La carpeta "Canciones" está vacia.')
        Salas.generar_base_datos()
        Salas.datos_iniciales_cliente()


    @staticmethod
    def crear_directorios_ppals():
        if not 'Canciones' in listdir():
            mkdir('Canciones')
        chdir('Canciones')
        Salas.path = getcwd()
        if not '__SalasPrograPop__' in listdir():
            mkdir('__SalasPrograPop__')
        chdir('__SalasPrograPop__')
        carpetas = listdir()
        if not '20 Segundos' in carpetas:
            mkdir('20 Segundos')
        if not 'Ecualizador' in carpetas:
            mkdir('Ecualizador')
        if not '2x Cancion' in carpetas:
            mkdir('2x Cancion')
        Salas.path_20_seg = getcwd() + sep+'20 Segundos'
        Salas.path_ecualizador = getcwd()+sep+'Ecualizador'
        Salas.path_2x = getcwd()+sep+'2x Cancion'

    @staticmethod
    def directorios_secundarios(nombre_sala):
        if not nombre_sala in listdir(Salas.path_20_seg):
            mkdir(Salas.path_20_seg + sep + nombre_sala)
        if not nombre_sala + ' - Ecualizador'in listdir(Salas.path_ecualizador):
            mkdir(Salas.path_ecualizador + sep + nombre_sala + ' - Ecualizador')
        if not nombre_sala + ' - 2x Cancion'in listdir(Salas.path_2x):
            mkdir(Salas.path_2x + sep + nombre_sala + ' - 2x Cancion')

    @staticmethod
    def datos_iniciales_cliente():
        dic_datos = {}
        for sala in Salas.salas:
            dic_datos[sala.nombre] = sala.artistas
        serial = dumps(dic_datos)
        Salas.info_cliente = serial

    @staticmethod
    def generar_base_datos():
        for sala in Salas.salas:
            with open(Salas.path+sep+sala.nombre+'.ppop', 'wb') as archivo:
                dump(sala, archivo)

    @staticmethod
    def cargar_base_datos():
        for nom_archivo in listdir(Salas.path):
            if '.ppop' in nom_archivo:
                with open(Salas.path + sep + nom_archivo, 'rb') as archivo:
                    sala = load(archivo)
                Salas.salas.append(sala)

    def __getstate__(self):
        nuevo_dic = self.__dict__.copy()
        log_d.debug('Hacer pop de todos los datos temporales como cant de usuarios conectados')
        return nuevo_dic



    def identificar_modificar_canciones(self):
        for nom_cancion in listdir(self.path):
            pos_sep = nom_cancion.find('-')
            pos_ext = nom_cancion.find('.')
            artista = nom_cancion[:pos_sep].strip()
            titulo = nom_cancion[pos_sep+1:pos_ext].strip()
            self.artistas.append(artista)
            self.nom_canciones.append(titulo)
            c = Cancion(titulo, artista, nom_cancion, self.path, self.path_20_seg, self.path_ecualizador, self.path_2x)
            self.canciones.append(c)

class Cancion:
    def __init__(self, titulo, artista, nombre_archivo, path, p_20_seg, p_ecu, p_2x):
        self.titutulo = titulo
        self.artista = artista
        self.nombre_archivo = nombre_archivo
        self.path = path
        self.path_20_seg = p_20_seg
        self.path_ecualizador = p_ecu
        self.path_2x = p_2x
        self.duracion = None
        # Ejecución de métodos:
        print(nombre_archivo)
        self.calc_duracion()
        self.version_20_seg()
        self.crear_version_ecualizador()
        self.crear_version_2x()
        
    def calc_duracion(self):
        with open(self.path+sep+self.nombre_archivo, 'rb') as archivo:
            header = archivo.read(44)
        size = int.from_bytes(header[40:44], 'little')
        byte_rate = int.from_bytes(header[28:32], 'little')
        self.duracion = size/byte_rate
        
    def cortar(self,seg, bytes_cancion):
        '''toma los primeros "seg" segundos de la cancio seleccionada y los retorna.
        La cancion queda con una duracion menor o igual a los segundos dados'''
        byte_rate = bytes_cancion[28:32]
        int_byte_rate = int.from_bytes(byte_rate, 'little')
        nvo_subchunk2size = (int_byte_rate*seg).to_bytes(4, 'little')
        nvo_data = bytes_cancion[44:int_byte_rate*seg+45]
        nuevos_bytes_cancion = bytes_cancion[:40] + nvo_subchunk2size + nvo_data
        return nuevos_bytes_cancion
    
    def version_20_seg(self):
        with open(self.path+sep+self.nombre_archivo, 'rb') as archivo:
            bytes_cancion = archivo.read()
        nuevos_bytes_cancion = self.cortar(20, bytes_cancion)
        with open('{}{}{}'.format(self.path_20_seg,sep, self.nombre_archivo), 'wb') as archivo:
            archivo.write(nuevos_bytes_cancion)
            
    def filtro_por_canal(self, canal, n, bps):
        canal_antiguo = canal
        nuevo_canal = bytearray()
        for i in range(n):
            num = 0
            while num <= len(canal)-bps:
                sample_antiguo = canal_antiguo[num:num+bps]
                if num == 0:
                    sample_nuevo_anterior = sample_antiguo
                else:
                    sample_nuevo_anterior = nuevo_canal[num-bps:num]
                sample_nuevo = (int((int.from_bytes(sample_antiguo, 'little')+int.from_bytes(sample_nuevo_anterior, 'little'))/2)).to_bytes(bps, 'little')
                nuevo_canal.extend(sample_nuevo)
                num += bps
            canal_antiguo = nuevo_canal
            nuevo_canal = bytearray()
        return canal_antiguo


    def reunir_canales(self, canal1, canal2, bps):
        canal_unico = bytearray()
        num = 0
        while num <= len(canal1) - bps:
            sample1 = canal1[num:num+bps]
            canal_unico.extend(sample1)
            sample2 = canal2[num:num+bps]
            canal_unico.extend(sample2)
            num += bps
        return canal_unico

    def crear_version_ecualizador(self):
        f = uniform(0.5, 3)
        n = randint(1, 10)
        with open(self.path_20_seg+sep+self.nombre_archivo, 'rb') as archivo:
            bytes_cancion = archivo.read()
        sample_rate = int.from_bytes(bytes_cancion[24:28], 'little')
        new_sample_rate = (int(sample_rate * f)).to_bytes(4, 'little')
        bits_per_sample = int.from_bytes(bytes_cancion[34:36], 'little')
        bytes_per_sample = int(bits_per_sample / 8)
        data = bytes_cancion[44:]
        canal1 = bytearray()
        canal2 = bytearray()
        sample = b''
        paridad = 1
        contador = 0
        for un_int in data:
            un_byte = un_int.to_bytes(1, 'big')
            sample += un_byte
            contador += 1
            if contador == bytes_per_sample:
                if paridad == 1:
                    canal1.extend(sample)
                    sample = b''
                    paridad = 2
                elif paridad == 2:
                    canal2.extend(sample)
                    sample = b''
                    paridad = 1
                contador = 0
        nuevo_canal1 = self.filtro_por_canal(canal1, n, bytes_per_sample)
        nuevo_canal2 = self.filtro_por_canal(canal2, n, bytes_per_sample)
        new_data = self.reunir_canales(nuevo_canal1, nuevo_canal2, bytes_per_sample)
        nuevos_bytes_cancion = bytes_cancion[:24] + new_sample_rate + bytes_cancion[28:44] + new_data
        con_tiempo_corregido = self.cortar(20, nuevos_bytes_cancion)
        with open('{}{}{}'.format(self.path_ecualizador,sep, self.nombre_archivo), 'wb') as archivo:
            archivo.write(con_tiempo_corregido)


    def sacar_byte_por_medio(self, canal):
        return canal[1::2]
    
    def crear_version_2x(self):
        with open(self.path+sep+self.nombre_archivo, 'rb') as archivo:
            bytes_cancion = archivo.read()
        bytes_40_seg = self.cortar(40, bytes_cancion)
        sample_rate = int.from_bytes(bytes_40_seg[24:28], 'little')
        nuevo_sample_rate = (sample_rate).to_bytes(4, 'little')
        bits_per_sample = int.from_bytes(bytes_40_seg[34:36], 'little')
        bytes_per_sample = int(bits_per_sample / 8)
        data = bytes_40_seg[44:]
        canal1 = bytearray()
        canal2 = bytearray()
        sample = b''
        paridad = 1
        contador = 0
        for un_int in data:
            un_byte = un_int.to_bytes(1, 'big')
            sample += un_byte
            contador += 1
            if contador == bytes_per_sample:
                if paridad == 1:
                    canal1.extend(sample)
                    sample = b''
                    paridad = 2
                elif paridad == 2:
                    canal2.extend(sample)
                    sample = b''
                    paridad = 1
                contador = 0
        nuevo_canal1 = self.sacar_byte_por_medio(canal1)
        nuevo_canal2 = self.sacar_byte_por_medio(canal2)
        if bytes_per_sample == 1:
            bps = bytes_per_sample
        else:
            bps = int(bytes_per_sample/2)
        nuevo_data = self.reunir_canales(nuevo_canal1, nuevo_canal2, bps)
        nuevo_subchunk2size = (len(nuevo_data)).to_bytes(4, 'little')
        nuevos_bytes_cancion = bytes_40_seg[:24]+nuevo_sample_rate+bytes_40_seg[28:40]+nuevo_subchunk2size+nuevo_data
        with open('{}{}{}'.format(self.path_2x,sep,self.nombre_archivo), 'wb') as archivo:
            archivo.write(nuevos_bytes_cancion)




if __name__ == '__main__':
    pass
    # inicio = dt.now()
    # Salas.crear_salas()
    # fin = dt.now()
    # tiempo = fin - inicio
    # print(tiempo)

