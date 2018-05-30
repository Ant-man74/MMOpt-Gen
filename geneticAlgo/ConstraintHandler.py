
from .SchedulingHandler import SchedulingHandler

from .XmlHandler import XmlHandler


"""
Takes care of calculating the different range of the algorythm so that other part of the algorythm can work properly
"""
def ConstraintHandler:

	allY = []
	allRy = []

	def __init__ (self):
		
		for k in range(16):	
			Y, Ry = SchedulingHandler.extractTiles('test_4_', k)
			self.allY.append(Y)
			self.allRy.append(Ry)

		self.setBufferRange()
		self.setForesigthRange()
		self.setTileKeepingRange()


	def setForesigthRange(self):
		return 0


	def setTileKeepingRange(self):
		return 0	

	"""
	Retrieve the maximum and minimum number of buffer necessary for the algorithm to work on every kernel
	"""
	def setBufferRange(self):

		allBufferRange = []
		for i in range(16):
			
			Zmin = self.minNbBuffer(self.allRy[k])
			Zmax = self.maxBuffersNb(self.allRy[k])
			allBufferRange.append([Zmin, Zmax])
			pass

		minVal = 0

		for i in range(len(allBufferRange)-1) :

			if allBufferRange[i][0] > minVal:
				minVal = allBufferRange[i][0]
		
		XmlHandler.setItemIn("mmopt","bufferRange",[minVal, np.amax(allBufferRange)])

	"""
	Find Xmin: the minimum of required tile  <===> aka the minimum number of buffer required to compute this output tile
	"""
	@staticmethod
	def minNbBuffer(self, Ry):
		#ListTile = List of number of required tile for computing
		# --> the max number means the output tile which needs the most input tile to be computed
		# --> so the minimum number of buffer to have 
		ListTile = []		
		
		for i in range(len(Ry)):
			ListTile.append(len(Ry[i]))
		
		Zmin = max(ListTile)
		return Zmin

	"""
	Find Zmax: the maximum number of buffer for a set of tile equal to the number of total prefetch
			necessary if we think that we charge  each input tile once in the buffers (worst case scenario unacceptable number of buffer)
			for example we have 150 tile used to constitue a picture each output tile require no more than 5 input tile
			we decide to charge all of the 150 tile into a special buffer to compute everything now sure the number of prefetch will be low and time also will be low but 150 buffer is not cool
	"""
	@staticmethod
	def maxBuffersNb(self, Ry):

		valMax = 0
		allNeededTile = []

		for i in range(len(Ry)):
			for x in Ry[i]:
				if x not in allNeededTile:
					allNeededTile.append(x)
		
		Zmax = len(allNeededTile)

		return Zmax
