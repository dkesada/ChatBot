# -*- coding: utf-8 -*-
#author: David Quesada López

from db import db

"""
Este módulo se encarga de generar respuestas a partir de la casa generada de las preguntas.
Primero se buscan casas similares a la generada desde la pregunta en la base de datos, y 
después se genera una respuesta acorde a la pregunta inicial.

Se está valorando si usar:
- Una CFG que genere respuestas para todo tipo de preguntas
- Varias CFG que generen respuestas para un solo tipo de preguntas.
  Esto implica reconocer primero el tipo de pregunta (ya se hace en el inGrammar, por lo que el arbol ayuda)
  y concordar las respuestas de cada CFG al tipo de preuntas que cubre.
- Usar un Markov Chain Model. Parece poco plausible, dado que el corpus de respuestas tendría que generarlo yo.
  Se pueden hacer algunas pruebas rápidas, ya que un documento de posibles respuestas debería generarlo para
  orientarme haciendo las CFG.
"""

def generarRespuesta(casa, pregunta, arbol):
	"""
	Función principal del módulo. Recibe una casa en su formato de array, busca casas similares en la base de datos
	y genera una respuesta en lenguaje natural acorde.
	En caso de que la casa sea un vector de 0's, se entiende que la pregunta no fue comprendida, y se genera una
	petición para que el usuario repita su pregunta con otras palabras.
	"""
	if sum(casa) is not 0:
		sim = db.obtenerSimilares(casa)
		res = generarTexto(sim,pregunta,arbol)
	else:
		res = preguntaNoComprendida()

	return res

def generarTexto(sim, pregunta, arbol):
	"""
	Comprueba las casas similares a lo preguntado y genera una respuesta acorde a la pregunta.
	"""
	res = 'Texto provisional de comprensión'
	
	for i in sim:
		print i
	
	return res
	
def preguntaNoComprendida():
	"""
	Función que genera una respuesta para pedir al usuario que repita su pregunta de otra manera.
	Para esto, no creo que haga falta una gramática ni una batería de respuestas tipadas, con unas cuantas
	respuestas enlatadas aleatorias debería ser suficiente.
	"""
	res = 'Texto provisional de no comprensión'
	
	return res
