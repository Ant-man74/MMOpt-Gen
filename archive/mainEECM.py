# -*- coding: utf-8 -*-
#programmer: Khadija
#date: Decembre 2016
#name: EECM

"""
This model implements a constructive heuristic EECM for solving the 3-PSDPP problem: min N,Delta,Z
---> Optimization order is: min N ---> min Delta ---> min Z
--->  EECM <---> ECM + min Z 
"""



import numpy as np              
from scipy import *
import cProfile
import pstats
import math        
import random
import operator
from timeit import Timer 
from time import *
from datetime import datetime  
import pickle
import sys
#from google.apputils import app

from MMOptEECM import *


#=======================================================================================
#                                   TestEECM()
#=======================================================================================
def TestEECM(alpha,beta):       
    """ INPUTS/OUTPUTS """
    print " ------- Inputs Data of EECM: -------"
    (X,Y,Ry)=InputsData()
    #print "Input Tile (Te) List X = ", X
    #print "Output Tile (Ts) List Y = ", Y
    #print "Input/Output Tile Configurations = "
    #print Ry
    
    print " ------ Outputs Data of EECM: ------"
    Di,Bi,Ti,N,Z0,Z,Sj,Uj,Delta=EECM(X,Y,Ry,alpha,beta)     
##    print "Prefetch Sequence Di = ", Di
##    print "Total Number Of Prefetched Input Tiles N = ", N 
##    print "Start Date of Prefetch Scheduling Ti = ", Ti 
##    print "Buffers Number Z0 = ", Z0
##    print "Destination (Buffers) Sequence Bi = ", Bi 
##    print "Buffers Number Z = ", Z     
##    print "Computation Sequence Sj = ", Sj
##    print "Start Date of Computation Scheduling Uj = ", Uj
##    print "Total Compute Time = %d Unit of Time " %Delta 
    print "Buffers Number (Z0,Z)= ", (Z0,Z)
    print "1- All Ouptputs are (N,Z,Delta) with values = ", (N,Z,Delta)
    
    print " ------ Lower Bounds of 3-PSDPP: ------"
    lbN,lbZ,lb1Delta,lb2Delta,lb3Delta,lbDelta,lbDelta1=LowerBounds(X,Y,Ry,alpha,beta)
    print "2- Lower Bounds are (lbN,lbZ,lbDelta) with values = ", (lbN,lbZ,lbDelta)
    print "2- New Lower Bounds in Delta are (lb3Delta,lbDelta1) with values = ", (lb3Delta,lbDelta1)


   

#=======================================================================================
#                                       MAIN()
#=======================================================================================
if __name__ == '__main__':
    StartTime=datetime.now() 
    print " ------ Kernel N° 1 ------"# - TD,1988   
    TestEECM(alpha=2,beta=3)
    EndTime=datetime.now()
    print('----- Duration of Execution -----:{} --- {} ===> {} '.format(StartTime, EndTime, EndTime-StartTime ))



