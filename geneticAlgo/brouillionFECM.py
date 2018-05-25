	"""
	Dét Bi0: la sequence de Destination correspondante à la liste Di en utilisant un nbre de
	buffers Z autant le nbre de Prefetches X-|Omega|
	"""
	def computePrefetchSchedule(self, Di, Z, Y, varPercent):

		allBuffer = np.asarray(np.zeros(Z))		# List of buffer and their status, may be dropped latter status : 0 empty, 1 filled, 2 available	
		assignedBuffer = []						# Content of which buffer containing triplet (tileNb, time used for a computation, maxComputation count)
		Bi = []									# Schedule of prefetch and buffer operation
		outputTileToCompute = Y 				# List of output tile to compute
		outputTileComputed = [] 				# List of computed ouput tile as of yet

		# Determining how many buffer are available for permanent most common prefetch
		permanentBuffer = int(Z*(varPercent/100))


		# ToDo Move to a method these to loop
		# First round : fill all the buffer with the most common tiles
		for i in range(permanentBuffer):
			#if all input tile have already been prefetched (in permanent buffer) break
			if len(Di)-1 >= i:				
				allBuffer[i] = 1
				assignedBuffer.append( (Di[i][0], 0, Di[i][1]) )
				Bi.append(Di[i][0])
			else:
				break
			pass

		for j in range(permanentBuffer, Z):
			#if all input tile have already been prefetched (in rest of buffer) break
			if len(Di)-1 >= j:
				allBuffer[j] = 1
				assignedBuffer.append( (Di[j][0], 0, Di[j][1]) )
				Bi.append(Di[j][0])
			else:
				break
			pass

		assignedBuffer, outputTileToCompute, outputTileComputed = self.computeWithBuffer(assignedBuffer, outputTileToCompute, outputTileComputed)

		while len(outputTileToCompute) != 0:
			
			#remember their place in the list as it's the buffer number and calculate what percent of buffer they have treated
			tempBufferArranged = assignedBuffer
			for x in len(assignedBuffer)-1 :
				tempBufferArranged[x]  = (x, assignedBuffer[x], 100-((assignedBuffer[x][1]/assignedBuffer[x][2])*100))
			

			sorted(tempBufferArranged, key = lambda x:3, reverse=True)
			

			step


			assignedBuffer, outputTileToCompute, outputTileComputed = self.computeWithBuffer(assignedBuffer, outputTileToCompute, outputTileComputed)

			pass

		print (allBuffer)
		print ("_______________")
		print (assignedBuffer)
		return Bi0

	"""

	"""
	def computeWithBuffer(self, assignedBuffer, outputTileToCompute, outputTileComputed):
		
		inputTileNbInBuffer = [inputTile[0] for inputTile in assignedBuffer]

		for i in range(0,len(self.xForYList)):
			# If the current Ry can be computed with what's in the buffer
			if set(self.xForYList[i][1]).issubset(inputTileNbInBuffer)				
				
				#Increment the time used for competiotion count
				for j in range(len(self.xForYList[i][1])):					
					if self.xForYList[i][1][j] == inputTileNbInBuffer[j]:
						assignedBuffer[j][1] = assignedBuffer[j][1] + 1

				outputTileComputed.append(self.xForYList[i][0])
				outputTileToCompute.remove(self.xForYList[i][0])
			pass

		return assignedBuffer, outputTileToCompute, outputTileComputed
	
