
import numpy as np
from Population import Population
from Individual import Individual

import random

class Evaluation:

	result = []

	def __init__(self, result):
		self.result = result

	def tournamentRound(self):
		#may not compare the whole pop?
		newPopulation = Population(True);
		remaining = 1

		while remaining != 0:
			
			remaining = len(self.result)-1
			pick1 = random.randint(0,remaining) 
			pick2 = random.randint(0,remaining) 			
			buff1, N1, T1 = self.result[pick1][1]
			buff2, N2, T2 = self.result[pick2][1]

			if buff1 < buff2 and N1 < N2 and T1 < T2 :
				newPopulation.addIndividual(Individual([self.result[pick1][0].chromosome1,self.result[pick1][0].chromosome2]))
			else :
				newPopulation.addIndividual(Individual([self.result[pick1][0].chromosome1,self.result[pick1][0].chromosome2]))
				newPopulation.addIndividual(Individual([self.result[pick2][0].chromosome1,self.result[pick2][0].chromosome2]))

			np.delete(self.result,pick1,0)
			np.delete(self.result,pick2,0)
			print (len(self.result)-1)
			pass

		return newPopulation


			