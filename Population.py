
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
