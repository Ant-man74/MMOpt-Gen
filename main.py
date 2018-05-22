
from geneticAlgo.Evaluation import Evaluation
from geneticAlgo.Population import Population
from geneticAlgo.Reproduction import Reproduction
from geneticAlgo.SchedulingHandler import SchedulingHandler
from geneticAlgo.XmlHandler import XmlHandler
from geneticAlgo.ReportGenerator import ReportGenerator

from datetime import datetime
import sys
import copy

def main():
	
	#variable
	allEvaluator = []
	
	#timer for execution time
	StartTime = datetime.now()

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
		#Save the iteration
		allEvaluator.append(copy.deepcopy(evaluator))		
		pop.cleanUp()
		# Rank the currentPop with pareto front and return a new population post sorting			
		newPop = evaluator.tournamentRound()

		# Reproduce and replace the old population with the new one
		reproduction = Reproduction(newPop)
		pop = reproduction.reproducePop()
		
		sys.stdout.write('\r')
		sys.stdout.write("Finished tour "+ str(x+1) +"/"+ maxTour)
		
		pass

	sys.stdout.write("\n")

	#generate Graph of wanted generation depending on the config files
	generator = ReportGenerator(allEvaluator)
	generator.generateResultReports()

	EndTime = datetime.now()
	totalTime = EndTime - StartTime
	print ("Total time: "+str(totalTime.seconds//3600)+":"+ str((totalTime.seconds//60)%60)+":"+ str(totalTime.seconds))

if __name__ == "__main__":
	main()