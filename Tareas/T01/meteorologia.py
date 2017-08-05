__author__ = 'Ricardo Del Rio'


from manejo_csv import importar_datos
from fecha_hora import FechaHora

class Meteorologia:
    reporte = []

    def cargar_datos(self):
        datos = importar_datos('meteorologia.csv') #datos[fila(f)][columna(c)]

        for f in range(len(datos)):  #recorre filas
            if  f == 0:
                if datos[0][0][0] == '\ufeff':
                    datos[0][0] = datos[0][0][1:]
            if f != 0:
                for c in range(len(datos[f])):   #recorre columnas
                    if datos[0][c] == 'id:string':
                        idn = datos[f][c]
                    elif datos[0][c] == 'fecha_inicio:string':
                        fecha_inicio = datos[f][c]
                    elif datos[0][c] == 'fecha_termino:string':
                        fecha_termino = datos[f][c]
                    elif datos[0][c] == 'tipo:string':
                        tipo = datos[f][c]
                    elif datos[0][c] == 'valor:float':
                        valor = float(datos[f][c])
                    elif datos[0][c] == 'lat:float':
                        lat = float(datos[f][c])
                    elif datos[0][c] == 'lon:float':
                        lon = float(datos[f][c])
                    elif datos[0][c] == 'radio:int':
                        radio = int(datos[f][c])
                pronostico = Pronostico(idn, fecha_inicio, fecha_termino, tipo, valor, lat, lon, radio)
                self.reporte.append(pronostico)
        self.reporte.sort()


class Pronostico:

    def __init__(self, idn, fecha_inicio, fecha_termino, tipo, valor, lat, lon, radio):
        self.idn = idn
        self.fecha_inicio = FechaHora(fecha_inicio)
        self.fecha_termino = FechaHora(fecha_termino)
        self.tipo = tipo
        self.valor = valor
        self.lat = lat
        self.lon = lon
        self.radio = radio

    def __lt__(self, other):
        return self.fecha_inicio < other.fecha_inicio

    def __eq__(self, other):
        return self.fecha_inicio == other.fecha_inicio

    def __gt__(self, other):
        return self.fecha_inicio > other.fecha_inicio

met = Meteorologia()

###########################################################

if __name__ == '__main__':

    meteorologia = Meteorologia()
    meteorologia.cargar_datos()
    print(type(meteorologia.reporte))
    print(len(meteorologia.reporte))
    print(meteorologia.reporte[50].fecha_inicio)

    for c in range(len(datos[0])):
        print(datos[0][c])


