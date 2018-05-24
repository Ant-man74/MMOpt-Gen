
import random

class FECM:

	X = [] 			# Input tile list
	Y = []			# Output tile List
	Z = None			# Number of buffer for this iteration
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
	
	"""
	Outputs of CGM: N,Z,Di,Bi,Sj,Ti,Uj,Delta (Outputs) Main loop
	"""
	def executeFECM(self):
		Di = self.mostCommonPrefetch(self.X, self.Ry) 		
		print(Di)
		#Phase 2
		Bi0 = self.destinationTile(Di,self.Z)
		#Ti=self.PrefetchStartDate(Di,alpha)
		#Sj,Uj,Delta=ComputeTile(Y,Ry,Di,Ti,alpha,beta) 
		
		""" Phase 3: min Z (based on KTNS's Idea) """
		"""
		A=FindIncidenceMatrix(Di,Ti,Sj,Uj,Y,Ry,beta)
		Z=FindBufferNumber(A)
		Bi=reduce(lambda x,y:x+y,DestinationTile(A,Z))
	
		"""

		return Sj, Uj, Di, Bi, Ti, Z, N, Delta

	"""
	List of the most commonly used input tile (sorted from most used to least used)
	""" 
	def mostCommonPrefetch(self, X, Ry):

		listX = self.findXOccurence(X, Ry)

		listX = sorted(listX, key = lambda x: x[1], reverse=True)
		Di = [inputTileNb[0] for inputTileNb in listX]

		return Di

	"""
	List containing a tuple showing the number of time each input tile is used ( Input tile number, number of occurence in total )
	""" 
	def findXOccurence(self, X, Ry):

		listX = []
		for i in range(len(X)):
			NbOccur = 0			
			for j in range(len(Ry)):
				NbOccur += list(Ry[j]).count(X[i])
			
			listX.append((X[i],NbOccur))
		
		return listX

	"""
	Dét Bi0: la sequence de Destination correspondante à la liste Di en utilisant un nbre de
	buffers Z autant le nbre de Prefetches X-|Omega|
	"""
	"""
	def destinationTile(self, Di, Z):
	    Bi0 = []
	    ListBuff = range(5)
	    for i in range(len(Di)):
	        NbBuff, ListBuff = self.affectBuffer(Di, i, ListBuff)
	        Bi0.insert(i,NbBuff)  
	    return Bi0

	
	Dét le N° de Buffer (NbBuff) affecté aléatoirement à partir de la liste initiale
	ListBuff à une Te i & MAJ de ListBuff (on supprime NbBuff de ListBuff) 
	"""
	"""
	def affectBuffer(self,Di,i,ListBuff):
	    NbBuff = random.choice(ListBuff)
	    ListBuff.remove(NbBuff)
	    return NbBuff,ListBuff

	"""