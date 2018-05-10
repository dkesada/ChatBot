# -*- coding: utf-8 -*-
#author: David Quesada López

from nltk import grammar, parse, data
from re import findall
from unidecode import unidecode
import os

"""
Módulo encargado de analizar las preguntas realizadas al chatbot por medio
de una gramática libre de contexto. Utiliza la librería nltk para implementarla.

La función principal a la que se llama desde fuera es analizarPregunta(pregunta),
que toma como argumento de entrada una pregunta en formato string (inicialmente
tomadas del archivo preguntas.txt) y devuelve una casa con los atributos
que se han especificado en la pregunta para su posterior búsqueda.
"""

def generarGramatica():
	"""
	Función que genera la CFG para reconocer las preguntas entrantes con nltk
	"""
	a = os.path.dirname(os.path.abspath(__file__))
	gramatica = data.load('file:' + a + '/entrada.cfg')

	return gramatica

def tokenizar(pregunta):
	"""
	Tokeniza el string inicial y lo convierte en un array de tokens.
	Simplifica el string de varias formas:
	- Lo pasa a minúscula
	- Unidecode pasa el string de unicode al ascii plano mas cercano (tildes y símbolos)
	- Elimina signos de puntuación 
	"""
	nums = []
	pregunta = ' €'.join(pregunta.split('€')) # Si el símbolo esta pegado a los números, lo separo
	res = findall('\w+', unidecode(pregunta.decode('utf-8').lower()))
	# La CFG no soporta los numeros de mas de una cifra.
	# O los guardo y los sustituyo por un token o les hago split y los junto después
	for i in range(len(res)):
		if res[i].isdigit() and int(res[i]) > 9:
			nums.append(res[i])
			res[i] = 'num'

	return res, nums

def analizar(preg, parser):
	for tree in parser.parse(preg):
		print tree
	#Caracs = list(it.subtrees(filter=lambda x: x.label()=='Carac')) # Provisional, para sacar las características especificadas

def analizarPregunta(pregunta):
	print pregunta
	gramatica = generarGramatica()
	parser = parse.RecursiveDescentParser(gramatica) # trace=2
	pregunta, numeros = tokenizar(pregunta)
	print pregunta
	piso = analizar(pregunta, parser)
	
	return piso
