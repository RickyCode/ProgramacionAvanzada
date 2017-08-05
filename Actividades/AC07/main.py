__author__ = 'Ignacio Castaneda, Diego Iruretagoyena, Ivania Donoso, CPB'

import random
from datetime import datetime


"""
Escriba sus decoradores y funciones auxiliares en este espacio.
"""

def rut_valido(rut): #Funcion de apoyo
    if rut.count('-') > 1:
        return False
    for c in rut:
        if c == '-':
            pass
        elif c.isnumeric():
            pass
        else: return False
    return True


def verificar_transferencia(funcion): #Decorador
    '''
    Verifica: la existencia de ambas cuantas,
    que el saldo sea suficiente,
    clave de a cuenta de origen
    '''
    def nueva_funcion(self, origen, destino, monto, clave):
        if not origen in self.cuentas:
            raise AssertionError('La cuenta de origen no existe')
        if not destino in self.cuentas:
            raise AssertionError('La cuenta de destino no existe')
        if monto > self.cuentas[origen].saldo:
            raise AssertionError('El monto para transferir excede el saldo de la cuenta')
        if clave != self.cuentas[origen].clave:
            raise AssertionError('La clave es incorrecta!')
        funcion(self, origen, destino, monto, clave)

    return nueva_funcion

def verificar_inversion(funcion): #Decorador
    '''
    Verifica:
    Que exista la cuenta,
    saldo suficiente
    clave correcta
    no excede maximo
    '''
    def nueva_funcion(self, cuenta, monto, clave):
        if not cuenta in self.cuentas:
            raise AssertionError('La cuenta no existe')
        if monto > self.cuentas[cuenta].saldo:
            raise AssertionError('Saldo insuficiente para realizar la inversion')
        if clave != self.cuentas[cuenta].clave:
            raise AssertionError('La clave es incorrecta!')
        if (monto + self.cuentas[cuenta].inversiones) > 10000000:
            raise AssertionError('Se excede el maximo permitido de inversion')
        funcion(self, uenta, monto, clave)
    return nueva_funcion

def verificar_cuenta(funcion):
    '''Verifica:
    Numero de cuenta no repetido
    Clave de 4 numeros
    RUT valido
    '''
    def nueva_funcion(self, nombre, rut, clave, numero, saldo_inicial=0):
        stop = False
        while not stop:
            if numero in self.cuentas:
                numero = self.crear_numero()
            else:
                stop = True
        if len(clave) != 4:
            raise AssertionError('Largo de clave incorrecto. Debe poseer 4 números')
        for c in clave:
            if not c.isnumeric():
                raise AssertionError('La clave solo debe contener numeros')
        if not rut_valido(rut):
            raise AssertionError('El formato del RUT es incorrecto')
        funcion(self, nombre, rut, clave, numero, saldo_inicial)
    return nueva_funcion

def verificar_saldo(funcion): #decorador
    '''Verifica que la cuenta exista
    que el saldo que se retorna sea correcto'''
    def nueva_funcion(self, numero_cuenta):
        if not (numero_cuenta in self.cuentas):
            raise AssertionError('La cuenta no existe')
        return self.cuentas[numero_cuenta].saldo
    return nueva_funcion

def log(path): #Constructor
    def decorador(funcion):
        def nueva_funcion(*args, **kwargs):
            nombre_funcion = str(funcion)[11:]
            nombre_funcion2 = nombre_funcion
            with open(path + 'registro.txt', 'a') as archivo:
                archivo.write('{0} {1}'.format(datetime.now(),
                                               ))

        return nueva_funcion
    return decorador



"""
No pueden modificar nada más abajo, excepto para agregar los decoradores a las 
funciones/clases.
"""

@log('.\\')
class Banco:
    def __init__(self, nombre, cuentas=None):
        self.nombre = nombre
        self.cuentas = cuentas if cuentas is not None else dict()

    @verificar_saldo
    def saldo(self, numero_cuenta):
        # Da un saldo incorrecto
        return self.cuentas[numero_cuenta].saldo * 5

    @verificar_transferencia
    def transferir(self, origen, destino, monto, clave):
        # No verifica que la clave sea correcta, no verifica que las cuentas 
        # existan
        self.cuentas[origen].saldo -= monto
        self.cuentas[destino].saldo += monto

    @verificar_cuenta
    def crear_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        # No verifica que el número de cuenta no exista
        cuenta = Cuenta(nombre, rut, clave, numero, saldo_inicial)
        self.cuentas[numero] = cuenta

    @verificar_inversion
    def invertir(self, cuenta, monto, clave):
        # No verifica que la clave sea correcta ni que el monto de las 
        # inversiones sea el máximo
        self.cuentas[cuenta].saldo -= monto
        self.cuentas[cuenta].inversiones += monto

    def __str__(self):
        return self.nombre

    def __repr__(self):
        datos = ''

        for cta in self.cuentas.values():
            datos += '{}\n'.format(str(cta))

        return datos

    @staticmethod
    def crear_numero():
        return int(random.random() * 100)


class Cuenta:
    def __init__(self, nombre, rut, clave, numero, saldo_inicial=0):
        self.numero = numero
        self.nombre = nombre
        self.rut = rut
        self.clave = clave
        self.saldo = saldo_inicial
        self.inversiones = 0

    def __repr__(self):
        return "{} / {} / {} / {}".format(self.numero, self.nombre, self.saldo,
                                          self.inversiones)


if __name__ == '__main__':
    bco = Banco("Santander")
    bco.crear_cuenta("Mavrakis", "4057496-7", "1234", bco.crear_numero())
    bco.crear_cuenta("Ignacio", "19401259-4", "1234", 1, 24500)
    bco.crear_cuenta("Diego", "19234023-3", "1234", 2, 13000)
    #bco.crear_cuenta("Juan", "19231233--3", "1234", bco.crear_numero())
    bco.crear_cuenta("Juan", "19231233-3", "1234", bco.crear_numero())

    print(repr(bco))
    print()

    """
    Estos son solo algunos casos de pruebas sugeridos. Sientase libre de agregar 
    las pruebas que estime necesaria para comprobar el funcionamiento de su 
    solucion.
    """
    try:
        print(bco.saldo(10))
    except AssertionError as error:
        print('Error: ', error)

    try:
        print(bco.saldo(1))
    except AssertionError as error:
        print('Error: ', error)

    try:
        bco.transferir(1, 2, 5000, "1234")
    except AssertionError as msg:
        print('Error: ', msg)

    try:
        bco.transferir(1, 2, 5000, "4321")
    except AssertionError as msg:
        print('Error: ', msg)

    print(repr(bco))
    print()

    try:
        bco.invertir(2, 200000, "1234")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))

    try:
        bco.invertir(2, 200000, "4321")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))
