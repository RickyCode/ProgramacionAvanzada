from variables_y_comandos import funciones

def llamar_funcion(nombre, *args):
    if args != ([],):
        funciones[nombre](*args[0])
    else:
        funciones[nombre]()
    texto = "\nSe ejecuto la funcion {0}\ncon los argumentos\n{1}". format(nombre,args[0])
    return texto

def interpretar(lista_comandos):
    '''
    Esta funcion recibe una lista de comandos.
    Por cada comando que se desea ejecutar llama a las funciones asociadas.
    '''
    nombres_comandos = [comando[0] for comando in lista_comandos]
    print('nombres comandos', str(nombres_comandos))
    atributos_comandos = [comando[1:] for comando in lista_comandos]
    print('Atributos comandos', str(atributos_comandos))
    print()
    return list(map(llamar_funcion, nombres_comandos, atributos_comandos))

if __name__ == '__main__':
    lista = [['imprimir','chao ',11],['imprimir', 'jajajja ', 3],['imprimir_hola']]
    print('\n'.join(interpretar(lista)))
