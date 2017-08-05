__author__ = 'Ricardo Del Río'
# Libre de estructuras Python


# Algoritmos basado en http://librosweb.es/libro/algoritmos_python/capitulo_16
# y material del curso Programación Avanzada de la Pontificia Universidad
# Catolica de Chile del 1er semestre del 2017.

class Nodo:

    def __init__(self, dato=None, prox=None):
        self.dato = dato
        self.prox = prox

    def __str__(self):
        return str(self.dato)


class _IteradorListaLigada:
    '''Iterador para la Clase ListaLigada'''

    def __init__(self, comienzo):
        self.actual = comienzo

    def __next__(self):
        '''Devuelve uno a uno los elementos'''
        if self.actual is None:
            raise StopIteration('No hay mas elementos en la lista')
        # Guarda eL dato:
        dato = self.actual.dato
        # Avanza en la lista:
        self.actual = self.actual.prox
        # Devuelve el dato:
        return dato


class ListaLigada:
    '''Modela una Lista Ligada compuesta or nodos'''
    # Evaluar el cnvertirla en una Lista Doblemente Ligada

    def __init__(self, *args):
        # Primer elemento:
        self.cabeza = None
        self.cola = None
        # len es cero cuando la lista esta vacia
        self.len = 0
        # Si se entregan elementos para añadir a la lista:
        if args:
            for elemento in args:
                self.append(elemento)

    def __call__(self, *args):
        # Si se entregan elementos para añadir a la lista:
        if args:
            for elemento in args:
                self.append(elemento)
        # Si no:
        else:
            raise ValueError(
                'No se ingresaron elementos para anadir a la lista.')

    def append(self, elemento):
        '''Agrega un elemento a la lista'''
        # Revisa si la lista tiene comienzo. Sino se crea un primer nodo.
        if not self.cabeza:
            self.cabeza = Nodo(elemento)
            self.cola = self.cabeza
        # Si ya tiene comienzo:
        else:
            self.cola.prox = Nodo(elemento)
            self.cola = self.cola.prox
        self.len += 1

    def pop(self, pos=None):
        '''
        Remueve y retorna el elemento de la ubicacion 'pos'
        Si no se entrega una ubicacion, elimina y retorna l ultimo elemento de la lista.
        '''
        # No esta implemetado para posiciones negativas.
        # Evaluar su implementeacion a futuro.
        # Si no se entrega una posicion de la lista:
        if not pos:
            pos = self.len - 1
        # Si se entrega:
        else:
            nodo = self.cabeza
            # Revisa que el elemento este en la lista o genera un IndexError:
            if pos < 0:
                raise IndexError('Esta lista solo recibe indices positivos')
            if pos >= self.len:
                raise IndexError(
                    'La lista posee menos de {} elementos'.format(
                        pos + 1))
        # Si se desea eliminar el primer elemento:
        if pos == 0:
            dato = self.cabeza.dato
            self.cabeza = self.cabeza.prox
        # Para eliminar cualquier otro elemento
        else:
            n_anterior = self.cabeza
            n_actual = self.cabeza.prox
            for i in range(1, pos):
                n_anterior = n_actual
                n_actual = n_actual.prox
            # Guarda el dato y elimina el nodo a borrar
            dato = n_actual.dato
            n_anterior.prox = n_actual.prox
        # Se modifica la longitud de la lista y se retorna el dato:
        self.len -= 1
        return dato

    def __str__(self):
        pass

    def __len__(self):
        return self.len

    def insert(self, pos, elem):
        '''Inserta el elemento 'elem' en la poscicion 'pos'
        Si la posicion no es valida, levanta un IndexError
        '''
        # Se revisa que la posicion sea valida
        if pos < 0:
            raise IndexError('Esta lista solo recibe indices positivos')
        if pos >= self.len:
            raise IndexError(
                'La lista posee menos de {} elementos'.format(
                    pos + 1))
        # Si se quiere insertar el elemento al principio:
        if pos == 0:
            nuevo_nodo = Nodo(elem, self.cabeza)
            self.cabeza = nuevo_nodo
        # Si se quiere insertar en otra posicion:
        else:
            n_anterior = self.cabeza
            for i in range(1, pos):
                n_anterior = n_anterior.prox
            # Se agrega el nuevo elemento:
            nuevo_nodo = Nodo(elem, n_anterior.prox)
            n_anterior.prox = nuevo_nodo
        # Modifica el largo dela lista:
        self.len += 1

    def remove(self, elemento):
        '''
        Elimina la primera aparicion de 'elemento' en la lista
        Si el elemento no esta e la lista se le vanta un ValueError'''
        # Si la lista esta vacia:
        if self.len == 0:
            raise ValueError('Lista vacia')
        # Si el elemento esta en a primera posicion:
        elif self.cabeza.dato == elemento:
            self.cabeza = self.cabeza.prox
            self.len -= 1
        # Si el elemento esta en otra posicion:
        else:
            n_anterior = self.cabeza
            n_actual = self.cabeza.prox
            for i in range(1, self.len):
                n_anterior = n_actual
                n_actual = n_actual.prox
                # Si encuentra el elemento lo elimina:
                if n_actual.dato == elemento:
                    n_anterior.prox = n_actual.prox
                    self.len -= 1
                    #del n_actual
                    return
            raise ValueError('El elemento no se encuentra en la lista')

    def __iter__(self):
        '''Devuelve el iterador de la lista'''
        return _IteradorListaLigada(self.cabeza)

    def index(self, elem):
        '''
        Recibe un elemento. Si este se encuentra en la lista, retorna la posicion.
        Si el elemento no existe levanta un ValueError
        '''
        # Si la lista esta vacia:
        if self.len == 0:
            raise ValueError('Lista vacia')
        n_actual = self.cabeza
        # Busca el elemento:
        for i in range(self.len + 1):
            # Si encuentra el elemento retorna su ubicacion:
            if n_actual.dato == elem:
                return i
            # avanza al nodo siguiente:
            n_actual = n_actual.prox
        raise ValueError('El elemento no se encuentra en la lista')

    def clear(self):
        self.cabeza = None
        self.cola = None
        self.len = 0

    def __add__(self, other):
        lista = ListaLigada()
        for i in self:
            lista.append(i)
        for i in other:
            lista.append(i)
        return lista

    def __sub__(self, other):
        lista = ListaLigada
        for i in self:
            lista.append()
        for i in other:
            if i in lista:
                lista.remove(i)
        return lista

    def __getitem__(self, pos):
        if (pos < 0) or (pos >= self.len):
            raise IndexError(
                'La lista no tiene un elemento en la posicion {} El ultimo elemento esta en la posicion {}'.format(
                    pos, self.len - 1))
        n_actual = self.cabeza
        for i in range(self.len):
            if i == pos:
                return n_actual.dato
            n_actual = n_actual.prox

    def get_slice(self, comienzo, termino):
        if (comienzo < 0) or (termino >= self.len):
            raise IndexError(
                'El primer numero no puede ser menor que 0, y el segundo no puede ser mayor que {}'.format(
                    self.len - 1))
        n_actual = self.cabeza
        lista = ListaLigada()
        for i in range(self.len):
            n_actual = n_actual.prox
            if (i > comienzo) and (i < termino):
                lista.append(n_actual.dato)
        return lista

    def elementos_unicos(self):
        lista = ListaLigada()
        for i in self:
            if not(i in lista):
                lista.append(i)
        return lista

    def __contains__(self, item):
        n_actual = self.cabeza
        for i in self:
            if item == i:
                return True
        return False

    def __delitem__(self, key):
        pass


# Funciones para usar con Listas Ligadas:


def split(texto, simbolo=','):
    palabra = ''
    lista_palabras = ListaLigada()
    for c in texto:
        if c == simbolo:
            lista_palabras.append(palabra)
            palabra = ''
        else:
            palabra += c
    lista_palabras.append(palabra)
    return lista_palabras


def join(simbolo, lista):
    texto = ''
    for palabra in lista:
        texto += (str(palabra) + simbolo)
    return texto


#--------------------------------------------------DICCIONARIO------------

class Diccionario:
    def __init__(self):
        self.llaves = ListaLigada()
        self.valores = ListaLigada()

    def __getitem__(self, llave):
        '''Permite ingresar una llave en parentesis de corchete. Ej: diccionario['llave'] '''

        # Si la llave esta en la lista de llaves:
        if llave in self.llaves:
            return self.valores[self.llaves.index(llave)]
        # Si no esta:
        else:
            raise KeyError('La llave entregada no pertenece al diccionario')

    def __setitem__(self, llave, valor):
        '''Permite asignar un valor a la llave. Ej: diccionario[llave] = valor'''
        # Si la llave esta en la lista de llaves:
        try:
            pos = self.llaves.index(llave)
            self.valores[pos] = valor
        # Si no esta:
        except BaseException:
            self.llaves.append(llave)
            self.valores.append(valor)

    def __contains__(self, llave):
        return llave in self.llaves

    def __delitem__(self, llave):
        pos = self.llaves[llave]
        del self.llaves[pos]
        del self.valores[pos]

    def __eq__(self, other):
        return self.llaves == other.llaves and self.valores == other.valores

    '''
    def __ge__(self, other):
        pass
    def __getattribute__(self, item):
        pass
    '''

    def __gt__(self, other):
        return len(self.llaves) > len(other.llaves)

    '''
    def __iter__(self, /):
        pass
    '''

    def __le__(self, other):
        pass

    def __len__(self):
        return len(self.llaves)

    def __lt__(self, other):
        pass

    def __ne__(self, other):
        pass

    '''
    def __new__(cls, *args, **kwargs):
        pass
    '''

    def __repr__(self):
        texto_dic = '{'
        for i in range(len(self.llaves)):
            texto_dic += '{0}: {1} , '.format(self.llaves[i], self.valores[i])
        texto_dic += '}'
        return repr(texto_dic)

    '''
    def __sizeof__(self):
        pass
    '''

    def clear(self):
        self.llaves.clear()
        self.valores.clear()

    def copy(self):
        return self

    def fromkeys(self):
        pass

    def get(self):
        pass

    def items(self):
        pass

    def keys(self):
        pass

    def pop(self, pos):
        pass  # esta es importante, completar


class Conjunto(ListaLigada):
    def __init__(self):
        pass


class Cola:
    def __init__(self):
        pass


class Pila:
    def __init__(self):
        pass


class Grafo:
    def __init__(self):
        pass


#----------------------------------------------------EJECUCION____________

if __name__ == '__main__':

    # Pruebas de liista ligada:
    print('Pruebas de lista ligada')
    lista = ListaLigada()
    lista.append(1)
    lista.append(2)
    lista.append(3)
    lista.append(4)
    lista.append(5)
    for i in lista:
        print(i)
    print('---')
    lista.clear()
    for i in lista:
        print(i)
    print('---')
    lista2 = ListaLigada(1, 2, 3, 4, 5)
    for i in lista2:
        print(i)
    print('---')
    lista(1, 2, 3, 4, 5)
    for i in lista:
        print(i)
    print('---')
    print(isinstance(lista, ListaLigada))
    print('---')
    print(5 in lista)
    print('---')
    print(lista[0])
    print(lista[1])
    print(lista[2])
    print(lista[3])
    print(lista[4])
    print(lista[5])
    print(lista[10])
    print(lista[2:])

    print('\n')

    # Prueba de diccionario
    print('Prueba de diccionario')
    diccionario = Diccionario()
    diccionario['hola'] = 'hola'
    print(diccionario['hola'])
    diccionario['hola'] = 'hello'
    print(diccionario['hola'])
    diccionario['hello'] = 'hello'
    print(diccionario['hello'])

    dict2 = diccionario
    print(str(diccionario == dict2))
    print(diccionario)
    dict3 = diccionario.copy()
    print(dict3)

    print('\n')

    # Prueba Split:
    texto = 'manzana,platano,uva,naranja'
    lista = split(texto)
    print(*lista)
    print(lista[1])  # segundo elemento

    print('\n')

    # Prueba Join
    print('prueba join')
    lista = ListaLigada('perro', 'conejo', 'cacatua')
    texto = join(', ', lista)
    print(texto)
    print(type(texto))
