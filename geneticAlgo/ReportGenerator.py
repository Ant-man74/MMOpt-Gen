import tkinter

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

class ReportGenerator:
	
	def printResultToFile(self, resultString,name):
		text_file = open(name+".csv", "w")
		text_file.write(resultString)
		text_file.close()

	def generateAGraph(self, xAxis, yAxis, sort):

		tupleList  = []
		for x in range(0,len(xAxis[1])):
			tupleList.append( (xAxis[1][x],yAxis[1][x] ))
			pass

		tupleList = sorted(tupleList, key = lambda x:x[sort])

		xAxisSorted = [singleTuple[0] for singleTuple in tupleList]
		yAxisSorted = [singleTuple[1] for singleTuple in tupleList]

		plt.plot(xAxisSorted, yAxisSorted, '.')
		plt.xlabel(xAxis[0])
		plt.ylabel(yAxis[0])


	def showPlot(self,title):
		plt.savefig( title, bbox_inches='tight')
		plt.show()
		plt.clf()
		plt.cla()
		plt.close()
