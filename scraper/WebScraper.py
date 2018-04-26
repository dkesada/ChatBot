#! /usr/bin/python
# -*- coding: utf-8 -*-
#author: David Quesada López

from urllib2 import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sys  


def getOp(info):
	op = 'alquiler'
	if 'venta' in info:
		op = 'venta'
	return op

def getTipo(info):
	tipo = 'rústica'
	if 'chalet' in info:
		tipo = 'chalet'
	elif 'piso' in info:
		tipo = 'piso'
	elif 'dúplex' in info:
		tipo = 'dúplex'
	elif 'ático' in info:
		tipo = 'ático'
	return tipo

def scrapInfo(soup, n):
	doc = open('descripciones/'+str(n), 'w')
	
	mainInfo = soup.findAll('span', {'class':'main-info__title-main'})
	mainInfo = mainInfo[0].get_text().lower()
	operacion = getOp(mainInfo)
	doc.write(operacion + ' ; ')
	tipoCasa = getTipo(mainInfo)
	doc.write(tipoCasa + ' ; ')
	ubicacion = soup.findAll('span', {'class':'main-info__title-minor'})
	doc.write(ubicacion[0].get_text() + ' ; ')
	
	precio = soup.findAll('span', {'class':'h3-simulated txt-bold'})
	doc.write(precio[0].get_text() + ' ;')
		
	carac = soup.findAll('div', {'class': 'details-property_features'})
	
	for c in carac:
		text = c.findAll('li')
		for line in text:
			doc.write(line.get_text() + ';')
			
	doc.close()
			

def main():
	# URL de Idealista tras una busqueda
	url = 'https://www.idealista.com/alquiler-viviendas/coslada-madrid/'

	driver = webdriver.Firefox()
	driver.get(url)

	casas = []
	i = 0
	
	print 'Iniciando el proceso...'
	
	try:
		casas = driver.find_elements_by_class_name('item')
		l = len(casas)

		while i < l:
			casas[i].click()
			i += 1
			html = driver.page_source
			soup = BeautifulSoup(html,'html.parser')
			# 1 archivo por cada casa con descripción y características
			scrapInfo(soup, i)
			print str(i*100/l) + '%...'
			driver.back()
			casas = driver.find_elements_by_class_name('item') #Tengo que hacerlo cada vez porque la lista de articulos se queda 'stale' si me muevo a uno de ellos y despues vuelvo
		
		driver.quit()
		print 'Proceso terminado.'

	except (NoSuchElementException):
		sys.exit("No hay casas que coger en esa url...")


reload(sys)  
sys.setdefaultencoding('utf8')
main()
