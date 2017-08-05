

def comparar_columna(columna_1, simbolo, comando, columna_2):
    nueva_c1 = map(comando, columna_1)
    nueva_c2 = map(comando, columna_2)
    if simbolo == '==':
        return list(map(lambda x,y: x == y, nueva_c1, nueva_c2))
    if simbolo == '<':
        return list(map(lambda x,y: x < y, nueva_c1, nueva_c2))
    if simbolo == '>':
        return list(map(lambda x,y: x > y, nueva_c1, nueva_c2))
    if simbolo == '<=':
        return list(map(lambda x,y: x <= y, nueva_c1, nueva_c2))
    if simbolo == '>=':
        return list(map(lambda x,y: x >= y, nueva_c1, nueva_c2))
    if simbolo == '!=':
        return list(map(lambda x,y: x != y, nueva_c1, nueva_c2))

def comparar(numero_1, simbolo, numero_2):
    if simbolo == '==':
        return numero_1 == numero_2
    if simbolo == '<':
        return numero_1 < numero_2
    if simbolo == '>':
        return numero_1 > numero_2
    if simbolo == '<=':
        return numero_1 <= numero_2
    if simbolo == '>=':
        return numero_1 >= numero_2
    if simbolo == '!=':
        return numero_1 != numero_2



if __name__ == '__main__':

    columna_1 = [1,3,5,7,9]
    columna_2 = [2,4,6,8,10]

    def comando(num):
        return num+1

    print(comparar_columna(columna_1, '==', comando, columna_2))
