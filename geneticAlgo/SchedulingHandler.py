
import numpy as np
import random
import os

from .FECM import FECM

from .XmlHandler import XmlHandler

"""
	Handle the Scheduling for the 3-MMOPT problem
"""


class SchedulingHandler:
	
	alpha = 0
	beta = 0

	def __init__(self):
		self.alpha = int(XmlHandler.getItemFrom("mmopt","alpha"))
		self.beta = int(XmlHandler.getItemFrom("mmopt","beta"))

	"""
	Execute the ECM algorythm according to the parameters
	For now change the kernel manualy
	"""
	def executeSchedule(self, algo, individual):

		Z, N, T = 0, 0, 0
		#16 is the number of images to do (numer of file in /Kernel)
		#for k in range(1):
		Y,Ry = SchedulingHandler.extractTiles('test_4_',15)
		X = SchedulingHandler.InputTile(Ry)

		#0 is ECM
		if algo == 0:
		   fecm = FECM( X, Y, Ry, self.alpha, self.beta, individual )  
		   Z, N, T = fecm.executeFECM()   			
		
		return Z, N, T

	"""
	Extract the data from the file "filename" for the "k" file
	"""
	@staticmethod
	def extractTiles(filename, k):
		#get Y Ry from Kernel
		Matrix0 = open(os.getcwd()+'/Kernels/'+filename+'{}.txt'.format(k), 'r')     
		List0 = Matrix0.readlines()
		Matrix0.close()
		#the number of the output tile
		Y = []
		Ry = [] 
		
		for List1 in List0:
			Y.append(int(List1.split(':')[0]))
			Ry.append(list(map(int,List1.split(':')[1].replace('#',' ').replace(',',' ').split())))
		return (Y,Ry)

	"""
	Retrieve the maximum and minimum number of buffer necessary for the algorithm to work on ONE kernel
	To have it work with all kernel uncomment all the line inside
	"""
	@staticmethod
	def setBufferRange():
		allBufferRange = []
		#for k in range(16):
		Y,Ry = SchedulingHandler.extractTiles('test_4_',15)
		Zmin = SchedulingHandler.MinNbBuffer(Ry)
		Zmax = SchedulingHandler.MaxBuffersNb(Ry)
		allBufferRange.append([Zmin, Zmax])
			#pass

		#minVal = 0
		#for i in range(len(allBufferRange)-1) :

		#	if allBufferRange[i][0] > minVal:
		#		minVal = allBufferRange[i][0]

		XmlHandler.setItemIn("mmopt","bufferRange",[Zmin,Zmax])

	"""
	Find X: the input tile list  <===> len(X)=lbN
	"""
	@staticmethod
	def InputTile(Ry):
		X = []
		
		for i in range(len(Ry)):
			X.append(Ry[i])
		
		X = SchedulingHandler.reduce(lambda x, y:x+y, X)
		X = list(set(X))
		X.sort()
		return X

	"""
	Find Xmin: the minimum of required tile  <===> aka the minimum number of buffer required to compute this output tile
	"""
	@staticmethod
	def MinNbBuffer(Ry):

		ListTile = []
		
		#ListTile = List of number of required tile for computing
		# --> the max number means the output tile which needs the most input tile to be computed
		# --> so the minimum number of buffer to have 
		for i in range(len(Ry)):
			ListTile.append(len(Ry[i]))
		
		Zmin = max(ListTile)
		return Zmin

	"""
	Find Z: the maximum number of buffer for a set of tile equal to the number of total prefetch
			necessary if we think that we charge  each input tile once in the buffers (worst case scenario unacceptable number of buffer)
			for example we have 150 tile used to constitue a picture each output tile require no more than 5 input tile
			we decide to charge all of the 150 tile into a special buffer to compute everything now sure the number of prefetch will be low and time also will be low but 150 buffer is not cool
	"""
	@staticmethod
	def MaxBuffersNb(Ry):

		valMax = 0
		allNeededTile = []

		for i in range(len(Ry)):
			for x in Ry[i]:
				if x not in allNeededTile:
					allNeededTile.append(x)
		
		Zmax = len(allNeededTile)

		return Zmax

	"""
	Find Xmin: the minimum of required tile  <===> 
	"""
	@staticmethod
	def RequiredTileNb(Ry):
		ListTile=[]
		for i in range(len(Ry)):
			ListTile.append(len(Ry[i]))
		Xmin=min(ListTile)
		return Xmin

	"""
	Det # Lower Bounds lbN,lbZ, lb1Delta & lb2Delta
	"""
	@staticmethod
	def LowerBounds(X,Y,Ry,alpha,beta):
		lbN = len(X)
		lbZ = SchedulingHandler.MinNbBuffer(Ry)
		lb1Delta = (alpha)*len(X)+beta+1
		lb2Delta = alpha+(beta*len(Y))+1
		lb3Delta = alpha*SchedulingHandler.RequiredTileNb(Ry)+(beta*len(Y))+1
		lbDelta = max(lb1Delta, lb2Delta) 
		lbDelta1 = max(lb1Delta, lb3Delta)	
		return lbN, lbZ, lb1Delta, lb2Delta, lb3Delta, lbDelta, lbDelta1

	"""
	Deprecated method of python 2.7 but necessary for this algorythm as I don't know how to replace it 
	"""
	@staticmethod
	def reduce(function, iterable, initializer=None):
		it = iter(iterable)
		
		if initializer is None:			
			try:
				initializer = next(it)
			except StopIteration:
				raise TypeError('reduce() of empty sequence with no initial value')		
		
		accum_value = initializer		
		
		for x in it:
			accum_value = function(accum_value, x)

		return accum_value