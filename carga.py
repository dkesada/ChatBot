#! /usr/bin/python
# -*- coding: utf-8 -*-
#author: David Quesada López

import sys
from re import search

"""
Módulo encargado de la carga de la información de la base de datos de pisos.
Recoge el archivo InfoPisos generado por el webscrapper y lo almacena en una matriz local.
La aproximación actual carga el archivo de texto a la memoria local, si el archivo creciese
bastante, puede pasarse a cargarlos a una base en MongoDB.

La función principal a la que se llama desde fuera es cargarCasas(), que devuelve la matriz con
los pisos cargados.
"""

def cargarCasas():
	"""
	Por ahora así. Puede sustituirse por una base de datos
	"""
	reload(sys)  
	sys.setdefaultencoding('utf8')
	path = 'scraper/InfoPisos'
	doc = open(path, 'r')
	casas = doc.read().split('\ni')
	doc.close()
	res = []
	for c in casas:
		c = c.split(';')
		res.append(cropArray(c))
	
	return res

def cropArray(c):
	"""
	Convierte los atributos textuales de las casas en atributos numéricos.
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
	res = []
	res.append(op(c[1]))
	res.append(tipo(c[2]))
	res.append(lugar(c[3]))
	res.append(int(''.join(c[4].split('.'))))
	c = ''.join(c)
	res.append(metros(c)) 
	res.append(habit(c))
	res.append(banos(c))
	res.append(estado(c))
	res.append(mobiliario(c))
	
	return res

def op(acc):
	res = 1	
	if 'venta' in acc:
		res = 2
	return res

def tipo(casa):
	res = 1
	if 'piso' in casa:
		res = 2
	elif 'dúplex' in casa:
		res = 3
	elif 'ático' in casa:
		res = 4
	elif 'rústica' in casa:
		res = 5
	return res

def lugar(ciudad):
	res = 1
	if 'Alcalá' in ciudad:
		res = 2
	elif 'Mejorada' in ciudad:
		res = 3
	elif 'Torrejón' in ciudad:
		res = 4
	return res

def metros(casa):
	s = search('[0-9]+ m²', casa)
	res = int(s.group(0).split('m')[0])
	return res
	
def habit(casa):
	s = search('([0-9]+ habit)|(Sin habit)', casa)
	res = 0
	if 'Sin' not in s.group(0):
		res = int(s.group(0).split('h')[0])	
	return res

def banos(casa):
	s = search('[0-9]+ baño', casa)
	res = int(s.group(0).split('b')[0])
	return res

def estado(casa):
	res = 1
	if 'buen estado' in casa:
		res = 2
	elif 'reformar' in casa:
		res = 3
	return res
	
def mobiliario(casa):
	res = 0
	if 'Amueblado' in casa:
		res = 1
	elif 'Cocina equipada' in casa:
		res = 2
	elif 'sin amueblar' in casa:
		res = 3
	return res
	
