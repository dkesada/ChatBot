# -*- coding: utf-8 -*-
#author: David Quesada López

from db import db
from nltk.parse.generate import generate
from nltk import data
import os
import markovify
from random import randint

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

class OutGrammar:
	
	def __init__(self):
		self.gramSeg = self.cargarGramaticaSeg()
		self.markovCompr = self.markovNoComprendido()

	def generarRespuesta(self, casa, pregunta, arbol):
		"""
		Función principal del módulo. Recibe una casa en su formato de array, busca casas similares en la base de datos
		y genera una respuesta en lenguaje natural acorde.
		En caso de que la casa sea un vector de 0's, se entiende que la pregunta no fue comprendida, y se genera una
		petición para que el usuario repita su pregunta con otras palabras.
		Cuenta con el grado de certidumbre para generar respuestas de distinto tipo, según lo seguro que esté el sistema
		de los resultados que ha obtenido.
		"""
		if sum(casa) is not 0:
			sim, cert = db.obtenerSimilares(casa)
			res = self.generarTexto(sim,cert,pregunta,arbol)
		else:
			res = self.preguntaNoComprendida()

		return res

	def generarTexto(self, sim, cert, pregunta, arbol):
		"""
		Comprueba la certidumbre de las casas encontradas y genera una respuesta acorde a la pregunta y la situación.
		"""
		
		if cert is 2:
			res = self.respuestaSegura(sim, pregunta, arbol)
		elif cert is 1:
			res = self.respuestaAproximada(sim, pregunta, arbol)
		else:
			res = self.respuestaNoEncontrada()
		
		return res
		
	def cargarGramaticaSeg(self):
		a = os.path.dirname(os.path.abspath(__file__))
		gramatica = data.load('file:' + a + '/segura.cfg')
		
		return gramatica

	def respuestaSegura(self, sim, pregunta, arbol):
		res = list(generate(self.gramSeg))
		res = res[randint(0,len(res)-1)]
		res = self.coordina(res, arbol)
		res = ' '.join(res)
		
		return res
		
	def coordina(self,frase,arbol):
		"""
		Coordina el sintagma nominal buscado en la pregunta con el que se ofrece en la respuesta
		"""
		
		sub = list(arbol.subtrees(filter=lambda x: x.label() in {"TipoS","TipoP"}))[0]
		genero, numero, nombre = self.procesaTipo(sub)
		sintagma = self.generaSintagma(genero, numero, nombre)
		sn = frase.index('Sn')
		frase = frase[0:sn] + sintagma + frase[sn+1:]
		frase = self.coordinaVerbo(frase, numero)
		return frase
		

	def procesaTipo(self,sub):
		"""Analiza el subarbol de TipoS o TipoP para saber el tipo, el género y qué nombre se busca"""
		genero = 0 # 0 = fem, 1 = masc
		numero = 0 # 0 = plural, 1 = singular
		nombre = self.tilda(sub.leaves())
		
		if "TipoS" in [sub.label()]:
			numero = 1
			genero = 1
			if "casa" in nombre: genero = 0
		else:
			numero = 0
			genero = 1
			if "casas" in nombre: genero = 0
		
		return genero, numero, nombre
			
	def generaSintagma(self, genero, numero, nombre):
		"""Genera el sintagma nominal adecuado en base al genero y número"""
		det = 'est'
		
		if genero is 0 and numero is 0:
			det += 'as'
		elif genero is 0 and numero is 1:
			det += 'a'
		elif genero is 1 and numero is 0:
			det += 'os'
		elif genero is 1 and numero is 1:
			det += 'e'
		
		return [det] + nombre

	def coordinaVerbo(self, frase, numero):
		"""Si aparecen 'puede' o 'parece' en la respuesta, los coordina"""
		if numero is 0:
			if 'parece' in frase:
				ind = frase.index('parece')
				frase[ind] = frase[ind]+'n'
			elif 'puede' in frase:
				ind = frase.index('puede')
				frase[ind] = frase[ind]+'n'
		
		return frase

	def tilda(self, nombre):
		if 'atico' in nombre:
			nombre[0] = 'ático'
		elif 'duplex' in nombre:
			nombre[0] = 'dúplex'
		elif 'rustica' in nombre:
			nombre[1] = 'rústica'
		elif 'rusticas' in nombre:
			nombre[1] = 'rústicas'
		return nombre
		

	def respuestaAproximada(self, sim, pregunta, arbol):
		
		return "aproximado"
		
	def respuestaNoEncontrada(self):
		"""
		Probablemente la aproximación de las preguntas no comprendidas sea también válida aquí
		"""
		return "nada"

	def markovNoComprendido(self):
		a = os.path.dirname(os.path.abspath(__file__))
		with open(a+'/respNoCompr.txt') as f:
			text = f.read()

		text_model = markovify.NewlineText(text)
		
		return text_model

	def preguntaNoComprendida(self):
		"""
		Función que genera una respuesta comunicando que no se ha entendido la pregunta.
		Para esto, no creo que haga falta una gramática ni una batería de respuestas tipadas, con respuestas enlatadas aleatorias debería ser suficiente.
		De hecho, unas cuantas respuestas y markovify para una red de markov podría venir bien para que sea un poco más sofisticado.
		"""	
		res = self.markovCompr.make_sentence(tries=100,max_overlap_total=95)
		
		return res
