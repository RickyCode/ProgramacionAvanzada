__author__ = 'Ricardo Del Rio'

from os import getcwd

def es_csv(archivo_csv):
    '''
    Recibe un archivo csv y comprueba que termine en ".csv". De ser asi retorna True. De lo contrario False.
    '''
    return archivo_csv[-4:] == '.csv'

def importar_datos(archivo_csv):
    '''
    Recibe como parametro el directorio o el nombre de un archivo ".csv"
    Retorna una lista de listas (matriz) con los datos del arhivo.
    '''
    with open(archivo_csv,'r',encoding='utf-8') as archivo:
        lista_archivo = []
        lineas = archivo.readlines()
        for linea in lineas:
            linea = linea[:-1]
            palabra = ''
            lista_linea = []
            for caracter in linea:
                if caracter != ',':
                    palabra += caracter
                else:
                    lista_linea.append(palabra)
                    palabra = ''
            lista_linea.append(palabra.strip())
            lista_archivo.append(lista_linea)

    return lista_archivo

def exportar(matriz, archivo_csv, sobreescribir = False):
    '''
    Recibe una lista de listas de datos que se transforma en un string separado con comas y filas.
    Estas son guardadas en un archivo ".csv" con el nombre indicado.
    Se puede optar por sobreescribir un archivo o agregar los datos al final.
    '''
    if sobreescribir:
        modo = 'w'
    else:
        modo = 'a'

    with open(archivo_csv,modo) as archivo:
        for f in matriz:
            linea = ''
            for c in f:
                linea += (str(c) + ',')
            linea = linea[:len(linea)-1] + '\n'
            archivo.write(linea)


#-----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    matriz = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
              ['a', 'b', 'c', 'd', 'e', 'f'],
              ['g', 'h', 'i', 'j', 'k', 'l'],
              ['m', 'n', 'o', 'p', 'q', 'r'],
              ['s', 't', 'u', 'v', 'w', 'x']]
    exportar(matriz, 'prueba.csv', 1)



