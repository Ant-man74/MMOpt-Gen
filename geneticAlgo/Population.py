
from .Individual import Individual
from .XmlHandler import XmlHandler

import random

class Population:

	popSizeToGenerate = None
	currentPopulation = []
	popSize = 0

	def __init__ (self):
		self.popSizeToGenerate = int(XmlHandler.getItemFrom("algoGen","popSize"))
		self.popSize = 0
		self.currentPopulation = []
		
	
	""" 
	Generate apopulation if the length specified in the xml file
	"""
	def generatePop(self):
		
		for x in range(0,int(self.popSizeToGenerate)):
			newIndividual = Individual()
			self.currentPopulation.append(newIndividual)			
			pass

		self.popSize = len(self.currentPopulation)
		return self

	""" 
	Return the current population for this object
	"""
	def getPopulation(self):
		return self.currentPopulation

	"""
	Add an individual to the current population
	"""
	def addIndividual(self, individual):
		self.currentPopulation.append(individual)
		self.popSize += 1

	"""
	Generate X new individual and put them in the current population
	"""
	def addXNewIndividual(self, x):
		for x in range(0,x):
			newIndividual = Individual()
			self.currentPopulation.append(newIndividual)
			self.popSize  = self.popSize + 1
			pass
			
	"""
	Reset the object to it's blank state
	"""
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
