__author__ = "cotehidalgov"

#Herencia
# -*- coding: utf-8 -*-

import random

##AQUÍ VA LA IMPORTACION DE LAS CLASES ABTRACTAS ----------------------------------

from abc import ABCMeta, abstractmethod

# Aqui van todos los platos y las comidas --------------------------------------

class Plate:
	def __init__(self, food, drink):
		self.food = food
		self.drink = drink



# -------------------- Comestibles ----------------------------
class Food(metaclass = ABCMeta):
	def __init__(self, ingredients):
		# Aqui vamos a asumir que ingredients es una lista
		self.ingredients = ingredients
		self.calidad = random.randint(50,200)

	def check_ingredients(self):
		#print("entra")
		#print(self.ingredients)
		for ingrediente in self.ingredients:
			if ingrediente == "PEPERONI":
				self.calidad += 50
				#print("Ingrediente bueno subio 50")

			elif ingrediente == "PINA":
				self.calidad -= 50
				#print("Ingrediente malo bajo 50")

			elif ingrediente == "CRUTONES":
				self.calidad += 20
				#print("Ingrediente bueno subio 20")

			elif ingrediente == "MANZANA":
				self.calidad -= 20
				#print("Ingrediente malo bajo 20")

	def check_time(self):

		if self.tiempo_preparacion > 30:
			self.calidad -= 30





class Pizza(Food):
	def __init__(self, ingredients, **kwargs):
		super().__init__(ingredients)
		self.tiempo_preparacion = random.randint(20, 100)

class Salad(Food):
	def __init__(self, ingredients, **kwargs):
		super().__init__(ingredients)
		self.tiempo_preparacion = random.randint (5, 60)




# --------------------- Bebestibles -----------------------------
class Drink(metaclass = ABCMeta):
	def __init__(self):
		self.calidad = random.randint(50,150)

class Soda(Drink):
	def __init__(self):
		super().__init__()
		self.calidad -= 30


class Juice(Drink):
	def __init__(self):
		super().__init__()
		self.calidad += 30





# Aqui van todas las personalidades y el chef --------------------------------------

class Personality(metaclass=ABCMeta):

	def react(self, plate):
		pass


class Cool(Personality):

	def __init__(self):
		self.im_happy_str = 'Yumi! Que rico'
		self.im_mad_str = 'Preguntare si puedo cambiar el plato'

class Hater(Personality):

	def __init__(self):
		self.im_happy_str = 'No esta malo, pero igual prefiero Pizza x2'
		self.im_mad_str = "Nunca mas vendre a Daddy Juan's!"

class Person(metaclass=ABCMeta): # Solo los clientes tienen personalidad en esta actividad
	def __init__(self, name, **kwargs):
		self.name = name

class Client(Person):
	def __init__(self, name, personalidad, **kwargs):
		super().__init__(name, **kwargs)
		self.personalidad = personalidad

	def im_happy(self):
		print (self.personalidad.im_happy_str)

	def im_mad(self):
		print (self.personalidad.im_mad_str)

	def eat(self, plate):
		promedio = (plate.food.calidad + plate.drink.calidad)/2
		if promedio > 100:
			self.im_happy()
		else:
			self.im_mad()




class Chef(Person):

	def __init__(self, name):
		super().__init__(name)
		self.lista_comidas = ['PIZZA', 'ENSALADA']
		self.lista_bebestibles = ['BEBIDA', 'JUGO']
		self.lista_ingred_pizza = ['PEPERONI', 'PINA', 'CEBOLLA', 'TOMATE', 'JAMON', 'POLLO']
		self.lista_ingred_ensalada = ['CRUTONES', 'ESPINACA', 'MANZANA', 'ZANAHORIA']
		self.ingredientes_selec_pizza = ['QUESO', 'SALSA DE TOMATE']
		self.ingredientes_selec_ensalada = ['LECHUGA']

	def cook(self):
		pos = random.randint(0, 1)
		if self.lista_comidas[pos] == 'PIZZA':
			for i in range(0, 3):
				pos = random.randint(0, 5)
				ingrediente = self.lista_ingred_pizza[pos]
				self.ingredientes_selec_pizza.append(ingrediente)

			comestible = Pizza(self.ingredientes_selec_pizza)
			#print("pizza")
			#print(comestible.calidad)
			comestible.check_ingredients()
			#print(comestible.calidad)
			comestible.check_time()
			#print(comestible.calidad)


		elif self.lista_comidas[pos] == 'ENSALADA':
			for i in range(0, 2):
				pos = random.randint(0, 3)
				ingrediente = self.lista_ingred_pizza[pos]
				self.ingredientes_selec_ensalada.append(ingrediente)

			comestible = Salad(self.ingredientes_selec_pizza)
			#print("ensalada")
			comestible.check_time()
			comestible.check_ingredients()

		pos = random.randint(0, 1)
		if self.lista_bebestibles[pos] == 'JUGO':
			bebestible = Juice()

		elif self.lista_bebestibles[pos] == 'BEBIDA':
			bebestible = Soda()
		self.ingredientes_selec_ensalada = ['LECHUGA']
		self.ingredientes_selec_pizza = ['QUESO', 'SALSA DE TOMATE']
		return Plate(comestible, bebestible)


#-------------------------------------------------------------------------------------------------------

class Restaurant:
	def __init__(self, chefs, clients):
		self.chefs = chefs
		self.clients = clients

	def start(self):
		for i in range(3): # Se hace el estudio por 3 dias
			print("----- Día {} -----".format(i + 1))
			plates = []
			for chef in self.chefs: 
				for j in range(3):  # Cada chef cocina 3 platos
					plates.append(chef.cook()) # Retorna platos de comida y bebida

			plato = plates [2]
			#print(plato.food.ingredients)
			#print(plato.food.calidad)
			#print(plato.drink.calidad)

			for client in self.clients:
				for plate in plates:
					client.eat(plate)



if __name__ == '__main__':
	chefs = [Chef("Cote"), Chef("Joaquin"), Chef("Andres")]

	clients = [Client(name="Bastian", personalidad=Hater()), Client(name="Flori", personalidad=Cool()),
				Client(name="Antonio", personalidad=Hater()), Client(name="Felipe", personalidad=Cool())]
	#for c in clients:
	#	c.im_happy()
	#	c.im_mad()
	restaurant = Restaurant(chefs, clients)
	restaurant.start()





