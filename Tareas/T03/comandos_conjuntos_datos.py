
### Funciones de apoyo:

def generador_intervalo(inicio, final, intervalo):
    numero = inicio
    yield numero
    while (numero + intervalo) <= final:
        numero += intervalo
        yield numero

## ---------------------------------------------------------------------------COMANDOS QUE RETORNAN UN CONJUNTO DE DATOS

def extraer_columna(nombre_de_archivo, columna):
    '''
    Dado un nombre de archivo en formato csv, retorna la columna cuyo nombre (´o head) sea igual a columna.
    :param nombre_del_archivo: str
    :param columna: str
    :returns: Columna
    '''
    with open(nombre_de_archivo) as archivo:
        primera_linea = archivo.readline().strip().split(';')
        numero = primera_linea.index(list(filter(lambda x: x == columna, primera_linea))[0])
        columna = [linea.strip().split(';')[numero] for linea in archivo]
        return columna


def filtrar(columna, simbolo, valor):
    '''
    Dado un conjunto de datos en columna, retorna todos los que pasen el ﬁltro dado por sımbolo y valor.
    El argumento simbolo debe ser un simbolo de comparacion.
    :param columna: Columna
    :param simbolo: str
    :param valor: int or float
    :returns: Columna
    '''
    if simbolo == '==':
        return list(filter(lambda x: x == valor, columna))
    if simbolo == '>':
        return list(filter(lambda x: x > valor, columna))
    if simbolo == '<':
        return list(filter(lambda x: x < valor, columna))
    if simbolo == '>=':
        return list(filter(lambda x: x >= valor, columna))
    if simbolo == '<=':
        return list(filter(lambda x: x <= valor, columna))
    if simbolo == '!=':
        return list(filter(lambda x: x != valor, columna))


def operar(columna, simbolo, valor):
    '''Dado un conjunto de datos, un simbolo de operacion, y un valor, se aplica la operacion indicada por simbolo
    y valor a cada dato de columna, y se retornan esos resultados. Si el sımbolo es >=<, entonces valor debe ser ≥ 0,
    e indica cuantos decimales aproximar. El argumento sımbolo debe ser un sımbolo de operacion.
    '''
    if simbolo == '+':
        return list(map(lambda x: x + valor, columna))
    if simbolo == '-':
        return list(map(lambda x: x - valor, columna))
    if simbolo == '*':
        return list(map(lambda x: x * valor, columna))
    if simbolo == '/':
        return list(map(lambda x: x / valor, columna))
    if simbolo == '>=<':
        return list(map(lambda x: round(x,valor), columna))


def evaluar(funcion, inicio, final, intervalo):
    if isinstance(inicio,int) and isinstance(final, int) and isinstance(intervalo, int):
        return list(map(funcion, range(inicio,final+1,intervalo)))
    else:
        return list(map(funcion, (n for n in generador_intervalo(inicio, final, intervalo))))


if __name__== '__main__':
    columna = extraer_columna('encuesta_uno.csv','familiares_muertos: int')
    print(columna)
    print(type(columna))
    print('primer elemento: {}'.format(columna[0]))
    print('ultimo: {}'.format(columna[-1]))

    with open('encuesta_uno.csv') as archivo:
        lineas = archivo.readlines()

    print()
    print('largo dado por la columna de la funcion: {}'.format(len(columna)))
    print('largo correcto: {}'.format(len(lineas)))

    def funcion(numero):
        return numero
    print()
    print(evaluar(funcion, 0.1, 1, 0.1))