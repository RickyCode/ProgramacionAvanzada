__author__ = 'Ricardo Del Rio'
# Libre de estructuras python

#from calendario import Calendario
from estructuras_propias import ListaLigada, Diccionario

'''
Este modulo contiene funciones para facilitar y acelerar aquellas tediosas y repetitivas partes
de la programacion, para asi dejar mas tiempo a las partes entrenenidas :D

***   VERSION MODIFICADA PARA TAREA 02 DE PRORAMACION AVANZADA   ***
No usa las estructuras de python, sino que las estructuras del modulo 'estructuras_propias.py')
'''

#-------------------------------------------------------------------------

# Idea:
# Hacer que el super input no retorne solo un str, sino que el tipo que se
# pidió.-


class SuperInput:
    def __init__(self, tipos='str', solicitud_input='>>> ',
                 mensaje_error='Input Incorrecto, volver a ingresar'):
        self.solicitud_input = solicitud_input
        if isinstance(tipos, str):
            self.lista = ListaLigada(tipos)
        elif isinstance(tipos, list) or isinstance(tipos, ListaLigada):
            self.lista = tipos
        self.mensaje_error = mensaje_error
        self.entrada = ''

    def superinput(self):
        stop = False
        while not stop:
            self.solicitar_entrada()
            if self.input_correcto():
                stop = True
                return self.entrada
            else:
                print(self.mensaje_error, '\n')

    def solicitar_entrada(self):
        self.entrada = input()

    def debe_ser_str(self, tipo):
        texto = ListaLigada('str', 'string', 'texto')
        if tipo in texto:
            return True
        return False

    def debe_ser_int(self, tipo):
        entero = ListaLigada('int', 'integer', 'entero', 'numero')
        if tipo in entero:
            return True
        return False

    def debe_ser_float(self, tipo):
        decimal = ListaLigada('float', 'decimal')
        if tipo in decimal:
            return True
        return False

    def input_correcto(self):
        '''
        Revisa si el parametro ingresado en el superinput (self.entrada) es de alguno de los tipos permitidos en
        self.lista
        Si lo es, retorna True. Si no, False.
        '''
        v1, v2, v4 = False, False, False  # Se quitaron v3, v5, v6
        for tipo in self.lista:
            if self.debe_ser_int(tipo):
                v1 = self.entrada.isnumeric()
            elif self.debe_ser_float(tipo):
                v2 = '.' in self.entrada  # Esto debe ser mas preciso
            elif self.debe_ser_str(tipo):
                v4 = True
        return (v1 or v2 or v4)  # Se quitaron v3, v5, v6


# ----------------------------------------------------------------------------------------------------------------------
class Menu():
    '''
    Recibe una lista de opciones que el programa enumera y presenta al usuario.
    Si se le entrega una lista de funciones, estas seran asociadas en el orden entregado a la lista de opciones,
    de modo que cuando un usuario selecciona una opcion automaticamente comienza la funcion asociada.
    Si no se entrega lista de funciones el programa retorna la opcion seleccionada por el usuario.
    El programa es sensible a los errores de los usuarios, solamente admite enteros en el rango de la cantidad de
    opciones disponibles. El programa vuelve a solicitar la información correcta cada vez que el usuario ingresa una
    opcion invalida
    '''

    def __init__(
            self,
            lista_opciones,
            lista_funciones=None,
            texto_inicio=None,
            texto_error=None):
        self.lista_opciones = lista_opciones
        self.lista_funciones = lista_funciones
        self.texto_inicio = texto_inicio
        self.texto_error = texto_error
        self.diccionario = Diccionario()

    def menu(self):
        stop = False
        while not stop:
            # Revisa que los argumentos enregados sean realmente listas:
            if isinstance(
                    self.lista_opciones,
                    list) or isinstance(
                    self.lista_opciones,
                    ListaLigada):
                if isinstance(
                        self.lista_funciones,
                        list) or isinstance(
                        self.lista_funciones,
                        ListaLigada):
                    # Revisa que ambas listas tengan el mismo largo:
                    if len(self.lista_funciones) == len(self.lista_opciones):
                        # Crea un diccionario con un numero y la funcion
                        # asociada:
                        contador = 0
                        for funcion in self.lista_funciones:
                            contador += 1
                            self.diccionario[contador] = funcion
                        # Despliga en pantalla las opciones diponibles:
                        contador = 0
                        if self.texto_inicio:
                            if isinstance(self.texto_inicio, str):
                                print(self.texto_inicio + '\n')
                            else:
                                raise TypeError(
                                    'El texto de inicio debe ser un "string" no "{}"'.format(
                                        type(
                                            self.texto_inicio)))
                        for opcion in self.lista_opciones:
                            contador += 1
                            print('{}) {}'.format(contador, opcion))
                        # Solicita la opcion que el usuario desea seleccionar y
                        # ejecuta la funcion:
                        entrada = int(
                            SuperInput(
                                'int',
                                '>>> Elige una opcion: ').superinput())
                        if (entrada > 0) and (entrada <= contador):
                            stop = True
                            self.diccionario[entrada]()
                        else:

                            if self.texto_error:
                                if isinstance(self.texto_error, str):
                                    print(self.texto_error + '\n')
                                else:
                                    raise TypeError(
                                        'El texto de error debe ser un "string"no "{}"'.format(
                                            type(
                                                self.texto_inicio)))
                            else:
                                self.texto_error = 'hola hola 226'
                    else:
                        raise IndexError(
                            'Ambas listas deben tener el mismo largo.')
                else:
                    raise TypeError(
                        'Se entrega "{}" cuando se pide una "list"'.format(
                            type(
                                self.lista_funciones)))
            else:
                raise TypeError(
                    'Se entrega "{}" cuando se pide una "list"'.format(
                        type(
                            self.lista_opciones)))

#-------------------------------------------------------------------------


def ordenar_para_imprimir(
        lista,
        espacio_por_elemento=10,
        elementos_por_fila=8):
    '''
    recibe una lista o una matriz(por ahora solo lista) y el espacio que se le quiere asignar a cada elemento (todos igual, en el futuro
    evaluar que permita poner distinto largo a cada columna. Tambien recibe la cantidad de elementos que se quiere imprimir por fila)
    Retorna un string con los datos de la matriz o lista de forma ordenada, listos para imprimir en pantalla
    '''
    texto = ''
    contador = 0
    maximo = 0
    for i in lista:
        if len(i) > maximo:
            maximo = len(i)
    espacio = max(espacio_por_elemento, maximo) + 1
    while contador < len(lista):
        for i in range(elementos_por_fila):
            if contador < len(lista):
                num = espacio - len(lista[contador])
                texto += (' ' * num + str(lista[contador] + ','))
                contador += 1
            else:
                return texto
        texto += '\n'


if __name__ == '__main__':

    def hola():
        print('hola')

    def chao():
        print('chao')

    lista1 = ListaLigada('Imprimir Hola', 'Imprimir Chao')
    lista2 = ListaLigada(hola, chao)

    m = Menu(lista1, lista2).menu()
