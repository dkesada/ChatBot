#! /usr/bin/python
# -*- coding: utf-8 -*-
#author: David Quesada López

import sys
from random import randint
from carga import carga
from inGrammar import inGrammar
from nlg import outGrammar

def generarPregunta():
	"""
	Por ahora cojo una pregunta de las que tengo
	"""
	
	doc = open('preguntas.txt', 'r')
	res = doc.read().split(';')
	doc.close()
	res = res[randint(0,len(res)-1)]

	return res

def main():
	"""
	Cuerpo principal del chatbot.

	1- Recibe una pregunta
	2- Analiza la pregunta para ver qué se pide
	3- Los pisos de la base deben estar clasificados, un árbol por ejemplo
	4- Las características identificadas deben generar una serie de pisos válidos
	5- Con los pisos válidos hay que generar una respuesta
	"""
	carga.cargarCasas()
	pregunta = generarPregunta()
	casa, arbol = inGrammar.analizarPregunta(pregunta)
	print casa
	respuesta = outGrammar.generarRespuesta(casa, pregunta, arbol)
	print respuesta

reload(sys)  
sys.setdefaultencoding('utf8')
main()
