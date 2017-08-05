from comandos_basicos import *
from comandos_conjuntos_datos import *
from comandos_valor_numerico import *
from comandos_booleano import *
from comandos_compuestos import *
from distribuciones_probabilidad import *

def imprimir(palabra,num): # PRUEBA
    texto = palabra*num + str(num)
    print('texto funcion imprimir: {}'.format(texto))

def imprimir_hola(): #PRUEBA
    texto = "hola"
    print('texto funcion impimir hola: {}'.format(texto))

funciones = {#Comandos Basicos
             "asignar": asignar,
             "crear_funcion": crear_funcion,
             'graficar': graficar,
             #Comandos que retornan onjuntos de datos
             'extraer_columna': extraer_columna,
             'filtrar': filtrar,
             'operar': operar,
             'evaluar': evaluar,
             #Comandos que retornan valor numerico
             'LEN': LEN,
             'PROM': PROM,
             'DESV': DESV,
             'MEDIAN': MEDIAN,
             'VAR': VAR,
             #Comandos que retornan un booleano
             'comparar_columna': comparar_columna,
             'comparar': comparar,
             #Comandos compuestos
             'do_if': do_if,
             #Comandos de Prueba
             "imprimir_hola": imprimir_hola,
             "imprimir": imprimir,
             #Distribuciones
             'normal': normal,
             'exponencial': exponencial,
             'gamma': gamma}

nuevas_variables_funciones = {}

distribuciones = {'normal': normal,
                  'exponencial': exponencial,
                  'gamma': gamma}