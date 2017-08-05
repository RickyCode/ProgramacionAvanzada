# PRIMERA PARTE: Estructura basica
from linklist import LList

# SEGUNDA PARTE: Clase Isla


class Isla:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conexiones = LList()

    def __repr__(self):
        return self.nombre

    def agregarConexion(self, isla):
        self.conexiones.add_end(isla)


# TERCERA PARTE: Clase Archipielago
class Archipielago:
    def __init__(self, nombre):
        self.nombre = nombre
        self.islas = LList()
        self.construir(nombre)

    def agregar_isla(self, nombre):
        if isinstance(nombre, Isla):
            isla = nombre  # nombre es un objeto isla
        else:
            isla = Isla(nombre)
        self.islas.add_end(isla)

    def conectadas(self, nombre_origen, nombre_destino):
        pass

    def agregar_conexion(self, nombre_origen, nombre_destino):
        a = self.islas.contains(nombre_origen)
        if not a:
            #print(nombre_origen)
            #print("NO PRESENTE\n")
            isla_origen = Isla(nombre_origen)
            self.agregar_isla(isla_origen)
        else:
            pos_isla_origen = self.islas.find(nombre_origen)
            isla_origen = self.islas.getValue(pos_isla_origen)
        b = self.islas.contains(nombre_destino)
        if not b:
            #print(nombre_destino)
            #print("NO PRESENTE\n")
            isla_destino = Isla(nombre_destino)
            self.agregar_isla(isla_destino)
        else:
            pos_isla_destino = self.islas.find(nombre_destino)
            isla_destino = self.islas.getValue(pos_isla_destino)
        isla_origen.agregarConexion(isla_destino)
        #input("")

    def construir(self, archivo):
        with open('mapa.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                print("b")
                line_txt = line[:-1]
                nombre_origen, nombre_destino = line_txt.split(',')
                self.agregar_conexion(nombre_origen, nombre_destino)

    def propagacion(self, nombre_origen, lista_islas=None):
        if not(lista_islas):  # caso inicial
            pos_isla_actual = self.islas.find(nombre_origen)
            isla_actual = self.islas.getValue(pos_isla_actual)
            lista_islas = LList()
        else:
            isla_actual = nombre_origen  # va a ser de tipo isla
        print(type(isla_actual))
        if isla_actual.conexiones.get_len() > 0:
            for destino in isla_actual.conexiones:
                if destino.conexiones.get_len() > 0:
                    for conexion in destino.conexiones:
                        # agregar conexiones nuevas
                        if lista_islas.contains(conexion.nombre):
                            pass
                        else:
                            lista_islas.add_end(conexion)
                    return self.propagacion(destino, lista_islas)
        return lista_islas

    def __repr__(self, text=""):
        for isla in self.islas:
            text += "{} ->".format(isla.value.nombre)
            print("ORIGEN")
            print(isla.value.nombre)
            if isla.value.conexiones.get_len() > 0:
                sub_isla_text = ""
                for i in isla.value.conexiones:
                    sub_isla_text += i.value.nombre + ","
                    print(i.value.nombre)
                input("SOLA CONEXION")
                sub_isla_text = sub_isla_text[:-1]
            text += sub_isla_text + "\n"
            input(text)
        return text


if __name__ == '__main__':
    # No modificar desde esta linea
    # (puedes comentar lo que no este funcionando aun)
    arch = Archipielago("mapa.txt")  # Instancia y construye
    print(arch)  # Imprime el Archipielago de una forma que se pueda entender
    print(arch.propagacion("Perresus"))
    print(arch.propagacion("Pasesterot"))
    print(arch.propagacion("Cartonat"))
    print(arch.propagacion("Womeston"))
