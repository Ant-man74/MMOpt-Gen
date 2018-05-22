
from geneticAlgo.Evaluation import Evaluation
from geneticAlgo.Population import Population
from geneticAlgo.Reproduction import Reproduction
from geneticAlgo.SchedulingHandler import SchedulingHandler
from geneticAlgo.XmlHandler import XmlHandler

import sys
import copy

def main():
	
	#variable
	firstEvaluator = []
	lastEvaluator = []
	global zMin
	global zMax

	# Handle config
	xmlHandler = XmlHandler()

	# Initialize scheduler
	scheduler = SchedulingHandler()	

	# Generate Population
	pop = Population()
	pop.generatePop()

	maxTour = XmlHandler.getItemFrom("algoGen","maxTour")

	# Run a number of iteration
	for x in range(0,int(maxTour)):
		result = []

		# Test the currentPop to get the result of each Individual
		for y in range(0,len(pop.currentPopulation)):

			if pop.currentPopulation[y].fullChromosome[1] == 1 :
				(Z,N,T) = scheduler.executeSchedule(pop.currentPopulation[y].fullChromosome[0],"ECM")
			elif pop.currentPopulation[y].fullChromosome[1] == 2 :
				(Z,N,T) = scheduler.executeSchedule(pop.currentPopulation[y].fullChromosome[0],"CGM")
			elif pop.currentPopulation[y].fullChromosome[1] == 3 :
				(Z,N,T) = scheduler.executeSchedule(pop.currentPopulation[y].fullChromosome[0],"EECM")
			result.append([pop.currentPopulation[y],(Z,N,T)]);
			sys.exit(0)
			pass

		evaluator = Evaluation(result)
	
		#Save first and last iteration
		if x == 0 : 
			firstEvaluator = copy.deepcopy(evaluator)			
		elif x == int(maxTour)-1 :
			lastEvaluator = copy.deepcopy(evaluator)			
			
		pop.cleanUp()

		# Rank the currentPop with pareto front and return a new population post sorting			
		newPop = evaluator.tournamentRound()

		# Reproduce and replace the old population with the new one
		reproduction = Reproduction(newPop)
		pop = reproduction.reproducePop()
		
		sys.stdout.write('\r')
		sys.stdout.write("Finished tour "+ str(x) +"/"+ maxTour)
		
		pass

	#print(firstPop)
	#print(lastPop)
	print(firstEvaluator.printAllCurrentResult())
	print(lastEvaluator.printAllCurrentResult())

if __name__ == "__main__":
	main()