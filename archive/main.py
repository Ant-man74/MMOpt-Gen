# -*- coding: utf-8 -*-
#programmer: Khadija
#date: December 2016
#name: Main()

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
import os
#from google.apputils import app

from NeededFcts import *
from ECM import *
from CGM import *




#=======================================================================================
#                                       Main()
#=======================================================================================
def Main():
        """ Output DATA """
        FileName= os.getcwd()+'/CGM_Solutions.txt'
        #FileName='C:\Users\hadjsalk\Desktop\ConstructivesHeuristics\ECM_Solutions.txt'
        FileRts=open(FileName, 'w')
        FileRts.write('Results CGM Heuristic on the MMOpt Benchmarks: \n \n')
        FileRts.write('N° ' +'\t |'+ 'lbN ' +'\t |'+ 'lbZ' +'\t |'+ 'lbDelta' +'\t |'+ 'N ' +'\t |'+ 'Z ' + 'Delta' +'\t |'+'\t |'+ 'CPU(s)' +'\t |'+ 'Gap(%)' + '\n \n')

        """ SOLVING BENCHMARKS """
        alpha=2
        beta=3
        for k in range(2):                
                StartTime=datetime.now()
                #Step1: Det Y,Ry,X à partir de fichier .txt        
                #Matrix0=open(os.getcwd()+'/Kernels/test_cameleon_{}.txt'.format(k),'r') #2 instances
                Matrix0=open(os.getcwd()+'/Kernels/test_4_{}.txt'.format(k),'r') #2 instances

                #Matrix0=open('C:\Users\hadjsalk\Desktop\ConstructivesHeuristics\Kernels\\test_fisheye_{}.txt'.format(k),'r') #3 instances
                #Matrix0=open('C:\Users\hadjsalk\Desktop\ConstructivesHeuristics\Kernels\\test_polaire_{}.txt'.format(k),'r') #3 instances  
                #Matrix0=open('C:\Users\hadjsalk\Desktop\ConstructivesHeuristics\Kernels\\test_fd_{}.txt'.format(k),'r') #2 instances
                #Matrix0=open('C:\Users\hadjsalk\Desktop\ConstructivesHeuristics\Kernels\\test_cameleon_{}.txt'.format(k),'r')#2 instances     
                List0=Matrix0.readlines()
                Matrix0.close()        
                Y=[]
                Ry=[]
                for List1 in List0:
                    Y.append(int(List1.split(':')[0])) 
                    Ry.append(map(int,List1.split(':')[1].replace('#',' ').replace(',',' ').split()))

                X=InputTile(Ry)        
                Xmin=RequiredTileNb(Ry)
                Xmax=BuffersNb(Ry)
                Z=BuffersNb(Ry)

                #Step2: Det All Bounds: lbZ, lbN & lbDelta
                #print " ------ Lower Bounds of 3-PSDPP: ------"
               # lbN,lbZ,lb1Delta,lb2Delta,lb3Delta,lbDelta,lbDelta1=LowerBounds(X,Y,Ry,alpha,beta)
                #print "0- Lower Bounds are (lbN,lbZ,lbDelta) with values = ", (lbN,lbZ,lbDelta)
                #print "0- New Lower Bounds in Delta are (lb3Delta,lbDelta1) with values = ", (lb3Delta,lbDelta1)

                #Step3: Apply Heuristic 1 - ECM
                #print " ------ Outputs Data of ECM: ------"
                Sj1,N1,Z1,Di1,Bi1,Ti1,Uj1,Delta1=ECM(X,Y,Ry,alpha,beta)
               # print "1- All Outputs-ECM are (N1,Z1,Delta1) with values = ", (N1,Z1,Delta1)

                #Step4: Apply Heuristic 2 -  CGM
               # print " ------ Outputs Data of CGM: ------"
               # Sj2,N2,Z2,Di2,Bi2,Ti2,Uj2,Delta2=CGM(X,Y,Ry,alpha,beta)
               # print "2- All Outputs-CGM are (N2,Z2,Delta2) with values = ", (N2,Z2,Delta2)

                #Step6: Det Ratio for each Heuristics: R1,R2 & R3a,R3b,R3c
                R1=float(Delta1)/float(lbDelta)
                R2=float(Delta2)/float(lbDelta)
                #print "Ratio of ECM's Potential is: %.2f " % R1
                #print "Ratio of CGM's Potential is: %.2f " %  R2  
                EndTime=datetime.now()
                #print('----- Duration of Execution -----:{} --- {} ===> {} '.format(StartTime, EndTime, EndTime-StartTime ))

                #--- Find Sol  
                elt1=lbN
                elt2=lbZ
                elt3=lbDelta
                elt4=N1
                elt5=Z1
                elt6=Delta1
                elt7=EndTime-StartTime
                elt8=R1

                FileRts.write(str(k) +'\t |'+ str(elt1) +'\t |'+ str(elt2) +'\t |'+ str(elt3) +'\t |'+ str(elt4) +'\t |'+ str(elt5) +'\t |'+ str(elt6) +'\t |'+ str(elt7) +'\t |'+ str(elt8) + '\n')
                #FileRts.write('\n'.join('Kernel N %d \t %.0f \t %.0f \t %.0f \t %.0f \t %.0f \t' % (k, elt1, elt2, elt3, elt4, elt5)  ))
        FileRts.close() 

	
	
#=======================================================================================
if __name__ == '__main__':
	Main()
 
