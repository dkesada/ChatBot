# -*- coding: utf-8 -*-
#author: David Quesada López

from re import search

"""
A partir de los subárboles que nos interesan del parsing con la CFG sacamos
los atributos para el array de la casa. 
La función principal procesaCarac recibe un subárbol, el array de la casa
inicializado a 0 y los números que se hayan extraído al tokenizar.

Como referencia, un array [0..8] de una casa representa:

	[0] - 1 Alquiler, 2 Venta
	[1] - 1 Chalet, 2 Piso, 3 Dúplex, 4 Ático, 5 Rústica
	[2] - 1 Coslada, 2 Alcalá, 3 Mejorada, 4 Torrejón
	[3] - Precio
	[4] - m2
	[5] - Habitaciones
	[6] - Baños
	[7] - 1 Nueva, 2 Buen estado, 3 A reformar
	[8] - 0 N/D, 1 Amueblada, 2 Cocina equipada, 3 Sin amueblar
"""

def procesaCarac(c, piso, nums):

	"""
	Función principal. Recibe un subárbol con una característica y pasa su label
	por un switch de funciones para elegir cómo tratarlo. Modificará una posición del
	array piso[0..8].
	"""

	label = c.label()
	hojas = ' '.join(c.leaves())
	switch = {
            'Precio': precio,
            'Lugar': lugar,
            'Tamano': tamano,
            'Estado': estado,
            'Muebles': muebles,
            'Habit': habit,
            'Banos': banos,
            'Alq': alq,
            'TipoP': tipos,
            'TipoS': tipos,
            'Op': op
            }
	foo = switch[label]
	foo(c, hojas, piso, nums)

def cifra(texto, nums):

	"""
	Función que extrae un número de un texto. Si el número es de más de dos cifras,
	lo recupera de la lista nums[] creada al tokenizar. Los números pueden ser un token 'num',
	cifras de 0 al 9 u ordinales del 'un' al 'diez'.
	"""

	if 'num' in texto:
		res = nums.pop(0)
	elif search('[0-9]+', texto) is not None:
		res = search('[0-9]+', texto).group(0)
	else:
		texto = texto.split(' ')
		ordinales = ['un','una','dos','tres','cuatro','cinco','seis','siete','ocho','nueve','diez']
		dic = {'un': 1,'una': 1,'dos': 2,'tres': 3,'cuatro': 4,'cinco': 5,'seis': 6,'siete': 7,'ocho': 8,'nueve': 9,'diez': 10}
		check = map(lambda x: x in ordinales, texto)
		num = texto[check.index(True)]
		res = dic[num]

	return int(res)

def op (arbol, hojas, piso, nums):
	piso[0] = 2
	if 'alquilar' in hojas:
		piso[0] = 1

def alq(arbol, hojas, piso, nums):
	piso[0] = 1

def tipos(arbol, hojas, piso, nums):
	if 'chalet' in hojas:
		piso[1] = 1
	elif 'piso' in hojas:
		piso[1] = 2
	elif 'duplex' in hojas:
		piso[1] = 3
	elif 'atico' in hojas:
		piso[1] = 4
	elif 'rustic' in hojas:
		piso[1] = 5

def lugar(arbol, hojas, piso, nums):
	if 'coslada' in hojas:
		piso[2] = 1
	elif 'alcala' in hojas:
		piso[2] = 2
	elif 'mejorada' in hojas:
		piso[2] = 3
	elif 'torrejon' in hojas:
		piso[2] = 4
   
def precio(arbol, hojas, piso, nums):
	piso[3] = cifra(hojas,nums)

def tamano(arbol, hojas, piso, nums):
	piso[4] = cifra(hojas, nums)

def habit(arbol, hojas, piso, nums):
	if 'sin' not in hojas:
		piso[5] = cifra(hojas, nums)

def banos(c, hojas, piso, nums):
	if 'sin' not in hojas:
		piso[6] = cifra(hojas, nums)

def estado(arbol, hojas, piso, nums):
	mueb = ['Nuevo','Segunda','Reforma']
	c = list(arbol.subtrees(filter=lambda x: x.label() in mueb))[0]
	if 'Nuevo' in c:
		piso[7] = 1
	elif 'Segunda' in c:
		piso[7] = 2
	elif 'Reforma' in c:
		piso[7] = 3

def muebles(arbol, hojas, piso, nums):
	piso[8] = 1
	if 'sin' in hojas:
		piso[8] = 3
	elif 'cocina' in hojas:
		piso[8] = 2

