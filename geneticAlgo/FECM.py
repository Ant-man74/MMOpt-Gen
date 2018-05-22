
import random
import numpy as np
import sys

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

	def __init__(self, X, Y, Ry, alpha, beta, individual):
		self.X = X
		self.Y = Y
		self.Ry = Ry
		self.alpha = alpha
		self.beta = beta	
		self.xForYList = self.xForYList(self.Y, self.Ry)
		
		self.Z = individual[0]
		self.geneForesigthMax = individual[2]
		self.geneSelfKeeping = individual[3]
		self.geneCoefAllUse = individual[4]
		self.geneCoefNextUse = individual[5]


	"""
	return a List of tuple with (Output tile nb Y, list of input tile necessary Ry[y]) sorted by output tile nb
	"""
	def xForYList(self, Y, Ry):

		xForYList = []
		for i in range(len(Y)):
			xForYList.append((Y[i], Ry[i]))

		xForYList = sorted(xForYList, key = lambda x:x[0])
		return xForYList

	
	"""
	Outputs of CGM: N,Z,Di,Bi,Sj,Ti,Uj,Delta (Outputs) Main loop
	"""
	def executeFECM(self):
		
		Di = self.mostCommonPrefetch(self.X, self.Ry)
		Ti = self.prefetchStartDate(Di)
		Sj = self.computeTile(self.Y, self.Ry, Di, Ti)
		inciMatrix = self.buildIncidenceMatrix(Di, self.Ry, Sj)		
		Bi, N, Uj0 = self.bufferAssignementSchedule(inciMatrix, Sj, self.xForYList)		
		Uj = self.findStartDateTs(Uj0, self.beta)
		delta = max(Uj) + self.beta

		return self.Z, N, delta

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
	Dét Sj  Computations Schedule old code I'm not 100% sure
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

		inciMatrix = []
		for i in range(len(Di)):

			inciMatrix.append( (Di[i],np.zeros(len(Ry))) )
			
			#change the disposition of the matrix if we have the optimal schedule
			if Sj is None:
				for j in range(len(Ry)):			
					if Di[i] in Ry[j]:
						inciMatrix[i][1][j] = 1
					pass
				pass
			else:
				for j in range(len(Ry)):
					# (Sj[i] == the number of the output tile			
					if Di[i] in Ry[ Sj[j] ]:
						inciMatrix[i][1][j] = 1
					pass
				pass

		return inciMatrix

	"""
	Determine the schedule of prefetch for buffer management, return a list of tuple (operation, bufferNb, inputTileNb)
	"""
	def bufferAssignementSchedule(self, inciMatrix, Sj, xForYList):

		freeBuffer = list(range(self.Z)) 		# list of all free buffer 
		assignedBuffer = []						# assigned buffer, list of tuple (bufferNb, inputTileNb)
		buffSequence = [] 						# all buffer operation, list of tuple (add/minus, bufferNb, inputTileNb)	
		N = 0									# the total number of preftch
		Uj0 = []								#the time at which each output tile can be computed at the earliest
		test =[]
		# for each output tile to load
		for i in range(0,len(self.Y)):

			# array of the input tile necessary for this row (Sj[i] == the number of the output tile we want the input tile of)
			tileToPrefetch = xForYList[ Sj[i] ][1]

			#for each tile to prefetch
			for j in range(0,len(tileToPrefetch)):
				
				isIn = self.checkPresenceInBuffer(assignedBuffer, tileToPrefetch[j])
				
				if isIn == False:
					
					# if all the buffer are occupied
					if len(assignedBuffer) >= self.Z:
						
						# determine which buffer can be overwritten and how many we will need to free
						unnecessaryBuffer = []			
						alreadyPresent = 0
						
						#search for all useless input tile that are in buffer and 
						for k in range(0, len(assignedBuffer)):

							# determine how many are we missing and which one are useless
							if assignedBuffer[k][1] not in tileToPrefetch:
								unnecessaryBuffer.append(assignedBuffer[k])
							else:
								alreadyPresent += 1
							pass
						
						necessarySpace = len(tileToPrefetch) - alreadyPresent
						#decide which tile to discard
						bufferToReplace = self.determineDiscardTile(i, unnecessaryBuffer, inciMatrix, necessarySpace)
						
						for discardedBuffer in bufferToReplace:
							assignedBuffer.remove(discardedBuffer)
							freeBuffer.append(discardedBuffer[0])
							buffSequence.append( ("minus", discardedBuffer[0], discardedBuffer[1]) )
							pass

					#finnaly assign the buffers
					bufferToAssign = random.choice(freeBuffer)
					freeBuffer.remove(bufferToAssign)
					assignedBuffer.append( (bufferToAssign, tileToPrefetch[j]) )
					buffSequence.append( ("add", bufferToAssign, tileToPrefetch[j]) )
					N += 1
				pass

			Uj0.append( self.prefetchComputationStartDate(Uj0, N, self.alpha) )
			pass

		return buffSequence, N, Uj0


	"""
	Check if an input tile is already present in the buffers
	"""
	def checkPresenceInBuffer(self, assignedBuffer, inputTile):
		ret = 0
		# List of input tile in buffer
		tileInBuffers = [tileNb[1] for tileNb in assignedBuffer]

		if inputTile in tileInBuffers:
			ret = 1
		else:
			ret = 0

		return ret

	"""
	Function that determine which buffer can be replaced depending on how many spots are needed
	return a list of triplet (buffer, stepUntilNextUse, amountOfTimeUsed)
	"""
	def determineDiscardTile(self, currentY, unnecessaryBuffer, inciMatrix, necessarySpace):

		outputTileList = [outputTile[0] for outputTile in inciMatrix]
		allStatBuffer = []

		for i in range(0,len(unnecessaryBuffer)):
			
			tileRow = outputTileList.index(unnecessaryBuffer[i][1])
			stepUntilNextUse, amountOfTimeUsed = self.analyzeRow(inciMatrix[tileRow][1], currentY)
			allStatBuffer.append( (unnecessaryBuffer[i], stepUntilNextUse, amountOfTimeUsed) )
			pass

		bufferToReplace = self.chooseReplacedBuffer(allStatBuffer, necessarySpace)
		return bufferToReplace

	"""
	Give statistic on the row for an input tile depending on the foresigth gene	
	"""
	def analyzeRow(self, inciMatrixRow, currentY):

		stepUntilNextUse = 0
		amountOfTimeUsed = 0

		# GeneMaxForesigth is how far do we look in the matrix in advance (if there are 3000 output tile we don't want to consider them all)
		if currentY + self.geneForesigthMax > len(inciMatrixRow):
			iterLength = len(inciMatrixRow)
		else:
			iterLength = currentY + self.geneForesigthMax

		for i in range(currentY, iterLength):
			if inciMatrixRow[i] == 0 and amountOfTimeUsed == 0:
				stepUntilNextUse += 1
			elif inciMatrixRow[i] == 1:
				amountOfTimeUsed += 1
			pass

		return stepUntilNextUse, amountOfTimeUsed
	
	"""
	Choose depending on statistic and necessary spot to free which buffer to discard 
	Use the genes: geneSelfKeeping, geneCoefNextUse, geneCoefAllUse
	allStatBuffer = [ ( (bufferNb,inputTileNb), stepUntilNextUse, amountOfTimeUsed), ... ]
	"""
	def chooseReplacedBuffer(self, allStatBuffer, necessarySpace):
		
		# Array of buffer Id that will be used to prefetch needed tile
		bufferToReplace = []
		# if we need more space than there are buffer available for replacement 
		if necessarySpace > len(allStatBuffer):
			print ("NameError: Out of buffer")	#to chnage to an exception later
		
		# if we have just the rigth amount of buffer we can replace
		elif necessarySpace == len(allStatBuffer):
			bufferToReplace = [statsBuffer[0] for statsBuffer in allStatBuffer]
		
		#if we have more buffer than can be replaced than necessary get the best one to replace
		else:
			
			allBufferFavored = []
			allBufferCandidate = []

			# Sort the buffers depending on gene if possible try to conserve the one within the margin
			for statBuffer in allStatBuffer:
				if statBuffer[1] <= self.geneSelfKeeping:
					allBufferFavored.append(statBuffer)
				else:
					allBufferCandidate.append(statBuffer)

				allBufferFavored = sorted(allBufferFavored, key = lambda x:x[1], reverse = True)
				pass

			# if after that step we have too much replacement, choose the best one
			if len(allBufferCandidate) > necessarySpace:

				allScore = self.gradeBuffer(allBufferCandidate)				

				while len(bufferToReplace) < necessarySpace:
					bufferToReplace.append(allScore.pop(0))
					pass


			#if there isn't enough buffer take buffer from the favored one
			elif len(allBufferCandidate) < necessarySpace:
				
				bufferToReplace = [statsBuffer[0] for statsBuffer in allBufferCandidate]
				
				allScoreFav = self.gradeBuffer(allBufferFavored)	
				
				while len(bufferToReplace) < necessarySpace:
					bufferToReplace.append(allScoreFav.pop(0))
					pass

			#else we had just enough extra buffer
			else:
				bufferToReplace = [statsBuffer[0] for statsBuffer in allBufferCandidate]

		return bufferToReplace

	"""
	Grade the buffer given in entry depending on the genes criteria
	Use the genes: geneCoefNextUse, geneCoefAllUse
	return a list of tuple (buffer, nbInputTile)
	"""
	def gradeBuffer(self, allBuffer):
		
		# sort by which buffer is used the soonest
		allBufferNextUse = sorted(allBuffer, key = lambda x:x[1])	
		# sort by which buffer is most used		
		allBufferAllUse = sorted(allBuffer, key = lambda x:x[2], reverse = True)
		allScore = []
		#grade all the Buffer
		for i in range(0,len(allBuffer)):
		
			index1 = allBufferNextUse.index(allBuffer[i])
			index2 = allBufferAllUse.index(allBuffer[i])
			scoreNextUse = ( index1 / len(allBufferNextUse) ) * self.geneCoefNextUse
			scoreAllUse = ( index1 / len(allBufferAllUse) ) * self.geneCoefAllUse
			allScore.append( (allBuffer[i], scoreAllUse + scoreNextUse) )
			pass
		
		allScore = sorted(allScore, key = lambda x:x[1])
		allBufferByScore = [statsBuffer[0][0] for statsBuffer in allScore]
		
		return allBufferByScore

	"""
	Dét Ti: Start date sequence for Bi, unused for the moment
	""" 
	def prefetchStartDatePostReassign(self, Bi, alpha):
		
		Ti = [1]
		decalage = 0
		
		for i in range(1, len(Bi)):

			if Bi[i-1][0] != "minus":
				Ti.insert(i,Ti[i-decalage-1] + alpha)
			else:
				decalage += 1		

		return Ti

	"""
	Dét timeForCompute: Time where a sequence of prefetch has finished and a computation could be done
	""" 
	def prefetchComputationStartDate(self, Uj0, N, alpha):
		
		if len(Uj0) != 0:
			timeForCompute = Uj0[len(Uj0)-1]
		else:
			timeForCompute = 0
		
		for i in range(len(Uj0), N):
			timeForCompute += alpha

		return timeForCompute


	"""
	Dét StartDateList: pour tte les Ts ds Sc en garantissant pas de chevauchement entre calculs 
	"""
	def findStartDateTs(Sj, Uj0, beta):
		#first tile that can be computed
		Uj=[Uj0[0]]   
		
		#for each computation
		for j in range(1,len(Uj0)):

			# if the computation can be done without overlap add them to the array of the computation timing
			if Uj0[j]-Uj[j-1] >= beta:
				Uj.insert(j,Uj0[j])
			# if there is an overlap add a delay of computation to the previous step
			else:
				Uj.insert(j,Uj[j-1]+beta)
		return Uj


