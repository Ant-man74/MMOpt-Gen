import tkinter

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from .XmlHandler import XmlHandler


"""
Helper class to generate result
"""
class ReportGenerator:

	allEvaluator = []
	wantedCriteria = []
	wantedGeneration = []

	def __init__(self, allEvaluator):
		
		self.allEvaluator = allEvaluator
		tempWantedGeneration = list(map(int, XmlHandler.getItemFrom("reportOption","wantedGeneration")))
		
		for gen in tempWantedGeneration:
			self.wantedGeneration.append(gen-1)

		self.wantedCriteria = XmlHandler.getItemFrom("reportOption","wantedGraph")


	"""
	Generate the graph specified by the user and dump the wanted generation into a file
	result is a list of tuple with ( Individual, (buff, prefetch, t) )
	"""
	def generateResultReports(self):
		
		resultCriteria = ["buffer", "prefetch", "delta"]
		geneCriteria = ["foresigth","tileKeeping","coefAllUse","coefNextUse"]
		#for each generation that we want
		for i in range(0,len(self.wantedGeneration)):			
			# for each tuple of criteria we want
			for j in range(0,len(self.wantedCriteria)):
				
				# first criteria, if it's a gene or a result
				if self.wantedCriteria[j][0] in geneCriteria:
					list1 = [oneResult[0].fullChromosome[geneCriteria.index(self.wantedCriteria[j][0])] for oneResult in self.allEvaluator[self.wantedGeneration[i]].result]
				else:
					list1 = [oneResult[1][resultCriteria.index(self.wantedCriteria[j][0])] for oneResult in self.allEvaluator[self.wantedGeneration[i]].result]
				
				list1 = (self.wantedCriteria[j][0], list1)

				# second criteria, if it's a gene or a result
				if self.wantedCriteria[j][0] in geneCriteria:
					list2 = [oneResult[0].fullChromosome[geneCriteria.index(self.wantedCriteria[j][0])] for oneResult in self.allEvaluator[self.wantedGeneration[i]].result]
				else:
					list2 = [oneResult[1][resultCriteria.index(self.wantedCriteria[j][1])] for oneResult in self.allEvaluator[self.wantedGeneration[i]].result]
				
				list2 = (self.wantedCriteria[j][1], list2)

				self.generateAGraph(self.wantedGeneration[i]+1, list1, list2, 0)
				
			pass
			
			dumpName = str(self.wantedGeneration[i]+1) + "GenerationNbDump"		
			self.printResultToFile(self.allEvaluator[self.wantedGeneration[i]],dumpName)			
		
		return

	"""
	Generate a graph given two array of data, sort by x axis with 0 and y axis with 1 in sort
	"""
	def generateAGraph(self, genNb, xAxis, yAxis, sort):

		tupleList  = []
		# list putting in relation each item from one another (from xAxis and yAxis)
		for x in range(0,len(xAxis[1])):
			tupleList.append( (xAxis[1][x],yAxis[1][x] ))
			pass
		
		# sort depending on x Axis or y axis
		tupleList = sorted(tupleList, key = lambda x:x[sort])

		# re extract the now sorted tuples
		xAxisSorted = [singleTuple[0] for singleTuple in tupleList]
		yAxisSorted = [singleTuple[1] for singleTuple in tupleList]

		# Graph it up
		plt.plot(xAxisSorted, yAxisSorted, '.')
		plt.xlabel(xAxis[0])
		plt.ylabel(yAxis[0])
		self.savePlot(xAxis[0] + "X" + yAxis[0] + str(genNb) + "GraphGen")

	"""
	Save the current plot to a file and cleanup
	"""
	def savePlot(self,title):
		plt.savefig( "result/"+title, bbox_inches='tight')
		plt.clf()
		plt.cla()
		plt.close()


	"""
	Print an evaluator result to a csv file
	"""
	def printResultToFile(self, evaluator, name):
		resultString = evaluator.getAllCurrentResult()
		text_file = open("result/" + name + ".csv", "w")
		text_file.write(resultString)
		text_file.close()
		






		