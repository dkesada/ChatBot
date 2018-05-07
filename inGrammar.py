#! /usr/bin/python
# -*- coding: utf-8 -*-
#author: David Quesada López

from nltk import grammar, parse
from re import findall
from unidecode import unidecode

"""
Módulo encargado de analizar las preguntas realizadas al chatbot por medio
de una gramática libre de contexto. Utiliza la librería nltk para implementarla.

La función principal a la que se llama desde fuera es analizarPregunta(pregunta),
que toma como argumento de entrada una pregunta en formato string (inicialmente
tomadas del archivo preguntas.txt) y devuelve una plantilla de un piso con los atributos
que se han especificado en la pregunta.
"""

def generarGramatica():
	"""
	Función que genera la FCG para reconocer las preguntas entrantes con nltk
	"""
	# Meter la gramática en un archivo a parte mejor
	gramatica = """
		  Pregunta -> Peticion Caracs | Caracs
		  Peticion -> Quiero | Enseña | Que | Cual | 
		  Caracs -> Carac Caracs | Carac
		  Carac ->
		  Tipo -> "casa" | "casas" | "piso" | "pisos" | "duplex" | "chalet" | "chalets" | "atico" | "aticos"

		  """
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


def analizarPregunta(pregunta):
	gramatica = generarGramatica()
	parser = parse.RecursiveDescentParser(gramatica)
	pregunta = tokenizar(pregunta)
	piso = analizar(pregunta, parser)
	
	return piso
