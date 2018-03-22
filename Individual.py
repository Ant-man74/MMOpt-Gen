
import random

class Individual:

	chromosome1 = None
	chromosome2 = None
	chromosome3 = None
	fullChromosome = [chromosome1, chromosome2, chromosome3]

	def __init__(self):
		#to replace with randomized REAL parameters		
		self.chromosome1 = random.randint(0,256)
		self.chromosome2 = random.randint(0,1)
		self.chromosome3 = random.randint(0,30)
		self.fullChromosome = [self.chromosome1,self.chromosome2,self.chromosome3]

	def __str__(self):
		return "["+str(self.chromosome1)+","+str(self.chromosome2)+","+str(self.chromosome3)+"]"

	def getFullChromosome(self):
		return fullChromosome

	def updateIndividual(self,newChromosome):
		self.chromosome1 = newChromosome[0]
		self.chromosome2 = newChromosome[1]
		self.chromosome3 = newChromosome[2]
		self.fullChromosome = [self.chromosome1,self.chromosome2,self.chromosome3]