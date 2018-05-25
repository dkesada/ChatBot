# -*- coding: utf-8 -*-
#author: David Quesada López

from pymongo import MongoClient

"""
Controlador sencillo de la base de datos Mongo. La base sólo tiene una colección casas 
que contiene documentos con el formato {'op':{},'tipo':{},'lugar':{},'precio':{},'tamano':{},'habit':{},'banos':{},'estado':{},'muebles':{}}
"""

form = {0:'op',1:'tipo',2:'lugar',3:'precio',4:'tamano',5:'habit',6:'banos',7:'estado',8:'muebles'}
connection = MongoClient('localhost', 27017)
db = connection.chatbot
casas = db.casas


def vacia():
	"""Comprueba si la base de datos está vacía o no"""
	res = False
	test = casas.find_one()
	if test is None:
		res = True
	return res

def guardarCasa(c):
	"""Guarda una casa en la base de datos"""
	casas.insert_one({form[0]:c[0], form[1]:c[1], form[2]:c[2], form[3]:c[3], form[4]:c[4], form[5]:c[5], form[6]:c[6], form[7]:c[7], form[8]:c[8]})


def obtenerSimilares(caracs):
	"""
	Obtiene casas similares de la base de datos en función a las características introducidas.
	Devuelve el cursor a los documentos encontrados, si los hubiera, y el grado de certidumbre de la búsqueda:
		- La búsqueda habrá sido certera (2) si con una query estricta se han encontrado resultados
		- La búsqueda habrá sido aproximada (1) si con una query estricta no se encuentran resultados, pero sí con una relajada
		- La búsqueda será fallida (0) si ni una query estricta ni una relajada encuentran resultados a lo preguntado
	Por ahora se busca literal lo que me piden. 
	La idea es hacer una búsqueda por similitud de vectores si no se encuentra ninguna casa que cumpla.
	"""
	cert = 2
	q = crearQuery(caracs)
	res = casas.find(q).limit(10) # Limito a 10 casas como mucho
	
	if res.count() is 0: # Falla la búsqueda estricta
		cert = 1
		q = crearQueryRelajada(caracs)
		res = casas.find(q).limit(10) # Limito a 10 casas como mucho
		if res.count() is 0: # Falla también la búsqueda relajada
			cert = 0
	
	return res, cert

def crearQuery(caracs):
	""" 
	Crea el diccionario que realiza la query en base a las características.
	Aquellas características que estén a 0 no influyen en la búsqueda (buscarán un dintinto de None, es decir, cualquiera)
	La query se ciñe estrictamente a los parámetros introducidos.
	"""
	res = {}
	aux = {'$ne':None}
	for i in form:
		res[form[i]] = aux
		if caracs[i] is not 0:
			res[form[i]] = caracs[i]
	
	return res

def crearQueryRelajada(caracs):
	""" 
	Crea el diccionario que realiza la query relajada en base a las características.
	La query buscará características que concuerden con lo pedido, pero no necesariamente exactas.
	Las características como tipo de casa o lugar son igual de estrictas, pero se relajan medidas
	como el precio (pasa a buscar el precio introducido o menor) o el tamaño (igual o mayor)
	"""
	res = {}
	aux = {'$ne':None}

	for i in form:
		res[form[i]] = aux
		if caracs[i] is not 0:
			if i in {0,1,2,7,8}:
				res[form[i]] = caracs[i]
			elif i is 3:
				res[form[i]] = {'$lte':caracs[i]}
			elif i in {4,5,6,7}:
				res[form[i]] = {'$gte':caracs[i]}
	
	return res
