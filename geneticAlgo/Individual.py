
from .SchedulingHandler import SchedulingHandler
from .XmlHandler import XmlHandler

import random

"""
Individual definition for a genetic algorythm
"""
class Individual:

	chromosomeLength = 6

	#Multiply by chromosome length
	fullChromosome = [None] * 6
		
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
			geneSelect = random.randint(0, self.chromosomeLength)
			fullChromosome[geneSelect] = Individual.genAGene(geneSelect)
		
		return fullChromosome
	
	"""
	generate a value for a chromosome, contain the method of generation for each gene return None if not defined
	"""
	@staticmethod
	def genAGene(x):

		zRange 				=	list(map(int, XmlHandler.getItemFrom("mmopt","bufferRange")))
		foresigthRange 		= 	list(map(int, XmlHandler.getItemFrom("mmopt","foresigthRange")))
		tileKeepingRange 	= 	list(map(int, XmlHandler.getItemFrom("mmopt","tileKeepingRange")))
		coefNextUseRange 	= 	list(map(int, XmlHandler.getItemFrom("mmopt","coefNextUseRange")))
		coefAllUseRange 	= 	list(map(int, XmlHandler.getItemFrom("mmopt","coefAllUseRange")))

		ret = None
		# Min max value of buffer
		if x is 1:
			ret = random.randint(zRange[0], zRange[1])
		
		# Method of scheduling EECM or CGM
		elif x is 2:
			ret = 0#random.randint(0,1) 
		
		#foresigth
		elif x is 3:
			ret = random.randint(foresigthRange[0], foresigthRange[1])
		
		#tileKeeping
		elif x is 4:
			ret = random.randint(tileKeepingRange[0], tileKeepingRange[1]) 
		
		#coefNextUse
		elif x is 5:
			ret = (random.randint(coefNextUseRange[0], coefNextUseRange[1]) / 10) + 1

		#coefAllUse
		elif x is 6:
			ret = (random.randint(coefAllUseRange[0], coefAllUseRange[1]) / 10) + 1

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