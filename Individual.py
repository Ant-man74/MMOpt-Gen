from XmlHandler import XmlHandler
from SchedulingHandler import SchedulingHandler

import random

class Individual:

	chromosome1 = None
	chromosome2 = None
	chromosome3 = None
	fullChromosome = [chromosome1, chromosome2, chromosome3]
	bufferLowerBound = None
	bufferUpperBound = None

	"""
	Init and pick chromosome randomly
	"""
	def __init__(self):
		# Init
		xmlHandler = XmlHandler()
		self.bufferLowerBound = xmlHandler.getItemFrom("mmopt","bufferLowerBound")
		self.bufferUpperBound = xmlHandler.getItemFrom("mmopt","bufferUpperBound")

		zMin, zMax = SchedulingHandler.getBufferRange()
		self.chromosome1 = random.randint(zMin,zMax) # Number of buffer 		
		self.chromosome2 = random.randint(1,2) # Method to use (ECM or CGM)
		
		self.fullChromosome = [self.chromosome1,self.chromosome2,self.chromosome3]

	"""
	Display the chromosome of the Individual
	"""
	def __str__(self):
		return "["+str(self.chromosome1)+","+str(self.chromosome2)+","+str(self.chromosome3)+"]"

	"""
	Return the full chromosome of the Individual
	"""
	def getFullChromosome(self):
		return self.fullChromosome

	"""
	Update an individual with a new chromosome
	"""
	def updateIndividual(self,newChromosome):
		self.chromosome1 = newChromosome[0]
		self.chromosome2 = newChromosome[1]
		self.chromosome3 = newChromosome[2]
		self.fullChromosome = [self.chromosome1,self.chromosome2,self.chromosome3]