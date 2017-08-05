import unittest
import main


class TestearFormato(unittest.TestCase):

    def test_archivo(self):
        #Veriﬁca que cada caracter sea de tipo string, adem´as de que la cantidad de estos sea igual a 408 y la
        # sumatoria de todos sea igual a 253.
        descifrador = main.Descifrador('mensaje_marciano.txt')

        with open('mensaje_marciano.txt') as archivo:
            lista = archivo.readlines()
            texto = lista.join()

        for c in texto:
            self.assertIsInstance(c,str)





class TestearMensaje(unittest.TestCase):
    def test_incorrectos(self):
        # Comprueba que no existan secuencias codiﬁcadas incorrectas, de un largo menor a 6 o mayor a 7 d´ıgitos,
        # #veriﬁca el funcionamiento de la funci´on elimina incorrectos.
        pass

    def test_caracteres(self):
        # Comprueba que no existan caracteres incorrectos en el mensaje decodiﬁcado, veriﬁca el funcionamiento de la
        # funci´on limpiador.
        pass

    def test_codificacion(self):
        #Comprueba que el mensaje codiﬁcado correctamente escrito contenga solo caracteres 1’s y 0’s.
        pass
