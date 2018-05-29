
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

	def __init__(self, X, Y, Ry, alpha, beta, Z):

		self.X = X
		self.Y = Y
		self.Ry = Ry
		self.alpha = alpha
		self.beta = beta	
		self.xForYList = self.xForYList(self.Y, self.Ry)

		self.Z = 4
		self.geneForesigthMax = 10
		self.geneSelfKeeping = 5
		self.geneCoefAllUse = 1
		self.geneCoefNextUse = 1.5



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
	def executeFECM(self, varPercent):
		
		Di = self.mostCommonPrefetch(self.X, self.Ry)
		Ti = self.prefetchStartDate(Di)
		Sj = self.computeTile(self.Y, self.Ry, Di, Ti)

		inciMatrix = self.buildIncidenceMatrix(Di, self.Ry, Sj)
		
		#for t in RyMatrix:
		#	print (t)

		Bi, N = self.bufferAssignementSchedule(inciMatrix, Sj, self.xForYList)
		print (Bi)
		print (N)

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

						for i in range(0, len(assignedBuffer)):
							#search for all useless input tile that are in buffer and determine how many are we missing
							if assignedBuffer[i][1] not in tileToPrefetch:
								unnecessaryBuffer.append(assignedBuffer[i])
							else:
								alreadyPresent += 1
						
						necessarySpace = len(tileToPrefetch) - alreadyPresent
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

					print (freeBuffer)
					print (assignedBuffer)
					print (buffSequence)
					print ("---------------------")			
				pass
			pass

		return buffSequence, N


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
	"""
	def determineDiscardTile(self, currentY, unnecessaryBuffer, inciMatrix, necessarySpace):

		outputTileList = [outputTile[0] for outputTile in inciMatrix]
		allStatBuffer = []

		for i in range(0,len(unnecessaryBuffer)):
			
			tileRow = outputTileList.index(unnecessaryBuffer[i][1])
			stepUntilNextUse, amountOfTimeUsed = self.analyzeRow(inciMatrix[tileRow][1], self.geneForesigthMax, currentY)
			allStatBuffer.append( (unnecessaryBuffer[i], stepUntilNextUse, amountOfTimeUsed) )
			pass

		bufferToReplace = self.chooseReplacedBuffer(allStatBuffer, self.geneSelfKeeping, self.geneCoefNextUse, self.geneCoefAllUse, necessarySpace)
		return bufferToReplace

	"""
	Give statistic on the row for an input tile depending on the foresigth gene	
	"""
	def analyzeRow(self, inciMatrixRow, geneForesigthMax, currentY):

		stepUntilNextUse = 0
		amountOfTimeUsed = 0

		# GeneMaxForesigth is how far do we look in the matrix in advance (if there are 3000 output tile we don't want to consider them all)
		if currentY+geneForesigthMax > len(inciMatrixRow):
			iterLength = len(inciMatrixRow)
		else:
			iterLength = currentY+geneForesigthMax

		for i in range(currentY, iterLength):
			if inciMatrixRow[i] == 0 and amountOfTimeUsed == 0:
				stepUntilNextUse += 1
			elif inciMatrixRow[i] == 1:
				amountOfTimeUsed += 1
			pass

		return stepUntilNextUse, amountOfTimeUsed
	
	"""
	Choose depending on statistic and necessary spot to free which buffer to discard 
	allStatBuffer = [ ( (bufferNb,inputTileNb), stepUntilNextUse, amountOfTimeUsed), ... ]
	"""
	def chooseReplacedBuffer(self, allStatBuffer, geneSelfKeeping, geneCoefNextUse, geneCoefAllUse , necessarySpace):
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

			# if possible try to conserve the one within the margin
			for statBuffer in allStatBuffer:
				if statBuffer[1] <= geneSelfKeeping:
					allBufferFavored.append(statBuffer)
				else:
					allBufferCandidate.append(statBuffer)

				allBufferFavored = sorted(allBufferFavored, key = lambda x:x[1], reverse = True)
				pass

			# if after that step we still have enough replacement
			if len(allBufferCandidate) > necessarySpace:
				
				# sort by which buffer is used the soonest
				allBufferNextUse = sorted(allBufferCandidate, key = lambda x:x[1])	
				# sort by which buffer is most used		
				allBufferAllUse = sorted(allBufferCandidate, key = lambda x:x[2], reverse = True)
				allScore = []
				#grade all the replacement
				for i in range(0,len(allBufferCandidate)):
				
					index1 = allBufferNextUse.index(allBufferCandidate[i])
					index2 = allBufferAllUse.index(allBufferCandidate[i])

					scoreNextUse = ( index1 / len(allBufferNextUse) ) * allBufferNextUse
					scoreAllUse = ( index1 / len(allBufferAllUse) ) * geneCoefAllUse
					allScore.append( (allBufferCandidate[i], scoreAllUse + scoreNextUse) )
					pass
				
				allScore = sorted(allScore, key = lambda x:x[1])
				
				while allBufferCandidate < necessarySpace:
					allBufferCandidate.append(pop(allScore[0]))
					pass



			#if there isn't enough buffer just do it with the next member of favored until there is enough
			elif len(allBufferCandidate) < necessarySpace:

				while len(allBufferCandidate) < necessarySpace:
					#if there are more than two buffer to choose from
					if len(allBufferFavored) >= 2:
						#if they are both used at the same time
						if allBufferFavored[0][1] == allBufferFavored[1][1]:
							#pick the one that is used the least in total
							nextBuff = sorted( [allBufferFavored[0],allBufferFavored[1]], key = lambda x:x[2]) [0]
						else:
							nextBuff = allBufferFavored[0]
					else:
						nextBuff = allBufferFavored[0]
					#next buff is a buffer from favoredBuffer that The algo deemed unworthy and thus is put in the trash
					allBufferCandidate.append(nextBuff)
					allBufferFavored.remove(nextBuff)
					pass

			bufferToReplace = [statsBuffer[0] for statsBuffer in allBufferCandidate]

		return bufferToReplace