__author__ = 'Ricardo Del Rio'

from math import sqrt

def distancia_coordenadas(lat1, lon1, lat2, lon2):
    ''' recibe dos la latitud y la longitud de dos puntos en el mapa
    Retorna la distancia entre ellos en metros
    Se considera 1° = 110km. i.e: 1° = 110.000 metros'''
    distancia_grados = sqrt(((lat1 - lat2) ** 2) + ((lon1 - lon2) ** 2))
    return distancia_grados * 110000

if __name__ == '__main__':

    lat1 = -34.35971116754556
    lon1 = -70.83202153365762

    lat2 = -36.010021700930594
    lon2 = -71.65330186859902

    print(str(distancia_2_coordenadas(lat1, lon1, lat2, lon2)) + ' metros.')

