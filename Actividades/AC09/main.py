__author__ = 'Ricardo Del Río', 'Domingo Ramirez'

from random import randint, choice, random, expovariate
from datetime import datetime

class Automovil:
    def __init__(self, conductor):
        self.rapidez = randint(12,20)
        self.tipo = choice(['auto','camioeta'])
        self.capacidad = 0
        self.pasajeros = [conductor]
        self.posicion_actual = 0

        if self.tipo == 'auto':
            self.capacidad = 5

        elif self.tipo == 'camioneta':
            self.capacidad = 8

        self.posicion_inicial = conductor.posicion_inicial

class Persona:
    def __init__(self):
        self.personalidad = choice(['Generoso', 'Egoista'])
        self.prob_detenerse = 0
        self.rapidez = randint(5,8)
        self.posicion_inicial = randint(0,60)
        self.posicion_actual = 0


        if self.personalidad == 'Generoso':
            self.prob_detenerse = 0.6
        elif self.personalidad == 'Egoista':
            self.prob_detenerse = 0.3

class Replica:
    def __init__(self): #Puede ser temblor o tsunami
        num = random()
        if num <= 0.7:
            self.intencidad = 'debil'
        else:
            self.intencidad = 'fuerte'

    def genera_tsunami(self):
        if self.intencidad == 'fuerte':
            num = random()
            if num < 0.7:
                return True
        return False

class Simulacion:
    def __init__(self):
        self.tiempo_maximo = 200
        self.tiempo = 0
        self.lambd = 1/randint(4,10)
        self.eventos = []
        self.personas = []
        self.automoviles = []
        self.cantidad_inicial_personas = 100
        self.cantidad_muertos = 0

        #Estadisticas
        self.victimas_tsunami = 0
        self.victimas_replica = 0
        self.vehivulos_salvados = 0
        self.personas_a_pie_salvadas = 0
        self.tiempo_ejecucion = None

    def generar_personas(self):
        for n in range(100):
            self.personas.append(Persona())

    def generar_automoviles(self):
        for n in range(25):
            self.automoviles.append(Automovil(self.personas.pop(randint(0,len(self.personas)-1))))

    def contador_replicas(self):
        contador = 1
        while True:
            yield contador
            contador += 1

    def proxima_replica(self):
        num = round(expovariate(self.lambd), 0)
        self.eventos.append((self.tiempo + int(num), 'replica', 'replica {}'.format(next(self.contador_replicas()))))

    def matar_gente_replica(self, intencidad):
        dict = {'debil': 0.1, 'fuerte':0.3}
        for persona in self.personas:
            if random() < dict[intencidad]:
                self.personas.remove(persona)
                self.cantidad_muertos += 1

    def matar_gente_tsunami(self):
        posicion_tsunami = randint(0,100)
        potencia = randint(3,8)
        alcance = potencia * 4

        for persona in self.personas:
            if ((persona.posicion_actual < (posicion_tsunami + alcance)) and
                (persona.posicion_actual > (posicion_tsunami - alcance))):
                if random() < (potencia/10):
                    self.personas.remove(persona)
                    self.cantidad_muertos += 1
                    self.victimas_tsunami += 1

        for auto in self.automoviles:
            if ((auto.posicion_actual < (posicion_tsunami + alcance)) and
                (auto.posicion_actual > (posicion_tsunami - alcance))):
                if random() < (potencia/10):
                    self.cantidad_muertos += len(auto.pasajeros)
                    self.automoviles.remove(auto)
                    self.victimas_tsunami += len(auto.pasajeros)


    def matar_autos(self, intencidad):
        dict = {'debil': 0.15, 'fuerte':0.6}
        for auto in self.automoviles:
            if random() < dict[intencidad]:
                self.cantidad_muertos += len(auto.pasajeros)
                self.automoviles.remove(auto)

    def calcular_avance(self):
        for persona in self.personas:
            persona.posicion_actual = persona.rapidez * self.tiempo
            if persona.posicion_actual >= 100:
                self.personas_a_pie_salvadas += 1

        for auto in self.automoviles:
            auto.posicion_actual = auto.rapidez * self.tiempo
            if auto.posicion_actual >= 100:
                self.vehivulos_salvados += len(auto.pasajeros)

    def run(self):
        inicial = datetime.now()

        self.generar_personas()
        self.generar_automoviles()
        self.proxima_replica()
        self.eventos.sort(key = lambda x: x[0])

        while self.tiempo < self.tiempo_maximo:
            evento_actual = self.eventos.pop(0)
            if evento_actual[1] == 'replica':
                replica = Replica()
                self.tiempo = evento_actual[0]
                self.calcular_avance()
                self.matar_gente_replica(replica.intencidad)
                self.matar_autos(replica.intencidad)
                if replica.genera_tsunami():
                    self.matar_gente_tsunami()

                self.proxima_replica()
                self.eventos.sort(key = lambda x: x[0])
        final = datetime.now()
        self.tiempo_ejecucion = final - inicial

if __name__ == '__main__':
    for i in range(10):
        s = Simulacion()
        s.run()

        print('Tiempo ejecucion = {}'.format(s.tiempo_ejecucion))
        print('Victimas Tsunami = {}'.format(s.victimas_tsunami))
        print('Personas Salvadas a Pie = {}'.format(s.personas_a_pie_salvadas))
        print('Personas en Auto Salvadas = {}'.format(s.vehivulos_salvados))


        print()
