
from XmlHandler import XmlHandler
from Individual import Individual

import random

class Reproduction:

	mutationRate = None
	crossOverRate = None
	population = None

	def __init__(self, popToRepro):
		xmlHandler = XmlHandler()
		self.mutationRate = int(xmlHandler.getItemFrom("algoGen","mutationRate"))
		self.crossOverRate = int(xmlHandler.getItemFrom("algoGen","crossOverRate"))
		self.population = popToRepro
		print
	
	# ToDo should be scalable for more chromosome + refactoring
	#Also this is quite a bad method as it's not how a point crossoer should be done but it's equivalent for the time being
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

			# select how many in the 3 gene will be shuffled (1 or 2) 
			geneShuffle = random.randint(1,2)

			# extract chromosome
			fullChromosome1 =  matingIndividual1.getFullChromosome()
			fullChromosome2 =  matingIndividual2.getFullChromosome()

			if geneShuffle == 1:
				# select which gene to shuffle
				geneSelect = random.randint(0,len(fullChromosome1)-1)
				# shuffle
				oldGene = fullChromosome1[geneSelect]
				fullChromosome1[geneSelect] = fullChromosome2[geneSelect]
				fullChromosome2[geneSelect] = oldGene

			elif geneShuffle == 2:
				
				# select which gene to shuffle
				geneSelect1 = 0
				geneSelect2 = 0				
				while geneSelect1 == geneSelect2:
					geneSelect1 = random.randint(0,len(fullChromosome1)-1)
					geneSelect2 = random.randint(0,len(fullChromosome1)-1)
					pass
				
				# shuffle
				oldGene1 = fullChromosome1[geneSelect1]
				fullChromosome1[geneSelect1] = fullChromosome2[geneSelect1]
				fullChromosome2[geneSelect1] = oldGene1

				oldGene2 = fullChromosome1[geneSelect2]
				fullChromosome1[geneSelect2] = fullChromosome2[geneSelect2]
				fullChromosome2[geneSelect2] = oldGene2

			# chance to mutate each individual
			fullChromosome1 = self.mutateIndividual(fullChromosome1)
			fullChromosome2 = self.mutateIndividual(fullChromosome2)

			# should I add or replace them? replacement problem to discuss?
			# replace parent in population
			self.population.currentPopulation[id1].updateIndividual(fullChromosome1)
			self.population.currentPopulation[id1].updateIndividual(fullChromosome2)

			return self.population
			pass


	def mutateIndividual(self, fullChromosome):
		
		mutate = random.randint(1,100)
		if mutate <= self.mutationRate:
			#select a random gene and plug in a new value
			geneSelect = random.randint(0,len(fullChromosome)-1)
			fullChromosome[geneSelect] = random.randint(1,5)
		return fullChromosome



