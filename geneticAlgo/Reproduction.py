
from .XmlHandler import XmlHandler
from .Individual import Individual

import random
import sys

class Reproduction:

	mutationRate = None
	crossOverRate = None
	population = None

	def __init__(self, popToRepro):
		
		self.mutationRate = int(XmlHandler.getItemFrom("algoGen","mutationRate"))
		self.crossOverRate = int(XmlHandler.getItemFrom("algoGen","crossOverRate"))
		self.population = popToRepro
	
	"""
	Clean one point cut reproduction of chromosome, scalable for as much gene as we want
	"""
	def reproducePop(self):
		
		# only mate 80% of the pop
		for x in range(0,int(round((len(self.population.currentPopulation)*40)/100))):
			
			# selection of two individual in the population
			id1 = random.randint(0,self.population.popSize-1)
			id2 = random.randint(0,self.population.popSize-1)

			while id1 == id2:
				id2 = random.randint(0,self.population.popSize-1)
				pass

			matingIndividual1 = self.population.currentPopulation[id1]
			matingIndividual2 = self.population.currentPopulation[id2]			

			# select a point at which the individual chromosome is going to be cut
			geneCutPoint = random.randint(1,len(matingIndividual1.fullChromosome)-1)

			# extract chromosome
			fullChromosome1 =  matingIndividual1.getFullChromosome()
			fullChromosome2 =  matingIndividual2.getFullChromosome()

			chromosome1Begin = fullChromosome1[:geneCutPoint]
			chromosome1End = fullChromosome1[-(len(fullChromosome1)-geneCutPoint):]

			chromosome2Begin = fullChromosome2[:geneCutPoint]
			chromosome2End = fullChromosome2[-(len(fullChromosome2)-geneCutPoint):]

			newChromosome1 = chromosome1Begin + chromosome2End
			newChromosome2 = chromosome2Begin + chromosome1End
			
			# replace parent in population
			self.population.currentPopulation[id1].updateIndividual(newChromosome1)
			self.population.currentPopulation[id2].updateIndividual(newChromosome2)

			#chance at mutation
			self.population.currentPopulation[id1].mutate()
			self.population.currentPopulation[id2].mutate()

			pass
		return self.population
			