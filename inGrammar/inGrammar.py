# -*- coding: utf-8 -*-
#author: David Quesada López

from nltk import parse, data
from re import findall
from unidecode import unidecode
import os
from conversor import procesaCarac

"""
Módulo encargado de analizar las preguntas realizadas al chatbot por medio
de una gramática libre de contexto. Utiliza la librería nltk para implementarla.

La función principal a la que se llama desde fuera es analizarPregunta(pregunta),
que toma como argumento de entrada una pregunta en formato string (inicialmente
tomadas del archivo preguntas.txt) y devuelve una casa con los atributos
que se han especificado en la pregunta para su posterior búsqueda.
"""

class InGrammar:
	
	def __init__(self):
		self.gramatica = self.generarGramatica()
		self.parser = parse.RecursiveDescentParser(self.gramatica) # trace=2
		self.caracs = ['Precio' , 'Lugar' , 'Tamano' , 'Estado' , 'Muebles' , 'Habit' , 'Banos' , 'Alq' , 'TipoP' , 'TipoS' , 'Op', 'Disp']
		self.stopwords = self.cargarStop()
	
	def generarGramatica(self):
		"""
		Función que genera la CFG para reconocer las preguntas entrantes con nltk
		"""
		a = os.path.dirname(os.path.abspath(__file__))
		gramatica = data.load('file:' + a + '/entrada.cfg')

		return gramatica

	def tokenizar(self, pregunta):
		"""
		Tokeniza el string inicial y lo convierte en un array de tokens.
		Simplifica el string de varias formas:
		- Lo pasa a minúscula
		- Unidecode pasa el string de unicode al ascii plano mas cercano (tildes y símbolos)
		- Elimina signos de puntuación 
		"""
		nums = []
		pregunta = ' €'.join(pregunta.split('€')) # Si el símbolo esta pegado a los números, lo separo
		pregunta = ' m2'.join(pregunta.split('m2'))
		pregunta = unidecode(pregunta.decode('utf-8').lower())
		pregunta = self.preprocesa(pregunta)
		res = findall('\w+', pregunta)
		# La CFG no soporta los numeros de mas de una cifra.
		# O los guardo y los sustituyo por un token o les hago split y los junto después
		for i in range(len(res)):
			if res[i].isdigit() and int(res[i]) > 9:
				nums.append(res[i])
				res[i] = 'num'

		return res, nums

	
	def preprocesa(self, pregunta):
		"""
		Estaría bien una función que eliminase palabras del dominio que no me interesan.
		Será del tipo stopWords, con una lista de palabras y n-gramas que no aporten nada. 
		Serán en su mayoría adjetivos o construcciones del tipo "Hola buenas" o "por favor"
		"""
		for i in self.stopwords:
			if i in pregunta: pregunta = "".join((pregunta.split(i)))
				
		return pregunta

	def cargarStop(self):
		a = os.path.dirname(os.path.abspath(__file__))
		
		with open(a+'/stopwords') as f:
			res = f.read().split('\n')
			res.remove('')
			
		return res
	
	def analizar(self, preg, nums):
		
		tree = None
		#for tree in parser.parse(preg):
		#	print tree
		try:
			tree = self.parser.parse(preg).next()
			c = list(tree.subtrees(filter=lambda x: x.label() in self.caracs)) # Para sacar las características especificadas
		except (StopIteration, ValueError): # Si el parsing falla
			c = None
		
		piso = self.generarPiso(c, nums)
		
		return piso, tree

	def generarPiso(self, caracs, nums):
		piso = [0] * 9
		if caracs is not None:
			for c in caracs:
				procesaCarac(c, piso, nums)
		
		return piso

	def analizarPregunta(self, pregunta):
		print pregunta
		pregunta, numeros = self.tokenizar(pregunta)
		print pregunta
		piso, arbol = self.analizar(pregunta, numeros)
		
		return piso, arbol
