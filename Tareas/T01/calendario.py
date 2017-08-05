_author__ = 'Ricardo Del Rio'

#-----------------------------------------------------------------------------------------------------------------------

class Calendario:
    def fecha_valida(self, dia, mes, ano):

        a = Ano(ano)

        if type(mes) == str:
            seguir = True
            for i in mes:
                if i == '0' and seguir:
                    mes = mes[1:]
                elif i != '0':
                    seguir = False

        if type(dia) == str:
            seguir = True
            for i in dia:
                if i == '0' and seguir:
                    dia = dia[1:]
                elif i != '0':
                    seguir = False

        if not ((int(mes) >= 1) and (int(mes) <= 12)):
            return False

        elif not ((int(dia) >= 1) and (int(dia) <= a.meses[int(mes)-1].cant_dias )):
            return False

        return True




#-----------------------------------------------------------------------------------------------------------------------

class Ano:
    def __init__(self, numero):
        self.numero = int(numero)
        self.tipo = ''
        self.meses = []
        self.total_dias = 0

        if not self.numero % 4 == 0:
            self.tipo = 'comun'
        elif not self.numero % 100 == 0:
            self.tipo = 'biciesto'
        elif not self.numero % 400 == 0:
            self.tipo = 'comun' #ano secular
        else:
            self.tipo = 'biciesto'

        meses = [1,2,3,4,5,6,7,8,9,10,11,12]

        for i in meses:
            mes = Mes(i,self.tipo)
            self.meses.append(mes)

    def cant_dias_total(self):
        '''calcula la cantidad de días de un ano en particular'''
        self.total_dias = 0
        for i in self.meses:
            mes = Mes(i,self.tipo)
            self.total_dias += mes.cant_dias
        return self.total_dias

    def cant_dias_hasta(self, num_mes):
        '''Calcula la cantidad de días desde principio de cierto año hasta l ultimo dia de un mes'''
        dias_hasta = 0
        for i in range(1,num_mes +1):
            mes = Mes(i,self.tipo)
            dias_hasta += mes.cant_dias
        return dias_hasta





#-----------------------------------------------------------------------------------------------------------------------
class Mes:
    def __init__(self, num, tipo_ano):
        self.num = num
        self.cant_dias = 0
        self.nombre = ''

        if self.num == '1' or self.num == 1:
            self.nombre = 'enero'
            self.cant_dias = 31

        elif self.num == '2' or self.num == 2:
            self.nombre = 'febrero'
            if tipo_ano == 'comun':
                self.cant_dias = 28
            elif tipo_ano == 'biciesto':
                self.cant_dias = 29

        elif self.num == '3' or self.num == 3:
            self.nombre = 'marzo'
            self.cant_dias = 31

        elif self.num == '4' or self.num == 4:
            self.nombre = 'abril'
            self.cant_dias = 30

        elif self.num == '5' or self.num == 5:
            self.nombre = 'mayo'
            self.cant_dias = 31

        elif self.num == '6' or self.num == 6:
            self.nombre = 'junio'
            self.cant_dias = 30

        elif self.num == '7' or self.num == 7:
            self.nombre = 'julio'
            self.cant_dias = 31

        elif self.num == '8' or self.num == 8:
            self.nombre = 'agosto'
            self.cant_dias = 31

        elif self.num == '9' or self.num == 9:
            self.nombre = 'septiembre'
            self.cant_dias = 30

        elif self.num == '10' or self.num == 10:
            self.nombre = 'octubre'
            self.cant_dias = 31

        elif self.num == '11' or self.num == 11:
            self.nombre = 'noviembre'
            self.cant_dias = 30

        elif self.num == '12' or self.num == 12:
            self.nombre = 'diciembre'
            self.cant_dias = 31

    def __le__(self, other):
        return self.num <= other.num

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    c = Calendario()

    while True:
        dia = int(input('Ingresa dia: '))
        mes = int(input('Ingresa mes: '))
        ano = int(input('Ingresa ano: '))

        print(c.fecha_valida(dia, mes, ano))
        print()

        a = Ano(ano)

        for i in a.meses:
            print(i.nombre)
            print(i.cant_dias)

        print()
