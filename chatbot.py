#! /usr/bin/python
# -*- coding: utf-8 -*-
#author: David Quesada López

import sys


def main():
	"""
	Cuerpo principal del chatbot.

	1- Recibe una pregunta
	2- Analiza la pregunta para ver qué se pide
	3- Los pisos de la base deben estar clasificados, un árbol por ejemplo
	4- Las características identificadas deben generar una serie de pisos válidos
	5- Con los pisos válidos hay que generar una respuesta
	"""
	pregunta = generarPregunta()
	casa = analizarPregunta()

reload(sys)  
sys.setdefaultencoding('utf8')
main()
