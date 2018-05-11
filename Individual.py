
from SchedulingHandler import SchedulingHandler
from XmlHandler import XmlHandler

import random

"""
Individual definition for a genetic algorythm
"""
class Individual:

	chromosome1 = None
	chromosome2 = None
	chromosome3 = None

	fullChromosome = [chromosome1, chromosome2, chromosome3]
	
	"""
	Init and pick chromosome randomly or init a chromosome with a specific configuration if provided
	"""
	def __init__(self, chrom = None):
		# Init
		if chrom is None: 
			#needs to be moved to a better spot because we call him each time we create a dude despite it not moving for the whole algo
			self.chromosome1 = Individual.genAGene(1)# Number of buffer 		
			self.chromosome2 = Individual.genAGene(2) # Method to use (ECM or CGM)			
			self.fullChromosome = [self.chromosome1,self.chromosome2,self.chromosome3]
		else:
			self.chromosome1 = chrom[0]
			self.chromosome2 = chrom[1]
			self.fullChromosome = [self.chromosome1,self.chromosome2,self.chromosome3]

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
	generate a value for the a chromosome, contain the method of generation for each chromosome
	"""
	@staticmethod
	def genAGene(x):
		ret = None
		if x is 1:
			ret = random.randint(zMin,zMax)
		elif x is 2:
			ret = random.randint(1,2) 
		return ret

	"""
	Display the chromosome of the Individual
	"""
	def __str__(self):
		return "["+str(self.chromosome1)+","+str(self.chromosome2)+","+str(self.chromosome3)+"]"

	"""
	Return a string formated for CSV file
	"""
	def printCsv(self):
		return str(self.chromosome1)+","+str(self.chromosome2)+","+str(self.chromosome3)

	"""
	Return a string containing CSV headers for all chromosome
	"""
	def printHeaderCsv(self):
		csvStr = ""
		for x in range(1,len(self.fullChromosome)+1):
			csvStr = csvStr + "Chromosome " + str(x) + ","
			pass
		return csvStr + "\n"