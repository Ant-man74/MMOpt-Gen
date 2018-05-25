
import random
import numpy as np

"""
	Class in charge of the proccessing of the kernel
	
	Variable used in this problem
		Input :
  			-Y  	= 	Set of output tile to compute
			-Ry 	= 	Incidence matrix of required tile X to get tile Y		
			-X 		= 	List of input tile
			-alpha 	= 	Duration of a prefetch
			-beta 	= 	Duration of a computation
		Output :
			-Sj 	=	Which output tile to compute
			-Uj 	= 	At which time to compute Sj

			-Di 	= 	Which input tile to prefetch
			-Bi 	= 	In which buffer we put the input tile
			-Ti 	= 	At which time we prefetch the input tile
			
			-Z 		= 	Number of buffer for this execution
			-N 		= 	Number of prefetch
			-Delta  = 	Time taken to accomplish the task
"""


class FECM:

	X = [] 			# Input tile list
	Y = []			# Output tile List
	Z = None		# Number of buffer for this iteration
	Ry = []			# Incidence Matrix of which input tile are required for an output tile 
	alpha = 0		# Time for a prefetch
	beta = 0		# Time for a computation
	xForYList = []	# List with ( output tile number : list of input tile necessary )

	def __init__(self, X, Y, Ry, alpha, beta, Z):

		self.X = X
		self.Y = Y
		self.Z = Z
		self.Ry = Ry
		self.alpha = alpha
		self.beta = beta	
		self.xForYList = self.xForYList(self.Y, self.Ry)

	"""
	return a List of tuple with (Output tile nb Y, list of input tile necessary Ry[y]) sorted by output tile with least input tile
	"""
	def xForYList(self, Y, Ry):

		xForYList = []
		for i in range(len(Y)):
			xForYList.append((Y[i], Ry[i]))

		xForYList = sorted(xForYList, key = lambda x:len(list(x[1])), reverse=True)
		return xForYList

	"""
	Outputs of CGM: N,Z,Di,Bi,Sj,Ti,Uj,Delta (Outputs) Main loop
	"""
	def executeFECM(self, varPercent):
		
		Di = self.mostCommonPrefetch(self.X, self.Ry)
		Ti = self.prefetchStartDate(Di)
		Sj = self.computeTile(self.Y, self.Ry, Di, Ti)
		RyMatrix = self.buildIncidenceMatrix(Di,self.Ry,Sj)

		self.bufferOverdriveeee(RyMatrix)
		for t in RyMatrix:
			print (t)
		#Phase 2
		#Bi0 = self.computePrefetchSchedule(Di, self.Z, self.Y, varPercent)
		#Ti=self.PrefetchStartDate(Di,alpha)
		#Sj,Uj,Delta=ComputeTile(Y,Ry,Di,Ti,alpha,beta) 
		
		""" Phase 3: min Z (based on KTNS's Idea) """
		"""
		A=FindIncidenceMatrix(Di,Ti,Sj,Uj,Y,Ry,beta)
		Z=FindBufferNumber(A)
		Bi=reduce(lambda x,y:x+y,DestinationTile(A,Z))
	
		"""

		return 0, 0, 0

	"""
	List of the most commonly used input tile (sorted from most used to least used)
	""" 
	def mostCommonPrefetch(self, X, Ry):

		# List containing a tuple showing the number of time each input tile is used ( Input tile number, number of occurence in total )
		listX = []
		for i in range(len(X)):
			NbOccur = 0			
			for j in range(len(Ry)):
				NbOccur += list(Ry[j]).count(X[i])
			
			listX.append((X[i],NbOccur))

		listX = sorted(listX, key = lambda x: x[1], reverse=True)
		
		Di = [inputTileNb[0] for inputTileNb in listX]

		return Di

	"""
	Dét Ti: la sequence de Start Date correspondante à la liste Di
	""" 
	def prefetchStartDate(self, Di):
		
	    Ti=[1]
	    for i in range(1, len(Di)):
	        Ti.insert(i,Ti[i-1] + self.alpha)
	    return Ti
 
	"""
	Dét Sj  Computations Schedule
	"""
	def computeTile(self, Y, Ry, Di, Ti):

		listAllConfigTs = {}  

		# Determining the order in which the output tile should be processed
		for i in range(len(Y)):
			
			# Configuration of each output tile with the tuple (N° of Ts in Y, max([Ti[x], for x in Ry]) + alpha)
			listTsDate = []			
			for j in Ry[Y.index(Y[i])]:
				listTsDate.append(Ti[Di.index(j)])			

			listAllConfigTs.update( {Y[i]: max(listTsDate) + self.alpha} )
			
		listAllConfigTs = sorted(listAllConfigTs.items(), key = lambda x:x[1], reverse = False)
		
		ordoOpti = [outputTile[0] for outputTile in listAllConfigTs]
		
		return ordoOpti

	"""
	Build a 0, 1 incidence matrix for the input, output tile
	"""
	def buildIncidenceMatrix(self, Di, Ry, Sj = None):
		
		RyMatrix = []

		for i in range(len(Di)):
			RyMatrix.append( np.zeros(len(Ry)) )
			
			#change the disposition of the matrix if we have the optimal schedule
			if Sj is None:
				for j in range(len(Ry)):			
					if Di[i] in Ry[j]:
						RyMatrix[i][j] = 1
					pass
				pass
			else:
				for j in range(len(Ry)):			
					if Di[i] in Ry[ Sj[j] ]:
						RyMatrix[i][j] = 1
					pass
				pass

		return RyMatrix

	"""
	"""
	def bufferOverdriveeee(self, RyMatrix):
		print ("ok")
