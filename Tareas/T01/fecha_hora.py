__author__ = 'Ricardo Del Río'

#-----------------------------------------------------------------------------------------------------------------------

from simplificadores import SuperInput
from calendario import Ano, Mes

#-----------------------------------------------------------------------------------------------------------------------


class FechaHora:
    def __init__(self,fecha = None,hora = None):

        if fecha == None:
            self.fecha = '1/1/2000'
        else:
            self.fecha = fecha

        if hora == None:
            self.hora = '00:00:00'
        else:
            self.hora = hora

        self.dia = ''
        self.mes = ''
        self.ano = ''

        self.horas = ''
        self.minutos = ''
        self.segundos = ''

        self.segundos_totales = 0

    def ingresar_fecha_hora(self):
        print('Formato fecha: dd/mm/aa')
        self.fecha = SuperInput('>>> Ingresa la Fecha: ', 'fecha').superinput()
        print('Formato hora: hh:mm:ss ')
        self.hora = SuperInput('>>> Ingresa la Hora: ', 'hora').superinput()

    def interpretar(self):
        '''
        Utiliza una fecha con formato dd/mm/aa
        Utiliza una hora en formato hh:mm:ss
        Crea los atributos de los Objetos de la Clase FechaHora
        '''
        fecha = self.fecha
        if '/' in fecha:
            self.dia = fecha[:fecha.find('/')]
            fecha = fecha[fecha.find('/')+1:]
            self.mes = fecha[:fecha.find('/')]
            fecha = fecha[fecha.find('/') + 1:]
            self.ano = fecha
        elif '-' in fecha:
            self.ano = fecha[:fecha.find('-')]
            fecha = fecha[fecha.find('-') + 1:]
            self.mes = fecha[:fecha.find('-')]
            fecha = fecha[fecha.find('-') + 1:]
            self.dia = fecha

        hora = self.hora
        if hora[0] == 0:
            self.horas = int(hora[1])
        else:
            self.horas = int(hora[:2])
        if hora[3] == 0:
            self.minutos = int(hora[4])
        else:
            self.minutos = int(hora[3:5])
        if hora[6] == 0:
            self.segundos = int(hora[7])
        else:
            self.segundos = int(hora[6:])

        self.segundos_totales = (self.segundos + (self.horas * 3600) + (self.minutos * 60))

    def interpretar_seg_totales(self):
        '''
        Cuando se modifican los segundos totales de la fecha hora e algun elemento (incendio, recursos, etc..)
        Lo interpreta y lo pasa a la división tradicional de horas, minutos y segundos para preparar su traspaso a
        las bases de datos
        '''
        self.horas = self.segundos // 3600
        self.minutos = (self.segundos % 3600) // 60
        self.segundos = (self.segundos % 3600) % 60

    def es_anterior(self, other):
        '''Retorna True si el objeto al que se aplica el metodo es una fecha anterior a la fecha/hora que
        se da como parametro'''
        if self.ano < other.ano:
            return True
        elif self.ano == other.ano:
            if self.mes < other.mes:
                return True
            elif self.mes == other.mes:
                if self.dia < other.dia:
                    return True
                elif self.dia == other.dia:
                    if self.segundos_totales < other.segundos_totales:
                        return True
        return False

    def es_igual(self, other):
        '''Ve si dos fecha/hora son iguales'''
        return ((self.ano == other.ano) and (self.mes == other.mes) and (self.dia == other.dia)
                and (self.segundos_totales == other.segundos_totales))

    def __lt__(self, other):
        return self.es_anterior(other)

    def __eq__(self, other):
        return self.es_igual(other)

    def _gt__(self, other):
        return ((not self.es_anterior(other)) and (not self.es_igual()))


    def calcular_diferencia(self, other):
        '''Se asume que el objeto al que se aplica el metodo es menor que el objeto que se entrega como parametro.
        Tambien se asume que los archivos son distintos.
        la lista retorna la diferencia en segundos entre ambas fechas'''
        a1 = Ano(self.ano)
        a2 = Ano(other.ano)
        diferencia_expresada_en_segundos = 0

        m1 = Mes(int(self.mes), a1.tipo)
        para_fin_de_mes = m1.cant_dias - int(self.dia)
        para_fin_de_ano = a1.cant_dias_total() - a1.cant_dias_hasta(int(self.mes))
        diferencia_expresada_en_segundos += (para_fin_de_mes * 86400)
        diferencia_expresada_en_segundos += (para_fin_de_ano * 86400)

        m2 = Mes(int(other.mes), a2.tipo)
        para_ppio_de_mes = int(other.dia)
        para_ppio_de_ano = a2.cant_dias_hasta(int(other.mes) - 1)
        diferencia_expresada_en_segundos += (para_ppio_de_mes * 86400)
        diferencia_expresada_en_segundos += (para_ppio_de_ano * 86400)

        if int(other.ano) - int(self.ano) > 1:
            for i in range(self.ano + 1, other.ano):
                a = Ano(i)
                diferencia_expresada_en_segundos += (a.cant_dias_total() * 86400)

        diferencia_expresada_en_segundos += abs(self.segundos_totales - other.segundos_totales)

        return diferencia_expresada_en_segundos

    def __str__(self):
        return '{} / {} / {}   {}:{}:{}'.format(self.dia, self.mes, self.ano, self.horas, self.minutos, self.segundos)





fecha_hora_actual = FechaHora()


if __name__ == '__main__':
    '''fecha_hora = FechaHora()
    fecha_hora.ingresar_fecha_hora()
    fecha_hora.interpretar()
    print(fecha_hora.dia,fecha_hora.mes,fecha_hora.ano)
    '''

    t1 = FechaHora('10/03/2017','09:00:00')
    t2 = FechaHora('20/03/2017','08:00:00')

    t1.interpretar()
    t2.interpretar()

    dif = t1.calcular_diferencia(t2)

    print(dif)
    print(dif * 0.139) # Tasa de prpagacion en condiciones normales
    print(dif * 0.14)
    print(dif * 0.1)
    print(dif * 0.138888889)


    f1 = FechaHora('17/12/2016')
    f1.interpretar()
    f2 = FechaHora('22/1/2017')
    f2.interpretar()
    f3 = FechaHora('7/03/2017')
    f3.interpretar()
    f4 = FechaHora('19/3/2017')
    f4.interpretar()
    print(f1)
    lista = [f4,f2,f3,f1]

    print(f1.es_anterior(f2))

    for i in lista:
        print(i)
    print()
    lista.sort()
    for i in lista:
        print(i)