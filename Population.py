
from Individual import Individual
from XmlHandler import XmlHandler

import random

class Population:

	currentPopulation = []
	popSize = None

	def __init__ (self, alt = None):
		if alt is None:
			xmlHandler = XmlHandler()
			self.popSize = int(xmlHandler.getItemFrom("algoGen","popSize"))
		elif alt is True:
			self.currentPopulation = []
			self.popSize = 0
	
	def generatePop(self):

		for x in range(0,int(self.popSize)):
			newIndividual = Individual()
			self.currentPopulation.append(newIndividual)			
			pass
		return self

	def getPopulation(self):
		return self.currentPopulation

	def addIndividual(self, individual):
		self.currentPopulation.append(individual)
		self.popSize += 1

	def addXNewIndividual(self, x):
		for x in range(0,x):
			newIndividual = Individual()
			self.currentPopulation.append(newIndividual)
			pass

	def cleanUp(self):
		self.currentPopulation = []
		self.popSize = 0

	"""
	Display the chromosome of the Individual
	"""
	def __str__(self):
		
		strRet = "[";
		for x in range(0,len(self.currentPopulation)-1):
			strRet = strRet + str(self.currentPopulation[x]) + "\n"
			pass
		strRet = strRet + "]";
		return strRet
