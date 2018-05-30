
from .SchedulingHandler import SchedulingHandler
from .XmlHandler import XmlHandler

import random

"""
Individual definition for a genetic algorythm
"""
class Individual:

	chromosomeLength = 6

	fullChromosome = [None] * chromosomeLength
	
	"""
	Init and pick chromosome randomly or init a chromosome with a specific configuration if provided
	"""
	def __init__(self, chrom = None):
		# Init
		if chrom is None: 
			for i in range(0,self.chromosomeLength):
				self.fullChromosome[i] = Individual.genAGene(i+1)
				pass
		else:
			for i in range(0,self.chromosomeLength):
				self.fullChromosome[i] = chrom[i]
				pass


	"""
	Return the full chromosome of the Individual
	"""
	def getFullChromosome(self):
		return self.fullChromosome

	"""
	Update an individual with a new chromosome
	"""
	def updateIndividual(self,newChromosome):
		
		for i in range(0,self.chromosomeLength):
				self.fullChromosome[i] = newChromosome[i]
				pass

	"""
	mutate a gene on a chromosome
	"""
	def mutate(self):

		mutate = random.randint(1,100)
		
		if mutate <= self.mutationRate:
			#select a random gene and plug in a new value
			geneSelect = random.randint(0,len(fullChromosome)-1)
			fullChromosome[geneSelect] = Individual.genAGene(geneSelect)
		
		return fullChromosome
	
	"""
	generate a value for a chromosome, contain the method of generation for each gene return None if not defined
	"""
	@staticmethod
	def genAGene(x):

		bufferRange = list(XmlHandler.getItemFrom("mmopt","bufferRange"))
		ret = None

		# Min max value of buffer
		if x is 1:
			ret = random.randint(bufferRange[0], bufferRange[1])
		
		# Method of scheduling (fixed to FECM for the moment)
		elif x is 2:
			ret = 2   #random.randint(0,1)

		# Foresigth max (How far should he look in the schedule to take decision)
		elif x is 3:
			ret = random.randint(bufferRange[0], bufferRange[1])

		# TileKeeping cap (up to what tile should he try to prioritse keeping it in buffer)
		elif x is 4:
			ret = None

		# CoefAllUse max (the coefficient for grading the score of tile to be replaced when considering total use of the tile)
		elif x is 5:
			ret = None

		# CoefNextUse max (the coefficient for grading the score of tile to be replaced when considering when is the tile used next)
		elif x is 6:
			ret = None
		
		return ret

	"""
	Display the chromosome of the Individual
	"""
	def __str__(self):
		strOut = "["
		
		for x in range(0, self.chromosomeLength):
			strOut = strOut + "\""+ str(self.fullChromosome[x]) +"\","
		strOut = strOut[:-1] + "]"
		
		return strOut

	"""
	Return a string formated for CSV file
	"""
	def printCsv(self):
	
		strOut = ""
		
		for x in range(0, self.chromosomeLength):
			strOut = strOut + ","+ str(self.fullChromosome[x]) +","
		strOut = strOut[:-1] 
		
		return strOut

	"""
	Return a string containing CSV headers for all chromosome
	"""
	def printHeaderCsv(self):

		csvStr = ""
		
		for x in range(1, self.chromosomeLength+1):
			csvStr = csvStr + "Chromosome " + str(x) + ","
			pass
		
		return csvStr + "\n"