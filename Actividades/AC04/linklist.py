class SNodo:  # SimpleNodo

    def __init__(self, value):
        self.value = value
        self.sig = None


class LList:

    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.length = 0

    def isEmpty(self):
        if self.primero is None:
            return True
        else:
            False

    def add_end(self, value):
        nodo = SNodo(value)
        if self.isEmpty():
            self.primero = nodo
            self.ultimo = self.primero
            self.set_len()
        else:
            self.ultimo.sig = nodo
            self.ultimo = nodo
            self.set_len()

    def add_start(self, value):
        nodo = SNodo(value)
        if self.isEmpty():
            self.primero = nodo
            self.ultimo = self.primero
            self.set_len()
        else:
            temp = self.primero
            self.primero = nodo
            self.primero.sig = temp
            self.set_len()

    def del_start(self):
        if self.isEmpty():
            print("Lista vacia. Operacion no valida")
        elif self.primero == self.ultimo:
            self.primero = None
            self.primero = self.ultimo
            self.set_len()
        else:
            temp = self.primero
            self.primero = self.primero.sig
            temp = None
            self.set_len()

    def del_end(self):
        if self.isEmpty():
            print("Lista vacia. Operacion no valida")
        elif self.primero == self.ultimo:
            self.ultimo = None
            self.ultimo = self.primero
            self.set_len()
        else:
            nodo_actual = self.primero
            while nodo_actual:
                if nodo_actual.sig == self.ultimo:
                    temp = self.ultimo
                    self.ultimo = nodo_actual
                    nodo_actual.sig = None
                    temp = None
                    self.set_len()
                else:
                    nodo_actual = nodo_actual.sig

    def listar(self):
        if self.isEmpty():
            print("lista vacia")
        else:
            nodo_actual = self.primero
            while nodo_actual:
                print(nodo_actual.value)
                nodo_actual = nodo_actual.sig

    def getValue(self, position, item=False):  # item define si retorna nodo o valor
        if self.get_len() > 0 and position >= 0 and position <= self.get_len():
            cursor = 0
            nodo_actual = self.primero
            while nodo_actual:
                if cursor == position:
                    if item:  # se retorna nodo
                        return nodo_actual
                    else:  # se retorna valor de nodo
                        return nodo_actual.value
                else:
                    cursor = cursor + 1
                    nodo_actual = nodo_actual.sig
        else:
            if position < 0 or position > self.get_len():
                print("Posicion inexistente")
            elif self.get_len() == 0:
                print("Lista vacia")
            else:
                pass

    def contains(self, value_search, printing=False):  # retorna bool si existe value en lista
        if self.isEmpty():
            return False
        else:
            nodo_actual = self.primero
            while nodo_actual:
                if nodo_actual.value.nombre == value_search:
                    return True
                else:
                    if nodo_actual.sig is None:
                        break
                    else:
                        nodo_actual = nodo_actual.sig
            return False

    def find(self, value_search):
        if self.isEmpty():
            #print("lista vacia")
            return False
        else:
            contador = -1
            nodo_actual = self.primero
            while nodo_actual:
                contador += 1
                if nodo_actual.value == value_search:
                    return contador
                else:
                    if nodo_actual.sig is None:
                        break
                    else:
                        nodo_actual = nodo_actual.sig
            return -1

    def set_len(self):
        if self.isEmpty():
            self.length = 0
        else:
            length1 = 0
            nodo_actual = self.primero
            while nodo_actual:
                length1 += 1
                nodo_actual = nodo_actual.sig
            self.length = length1

    def get_len(self):
        return self.length

    def __repr__(self):
        ret = "["
        nodo_actual = self.primero
        while nodo_actual:
            ret += "{}, ".format(nodo_actual.value)
            nodo_actual = nodo_actual.sig
        return ret.strip(", ") + "]"

    def __getitem__(self, i):  # retorna nodos, no valores
        elem_actual = self.primero
        for _ in range(i):
            if elem_actual:
                elem_actual = elem_actual.sig
        if not elem_actual:
            raise IndexError(
                "El indice ingresado está fuera del rango de la lista")
        return elem_actual

    def del_pos(self, pos):
        if pos < 0 or pos >= self.length:
            #print("ERROR: Posicion inexistente para borrar")
            return ""
        if pos == 0:  # 0
            self.del_start()
        elif pos == self.length - 1:  # ultima posicion
            self.del_end()
        else:
            nodo_ant = self.getValue(pos - 1, True)
            nodo_actual = nodo_ant.sig
            nodo_sig = nodo_actual.sig
            nodo_ant.sig = None
            nodo_ant.sig = nodo_sig
            nodo_actual = None
            self.set_len()
"""
a=LList()
for i in range(20):
    a.add_end(i)
print(a)
a.del_pos(15)
print(a)
print(a.getValue(18))
"""
