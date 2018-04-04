
from XmlHandler import XmlHandler
from Population import Population
from Reproduction import Reproduction
from SchedulingHandler import SchedulingHandler

def main():
	
	# Handle config
	xmlHandler = XmlHandler()
	xmlHandler.loadConfig()
	maxTour = xmlHandler.getItemFrom("algoGen","maxTour")

	# Initialize scheduler
	scheduler = SchedulingHandler()

	# Generate Population
	pop = Population()
	pop.generatePop()

	# Debug
	#for i in range(0,len(pop.currentPopulation)):
	#	print (pop.currentPopulation[i])

	# Run a number of iteration
	for x in range(1,int(maxTour)):
		
		result = []

		# Test the currentPop to get the result of each Individual
		for y in range(0,len(pop.currentPopulation)):

			if pop.currentPopulation[y].fullChromosome[1] == 1 :
				(Z,N,T) = scheduler.executeECM(pop.currentPopulation[y].fullChromosome[0])
			elif pop.currentPopulation[y].fullChromosome[1] == 2 :
				(Z,N,T) = scheduler.executeCGM(pop.currentPopulation[y].fullChromosome[0])

			result.append([pop.currentPopulation[y],(Z,N,T)]);


		# Rank the currentPop with pareto front

		# Reproduce and replace the old population with the new one
		reproduction = Reproduction(pop)
		pop = reproduction.reproducePop()

	#pass


if __name__ == "__main__":
	main()