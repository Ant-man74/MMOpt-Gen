
import numpy as np
#from scipy import *
import cProfile
import pstats
import math
import random
import operator
from timeit import Timer 
from time import *
from datetime import datetime
import pickle
import sys
#from google.apputils import app

#from NeededFcts import *
from ECM import *
from XmlHandler import XmlHandler

class SchedulingHandler:

	alpha = 2
	beta = 3
	
	def __init__(self):
		self.initParam()

	"""
	Retrieve parameters for the execution of the ECM and CGM algorithm
	"""
	def initParam(self):
		xmlHandler = XmlHandler()
		self.alpha = int(xmlHandler.getItemFrom("mmopt","alpha"))
		self.beta = int(xmlHandler.getItemFrom("mmopt","beta"))

	"""
	Execute the ECM algorythm according to the parameters
	"""
	def executeECM(self,nbBuff):
		StartTime=datetime.now()
		#16 is the number of images to do (numer of file in /Kernel)
		for k in range(16):
			
			Y,Ry = SchedulingHandler.extractTiles('test_4_',k)	
			Xmin = SchedulingHandler.RequiredTileNb(Ry)
			Xmax = SchedulingHandler.BuffersNb(Ry)
			X = SchedulingHandler.InputTile(Ry)
			Z = SchedulingHandler.BuffersNb(Ry)
			
			#Step2: Det All Bounds: lbZ, lbN & lbDelta
			#print " ------ Lower Bounds of 3-PSDPP: ------"
			lbN,lbZ,lb1Delta,lb2Delta,lb3Delta,lbDelta,lbDelta1 = SchedulingHandler.LowerBounds(X,Y,Ry,self.alpha,self.beta)
			# print "0- Lower Bounds are (lbN,lbZ,lbDelta) with values = ", (lbN,lbZ,lbDelta)
			#print "0- New Lower Bounds in Delta are (lb3Delta,lbDelta1) with values = ", (lb3Delta,lbDelta1)

			#Step3: Apply Heuristic 1 - ECM
			#print " ------ Outputs Data of ECM: ------"
			
	#	Sj1,N1,Z1,Di1,Bi1,Ti1,Uj1,Delta1=ECM(X,Y,Ry,self.alpha,self.beta,nbBuff)
			
			#print "1- All Outputs-ECM are (N1,Z1,Delta1) with values = ", (N1,Z1,Delta1)
			#Step0: Det DeltaMCT
			
			DeltaMCT=[34,35,38,53,53,69,71,70,60,60,60,90,90,120,120,150]
			
			#Step6: Det Ratio for ECM heuristic
			
	#	R1=float(Delta1)/float(DeltaMCT[k])
			
			#print "Ratio of ECM's Potential is: %.2f " % R1

		EndTime = datetime.now()
		#print('----- Duration of Execution -----:{} --- {} ===> {} '.format(StartTime, EndTime, EndTime-StartTime ))

		return nbBuff, 5, EndTime-StartTime

	"""
	Execute the CGM algorythm according to the parameters
	"""
	def executeCGM(self,nbBuff):
		StartTime=datetime.now()
		#16 is the number of images to do (numer of file in /Kernel)
		for k in range(16):
			
			Y,Ry = SchedulingHandler.extractTiles('test_4_',k)	
			Xmin = SchedulingHandler.RequiredTileNb(Ry)
			Xmax = SchedulingHandler.BuffersNb(Ry)
			X = SchedulingHandler.InputTile(Ry)
			Z = SchedulingHandler.BuffersNb(Ry)
			
			#Step2: Det All Bounds: lbZ, lbN & lbDelta
			#print " ------ Lower Bounds of 3-PSDPP: ------"
			lbN,lbZ,lb1Delta,lb2Delta,lb3Delta,lbDelta,lbDelta1 = SchedulingHandler.LowerBounds(X,Y,Ry,self.alpha,self.beta)
			# print "0- Lower Bounds are (lbN,lbZ,lbDelta) with values = ", (lbN,lbZ,lbDelta)
			#print "0- New Lower Bounds in Delta are (lb3Delta,lbDelta1) with values = ", (lb3Delta,lbDelta1)

			#Step3: Apply Heuristic 1 - CGM
			#print " ------ Outputs Data of CGM: ------"
			
	#	Sj1,N1,Z1,Di1,Bi1,Ti1,Uj1,Delta1=CGM(X,Y,Ry,self.alpha,self.beta,nbBuff)
			
			#print "1- All Outputs-CGM are (N1,Z1,Delta1) with values = ", (N1,Z1,Delta1)
			#Step0: Det DeltaMCT
			
			DeltaMCT=[34,35,38,53,53,69,71,70,60,60,60,90,90,120,120,150]
			
			#Step6: Det Ratio for CGM heuristic
			
	#	R1=float(Delta1)/float(DeltaMCT[k])
			
			#print "Ratio of CGM's Potential is: %.2f " % R1

		EndTime=datetime.now()
		#print('----- Duration of Execution -----:{} --- {} ===> {} '.format(StartTime, EndTime, EndTime-StartTime ))

		return nbBuff, 5, EndTime-StartTime

	"""
	Extract the data from the file "filename" for the "k" file
	"""
	@staticmethod
	def extractTiles(filename, k):
		#Step1: Det Y,Ry,X à partir de test_4_k.txt	
		Matrix0=open('Kernels/'+filename+'{}.txt'.format(k),'r')     
		List0=Matrix0.readlines()
		Matrix0.close()
		#the number of the output tile
		Y=[]
		Ry=[] 
		for List1 in List0:
			Y.append(int(List1.split(':')[0]))
			Ry.append(map(int,List1.split(':')[1].replace('#',' ').replace(',',' ').split()))
		return (Y,Ry)

	"""
	Retrieve the maximum and minimum number of buffer necessary for the algorithm to work on every kernel
	"""
	@staticmethod
	def getBufferRange():
		allBufferRange = []
		for k in range(16):
			Y,Ry = SchedulingHandler.extractTiles('test_4_',k)
			Xmin = SchedulingHandler.RequiredTileNb(Ry)
			Xmax = SchedulingHandler.BuffersNb(Ry)
			allBufferRange.append([Xmin,Xmax])
		return (np.amin(allBufferRange),np.amax(allBufferRange))

	"""
	Find X: the input tile list  <===> len(X)=lbN
	"""
	@staticmethod
	def InputTile(Ry):
		X=[]
		for i in range(len(Ry)):
				X.append(list(Ry[i]))
		X=SchedulingHandler.reduce(lambda x,y:x+y, X)
		X=list(set(X))
		X.sort()
		return X

	"""
	Find Z: the number of buffer <===> Z=lbZ
	"""
	@staticmethod
	def BuffersNb(Ry):
		ListBuff=[]
		for i in range(len(Ry)):
			ListBuff.append(len(list(Ry[i])))
		Z=max(ListBuff)
		return Z

	"""
	Find Xmin: the minimum of required tile  <===> 
	"""
	@staticmethod
	def RequiredTileNb(Ry):
		ListTile=[]
		for i in range(len(Ry)):
			ListTile.append(len(list(Ry[i])))
		Xmin=min(ListTile)
		return Xmin

	"""
	Det # Lower Bounds lbN,lbZ, lb1Delta & lb2Delta
	"""
	@staticmethod
	def LowerBounds(X,Y,Ry,alpha,beta):
		lbN=len(X)
		lbZ=SchedulingHandler.BuffersNb(Ry)
		lb1Delta=(alpha)*len(X)+beta+1
		lb2Delta=alpha+(beta*len(Y))+1
		lb3Delta=alpha*SchedulingHandler.RequiredTileNb(Ry)+(beta*len(Y))+1
		lbDelta= max(lb1Delta,lb2Delta) 
		lbDelta1= max(lb1Delta,lb3Delta)	
		return lbN,lbZ,lb1Delta,lb2Delta,lb3Delta,lbDelta,lbDelta1

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