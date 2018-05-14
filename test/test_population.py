import unittest
from geneticAlgo.Population import Population
from geneticAlgo.XmlHandler import XmlHandler
from geneticAlgo.Individual import Individual



def setup_function(function):
   xmlHandler = XmlHandler()

def test_popConstructor():
	pop = Population()
	assert pop.popSizeToGenerate != None

def test_genPop():
	pop = Population()
	pop.generatePop()
	assert all(isinstance(x, Individual) for x in pop.currentPopulation)

def test_popAddX():
	pop = Population()
	pop.generatePop()
	oldPopSize = len(pop.currentPopulation)
	pop.addXNewIndividual(5)
	newPopSize = len(pop.currentPopulation)
	assert  oldPopSize+5 == newPopSize

def test_cleanUp():
	pop = Population()
	pop.generatePop()
	pop.cleanUp()
	assert pop.currentPopulation == [] and pop.popSize == 0