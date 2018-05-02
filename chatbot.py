#! /usr/bin/python
# -*- coding: utf-8 -*-
#author: David Quesada López

import sys
from textblob import TextBlob
from random import randint

def cargarCasas():
	path = 'scraper/InfoPisos'
	doc = open(path, 'r')
	casas = doc.read().split('\n')
	doc.close()
	res = []
	for c in casas:
		c = c.split(';')
		res.append(c)
	
	return res
	
def generarPregunta():
	"""
	Por ahora cojo una pregunta de las que tengo
	"""
	
	doc = open('preguntas.txt', 'r')
	res = doc.read().split(';')
	doc.close()
	return res[randint(0,len(res)-1)]

def analizarPregunta(preg):
	print(preg)
	blob = TextBlob(preg)
	blob.translate(to='en').tags
	blob.translate(to='en').parse() #No me convence

def main():
	"""
	Cuerpo principal del chatbot.

	1- Recibe una pregunta
	2- Analiza la pregunta para ver qué se pide
	3- Los pisos de la base deben estar clasificados, un árbol por ejemplo
	4- Las características identificadas deben generar una serie de pisos válidos
	5- Con los pisos válidos hay que generar una respuesta
	"""
	casas = cargarCasas() # Por ahora así. Puede sustituirse por una base de datos de mongo
	pregunta = generarPregunta()
	casa = analizarPregunta(pregunta)

reload(sys)  
sys.setdefaultencoding('utf8')
main()
