
#from variables_y_comandos import funciones, distribuciones
import numpy
from matplotlib import pyplot as plt
import sys

## -------------------------------------------------------------------------------------------------------------SIMBOLOS

simbolos_comparacion = ('==', '>', '<', '>=', '<=', '!=')
simbolos_operaciones = ('+', '-', '*', '/', '>=<')

## -----------------------------------------------------------------------------------------------------COMANDOS BASICOS



def asignar(variable, comando_o_dato):
    '''
    Guarda el valor de  retorno de comando o el valor de dato, bajo el nomnre 'variable'. No permite guardar
    información si el nombre ingresado es igual al nombre de algún comando propio de RQL o al nombre de alguna
    distribución de probabilidad.
    :param variable: str
    :param comando o dato: any
    :returns: None
    '''
    if callable(comando_o_dato):
        #if funciones.has_hey(variable):
        #    pass #Debe generarse un error
        #else:
        #    #nuevas_variables_funciones[variable] = comando_o_dato()
        #    pass
        pass

    else:
        #if funciones.has_hey(variable):
        #    pass #Debe generarse un error
        #else:
        #    #nuevas_variables_funciones[variable] = comando_o_dato
        #    pass
        pass

def crear_funcion(nombre_modelo, *parametros):
    '''
    Recibe el nombre de algun modelo de probabilidad y los parametros necesarios por el modelo, y retorna una nueva
    funcion que puede ser ocupada en el comando 'evaluar' para generar una columna de datos
    :param nombre_modelo: str ("normal", "gamma", "exponencial")
    :param *parametros: int or float
    :returns: funcion
    '''
    def funcion(x):
        #distribuciones[nombre_modelo](*parametros, x)
        pass
    return funcion

def graficar(columna, opcion):
    # Se puede usar matplotlib 2.0 y numpy 1.12
    '''
    Grafica(2D) los datos de una columna. El eje Y correspondera a los valores de columna. EL eje X dependera de
    'opcion':
    ’numerico’ El eje X corresponde a una enumeracion de los datos. Por ejemplo, si los datos son [10, 12, 13],
        entonces los puntos del graﬁco seran [(0, 10), (1, 12), (2, 12)]
    ’normalizado’ El eje X corresponde a una enumeracion normalizada de los datos. Por ejemplo, si los datos son
        [10, 12, 13], los puntos del graﬁco seran [(0/(10+12+13), 10), (1/35, 12), (2/35, 12)]
    ’rango:a,b,c’ Dado un string con el formato ’rango:a,b,c’, se debera interpretar del siguiente modo: Se deﬁne
        un rango de valores dado [a, b] y un step c, el eje X se compondra por los numeros generados por dicho rango.
        Esto solo es posible si la cantidad de numeros generados por el rango es mayor o igual a la cantidad de datos.
        Ademas, si a<b, entonces c debe ser positivo; mientras que si a>b, entonces c debe ser negativo.
    Columna Si, en lugar de recibir un string, se recibe otra columna de datos en el argumento opcion,
        los valores de la nueva columna seran el eje X. Esta columna debe tener la misma cantidad de datos que la
        utilizada para el eje Y .
    '''
    if opcion == 'numerico':
        (plt.plot(punto) for punto in columna)

if __name__ == '__main__':
    graficar([(0, 10), (1,12), (2,12)], 'numerico')







