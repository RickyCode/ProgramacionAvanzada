__author__ = 'Ricardo Del Rio'
# Libre de estructuras python

# ----------------------------------- Imports ----------------------------

from manejo_csv import importar_datos
from pais import Pais
from simplificadores import Menu
from os import path
from connections_generator import generate_connections
from estructuras_propias import ListaLigada
from mundo import Mundo

# ----------------------------------- Definicion de clases ------------


class Juego:
    def __init__(self):
        self.dia_actual = 0
        self.salir = False
        self.mundo = Mundo()

    def comenzar(self):
        '''
        Si hay una partida guardada pregunta al usuario si abirla o crear una nueva.
        Si no hay una partida guardada le avisa al usuario y comienza una nueva partida.
        '''
        if path.isfile('partida_guardada.csv'):
            lista1 = ListaLigada(
                'Comenzar Nueva Partida',
                'Comenzar Partida Guardada')
            lista2 = ListaLigada(self.partida_nueva, self.partida_guardada)
            Menu(lista1, lista2).menu()
        else:
            print('No hay partidas guardadas. \nSe ha iniciado una nueva partida.\n')
            self.partida_nueva()

    def cargar_conexiones(self):
        '''
        Carga las conexiones terrestres y aereas
        '''
        self.mundo.establecer_conecciones_terrestres()
        self.mundo.establecer_conexiones_aereas()

    def partida_nueva(self):
        '''
        LLama a la funcion que genera las conexiones aereas.
        Llama al metodo que carga los datos de las conexiones en los grafos correspondientes
        Lee el archivo 'population.csv' y crea objetos de la clase Pais con cada linea del archivo.
        '''
        generate_connections()
        self.cargar_conexiones()
        self.mundo.lista_paises = ListaLigada()
        for datos_pais in importar_datos('population.csv'):
            if datos_pais[0] == 'Pais':
                pass
            else:
                nuevo_pais = Pais(*datos_pais)
                self.mundo.lista_paises.append(nuevo_pais)

    def partida_guardada(self):
        '''
        Como es una partida ya creada no llama al generador de conexiones aereas.
        Llama al metodo que carga los datos de las conexiones en los grafos correspondientes
        Lee el archivo 'partida_guardada.csv' y crea objetos de la clase Pais con cada linea del archivo.
        '''
        self.cargar_conexiones()
        self.mundo.lista_paises = ListaLigada()
        for datos_pais in importar_datos('partida_guardada.csv'):
            if datos_pais[0] == 'Pais':
                pass
            else:
                nuevo_pais = Pais(*datos_pais)
                self.mundo.lista_paises.append(nuevo_pais)

    def desplegar_menu_principal(self):
        '''Despliega las opciones diarias que tiene un jugador'''
        lista1 = ListaLigada(
            'Pasar el Dia',
            'Estadisticas',
            'Guardar Estado',
            'Salir')
        lista2 = ListaLigada(
            self.pasar_dia,
            self.desplegar_menu_estadisticas,
            self.guardar_estado,
            self.terminar)
        Menu(lista1, lista2).menu()

    def desplegar_menu_estadisticas(self):
        '''Despliega las opciones que tiene el jugador cuando desea ver las estadisticas'''
        lista1 = ListaLigada(
            'Resumen del Dia',
            'Por Pais',
            'Global',
            'Muertes e Infecciones por Dia',
            'Promedio Muertes e Infecciones')
        m = self.mundo
        lista2 = ListaLigada(
            m.mostrar_resumen_diario(),
            m.mostrar_estad_por_pais(),
            m.estad_global(),
            m.muertes_infecciones_dias(),
            m.prom_muertes_infecciones())
        Menu(lista1, lista2).menu()

    def pasar_dia(self):
        '''Avanza un dia en la linea temporal del programa'''
        self.dia_actual += 1

    def guardar_estado(self):
        #nombre, poblacion, infectados, muertos, fecha_infeccion, aeropuerto, frontera, mascarillas, fecha_cura, estado
        pass

    def terminar(self):
        '''Retorna True'''
        self.salir = True


# ----------------------------------- A partir de aqui el codigo ---------


j = Juego()
j.comenzar()
while not j.salir:
    j.desplegar_menu_principal()
