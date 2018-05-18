# -*- coding: utf-8 -*-
#author: David Quesada López

from pymongo import MongoClient

"""
Controlador sencillo de la base de datos Mongo. La base sólo tiene una colección casas 
que contiene documentos con el formato {'op':{},'tipo':{},'lugar':{},'precio':{},'tamano':{},'habit':{},'banos':{},'estado':{},'muebles':{}}
"""

connection = MongoClient('localhost', 27017)
db = connection.chatbot
casas = db.casas

def vacia():
	"""Comprueba si la base de datos está vacía o no"""
	ret = False
	test = casas.find_one()
	if test is None:
		ret = True
	return ret

def guardarCasa(c):
	"""Guarda una casa en la base de datos"""
	casas.insert_one({'op':c[0], 'tipo':c[1], 'lugar':c[2], 'precio':c[3], 'tamano':c[4], 'habit':c[5], 'banos':c[6], 'estado':c[7], 'muebles':c[8]})


def obtenerSimilares(caracs):
	"""Obtiene casas similares de la base de datos en función a las características introducidas."""
	
	return None
