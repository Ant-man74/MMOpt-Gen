



class FCGM:

	X = [] 			# Input tile list
	Y = []			# Output tile List
	Ry = []			# Incidence Matrix of which input tile are required for an output tile 
	alpha = 0		# Time for a prefetch
	beta = 0		# Time for a computation
	xForYDict = {}	# Dictionnary with { key = output tile number : item = list of input tile necessary}

	def __init__(self, X, Y, Ry, alpha, beta, Z):

		self.X = X
		self.Y = Y
		self.Ry = Ry
		self.alpha = alpha
		self.beta = beta
		self.xForYList = self.xForYList(self.Y, self.Ry)

	"""
	return a List of tuple with (Output tile nb Y, list of input tile necessary Ry[y]) sorted by output tile with least input tile
	"""
	def xForYList(self, Y, Ry):

		xForYList = []
		for j in range(len(Y)):
			xForYList.append((Y[j], Ry[j]))

		xForYList = sorted(xForYList, key = lambda x:len(list(x[1])), reverse=True)
		return xForYList
	
	"""
	Outputs of CGM: N,Z,Di,Bi,Sj,Ti,Uj,Delta (Outputs) Main loop
	"""
	def executeFCGM(self):
	
		dd = self.computeSequence()


		return 0, 0, 0

	def computeSequence(self):
		ySortedMostTile = [outputTile[0] for outputTile in self.xForYList]
		print(ySortedMostTile)
		NewY,GroupY = self.FindNewGroupY(self.Y, self.Ry, ySortedMostTile)
		print (NewY)
		print (GroupY)
		return ordoY

	"""
	Det NewY,GroupY: 
	"""
	def FindNewGroupY(self,Y,Ry,OrdoY):
	    DictGroupG0 = self.FindGroupG(Y, Ry, OrdoY, OrdoY[0])
	    NewY = [list(DictGroupG0.keys())[0]]
	    GroupY = [list(DictGroupG0.values())[0]]
	    print(DictGroupG0)
	    """
	    for j in range(1,len(OrdoY)):
	        
	        if OrdoY[j] not in NewY+reduce(lambda x, y:x+y, GroupY):#(OrdoY[j] not in NewY) and (OrdoY[j] not in reduce(lambda x,y:x+y,GroupY)):
	            DictGroupG = self.FindGroupG(Y, Ry, OrdoY, OrdoY[j])
	        else: continue
	        
	        NewY.append(list(DictGroupG.keys())[0])
	        GroupY.append(list(set(list(DictGroupG.values())[0])-set(reduce(lambda x, y:x+y, GroupY))))        
	   	"""
	    return NewY,GroupY

	"""
	Det DictGroupG: {y:GroupG}, où GroupG définit la liste de tuiles y' ds Y, où y'#y  & Ry' inclus= Ry """ 
	def FindGroupG(self,Y,Ry,OrdoY,y):
	    GroupG=[]
	    #OrdoY=filter(lambda j: j != y, OrdoY)#Ts!= y and 
	    for Ts in OrdoY:
	        if Ts!=y and set(Ry[Y.index(Ts)]).issubset(set(Ry[Y.index(y)])):
	            GroupG.append(Ts)
	        else:continue
	    DictGroupG={y:GroupG}
	    return DictGroupG


