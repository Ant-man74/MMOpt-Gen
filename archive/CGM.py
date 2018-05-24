# -*- coding: utf-8 -*-
#programmer: Khadija
#date: December 2016
#name: CGM Algorithm 
"""
CGM: Heuristic 2 for the MCT Problem
*** l'idée est d'améliorer l'algo CGM en appliquant "Shifting Prefetches" si nécessaire  ***
"""


import numpy as np             
from scipy import *
import math        
import random
import logging
import operator 



#=======================================================================================
#=======================================================================================
#=======================================================================================


#======================================= Phase 1 =======================================
"""
Phase1: Find Sj0
     Step1: Find NewY & NewRy <---> ordonner Y ds l'ordre décroissant en fct [Ry|
     Step2: Find GroupG for each y in NewY <---> GroupG(y)=[y'#y & Ry' inclus= Ry]
     Step3:
"""

#=======================================================================================
#================================== ComputeSequence0() =================================
def ComputeSequence0(Y,Ry):
    OrdoY=ComputeTile1(Y,Ry)
    NewY,GroupY=FindNewGroupY(Y,Ry,OrdoY)
    Sj0,GroupSj0=ComputeTile2(Y,Ry,NewY,GroupY)
    Sj0Ry=FindConfigSj0(Y,Ry,Sj0)
    return Sj0,Sj0Ry,GroupSj0


#=======================================================================================
#==================================== ComputeTile1() ===================================
"""
Det OrdoY: Y ordonnée ds l'ordre décroissant en fct |Ry|
""" 
def ComputeTile1(Y,Ry):
    DictTile1=FindDictTile1(Y,Ry)
    OrdoY=[]
    ListDictTile1=sorted(DictTile1.items(),key=lambda x:len(x[1]),reverse=True)
    for j in xrange(len(ListDictTile1)):
        OrdoY.insert(j,ListDictTile1[j][0])
    return OrdoY
#=================================== FindDictTile1() ===================================
"""
Det DictTile1: un dictionnaire a partir de 2 listes as inputs
""" 
def FindDictTile1(Y,Ry):
    DictTile1={}
    for j in xrange(len(Y)):
        DictTile1.update({Y[j]:Ry[j]})
    return DictTile1


#=======================================================================================
#============================ FindNewGroupY(Y,Ry,OrdoY) ================================
"""
Det NewY,GroupY: 
"""
def FindNewGroupY(Y,Ry,OrdoY):
    DictGroupG0=FindGroupG(Y,Ry,OrdoY,OrdoY[0])
    print(DictGroupG0)
    print("__________________________________")
    NewY=[DictGroupG0.keys()[0]]
    GroupY=[DictGroupG0.values()[0]]
    for j in xrange(1,len(OrdoY)):
        if OrdoY[j] not in NewY+reduce(lambda x,y:x+y,GroupY):#(OrdoY[j] not in NewY) and (OrdoY[j] not in reduce(lambda x,y:x+y,GroupY)):
            DictGroupG=FindGroupG(Y,Ry,OrdoY,OrdoY[j])
        else: continue
        NewY.append(DictGroupG.keys()[0])
        GroupY.append(list(set(DictGroupG.values()[0])-set(reduce(lambda x,y:x+y,GroupY))))        
    return NewY,GroupY
#===================================== FindGroupG() ====================================
"""
Det DictGroupG: {y:GroupG}, où GroupG définit la liste de tuiles y' ds Y, où y'#y  & Ry' inclus= Ry """ 
def FindGroupG(Y,Ry,OrdoY,y):
    GroupG=[]
    #OrdoY=filter(lambda j: j != y, OrdoY)#Ts!= y and 
    for Ts in OrdoY:
        if Ts!=y and set(Ry[Y.index(Ts)]).issubset(set(Ry[Y.index(y)])):
            GroupG.append(Ts)
        else:continue
    DictGroupG={y:GroupG}
    return DictGroupG


#=======================================================================================
#==================================== ComputeTile2() ===================================
"""
Det Sj0: NewY ordonnée ds l'ordre croissant en fct |Ry|
""" 
def ComputeTile2(Y,Ry,NewY,GroupY):
    DictTile2=FindDictTile2(Y,Ry,NewY)
    Sj0=[]
    GroupSj0=[]
    ListDictTile2=sorted(DictTile2.items(),key=lambda x:len(x[1]),reverse=False)
    for j in xrange(len(ListDictTile2)):
        Sj0.insert(j,ListDictTile2[j][0])
    for y in Sj0:
        GroupSj0.append(GroupY[NewY.index(y)])
    return Sj0,GroupSj0
#==================================== FindDictTile2() ==================================
"""
Det DictTile2: un dictionnaire de configuration de la liste NewY a partir de Y et Ry 
""" 
def FindDictTile2(Y,Ry,NewY): 
    DictTile2={}
    for a in NewY:
        DictTile2.update({a:Ry[Y.index(a)]})
    return DictTile2


#=======================================================================================
#==================================== FindConfigSj0() ==================================
"""
Det Sj0Ry: Ry de chaque Ts ds Sj0
""" 
def FindConfigSj0(Y,Ry,Sj0):
    Sj0Ry=[]
    for y in Sj0:
        Sj0Ry.append(Ry[Y.index(y)])
    return Sj0Ry





#=======================================================================================
#======================================= Phase 2 =======================================
#=======================================================================================
"""
Phase3: Find Di, Bi , Tj, Uj & Delta
     Step1: Find Di <---> liste de Prefetches correspondante à la liste Sj0
     Step2: Find Bi <---> Affecter a chaque Prefetch step un buffer #
"""

#=======================================================================================
#==================================== PrefetchTile() ===================================
"""
Det Di: la sequence de Préchargements correspondante à la liste de Ts Sj0
"""
def PrefetchTile(Sj0,Sj0Ry,Di):
    for j in xrange(1,len(Sj0)):
        Di.insert(j,NextPrefetch(Sj0,Sj0Ry,Di,Sj0[j]))
    return Di
#==================================== NextPrefetch() ===================================
"""
Det NextTile: la liste de Te x a précharger pour la 1 ère fois en // du calcul d Ts y 
""" 
def NextPrefetch(Sj0,Sj0Ry,Di,y):
    NextTile=[]
    for x in Sj0Ry[Sj0.index(y)]:
        if x in reduce(lambda x,y:x+y,Di):
            continue
        else:
            NextTile.append(x)            
    return NextTile

#=======================================================================================
#================================= DestinationTile() ===================================
"""
Det Bi: la sequence de Destination correspondante à la liste Di en utilisant la liste
de buffers Z de BuffersNb elements
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
Det NbBuff,ListBuff: le N° de Buffer (NbBuff) affecté aléatoirement à partir de la liste initiale
ListBuff à une Te i & MAJ de ListBuff (on supprime NbBuff de ListBuff) 
"""
def AffectBuffer(Di,i,ListBuff):
    NbBuff=random.choice(ListBuff)
    ListBuff.remove(NbBuff)
    return NbBuff,ListBuff




#=======================================================================================
#======================================= Phase 3 =======================================
#=======================================================================================
"""
Phase3: Find Sj, Tj, Uj & Delta
     Step1: Find Sj <---> integrer ds Sj0 le GroupG correspondant a chaque tuile y
     Step2: Find Tj, Uj & Delta
"""

#=======================================================================================
#=================================== ComputeSequence() =================================
"""
Det Sj: la sequence de calculs concatenant les ts ds Sj0 et celles ds Sj0GroupG
""" 
def ComputeSequence(Y,Ry,Sj0,Sj0Ry,GroupSj0):
    Sj=[]
    for j in xrange(len(Sj0)):
        Sj.extend([Sj0[j]]+GroupSj0[j])
    return Sj


#=======================================================================================
#==================================== StartDateTile0() =================================
"""
Det Ti1,Uj1,Delta1 (together)
"""
def StartDateTile0(Y,Ry,Di0,alpha,beta,Sj0,GroupSj0):
    Uj0=StartDateSj0(Di0,Sj0,GroupSj0,alpha,beta)
    Uj1=ComputeStartDate(Di0,Sj0,GroupSj0,alpha,beta)
    Ti1=PrefetchStartDate(Di0,Uj0,alpha,beta)
    Delta1=Uj1[-1]+beta
    return Ti1,Uj1,Delta1


#=======================================================================================
#================================= ComputeStartDate() ==================================
"""
Det Uj1: la sequence de StartDate correspondante à la liste Sj
""" 
def ComputeStartDate(Di0,Sj0,GroupSj0,alpha,beta):
    Uj0=StartDateSj0(Di0,Sj0,GroupSj0,alpha,beta)
    Uj0Group=StartDateGroupSj0(Sj0,GroupSj0,alpha,beta,Uj0)
    Uj1=[]
    for j in xrange(len(Sj0)):
        Uj1.extend([Uj0[j]]+Uj0Group[j])
    return Uj1
#==================================== StartDateSj0() ===================================
"""
Det Uj0: la sequence de StartDate correspondante à la liste Sj0
""" 
def StartDateSj0(Di0,Sj0,GroupSj0,alpha,beta):
    Uj0=[alpha*len(Di0[0])+1]
    for j in xrange(1,len(Sj0)):
        A=Uj0[j-1]+beta+(len(GroupSj0[j-1])*beta)
        B=Uj0[j-1]+alpha*(len(Di0[j]))
        Uj0.insert(j,max(A,B))
    return Uj0
#================================ StartDateGroupSj0() ==================================
"""
Det Uj0Group: la sequence de StartDate correspondante à la liste GroupSj0
""" 
def StartDateGroupSj0(Sj0,GroupSj0,alpha,beta,Uj0):
    Uj0Group=[]
    for j in xrange(len(Sj0)):
        if GroupSj0[j]:
            Uj0Group.append(CalculDate0(GroupSj0[j],beta,Uj0[j]))
        else:
            Uj0Group.append([])
    return Uj0Group

#=======================================================================================
#================================= PreftchStartDate() ==================================
"""
Det Ti: la sequence de Start Date correspondante à la liste Di
""" 
def PrefetchStartDate(Di0,Uj0,alpha,beta):
    Ti=[[1]+CalculDate(Di0[0],alpha,1)]
    for i in xrange(1,len(Di0)):
        if Di0[i]:
            if len(Di0[i])==1:
                Ti.insert(i,[Uj0[i-1]])
            else:
                Ti.insert(i,[Uj0[i-1]] + CalculDate(Di0[i],alpha,Uj0[i-1]))  
        else:
            Ti.insert(i,[])
    return Ti
#==================================== CalculDate() =====================================
"""
On prend une liste S, une cte a et une date initiale InitialDate
A chaque elt de 1 à len(liste), on incremente la date initiale par la cte
On retourne une liste de date S1
"""
def CalculDate0(S,a,InitialDate):
    S0=[]
    for i in xrange(len(S)):
        InitialDate+=a
        S0.append(InitialDate)
    return S0

def CalculDate(S,a,InitialDate):
    S1=[]
    for i in xrange(1,len(S)):
        InitialDate+=a
        S1.append(InitialDate)
    return S1



#=======================================================================================
#=======================================================================================
#=======================================================================================



#=======================================================================================
#======================================= Phase 4 =======================================
#=======================================================================================
"""
Phase4: Find Tj, Uj & Delta
        ---> Apply the idea of "Shifting Prefetches/Computations if necessary"
"""
#=======================================================================================
#==================================== StartDateTile() ==================================
"""
Det Ti,Uj,Delta (together)
"""
def StartDateTile(Y,Ry,Sj,Di,Ti1,Uj1,alpha,beta):
    #Start Date of Prefetches
    Ti=FindTi(Ti1,alpha,beta)    
    #Start Date of Computations & Delta
    Uj=FindUj(Y,Ry,Sj,Di,Ti,Uj1,alpha,beta)    
    Delta=Uj[-1]+beta
    return Ti,Uj,Delta

""" Fct1: FindTi() """
def FindTi(Ti1,alpha,beta):    
    Ti=[Ti1[0]]
    for i in xrange(1,len(Ti1)):
        if Ti1[i]>=Ti[i-1]+alpha:
            Ti.insert(i,Ti[i-1]+alpha)
        else:
            Ti.insert(i,Ti1[i])
    return Ti

""" Fct1: FindUj() """
def FindUj(Y,Ry,Sj,Di,Ti,Uj1,alpha,beta):
    Uj=[Uj1[0]]
    for j in xrange(1,len(Uj1)):
        TileStartDate=[Ti[Di.index(x)] for x in Ry[Y.index(Sj[j])]]
        A=max(TileStartDate)+alpha
        B=Uj[j-1]+beta
        Uj.insert(j,max(A,B))
    return Uj




#=======================================================================================
#=======================================================================================
#=======================================================================================



#=======================================================================================
#                               Fonctions Principales
#=======================================================================================
"""
Outputs of CGM: N,Z,Di,Bi,Sj,Ti,Uj,Delta (Outputs)
"""
def CGM(X,Y,Ry,alpha,beta):
    Sj0,Sj0Ry,GroupSj0=ComputeSequence0(Y,Ry)    
    Di0=[Sj0Ry[0]]
    Di0=PrefetchTile(Sj0,Sj0Ry,Di0)
    Di=reduce(lambda x,y:x+y,Di0)
    N=len(Di)
    Z=N
    Bi=DestinationTile(Di,Z)
    Sj=ComputeSequence(Y,Ry,Sj0,Sj0Ry,GroupSj0)
    Ti0,Uj1,Delta1=StartDateTile0(Y,Ry,Di0,alpha,beta,Sj0,GroupSj0)
    Ti1=reduce(lambda x,y:x+y,Ti0)
    Ti,Uj,Delta=StartDateTile(Y,Ry,Sj,Di,Ti1,Uj1,alpha,beta)                 
    return Sj,N,Z,Di,Bi,Ti,Uj,Delta

