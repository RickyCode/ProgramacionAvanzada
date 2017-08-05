
__author__ = 'Ricardo Del Rio'

from manejo_csv import importar_datos, exportar
from fecha_hora import FechaHora, fecha_hora_actual
from meteorologia import Meteorologia, Pronostico, m
from longitudes import distancia_coordenadas
from simplificadores import Menu
from longitudes import distancia_2_coordenadas

#-----------------------------------------------------------------------------------------------------------------------

class Incendios:
    '''
    Hereda de:
    Compone a:
    Afrega a: Incendio(Varios objetos)
    '''
    incendios = []

    def cargar_datos(self):
        datos = importar_datos('incendios.csv') #datos[fila(f)][columna(c)]

        for f in range(len(datos)):  #recorre filas
            if f != 0:
                for c in range(len(datos[f])):   #recorre columnas
                    if datos[0][c] == 'id:string':
                        idn = datos[f][c]
                    elif datos[0][c] == 'lat:float':
                        lat = float(datos[f][c])
                    elif datos[0][c] == 'lon:float':
                        lon = float(datos[f][c])
                    elif datos[0][c] == 'potencia:int':
                        potencia = int(datos[f][c])
                    elif datos[0][c] == 'fecha_inicio:string':
                        fecha_inicio = datos[f][c]
                incendio = Incendio(idn, lat, lon, potencia, fecha_inicio)
                self.incendios.append(incendio)

    def guardar_cambios(self):
        matriz = []
        for i in self.incendios:
            matriz.append(i.en_lista)
        exportar(matriz, 'incendios.csv', 1)

#-----------------------------------------------------------------------------------------------------------------------

class Incendio:
    '''
    Hereda de:
    Compuesta a:
    Agrega a: Metereología, FechaHora
    '''

    def __init__(self, idn, lat, lon, potencia, fecha_inicio):
        self.id = idn
        self.lat = float(lat)
        self.lon = float(lon)
        self.potencia = int(potencia)

        pos = fecha_inicio.find(' ')
        self.fecha_hora_inicio = FechaHora(fecha_inicio[:pos], fecha_inicio[pos+1:])

        self.recursos = [[]]              # AUN NADA LA MODIFICA Dependera de la fecha/hora del programa
        #Si en una estrategia se le asigna un recurso a este incendio se suma a esta lista. Junto
        #con un objeto fecha hora del momento en que seasigno el recurso. Tal vez sea mejor agregarlo en recursos.csv

        self.tasa_propagacion = 0.139       # AUN NADA LA MODIFICA Dependera de la fecha/hora del programa
        # Tasa Propagación: 500 mts por hora (500mts por cada 3600 segundos, 0.139 mts cada seg)
        self.superficie_afectada = 0    # AUN NADA LA MODIFICA Dependera de la fecha/hora del programa
        self.puntos_poder = 0           # AUN NADA LA MODIFICA Dependera de la fecha/hora del programa
        #Puntos de poder: superficie_afectada * potencia
        self.porcentaje_extincion = 0   # AUN NADA LA MODIFICA Dependera de la fecha/hora del programa

        self.radio = 0
        self.lista_pronosticos = []
        self.ultimo_pronostico = None

        self.fecha_termino = None
        self.lista_fechas = []
        self.lista_cambios_tasa = []


        self.en_lista = [[ind],[lat],[lon],[potencia],[fecha_inicio]] ##Ojo que la fecha de inicio debe quedar en el formato correspondiente para guardar.

    def variables_ambientales(self, fecha_hora_actual):
        '''Analiza cuales pronosticos afectan al incendio en distintas fechas/horas posteriores al inicio del
        incendio
        Se toman los pronisticos entre la fecha de inicio del incendio y la fecha entregada como parametro.
        Si no se entrega una fecha, se considera el periodo hasta la fecha actual del programa
        (si el incendio estpa activo).
        Los datos se incorporan a una lista.
        Se coincidera el comienzo del incendio como el segundo cero
        Todas las fechas de inicio y de termino de un pronostico se contrastan con ese segundo 0
        si el pronostico es anterior al incencio, se contrsta solamente la fecha_termino con el segundo 0'''
        for p in m.reporte:
            #Si el pronostico empieza antes que el incendio y termina despues de que el incencio empezo:
            if ((p.fecha_inicio < self.fecha_hora_inicio) and (p.fecha_termino > self.fecha_hora_inicio)):
                p.calcular_diferencia(self.fecha_hora_inicio)
                [0,500 + self.variacion_tasa_prop(p)]
                [p.calcular_diferencia(self.fecha_hora_inicio), self.variacion_tasa_prop(p)]


# -----------------------------------------------------
        #Solo toma un pronostico si en su fecha de inicio cae sobre el incendio.
        #Corregir esto

        segundo_actual = fecha_hora_actual.calcular_diferencia(self.fecha_hora_inicio)
        segundo_incendio = 0
        self.lista_pronosticos = m.reporte
        while segundo_incendio <= segundo_actual:
            for p in self.lista_pronosticos:
                if p.fecha_inicio.calcular_diferencia(self.fecha_hora_inicio) == segundo_incendio:
                    if (distancia_coordenadas(self.lat , self.lon, p.lat, p.lon)) < (self.radio + p.radio):
                        self.actualizar_tasa(p, 1)
                    else:
                        self.lista_pronosticos.pop(self.lista_pronosticos.index(p))

                if p.fecha_termino.calcular_diferencia(self.fecha_hora_inicio) == segundo_incendio:
                    self.actualizar_tasa(p, 0)

                else:
                    self.lista_pronosticos.pop(self.lista_pronosticos.index(p))


        segundo += 1
        self.radio += self.tasa_propagacion

#-----------------------------------------------------





                self.lista_pronosticos.append(p)
                self.lista_fechas

    def variacion_tasa_prop(self,pronostico):
        tipo = pronostico.tipo
        if tipo == 'VIENTO':
            return ((pronostico.valor / 10) / 3600)

        elif tipo == 'TEMPERATURA':
            if pronostico.valor > 30:
                return (((pronostico.valor % 30) * 25) / 3600)

        elif tipo == 'NUBES':  # No afecta la tasa de propagacion
            pass

        elif tipo == 'LUVIA':
            return -((pronostico.valor * 50) / 3600)
        return 0






        for p in m.reporte:
            fecha1 = self.fecha_hora_inicio #Comienza incendio
            fecha2 = p.fecha_termino        #Termina pronostico
            fecha3 = p.fecha_inicio         #Comienza Pronostico

            continuar = True

            #Esta parte no sirve, tiene que comparar si hay tope con todos los demás pronosticos
            '''if self.ultimo_pronostico:
                if (p.fecha_inicio.es_anterior(self.ultimo_pronostico.fecha_termino) and
                    self.ultimo_pronostico.fecha_inicio.es_anterior(p.fecha_inicio) and
                    (p.tipo == self.ultimo_pronostico.tipo))
                    continuar = False
            ####

            if continuar:
                if fecha1.es_anterior(fecha2) or fecha1.es_anterior(fecha3):
                    if distancia_2_coordenadas(self.lat, self.lon, p.lat, p.lon) < (self.radio + p.radio):
                        self.lista_pronosticos.append(p)
                        self.lista_fechas.append(p.fecha_inicio)
                        self.lista_fechas.append(p.fecha_termino)
                        self.actualizar_datos_incendio()'''

    def actualizar_datos_incendio(self):
        lista_fechas = []

        for i in
        #Tasa Propagacion

        self.ultimo_pronostico = self.lista_pronosticos[-1]
        pronostico = self.ultimo_pronostico
        tipo = pronostico.tipo

        if tipo == 'VIENTO':
            self.tasa_propagacion += ((pronostico.valor / 10) / 3600)

        elif tipo == 'TEMPERATURA':
            if pronostico.valor > 30:
                self.tasa_propagacion += (((pronostico.valor%30) * 25) / 3600)

        elif tipo == 'NUBES': #No afecta la tasa de propagacion
            pass

        elif tipo == 'LUVIA':
            self.tasa_propagacion -= ((pronostico.valor * 50) / 3600)






        self.tasa_propagacion =



    def __le__(self, other, categoria):
        self.puntos_poder <= other.puntos_poder

    def __str__(self):


#-----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    incendios = Incendios()
    incendios.cargar_datos()
    print(type(incendios.incendios))
    print(len(incendios.incendios))


