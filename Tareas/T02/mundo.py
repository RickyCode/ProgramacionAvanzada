__author__ = 'Ricardo Del Rio'
# Libre de estructuras python

from estructuras_propias import ListaLigada, Diccionario
from simplificadores import SuperInput
from functools import reduce
from manejo_csv import importar_datos


class Mundo:
    def __init__(self):
        self.propuestas = ListaLigada()
        self.grafo_terrestre = None
        self.grafo_aereo = None

        self.infectados_totales = 0
        self.muertos_totales = 0
        self.infectados_totales = 0

        # litas
        self.lista_paises = ListaLigada()
        self.paises_infectados = ListaLigada()
        self.paises_aeropuertos_cerrados = ListaLigada()
        self.paises_fronteras_cerradas = ListaLigada()
        self.paises_con_mascarillas = ListaLigada()
        self.paises_limpios = ListaLigada()
        self.paises_muertos = ListaLigada()

        # estadisticas
        self.resumen_del_dia = ''
        self.estadisticas_globales = ''

    def establecer_conecciones_terrestres(self):
        '''Crea un grafo de listas de adyacencia con las conexiones terrestres'''
        self.grafo_terrestre = Diccionario()
        for datos_fronteras_terrestres in importar_datos('borders.csv', ';'):
            if datos_fronteras_terrestres[0][:3] == 'ï»¿':
                datos_fronteras_terrestres[0] = datos_fronteras_terrestres[0][3:]
            if datos_fronteras_terrestres[0] == 'Pais 1':
                pass
            else:
                if datos_fronteras_terrestres[0] in self.grafo_terrestre:
                    self.grafo_terrestre[datos_fronteras_terrestres[0]].append(
                        datos_fronteras_terrestres[1])
                else:
                    self.grafo_terrestre[datos_fronteras_terrestres[0]] = ListaLigada(
                        datos_fronteras_terrestres[1])

    def establecer_conexiones_aereas(self):
        '''Crea un grafo de listas de adyacencia con las conexiones aereas'''
        self.grafo_aereo = Diccionario()
        for datos_fronteras_aereas in importar_datos('random_airports.csv'):
            if datos_fronteras_aereas[0][:3] == 'ï»¿':
                datos_fronteras_aereas[0] = datos_fronteras_aereas[0][3:]
            if datos_fronteras_aereas[0] == 'Pais 1':
                pass
            else:
                if datos_fronteras_aereas[0] in self.grafo_aereo:
                    self.grafo_aereo[datos_fronteras_aereas[0]].append(
                        datos_fronteras_aereas[1])
                else:
                    self.grafo_aereo[datos_fronteras_aereas[0]
                                     ] = ListaLigada(datos_fronteras_aereas[1])

    def ordenar_propuestas(self):
        self.propuestas.sort()

    def estad_resumen_diario(self):
        '''
        Actualiza los totales de gente infectada y gente muerta y las listas de paises en distintas situaciones.
        Crea un string con el resumen de estadisticas del dia anterior
        '''

        # Calcula el total de muertos y el total de infectados del mundo.
        # Se les restan los totales del dia anterior para obtener la cantidad
        # diaria.
        muertos_totales_anterior = self.muertos_totales
        infectados_totales_anterior = self.infectados_totales
        self.muertos_totales = 0
        self.infectados_totales = 0
        for pais in self.lista_paises:
            self.muertos_totales += pais.muertos
            self.infectados_totales += pais.infectados
        infectados_del_dia = self.infectados_totales - infectados_totales_anterior
        muertos_del_dia = self.muertos_totales - muertos_totales_anterior

        # Ojo tengo que asegurarme que la sobrecarga resta solo mantenga los elementos que  estan en la primera lista y no en la segunda, pero no al reves.
        # Esto para evitar que aparezcan en la lista los paises que recibieron
        # la cura.

        lista_tmp = ListaLigada(
            filter(
                lambda x: x.aeropuerto == False,
                self.lista_paises))
        aeropuertos_cerrados_dia = ', '.join(
            lista_tmp - self.paises_aeropuertos_cerrados)
        self.paises_aeropuertos_cerrados = lista_tmp

        lista_tmp = ListaLigada(
            filter(
                lambda x: x.frontera,
                self.lista_paises))
        fronteras_cerradas_dia = ', '.join(
            lista_tmp - self.paises_fronteras_cerradas)
        self.paises_fronteras_cerradas = lista_tmp

        lista_tmp = ListaLigada(
            filter(
                lambda x: x.infectado,
                self.lista_paises))
        paises_infectados_dia = ', '.join(lista_tmp - self.paises_infectados)
        self.paises_infectados = lista_tmp

        lista_tmp = ListaLigada(
            filter(
                lambda x: x.mascarillas,
                self.lista_paises))
        paises_mascarillas_dia = ', '.join(
            lista_tmp - self.paises_con_mascarillas)
        self.paises_con_mascarillas = lista_tmp

        del lista_tmp

        self.resumen_del_dia = (
            'El dia de ayer...\n'
            'Se infectaron: {0} personas.\n'
            'Murieron: {1} personas.\n'
            'La infeccion llego a: {2}\n'
            'Se cerraron lo aeropuertos de: {3}\n'
            'Se cerraron las fronteras de: {4}\n'
            'Se entregaron mascarillas en: {5}\n'.format(
                infectados_del_dia,
                muertos_del_dia,
                paises_infectados_dia,
                aeropuertos_cerrados_dia,
                fronteras_cerradas_dia,
                paises_mascarillas_dia))

    def mostrar_resumen_diario(self):
        print(self.resumen_del_dia)

    def mostrar_estad_por_pais(self):
        conteo = enumerate(self.lista_paises, 1)
        diccionario_paises = Diccionario()
        for i, j in conteo:
            print('{} ')
            diccionario_paises[i] = j
        entrada = SuperInput(
            '>>> Ingresa el numero del pais que quieres revisar: ', int)
        diccionario_paises[entrada].mostrar_estadisticas()

    def estad_global(self):

        self.paises_limpios = ListaLigada(
            filter(lambda x: x.infectado(), self.lista_paises))
        self.paises_muertos = ListaLigada(
            filter(lambda x: x.muerto(), self.lista_paises))

        poblacion_total = sum(map(lambda x: x.poblacion, self.lista_paises))
        muertos_totales = sum(map(lambda x: x.muertos, self.lista_paises))
        vivos_totales = poblacion_total - muertos_totales

        print('Paises limpios:            \n{0}\n'
              'Paises infectados:         \n{1}\n'
              'Paises muertos:            \n{2}\n'
              'Poblacion total viva       \n{3:11}'
              'Poblacion total infectada: \n{4:11}'
              'Poblacion total sana:      \n{5:11}'.format(', '.join(self.paises_limpios),
                                                           ', '.join(self.paises_infectados),
                                                           ', '.join(self.paises_muertos),
                                                           vivos_totales,
                                                           self.infetados_totales,
                                                           self.muertos_totales))

    def muertes_infecciones_dias(self, today):
        print('Muertes e Infecciones Por Dia:\n')
        for i in range(today):
            infecciones_dia = reduce(
                lambda x,
                y: x.bitacora[i][0] +
                y.bitacora[i][0],
                self.lista_paises)
            muertes_dia = reduce(
                lambda x,
                y: x.bitacora[i][1] +
                y.bitacora[i][1],
                self.lista_paises)
            print(
                'Dia {}: {}infectados {}muertos'.filter(
                    today,
                    infecciones_dia,
                    muertes_dia))
        print()

    def prom_muertes_infecciones(self, today):
        infecciones_dia = reduce(
            lambda x, y: x + y, map(lambda x: x.bitacora[today][0], self.lista_paises))
        muertes_dia = reduce(
            lambda x, y: x + y, map(lambda x: x.bitacora[today][1], self.lista_paises))

        # muertos/poblacion_total


class Propuesta:
    def __init__(self, tipo, pais):
        self.tipo = tipo
        self.pais = pais  # nombre pais
        self.prioridad = 0  # float

    def calcular_prioridad(self):
        pass

    def __le__(self, other):
        return self.prioridad <= other.prioridad
