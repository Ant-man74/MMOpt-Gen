
from .SchedulingHandler import SchedulingHandler
from .XmlHandler import XmlHandler

import random

"""
Individual definition for a genetic algorythm
"""
class Individual:

	chromosome1 = None
	chromosome2 = None

	fullChromosome = [chromosome1, chromosome2]
	
	"""
	Init and pick chromosome randomly or init a chromosome with a specific configuration if provided
	"""
	def __init__(self, chrom = None):
		# Init
		if chrom is None: 
			#needs to be moved to a better spot because we call him each time we create a dude despite it not moving for the whole algo
			self.chromosome1 = Individual.genAGene(1)
			self.chromosome2 = Individual.genAGene(2) 	
			self.fullChromosome = [self.chromosome1,self.chromosome2]
		else:
			self.chromosome1 = chrom[0]
			self.chromosome2 = chrom[1]
			self.fullChromosome = [self.chromosome1,self.chromosome2]

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
		self.fullChromosome = [self.chromosome1,self.chromosome2]

	"""
	mutate a gene on a chromosome
	"""
	def mutate(self):
		mutate = random.randint(1,100)
		if mutate <= self.mutationRate:
			#select a random gene and plug in a new value
			geneSelect = random.randint(0,len(fullChromosome)-1)
			fullChromosome[geneSelect] = random.randint(1,5)
		return fullChromosome
	
	"""
	generate a value for a chromosome, contain the method of generation for each gene
	"""
	@staticmethod
	def genAGene(x):
		zMin, zMax = SchedulingHandler.getBufferRange()
		ret = None
		# Min max value of buffer
		if x is 1:
			ret = random.randint(zMin,zMax)
		# Method of scheduling EECM or CGM
		elif x is 2:
			ret = random.randint(0,1) 
		return ret

	"""
	Display the chromosome of the Individual
	"""
	def __str__(self):
		strOut = "["
		for x in range(0,len(self.fullChromosome)):
			strOut = strOut + "\""+ str(self.fullChromosome[x]) +"\","
		strOut = strOut[:-1] + "]"
		return strOut

	"""
	Return a string formated for CSV file
	"""
	def printCsv(self):
		strOut = ""
		for x in range(0,len(self.fullChromosome)):
			strOut = strOut + ","+ str(self.fullChromosome[x]) +","
		strOut = strOut[:-1] 
		return strOut

	"""
	Return a string containing CSV headers for all chromosome
	"""
	def printHeaderCsv(self):
		csvStr = ""
		for x in range(1,len(self.fullChromosome)+1):
			csvStr = csvStr + "Chromosome " + str(x) + ","
			pass
		return csvStr + "\n"