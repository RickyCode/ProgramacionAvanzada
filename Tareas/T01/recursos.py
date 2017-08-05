
__author__ = 'Ricardo Del Rio'


from manejo_csv import importar_datos

class Recursos:
    recursos = []

    def cargar_datos(self):
        datos = importar_datos('recursos.csv') #datos[fila(f)][columna(c)]

        for f in range(len(datos)):  #recorre filas
            if  f == 0:
                if datos[0][0][0] == '\ufeff':
                    datos[0][0] = datos[0][0][1:]
            if f != 0:
                for c in range(len(datos[f])):   #recorre columnas
                    if datos[0][c] == 'id:string':
                        idn = datos[f][c]
                    elif datos[0][c] == 'tipo:string':
                        tipo = datos[f][c]
                    elif datos[0][c] == 'lat:float':
                        lat = float(datos[f][c])
                    elif datos[0][c] == 'lon:float':
                        lon = float(datos[f][c])
                    elif datos[0][c] == 'velocidad:int':
                        velocidad = int(datos[f][c])
                    elif datos[0][c] == 'autonomia:int':
                        autonomia = int(datos[f][c])
                    elif datos[0][c] == 'delay:int':
                        delay = int(datos[f][c])
                    elif datos[0][c] == 'tasa_extincion:int':
                        tasa_extincion = int(datos[f][c])
                    elif datos[0][c] == 'costo:int':
                        costo = int(datos[f][c])
                recurso = Recurso(idn, tipo, velocidad, lat, lon, autonomia, delay, tasa_extincion, costo)
                self.recursos.append(recurso)



class Recurso:

    def __init__(self, idn, tipo, velocidad, lat, lon, autonomia, delay, tasa_extincion, costo):
        self.idn = idn
        self.tipo = tipo
        self.velocidad = velocidad
        self.lat = lat
        self.lon = lon
        self.autonomia = autonomia
        self.delay = delay
        self.tasa_extincion = tasa_extincion
        self.costo = costo

        #AUN NADA MODIFICA ESTOS ATRIBUTOS, DEBEN MODIFICARSE EN BASE A LA LINEA DE TIEMPO
        self.ubicacion = None
        self.estado = ''
        self.tiempo_restante = ''

    def detalles(self):
        return 'ID: %5s \n Tipo: %13s \n Tipo: %15s \n Recurso ID: %10s '  %(self.id, self.nombre,
                                                                              self.contrasena, self.recurso_id)


###########################################################

if __name__ == '__main__':

    recursos = Recursos()
    recursos.cargar_datos()
    print(type(recursos.recursos))
    print(len(recursos.recursos))

