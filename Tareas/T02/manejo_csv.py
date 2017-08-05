__author__ = 'Ricardo Del Rio'
# ***   VERSION MODIFICADA PARA TAREA 02 DE PRORAMACION AVANZADA   ***
# Libre de estructuras python

from estructuras_propias import ListaLigada, split, join

def es_csv(archivo_csv):
    '''
    Recibe un archivo csv y comprueba que termine en ".csv". De ser asi retorna True. De lo contrario False.
    '''
    return archivo_csv[-4:] == '.csv'


def importar_datos(archivo_csv, simbolo=','):
    '''
    Recibe como parametro el directorio o el nombre de un archivo ".csv"
    Retorna una lista de listas (matriz) con los datos del arhivo.
    '''
    with open(archivo_csv, 'r') as archivo:
        lista_archivo = ListaLigada()
        for linea in archivo:
            # esta funcion retorna una ListaLigada
            lista_linea = split(linea.strip('\n'), simbolo)
            lista_archivo.append(lista_linea)
    return lista_archivo


def exportar(matriz, archivo_csv, sobreescribir=False):
    '''
    Recibe una lista de listas de datos que se transforma en un string separado con comas y filas.
    Estas son guardadas en un archivo ".csv" con el nombre indicado.
    Se puede optar por sobreescribir un archivo o agregar los datos al final.
    '''
    if sobreescribir:
        modo = 'w'
    else:
        modo = 'a'

    with open(archivo_csv, modo) as archivo:
        for f in matriz:
            linea = join(', ', f)
            archivo.write(linea + '\n')

#-------------------------------------------------------------------------


if __name__ == '__main__':

    matriz = ListaLigada(ListaLigada(1, 2, 3, 4, 5, 6, 7, 8, 9),
                         ListaLigada('a', 'b', 'c', 'd', 'e', 'f'),
                         ListaLigada('g', 'h', 'i', 'j', 'k', 'l'),
                         ListaLigada('m', 'n', 'o', 'p', 'q', 'r'),
                         ListaLigada('s', 't', 'u', 'v', 'w', 'x'))
    exportar(matriz, 'prueba.csv', 1)

    '''
    lista = importar_datos('population.csv')
    print(lista)
    '''
