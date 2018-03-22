
import random

from XmlHandler import XmlHandler
from Individual import Individual

class Population:

	currentPopulation = []
	popSize = None

	def __init__ (self):
		xmlHandler = XmlHandler()
		self.popSize = xmlHandler.getItemFrom("algoGen","popSize")

	def generatePop(self):

		for x in range(0,int(self.popSize)):
			newIndividual = Individual()
			self.currentPopulation.append(newIndividual)			
			pass
		return self.currentPopulation

	def getPopulation(self):
		return self.currentPopulation
