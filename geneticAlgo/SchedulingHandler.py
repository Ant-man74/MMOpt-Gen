
import numpy as np
import random
from datetime import datetime
import sys
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
	"""
	def executeSchedule(self,algo,config):

		StartTime=datetime.now()			

		#16 is the number of images to do (numer of file in /Kernel)
		for k in range(16):

			Y,Ry = SchedulingHandler.extractTiles('test_4_',k)
			X = SchedulingHandler.InputTile(Ry)
			
			if algo == "FECM":
			   fecm = FECM( X, Y, Ry, self.alpha, self.beta, config )  
			   Z, N, T = fecm.executeFECM(60)   

			sys.exit(0)
			

		EndTime = datetime.now()
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