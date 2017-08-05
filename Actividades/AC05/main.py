from custom_exception import CustomException, nuevo_lectura_archivo, nuevo_limpiador

class Descifrador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.suma=0
        with open(self.nombre, "r") as self.archivo:
            lineas = self.archivo.readlines()
            self.codigo = ''
            self.texto = "".join(lineas).replace('\n', '')
            i = 0

    def lectura_archivo(self):
        with open(self.nombre, "r") as archivo:
            lineas = archivo.readlines()
            self.codigo = ''
            texto = "".join(lineas).replace('\n', '')
            for caracter in texto:

                #-------------------1
                if not (caracter == '0' or caracter == '1'):
                    raise CustomException(caracter)
                #-------------------1

                self.codigo += caracter
            return self.codigo

    def elimina_incorrectos(self):
        lista=self.codigo.split(" ")
        self.codigo=''
        for i in lista:
            if len(i) < 6 or len(i) > 7:
                pass
            else:
                self.codigo+=' '+i
        return self.codigo

    def cambiar_binario(self, binario):
        lista = binario.split(' ')
        texto = []
        for x in lista[1:]:
            texto.append(chr(int(x, 2)))
        return texto

    def limpiador(self, lista):
        i = -1
        string = ''
        while i < len(lista):
            i += 1
            if '$' != lista[i]:
                string += lista[i]
        return string

if __name__ == "__main__":
    try:
        des = Descifrador('mensaje_marciano.txt')

        # -------------1
        try:
            codigo = des.lectura_archivo()
        except CustomException as error:
            print('Error: {}'.format(error))
            codigo = nuevo_lectura_archivo('mensaje_marciano.txt')
            des.codigo = codigo
        # -------------1

        codigo=des.elimina_incorrectos()

        # -------------2
        try:
            lista = des.cambiar_binarios(des.codigo)
        except AttributeError as error:
            print('Error: {}'.format(error))
            lista = des.cambiar_binario(des.codigo)
        # -------------2

        # -------------3
        try:
            texto = des.limpiador(lista)
        except IndexError as error:
            print('Error: {}'.format(error))
            texto = nuevo_limpiador(lista)
        # -------------3

        print(texto)

    except Exception as err:
        print('Esto no debiese imprimirse')