__author__ = 'Ricardo Del Rio'

from simplificadores import SuperInput
from manejo_csv import importar_datos, exportar

#-----------------------------------------------------------------------------------------------------------------------

class Usuarios:
    lista_usuarios = []
    ultimo_id = ''
    usuario_contrasena = {}


    def cargar_datos(self):
        datos = importar_datos('usuarios.csv') #datos[fila(f)][columna(c)]

        for f in range(len(datos)): #recorre filas
            if  f == 0:
                if datos[0][0][0] == '\ufeff':
                    datos[0][0] = datos[0][0][1:]

            if f != 0:
                for c in range(len(datos[f])): #recorre columnas
                    if datos[0][c] == 'id:string':
                        idn = datos[f][c]
                    elif datos[0][c] == 'nombre:string':
                        nombre = datos[f][c]
                    elif datos[0][c] == 'contraseña:string':
                        contrasena = datos[f][c]
                    elif datos[0][c] == 'recurso_id:string':
                        recurso_id = datos[f][c]
                usuario = Usuario(idn, nombre, contrasena, recurso_id)
                self.lista_usuarios.append(usuario)
                self.usuario_contrasena[nombre] = contrasena
        if len(self.lista_usuarios) > 0:
            self.lista_usuarios.sort()
            self.ultimo_id = self.lista_usuarios[-1].idn

    def guardar_datos(self):
        matriz = []
        for i in self.lista_usuarios:
            matriz.append(i.en_lista)
        exportar(matriz, 'incendios.csv', 1)

    def verificacion_usuario_contrasena(self):
        stop = False
        while not stop:
            nombre = SuperInput('Ingresa el nombre de usuario: ').superinput()
            contrasena = SuperInput('Ingresa la contrasena: ').superinput()

            if self.usuario_contrasena.get(nombre):
                if self.usuario_contrasena[nombre] == contrasena:
                    stop = True
                    for usuario in self.lista_usuarios:
                        if usuario.nombre == nombre:
                            return usuario.recurso_id
                else:
                    print('Contrasena incorrecta! \n')
            else:
                print('El usuario no existe! \n')

    def agregar_usuario(self):
        idn = str(int(self.ultimo_id)+1)
        nombre = SuperInput('>>> Nombre Usuario: ', 'str').superinput()
        stop = False
        while not stop:
            contrasena = SuperInput('>>> Contraseña: ', 'str').superinput()
            contrasena2 = SuperInput('>>> Repita Contrasena: ', 'str').superinput()
            if contrasena == contrasena2:
                stop = True
            else:
                print('Las contrasenas no coinciden \n')
        recurso = SuperInput('>>> Recurso: ', 'int').superinput()
        usuario = Usuario(idn, nombre, contrasena, recurso)
        self.usuario_contrasena[nombre] = contrasena
        self.lista_usuarios.append(usuario)
        self.ultimo_id = self.lista_usuarios.sort()[-1].idn
        self.guardar_datos()

    def eliminar_usuario(self):
        print('\n LISTADO DE USUARIOS ACTUALES DEL SISTEMA: \n')
        for usuario in self.lista_usuarios:
            print(usuario)
        print()
        stop = False
        while not stop:
            identificador = SuperInput('>>> Ingresa el ID del usuario a eliminar: ').superinput()
            for usuario in self.lista_usuarios:
                if usuario.idn == identificador:
                    del self.usuario_contrasena[usuario.nombre]
                    self.lista_usuarios.pop(usuario)
                    stop = True
            if not stop:
                print('El usuario ingresado no existe. \n')
        self.guardar_datos()

    def modificar_usuario(self):
        print('\n LISTADO DE USUARIOS ACTUALES DEL SISTEMA: \n')
        for usuario in self.lista_usuarios:
            print(usuario)
        print()
        stop = False
        while not stop:
            identificador = SuperInput('>>> Ingresa el ID del usuario a modificar: ',).superinput()
            for usuario in self.lista_usuarios:
                if usuario.idn == identificador:
                    print('\n Estos son los datos del usuario seleccionado: \n')
                    print(usuario.detalles())
                    print('\n Escribe los nuevos datos o presiona <enter> para para NO modificar cierta informacion:\n')

                    nombre = SuperInput('Nombre: ').superinput()
                    stop = False
                    while not stop:
                        contrasena = SuperInput('>>> Contraseña: ', 'str').superinput()
                        contrasena2 = SuperInput('>>> Repita Contrasena: ', 'str').superinput()
                        if contrasena == contrasena2:
                            stop = True
                        else:
                            print('Las contrasenas no coinciden \n')
                    recurso = SuperInput('Recurso ID: ')

                    if nombre:
                        usuario.nombre = nombre
                    if contrasena:
                        usuario.contrasena = contrasena
                    if recurso:
                        usuario.recurso_id = recurso
                    self.usuario_contrasena[nombre] = contrasena
                    stop = True

            if not stop:
                print('El usuario ingresado no existe. \n')
        self.guardar_datos()


    def __str__(self):
        texto =''
        for usuario in self.lista_usuarios:
            texto += (usuario.detalles() + '\n')
        return texto




#-----------------------------------------------------------------------------------------------------------------------

class Usuario:
    def __init__(self, idn, nombre, contrasena, recurso_id):
        self.idn = idn
        self.nombre = nombre
        self.contrasena = contrasena
        self.recurso_id = recurso_id

    def en_lista(self):
        return [self.idn, self.nombre, self.contrasena, self.recurso_id]

    def __str__(self):
        return '%5s %20s' %(self.contrasena, self.recurso_id)

    def detalles(self):
        return 'ID: %5s \n Nombre: %15s \n Contrasena: %15s \n Recurso ID: %10s '  %(self.idn, self.nombre,
                                                                              self.contrasena, self.recurso_id)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.idn < other.idn



#-----------------------------------------------------------------------------------------------------------------------

class UsuarioANAF(Usuario):
    def __init__(self):
        Usuario.__init__(self, idn, nombre, contrasena, recurso_id)



#-----------------------------------------------------------------------------------------------------------------------


class Piloto(Usuario):
    def __init__(self):
        Usuario.__init__(self, idn, nombre, contrasena, recurso_id)

#-----------------------------------------------------------------------------------------------------------------------


class Jefe(Usuario):
    def __init__(self):
        Usuario.__init__(self, idn, nombre, contrasena, recurso_id)


