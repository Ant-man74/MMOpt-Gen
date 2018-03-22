
from XmlHandler import XmlHandler
from Population import Population
from Reproduction import Reproduction

def main():
	xmlHandler = XmlHandler()
	xmlHandler.loadConfig()
	maxTour = xmlHandler.getItemFrom("algoGen","maxTour")

	pop = Population()
	currentPop = pop.generatePop()

	for x in range(1,maxTour):
		
		# test the currentPop to get the result

		# rank the currentPop with pareto front

		reproduction = Reproduction(currentPop)
		currentPop = reproduction.reproducePop()

	pass


if __name__ == "__main__":
	main()