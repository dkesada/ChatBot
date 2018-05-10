#! /usr/bin/python
# -*- coding: utf-8 -*-
#author: David Quesada López

import sys
from random import randint
from carga import carga
from inGrammar import inGrammar

def generarPregunta():
	"""
	Por ahora cojo una pregunta de las que tengo
	"""
	
	doc = open('preguntas.txt', 'r')
	res = doc.read().split(';')
	doc.close()
	return res[randint(0,len(res)-1)]

def main():
	"""
	Cuerpo principal del chatbot.

	1- Recibe una pregunta
	2- Analiza la pregunta para ver qué se pide
	3- Los pisos de la base deben estar clasificados, un árbol por ejemplo
	4- Las características identificadas deben generar una serie de pisos válidos
	5- Con los pisos válidos hay que generar una respuesta
	"""
	casas = carga.cargarCasas()
	pregunta = generarPregunta()
	casa = inGrammar.analizarPregunta(pregunta)

reload(sys)  
sys.setdefaultencoding('utf8')
main()