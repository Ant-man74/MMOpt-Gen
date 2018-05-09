# -*- coding: utf-8 -*-
"""
ECM: Heuristic 1 for the MCT Problem
*** l'idée est de reprendre les 2 étapes de l'heuristique H1 pour le pb 3-PSDPP ***
"""

import numpy as np             
#from scipy import *
import math        
import random
import logging
import operator 

#=======================================================================================
#=======================================================================================
#=======================================================================================

#======================================= Phase 1 =======================================
"""
Phase1: Find Pi= (Di,Bi,Ti) (Prefetches Schedule)
    Step1: Calculer pour chaque Te de X son Nb_Occ
    Step2: Dét Di: X ds l'ordre decroissant d Nb_Occ (d_i)
    Step3: Dét Bi: Affecter aléatoirement à chaque Te 1 buffer parmi X' Buffers (b_i)
    Step4: Dét Ti: Dét pour chaque Te sa date de début de préchargement (t_i)
"""

#=======================================================================================
#                               Fonctions Principales
#=======================================================================================
"""
Outputs of ECM: X,Y,Ry (Inputs) & N,Z,Di,Bi,Sj,Ti,Uj,Delta (Outputs)
"""
def ECM(X,Y,Ry,alpha,beta,Z):
    Di, N=PrefetchTile(X,Ry)
    Bi=DestinationTile(Di,Z)
    Ti=PrefetchStartDate(Di,alpha)
    Sj,Uj,Delta=ComputeTile(Y,Ry,Di,Ti,alpha,beta)
    return Sj,Z,Di,Bi,Ti,Uj,Delta, N

#=======================================================================================
#=================================== PrefetchTile() ====================================
"""
Dét Di: la sequence de Prefetch correspondante à la liste de Te X de X'
""" 
def PrefetchTile(X,Ry):
    Di=[]  
    N = 0 
    """ 1:Dét le DictX """
    DictX=FindDictX(X,Ry)
    print(DictX)
    """ 2: Trier DicX ds Ordre Decroissant en fonct de DictX.Values() """
    ListDictX=sorted(DictX.items(),key=lambda x:x[1], reverse=True)
    for i in range(len(ListDictX)):
        N = N+1
        Di.insert(i,ListDictX[i][0])
    return Di, N
#====================================== FindDictX() ====================================
"""
Dét DictX: un Dictionnaire qui determine pour chaque Te de la liste X, le Nb d'occurence
% à chaque elt de Ry:
DictX= {DictTe0,DictTe1,...,DictTeX}, où
DictTe={key:value}, avec
    ---> key: N° Te
    ---> value: NbOccur
""" 
def FindDictX(X,Ry):
    DictX={}
    for i in range(len(X)):
        DictX.update(FindNbOccurTe(X,i,Ry))
    return DictX
#================================== FindNbOccurTe() ====================================
"""
Dét NbOcc: pour une Te de la liste X, le Nb d'occurence ds chaque elt de Ry
DictTe={key:value}, où
    ---> key: N° Te
    ---> value: NbOccur
""" 
def FindNbOccurTe(X,i,Ry):
    NbOccur=0
    for j in range(len(Ry)):
        NbOccur+=list(Ry[j]).count(X[i])
    return {X[i]:NbOccur}


#=======================================================================================
#================================ DestinationTile() ====================================
"""
Dét Bi: la sequence de Destination correspondante à la liste Di en utilisant un nbre de
buffers Z autant  X' (len(Di)
"""
def DestinationTile(Di,Z):
    Bi=[]
    ListBuff=list(range(Z))
    for i in range(len(Di)):
        NbBuff,ListBuff=AffectBuffer(Di,i,ListBuff)
        Bi.insert(i,NbBuff)  
    return Bi
#=================================== AffectBuffer() ====================================
"""
Dét le N° de Buffer (NbBuff) affecté aléatoirement à partir de la liste initiale
ListBuff à une Te i & MAJ de ListBuff (on supprime NbBuff de ListBuff) 
"""
def AffectBuffer(Di,i,ListBuff):
    NbBuff=random.choice(ListBuff)
    ListBuff.remove(NbBuff)
    return NbBuff,ListBuff


#=======================================================================================
#================================== PreftchStartDate() =================================
"""
Dét Ti: la sequence de Start Date correspondante à la liste Di
""" 
def PrefetchStartDate(Di,alpha):
    Ti=[1]
    for i in range(1,len(Di)):
        Ti.insert(i,Ti[i-1] + alpha)
    return Ti




#=======================================================================================
#=======================================================================================
#=======================================================================================



#=======================================================================================
#======================================= Phase 2 =======================================
#=======================================================================================
"""
Phase2: Find Sj, Uj & Delta (Computations Schedule)
    Step5: Dét Sj: Calculer chaque Ts dès que ses Te requises sont préchargées
               ---> Sj=Y ds ordre Croissant de max(Ti[Te requises])
    Step6: Dét Uj: dét pour chaque Ts sa date de début de calcul
               Uj[y]=max(Ti[Te requises])+alpha
               ---> Pas de chevauchement entre calculs: Uj[y+1] >= Uj[y]+beta
    Step7: Dét Delta: Total Completion Time ---> Delta=Uj[-1]+beta
"""

#=======================================================================================
#=============================== ComputeStartDateTile() ================================
"""
Dét Sj,Uj,Delta: Computations Schedule
"""
def ComputeTile(Y,Ry,Di,Ti,alpha,beta):
    Sj=[]
    Uj0=[]
    """ Dét Sj,Uj0 """
    DictAllConfigTs=FindAllConfigTs(Y,Ry,Di,Ti,alpha)
    ListAllConfigTs=sorted(DictAllConfigTs.items(),key=lambda x:x[1], reverse=False)
    for j in range(len(ListAllConfigTs)):
        Sj.insert(j,ListAllConfigTs[j][0])
        Uj0.insert(j,ListAllConfigTs[j][1])     
    """ Dét Uj, Delta"""
    Uj=[Uj0[0]]
    Uj=FindStartDateTs(Sj,Uj0,Uj,beta)    
    Delta=max(Uj) + beta #  Delta=Uj[-1] +beta
    return Sj,Uj,Delta
#=================================== FindAllConfigTs() =================================
"""
Dét DictAllConfigTs: la configuration de tte les Ts de la liste Y:
"""
def FindAllConfigTs(Y,Ry,Di,Ti,alpha):
    DictAllConfigTs={}  
    for j in range(len(Y)):
        ListTsDate,DictConfigTs=FindConfigTs(Y,Ry,Y[j],Di,Ti,alpha)
        DictAllConfigTs.update(DictConfigTs)
    return DictAllConfigTs
#=================================== FindConfigTs() ====================================
"""
Dét ListTsDate,DictConfigTs: la configuration de chaque Ts où
    - key = y   ---> N° of Ts in Y
    - Value= Uj0[y]  ---> max([Ti[x], for x in Ry]) + alpha
"""
def FindConfigTs(Y,Ry,y,Di,Ti,alpha):
    ListTsDate=[]
    for x in Ry[Y.index(y)]:
        ListTsDate.append(Ti[Di.index(x)])  
    DictConfigTs={y:max(ListTsDate, default=0)+alpha}
    return ListTsDate,DictConfigTs
#================================= FindStartDateTs() ===================================
"""
Dét StartDateList: pour tte les Ts ds Sc en garantissant pas de chevauchement entre calculs 
"""
def FindStartDateTs(Sj,Uj0,Uj,beta):    
    for j in range(1,len(Uj0)):
        if Uj0[j]-Uj[j-1] >= beta:
            Uj.insert(j,Uj0[j])
        else:
            Uj.insert(j,Uj[j-1]+beta)
    return Uj


#=======================================================================================
#=======================================================================================
#=======================================================================================




