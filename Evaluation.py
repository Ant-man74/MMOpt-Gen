
import numpy as np
from Population import Population
from Individual import Individual

import random

"""
Evaluation class for a genetic algorythm for the 3MMOPT problem
"""
class Evaluation:

	#array with [individual, result (Z,N,T)]
	result = []

	def __init__(self, result):
		self.result = result

	"""
	Evaluate the resut contained in self.result and generate a new population according to the pareto dominance of two randomly selected solution
	if one solution is absolutely superior (all criteria better) it will be added to a new population
	if no solution is absolutely superior they are added back into the new population (both of them)
	"""
	def tournamentRound(self):

		newPopulation = Population(True);
		#-1 because we want to stay in range for the array
		remaining = len(self.result)-1
		indToAdd = 0

		#while we haven't evaluated all the pop via random selection
		while remaining > 0:

			#pick two random individual of the population
			pick1 = random.randint(0,remaining) 
			pick2 = random.randint(0,remaining)
			
			#retrieve their result
			buff1, N1, T1 = self.result[pick1][1]
			buff2, N2, T2 = self.result[pick2][1]

			#if an individual is absolutly better than the other select him otherwise add them both, will need revision
			if buff1 < buff2 and T1 < T2:
				newPopulation.addIndividual(Individual([self.result[pick1][0].chromosome1,self.result[pick1][0].chromosome2]))
				indToAdd = indToAdd + 1
			elif buff1 < buff2 and T1 > T2:
				newPopulation.addIndividual(Individual([self.result[pick2][0].chromosome1,self.result[pick2][0].chromosome2]))
				indToAdd = indToAdd + 1
			else:
				newPopulation.addIndividual(Individual([self.result[pick1][0].chromosome1,self.result[pick1][0].chromosome2]))
				newPopulation.addIndividual(Individual([self.result[pick2][0].chromosome1,self.result[pick2][0].chromosome2]))

			del(self.result[pick1])
			del(self.result[pick2-1])

			remaining = len(self.result)-1
			pass

		newPopulation.addXNewIndividual(indToAdd)

		return newPopulation

	"""
	return a result "B, N, T" under a string format
	"""
	def printAResult(self,x):

		buff, prefetch , t = self.result[x][1]
		return str(buff) + ", " + str(prefetch) + ", " + str(t)

	"""
	print all current result and their associated Individual in a string formated for CSV output
	"""
	def printAllCurrentResult(self):

		headerResult = "\nBuffer Number (Z), PreFetch Number(N), Time (T), "
		fullStr = headerResult + self.result[0][0].printHeaderCsv() + ""

		for x in range(0,len(self.result)):
			res = self.printAResult(x) + " , " + self.result[x][0].printCsv() + ""
			fullStr = fullStr + res + "\n"
			pass

		return fullStr


			