# -*- coding: utf-8 -*-
"""
    ToSP Kernels - Heuristics Test --- NeededFcts
"""


import numpy as np             
from scipy import *
import math        
import random
import logging
import operator 


#==================================== InputTile() ======================================
"""
Dét X: la liste des input tiles  <===> len(X)=lbN
"""
def InputTile(Ry):
    X=[]
    for i in range(len(Ry)):
        X.append(list(Ry[i]))
    X=reduce(lambda x,y:x+y, X)
    X=list(set(X))
    X.sort()
    return X

#==================================== BuffersNb() ======================================
"""
Dét Z: le nombre de buffers <===> Z=lbZ
"""
def BuffersNb(Ry):
    ListBuff=[]
    for i in range(len(Ry)):
        ListBuff.append(len(Ry[i]))
    Z=max(ListBuff)
    return Z

#================================== RequiredTileNb() ===================================
"""
Dét Xmin: le nombre Min. de Te requises  <===> 
"""
def RequiredTileNb(Ry):
    ListTile=[]
    for i in range(len(Ry)):
        ListTile.append(len(Ry[i]))
    Xmin=min(ListTile)
    return Xmin



#=================================== LowerBounds() =====================================
"""
Det # Lower Bounds lbN,lbZ, lb1Delta & lb2Delta
"""
def LowerBounds(X,Y,Ry,alpha,beta):
    lbN=len(X)
    lbZ=BuffersNb(Ry)
    #lb1Delta=(alpha*(len(X)-len(Omega)))+beta+1
    lb1Delta=(alpha*len(X))+beta+1
    lb2Delta=alpha+(beta*len(Y))+1
    lb3Delta=alpha*RequiredTileNb(Ry)+(beta*len(Y))+1
    lbDelta= max(lb1Delta,lb2Delta) 
    lbDelta1= max(lb1Delta,lb3Delta)     
    return lbN,lbZ,lb1Delta,lb2Delta,lb3Delta,lbDelta,lbDelta1




