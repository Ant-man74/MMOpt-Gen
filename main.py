
from geneticAlgo.Evaluation import Evaluation
from geneticAlgo.Population import Population
from geneticAlgo.Reproduction import Reproduction
from geneticAlgo.SchedulingHandler import SchedulingHandler
from geneticAlgo.XmlHandler import XmlHandler
from geneticAlgo.ReportGenerator import ReportGenerator

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
	scheduler.setBufferRange()

	# Generate Population
	pop = Population()
	pop.generatePop()

	maxTour = XmlHandler.getItemFrom("algoGen","maxTour")

	# Run a number of iteration
	for x in range(0,int(maxTour)):
		result = []

		# Test the currentPop to get the result of each Individual
		for y in range(0,len(pop.currentPopulation)):

			#to change method change the method array and number def in Individual
			(Z,N,T) = scheduler.executeSchedule(pop.currentPopulation[y].fullChromosome[1], pop.currentPopulation[y].fullChromosome)

			result.append([pop.currentPopulation[y],(Z,N,T)]);
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
	sys.stdout.write("\n")

	#print(firstPop)
	#print(lastEvaluator)
	#print(firstEvaluator.printAllCurrentResult())
	generator = ReportGenerator()

	list1a, list2a = firstEvaluator.getCoupleList("buffer",2)
	list3a, list4a = firstEvaluator.getCoupleList("buffer","delta")

	list1b, list2b = lastEvaluator.getCoupleList("buffer",2)
	list3b, list4b = lastEvaluator.getCoupleList("buffer","delta")

	generator.generateAGraph(("buffer", list1a), ("foresigth",list2a), 0)
	generator.generateAGraph(("buffer", list1b), ("foresigth",list2b), 0)

	generator.showPlot("bufferXprefetch")

	generator.generateAGraph(("buffer", list3a), ("delta",list4a), 0)
	generator.generateAGraph(("buffer", list3b), ("delta",list4b), 0)

	generator.showPlot("bufferXDelta")


	generator.printResultToFile(firstEvaluator.getAllCurrentResult(),"filefirstEvaluator")
	generator.printResultToFile(lastEvaluator.getAllCurrentResult(),"filelastEvaluator")

if __name__ == "__main__":
	main()