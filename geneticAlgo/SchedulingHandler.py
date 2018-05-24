
import numpy as np
import random
from datetime import datetime
import sys
import os

from .CGM import *
from .EECM import *
from .FCGM import FCGM
from .FECM import FECM

from .XmlHandler import XmlHandler

"""
	Handle the Scheduling for the 3-MMOPT problem
	Variable used in this problem
		Input :
  			-Y  	= 	set of output tile to compute
			-Ry 	= 	incidence matrix of required tile X to get tile Y		
			-X 		= 	the list of input tile
			-alpha 	= 	Duration of a prefetch
			-beta 	= 	Duration of a computation
		Output :
			-Sj 	=	which output tile to compute
			-Uj 	= 	At which time to compute Sj

			-Di 	= 	Which input tile to prefetch
			-Bi 	= 	In which buffer we put the input tile
			-Ti 	= 	At which time we prefetch the input tile
			
			-Z 		= Number of buffer for this execution
			-N 		= Number of prefetch
			-Delta  = time taken to accomplish the task

		Other :
			-Xmin 	=	the minimum number of buffer necessary for all tile to be computed
			-Xmax	=	the maximum number of buffer that the algorythm can have (equal to the number of prefetch)		
	"""
class SchedulingHandler:

	
	
	alpha = 2
	beta = 3

	def __init__(self):
		self.initParam()

	"""
	Retrieve parameters for the execution of the ECM and CGM algorithm
	"""
	def initParam(self):
		self.alpha = int(XmlHandler.getItemFrom("mmopt","alpha"))
		self.beta = int(XmlHandler.getItemFrom("mmopt","beta"))

	"""
	Execute the ECM algorythm according to the parameters
	"""
	def executeSchedule(self,iterZ,algo):
		StartTime=datetime.now()			

		#16 is the number of images to do (numer of file in /Kernel)
		for k in range(16):

			Y,Ry = SchedulingHandler.extractTiles('test_4_',k)
			X = SchedulingHandler.InputTile(Ry)
			
			#Step2: Det All Bounds: lbZ, lbN & lbDelta
			#print " ------ Lower Bounds of 3-PSDPP: ------"
			#lbN,lbZ,lb1Delta,lb2Delta,lb3Delta,lbDelta,lbDelta1 = SchedulingHandler.LowerBounds(X,Y,Ry,self.alpha,self.beta)
			#print "0- Lower Bounds are (lbN,lbZ,lbDelta) with values = ", (lbN,lbZ,lbDelta)
			#print "0- New Lower Bounds in Delta are (lb3Delta,lbDelta1) with values = ", (lb3Delta,lbDelta1)

			#Step3: Apply Heuristic 1 
			#print " ------ Outputs Data of ECM: ------"
			if algo == "ECM":
				Sj, Uj, Di, Bi, Ti, Z, N, Delta = ECM(X, Y, Ry, self.alpha, self.beta, iterZ)

			elif algo == "CGM":
				Sj, Uj, Di, Bi, Ti, Z, N, Delta = CGM(X, Y, Ry, self.alpha, self.beta, iterZ)

			elif algo == "EECM":
			    Sj, Uj, Di, Bi, Ti, Z0, Z, N, Delta = EECM(X, Y, Ry, self.alpha, self.beta, iterZ)     

			elif algo == "FCGM":
			   fcgm = FECM( X, Y, Ry, self.alpha, self.beta, iterZ )  
			   Z, N, T = fcgm.executeFECM()   

			sys.exit(0)
			
			#print "1- All Outputs-ECM are (N1,Z1,Delta1) with values = ", (N1,Z1,Delta1)
			#Step0: Det DeltaMCT
			#DeltaMCT = [34,35,38,53,53,69,71,70,60,60,60,90,90,120,120,150]
			#Step6: Det Ratio for ECM heuristic
			#???
			#R1 = float(Delta)/float(DeltaMCT[k])
			
			#print "Ratio of ECM's Potential is: %.2f " % R1

		EndTime = datetime.now()
		#print('----- Duration of Execution -----:{} --- {} ===> {} '.format(StartTime, EndTime, EndTime-StartTime ))
		return Z, N, EndTime-StartTime

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
	Retrieve the maximum and minimum number of buffer necessary for the algorithm to work on every kernel
	"""
	@staticmethod
	def getBufferRange():
		allBufferRange = []
		for k in range(16):
			Y,Ry = SchedulingHandler.extractTiles('test_4_', k)
			Zmin = SchedulingHandler.MinNbBuffer(Ry)
			Zmax = SchedulingHandler.MaxBuffersNb(Ry)
			allBufferRange.append([Zmin, Zmax])
		return (np.amin(allBufferRange),np.amax(allBufferRange))

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
		return Zmin+1

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