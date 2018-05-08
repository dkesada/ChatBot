# -*- coding: utf-8 -*-
#author: David Quesada López

from nltk import grammar, parse, data
from re import findall
from unidecode import unidecode

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
	gramatica = data.load('file:entrada.cfg')

	return grammar.FeatureGrammar.fromstring(gramatica)

def tokenizar(pregunta):
	"""
	Tokeniza el string inicial y lo convierte en un array de tokens.
	Simplifica el string de varias formas:
	- Lo pasa a minúscula
	- Unidecode pasa el string de unicode al ascii plano mas cercano (tildes y símbolos)
	- Elimina signos de puntuación 
	"""
	return findall('\w+', unidecode(pregunta.decode('utf-8').lower()))

def analizar(preg, parser):
	it = parser.parse(preg)
	Caracs = list(it.subtrees(filter=lambda x: x.label()=='Carac')) # Provisional, para sacar las características especificadas

def analizarPregunta(pregunta):
	gramatica = generarGramatica()
	parser = parse.RecursiveDescentParser(gramatica)
	pregunta = tokenizar(pregunta)
	piso = analizar(pregunta, parser)
	
	return piso
