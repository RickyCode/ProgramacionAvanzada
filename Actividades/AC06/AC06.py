from datetime import datetime as dt
from functools import reduce


def set_id():
    id = 0
    yield  id
    while True:
        id += 1
        yield id

def calcular_promedio():
    suma_total = yield
    cant_elementos = 1
    while True:
        cant_elementos += 1
        suma_total += yield suma_total/cant_elementos

class Movies:
    lista_peliculas = []
    lista_elencos = []

    def popular(self, y):
        pelicula = []
        return list(filter(lambda x: x.rating > y, self.lista_peliculas))

    def with_genres(self, y):
        return list(filter(lambda x: x.genres > y, self.lista_peliculas))

    def tops_of_genre(self, genero):
        peliculas_genero = list(filter(lambda x, genero in x.genres, self.lista_peliculas)).sort()
        return #completar

    def actor_rating(self, nombre_actor):
        participo_elencos = list(filter(lambda x: nombre_actor == x.name, self.lista_elencos))
        nombres_peliculas = [elenco.movie_title for elenco in participo_elencos]
        participo_peliculas = list(filter(lambda x: x.title in nombres_peliculas,self.lista_peliculas))
        return reduce(lambda x: calcular_promedio().send(x.rating), participo_peliculas)



class Cast:
    def __init__(self, movie_title, name, character):
        self.name = name
        self.movie = movie_title
        self.character = character



class Movie:
    get_id = set_id()

    def __init__(self, title, rating, release, *args):
        self.id = next(Movie.get_id)
        self.title = title
        self.rating = float(rating)
        self.release = dt.strptime(release, '%Y-%m-%d')  # 2015-03-04
        self.genres = []

    def __le__(self, other):
        return self.rating <= other.rating


if __name__ == "__main__":
    m = Movies()
    with open('movies.txt', 'r') as f:
        movies = (linea for linea in f)
        m.lista_peliculas = [Movie(*mo.strip().split(',')) for mo in movies]

    with open('cast.txt', 'r') as f:
        elencos = (linea for linea in f)
        m.lista_elencos = [Cast(*el.strip().split(',')) for el in elencos]

    ##BORRAR
    for i in m.lista_peliculas:
        print(i.title)

    print()
    hola = m.popular(40)
    print(hola)
    print(repr(len(hola)))






