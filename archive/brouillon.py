#X input tile

#Y output tile
Y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#Ry necessary input tile to compute Y
Ry = [[6, 0],
	  [2, 5],
	  [0, 4, 1, 7],
	  [0, 8, 3],
	  [1, 5, 8, 6],
	  [5, 4],
	  [7, 3, 6, 5],
	  [7, 4, 2],
	  [6, 4],
	  [1, 0, 8]]

#ComputeTile²
	
	ListDictTile1 = [(2, [0, 4, 1, 7]),
	 (4, [1, 5, 8, 6]),
	 (6, [7, 3, 6, 5]),
	 (3, [0, 8, 3]),
	 (7, [7, 4, 2]),
	 (9, [1, 0, 8]),
	 (0, [6, 0]),
	 (1, [2, 5]),
	 (5, [5, 4]),
	 (8, [6, 4])]

	#sort decroissant des output tile suivant le plus de input tile nécaissaire
	OrdoY = [2, 4, 6, 3, 7, 9, 0, 1, 5, 8]
	
	matrix = np.zeros((len(Ry),len(Sj)))
	inciMatrix = []
	for j in range(len(Sj)):
		for	inputTile in self.xForYList[allYForIndex.index(Sj[j])][1]:
			
			pass

	 5  0  8  2  4  9  1  7  3  4

0	[0. 1. 0. 1. 0. 1. 0. 0. 1. 0.]
4	[1. 0. 1. 1. 0. 0. 0. 1. 0. 0.]
5	[1. 0. 0. 0. 1. 0. 1. 0. 0. 1.]
6	[0. 1. 1. 0. 1. 0. 0. 0. 0. 1.]
1	[0. 0. 0. 1. 1. 1. 0. 0. 0. 0.]
7	[0. 0. 0. 1. 0. 0. 0. 1. 0. 1.]
8	[0. 0. 0. 0. 1. 1. 0. 0. 1. 0.]
2	[0. 0. 0. 0. 0. 0. 1. 1. 0. 0.]
3	[0. 0. 0. 0. 0. 0. 0. 0. 1. 1.]


