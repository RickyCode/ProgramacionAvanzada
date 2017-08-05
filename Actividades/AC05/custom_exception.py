
class CustomException(Exception):
    def __init__(self, caracter):
        super().__init__('El caracter {} no es un "0" o un "1"'.format(caracter))


def nuevo_lectura_archivo(nombre):
    with open(nombre, "r") as archivo:
        lineas = archivo.readlines()
        codigo = ''
        texto = "".join(lineas).replace('\n', '')
        a_encontrado = False
        chunk = ''
        for caracter in texto:
                if caracter == 'a':
                    a_encontrado = True
                if ((not a_encontrado) and caracter != 'a'):
                    codigo += caracter
                elif a_encontrado:
                    if caracter.isspace() and (len(chunk) > 0):
                        chunk = chunk[::-1]
                        codigo += (chunk + ' ')
                        chunk = ''
                    else:
                        chunk += caracter
        chunk = chunk[::-1]
        codigo += (chunk + ' ')
        return codigo


def nuevo_limpiador(lista):
    i = -1
    string = ''
    while i < len(lista)-1:
        i += 1
        if '$' != lista[i]:
            string += lista[i]
    return string