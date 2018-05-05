#! /usr/bin/python
# -*- coding: utf-8 -*-
#author: David Quesada López

from nltk import grammar, parse

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
	
	gramatica = """
		  Pregunta -> Peticion Tipo Caracs
		  Peticion -> V NP | V NP PP
		  Tipo -> "casa" | "casas" | "piso" | "pisos" | "dúplex" | "chalet" | "chalets" | "ático" | "áticos"
		  Caracs -> Carac Caracs | Carac 

		  """
	return grammar.FeatureGrammar.fromstring(gramatica)


def analizarPregunta(pregunta):
	gramatica = generarGramatica()
	parser = parse.RecursiveDescentParser(gramatica)
	piso = analizar(pregunta, parser)
	
	return piso
