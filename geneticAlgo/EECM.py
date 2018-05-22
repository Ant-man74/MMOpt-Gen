# -*- coding: utf-8 -*-

"""
This model implements a constructive heuristic EECMV2 for solving the 3-PSDPP problem: min N,Delta,Z

The 3-PSDPP is a new multi-objective scheduling problem arises in the embedded vision systems domain (Memory Hierarchy).
        Inputs: X input tile, Y output tile, Ry (Requirement Te/Ts) <--> matrix Mij (x,y), alpha & beta.
        Outputs: N, Delta, Z, prefetchs & computations schedules 

---> Optimization order is: min N ---> min Delta ---> min Z
                       ---> ECM + min Z
---> 3-PSDPP's Idea 1: EECM (min N, min Delta, min Z)
"""

import numpy as np
import math        
import random
import logging
import operator
import sys


#================================= Steps 
"""
Step0: A: Dét (Y,Ry) à partir file.txt
       B: Dét X à partir Ry
       C: Dét Lower Bounds: lbN, lbZ,lbDelta
Step1: min N     ---> Ordonner Te ds l'ordre décroissant de leur Nb_Occ
Step2: min Delta ---> Avancer les Calculs pouvant etre avancés
Step3: min Z     ---> Réutiliser le buffer de la Te x qui ne sera + utile après son last Compute (Ei(x)),
                      pour une autre Te x' où sa u_j(FirstCompute de x') >= u_j(LastCompute de x)+beta.
                      <---> l'idée est retarder le préchargement de x' vers u_j(FirstCompute de x')-alpha
"""


#======================================================================================
#                               Fonctions Utiles
#=======================================================================================
#==================================== OutputTile() =====================================
"""
Définition de la liste Y de Ts à calculer & l'ensemble Ry (Requirements Set of Te%Ts)
"""
def OutputTile():
    #Matrix0=open('TD1988-MatrixValue.txt','r')
    """ Small Instances """    
    Matrix0 = open('Kernel-test_2D\\test_2D-MatrixValue.txt','r') #kernel1
    #Matrix0=open('Kernel-test_2D_PE\\test_2D_PE-MatrixValue.txt','r')#kernel2
    #Matrix0=open('Kernel-fisheye\\fisheye-MatrixValue.txt','r')#kernel3
    #Matrix0=open('Kernel-polaire\polaire-MatrixValue.txt','r')#kernel6
    #Matrix0=open('Kernel-polaire_mipmap_iso\polaire_mip_iso-MatrixValue.txt','r')#kernel7
    """ Tested-Big Instances """
    #Matrix0=open('Kernel-fisheye_mipmap_iso\\fisheye_mip_iso-MatrixValue.txt','r')#kernel4
    #Matrix0=open('Kernel-fisheye_mipmap_aniso\\fisheye_mip_aniso-MatrixValue.txt','r')#kernel5
    #Matrix0=open('Kernel-polaire_mipmap_aniso\polaire_mip_aniso-MatrixValue.txt','r')#kernel8
    #Matrix0=open('Kernel-fd_resize_PE\\fd_resize_PE-MatrixValue.txt','r')#kernel9
    #Matrix0=open('Kernel-fd_haar_ePE\\fd_haar_ePE-MatrixValue.txt','r')#kernel10
    """ New Instances """
    #Matrix0=open('Kernel-cameleon\\cameleon-MatrixValue.txt','r')#kernel11
    #Matrix0=open('Kernel-cameleon_sd\\cameleon_sd-MatrixValue.txt','r')#kernel12

    Nb=[Line.split() for Line in Matrix0]
    Matrix0.close()
    List0=list(Nb)# List0 est une liste de list1 de chaine de caractère
    #--- Dét Y, Ry 
    Y=[]
    Ry=[]
    for List1 in List0:
        Y.append(int(List1[0]))
        A=set(map(int,List1[2:]))
        Ry.append(sorted(list(A)))
        #Ry.append(A) ou Ry.append(set(sorted(list(A))))
    return Y,Ry

#==================================== InputTile() ======================================
"""
Dét la liste des input tiles X <===> len(X)=lbN
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
Dét le nombre de buffers Z <===> Z=lbZ
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

#==================================== InputsData() =====================================
"""
Dét les Inputs à partir d'un fichier .txt: (X,Y,Ry) 
"""
def InputsData(): 
    Y,Ry=OutputTile()
    X=InputTile(Ry)
    #Z=BuffersNb(Ry) 
    return (X,Y,Ry)#,Z




#=======================================================================================
#=======================================================================================
#=======================================================================================




#=======================================================================================
#                               1: Optimiser N ?
#=======================================================================================
"""
    1: Calculer pour chaque Te de X son Nb_Occ
    2: Dét Di: X ds l'ordre decroissant d Nb_Occ (d_i)
    3: Dét Bi0: Affecter aléatoirement à chaque Te 1 buffer parmi X-|Omega| Buffers (b_i)
    4: Dét Ti: Dét pour chaque Te sa date de début de préchargement (t_i)
"""

#=======================================================================================
#=================================== PrefetchTile() ====================================
"""
Dét Di: la sequence de Prefetch correspondante à la liste de Te X 
""" 
def PrefetchTile(X,Ry):
    Di=[]    
    """ 1:Dét le DictX """
    DictX=FindDictX(X,Ry)
    """ 2: Trier DicX ds Ordre Decroissant en fonct de DictX.Values() """
    ListDictX=sorted(DictX.items(),key=lambda x:x[1], reverse=True)
    for i in range(len(ListDictX)):
        Di.insert(i,ListDictX[i][0])
    #Sp=dic.keys()
    return Di

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
        DictX.update(FindNbOccurTe1(X,i,Ry))
    return DictX

#================================== FindNbOccurTe1() ===================================
"""
Dét NbOcc: pour une Te de la liste X, le Nb d'occurence ds chaque elt de Ry
DictTe={key:value}, où
    ---> key: N° Te
    ---> value: NbOccur
""" 
#Method 1
def FindNbOccurTe1(X,i,Ry):
    NbOccur=0
    for j in range(len(Ry)):
        NbOccur+=list(Ry[j]).count(X[i])
    return {X[i]:NbOccur}
#Method 2
def FindNbOccurTe2(X,i,Ry):
    NbOccur=0
    for j in range(len(Ry)):
        if X[i] in Ry[j]:
            NbOccur+=1
        else:continue
    return {X[i]:NbOccur}



#=======================================================================================
#================================ DestinationTile0() ===================================
"""
Dét Bi0: la sequence de Destination correspondante à la liste Di en utilisant un nbre de
buffers Z autant le nbre de Prefetches X-|Omega|"""
def DestinationTile0(Di,Z):
    Bi0=[]
    ListBuff=list(range(Z))
    for i in range(len(Di)):
        NbBuff,ListBuff=AffectBuffer0(Di,i,ListBuff)
        Bi0.insert(i,NbBuff)  
    return Bi0

#=================================== AffectBuffer0() ===================================
"""
Dét le N° de Buffer (NbBuff) affecté aléatoirement à partir de la liste initiale
ListBuff à une Te i & MAJ de ListBuff (on supprime NbBuff de ListBuff) 
"""
def AffectBuffer0(Di,i,ListBuff):
    NbBuff=random.choice(ListBuff)
    ListBuff.remove(NbBuff)
    return NbBuff,ListBuff


#=======================================================================================
#================================== PreftchStartDate() =================================
"""
Dét Ti: la sequence de Start Date correspondante à la liste de Prefetches(Di)
""" 
def PrefetchStartDate(Di,alpha):
    Ti=[1]
    for i in range(1,len(Di)):
        Ti.insert(i,Ti[i-1] + alpha)
    return Ti

###=======================================================================================
###================================= ComputeStartDate0() =================================
##"""
##Dét Bc0: la sequence de Start Date correspondante à la liste de Computed Ts (Y)
##""" 
##def ComputeStartDate0(Sc0,Sp0,alpha,beta):
##    Bc0=[len(Sp0)*alpha+1] #Bc0=[max(Bp0)+alpha+1]
##    for j in range(1,len(Sc0)):
##        Bc0.insert(j,(Bc0[j-1]+beta))
##    return Bc0




#=======================================================================================
#=======================================================================================
#=======================================================================================




#=======================================================================================
#                               2: Optimiser Delta ?
#=======================================================================================
"""
    5: Dét Sj: Calculer chaque Ts dès que ses Te requises sont préchargées
               ---> Sj=Y ds ordre Croissant de max(Bp[Te requises])
    6: Dét Uj: dét pour chaque Ts sa date de début de calcul
               Uj[y]=max(Ti[Te requises])+alpha
               ---> Pas de chevauchement entre calculs: Uj[y+1] >= Uj[y]+beta
    7: Dét Delta: Total Completion Time ---> Delta=Uj[-1]+beta
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
    Delta=max(Uj) + beta
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
    DictConfigTs={y:max(ListTsDate)+alpha}
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




#=======================================================================================
#                       3: Optimiser Z ? ---> Idea 1
#=======================================================================================
"""
Use the same idea as KTNS algorithm to find a Destination sequence

    8: Dét A: matrice d'incidence Te/Ts, où
               ---> Te ds l'ordre celui de Di
               ---> Ts ds l'ordre celui de Sj
               
    9: Dét D: affecter chaque bloc1 de A à un buffer, où nb initial de buff est =Z
               ---> Z=BuffersNb(Ry)
"""

#=======================================================================================
#================================ FindIncidenceMatrix() ================================
"""
Dét A: incidence matrix (0-1) of Te/Ts using Di & Sj
"""
def FindIncidenceMatrix(Di,Ti,Sj,Uj,Y,Ry,beta):
    print (Di)
    print(Sj)
    sys.exit(0)
    A=np.zeros((len(Di),len(Sj)),dtype=int)
    for i in range(len(Di)):
        DictConfigTe=list(FindConfigTe(Di,Ti,Di[i],Sj,Uj,Y,Ry,beta).items())
        Tile1=DictConfigTe[0][1][0]
        Tile2=DictConfigTe[0][1][1]
        for j in range(Sj.index(Tile1),Sj.index(Tile2)+1):
            A[i][j]=1
    return A

##    for i in range(len(Sp)):
##        DictConfigTe=FindConfigTe(Sp,Bp,Sp[i],Sc,Bc,Y,Ry,beta)
##        Tile1=DictConfigTe.values()[0][0]
##        Tile2=DictConfigTe.values()[0][1]
##        #print "ConfigTe: ", (i,Tile1,Tile2)
##        for j in range(Sc.index(Tile1),Sc.index(Tile2)+1):
##            #print "TS: ", (j, list(range(Sc.index(Tile1),Sc.index(Tile2)+1)))
##            A[i][j]=1
##            #print "Matrix A: ", A[i][j]
##        for j in range(len(A[0])):
##            if j in range(Sc.index(Tile1),Sc.index(Tile2+1)):#Tile1:Computation n°1 & Tile2: Last Computation
##                A[i][j]==1
##            else:
##                A[i][j]==0 
#=================================== FindConfigTe() ====================================
"""
Dét DictConfigTe, où
    - key= x   ---> N° of Te in Di
    - Value= (First Computation, Last Computation)
"""
def FindConfigTe(Di,Ti,x,Sj,Uj,Y,Ry,beta):
    ListTs=FindListTs(Y,Ry,x)
    ListTsDate=FindListTsDate(ListTs,Sj,Uj)        
    DictConfigTe={x:(Sj[Uj.index(min(ListTsDate))],Sj[Uj.index(max(ListTsDate))])}
    return DictConfigTe
#================================== FindListTs() =======================================
"""
Dét ListTs: la liste de Ts où la tuile Te donnée (x) est ds Ry
"""
def FindListTs(Y,Ry,x):
    ListTs=[]
    for j in range(len(Ry)):
        if x in Ry[j]:
            ListTs.append(Y[j])
    return ListTs
#================================ FindListTsDate() =====================================
"""
Dét ListTsDate: la liste de Start Date de la ListTs pour la Te x 
"""
def FindListTsDate(ListTs,Sj,Uj):
    ListTsDate=[]
    for Ts in ListTs:
        ListTsDate.append(Uj[Sj.index(Ts)])
    return ListTsDate



#=======================================================================================
#================================= FindBufferNumber() ==================================
"""
Dét Z: Nb d Buffers correspondant à la matrice A
"""
def FindBufferNumber(A):
    (x,y)=np.shape(A)
    ListBuff=[]
    for j in range(len(A[0])):
        ListBuff.append(ColumnCapacity(A,j))
    Z=max(ListBuff)
    return Z

#================================== ColumnCapacity() ===================================
def ColumnCapacity(A,j):
    """
    Determiner la valeur qui calcule la somme de 1 de la colonne j de la matrice A
    """
    return sum(A[:,j])

#=======================================================================================
#================================== DestinationTile() ==================================
"""
Dét Bi: Destination de tuiles préchargées (Quel Buffer pour Quelle Tuile)
---> (Bi est une liste de listes)
"""
def DestinationTile(A,Z):
    Bi=[]
    ListFreeBuff=list(range(Z))
    DicAffectBuffAllBloc1={}
    ListFreeBuff,DicAffectBuffAllBloc1,D=FindAllListBuff(A,ListFreeBuff,DicAffectBuffAllBloc1,Bi)    
    return Bi

#====================================== FindBloc1() ====================================
"""
On prend la matrice A
On retourne une liste contient les indices i correspondants aux blocs de 1
(x=len(A[:,0]) & y=len(A[0,:]))
On peut aussi retourner un 3 tuples (Di, Bi, Ti)
<--->(Quelle Tuile x, Quelle Buffer z, à Quelle Dtae) avec Z et alpha comme données
"""
def FindBloc1(A,j):
    (x,y)=np.shape(A)
    DicBloc1={}
    for i in range(0,x):
        if A[i][j] == 0: continue
        if j == 0:
            if A[i][j] == 1 and A[i][j+1] == 0:
                DicBloc1 [i] = (j,j)
            else:
                """ On compte les 1 jusqu'à trouver un 0 (On regarde ts les j aprés où A[i][j]= P[i][j+k]= 1) """
                k = 1
                while k<y and A[i][j+k] == 1:#j=0 ==> j+k<y
                    k += 1                
                DicBloc1 [i] = (j, j+k-1)
        elif j == y-1:
            if A[i][j-1]== 1: continue
            DicBloc1 [i] = (j, j)        
        else:
            """
                Si 0 < j < y-1: 
                    1: A[i][j-1] == 0
                    2: Pour ts les j colonnes aprés: A[i][j]== A[i][j+k] == 1
            """        
            if A[i][j-1]== 1: continue
            k = 1
            while j+k < y and A[i][j+k] ==  1:
                k += 1
            DicBloc1[i]=(j,j+k-1)
    return DicBloc1
#=================================== FindAllListBuff() =================================
"""
Dét ListFreeBuff,DicAffectBuffAllBloc1,Bi: destination pour tte colonne j de A
"""
def FindAllListBuff(A,ListFreeBuff,DicAffectBuffAllBloc1,Bi):
    for j in range(len(A[0])):
        
        """ Step0: Initialize """       
        DicAffectBuff={}
        ListAffectBuff=[]
        ListToFreeBuff=[]
        
        """ Step1: Affect Buff """
        DicAffectBuff,ListAffectBuff,ListFreeBuff=FindListBuff(A,j,ListFreeBuff)
        
        """ Step2: Buff To Free """
        DicAffectBuffAllBloc1.update(DicAffectBuff)
        ListToFreeBuff=FreeBuffer(j,DicAffectBuffAllBloc1)
        
        """ Step3: Update ListFreeBuff """
        ListFreeBuff.extend(ListToFreeBuff)
        
        """ Step4: Bi List """
        Bi.insert(j,ListAffectBuff)
        
    return ListFreeBuff,DicAffectBuffAllBloc1,Bi

#==================================== FindListBuff() ===================================
"""
Dét D1,L1,L: la liste ListAffectBuff pour une colonne j 
"""
def FindListBuff(A,j,L):
    ListBloc1=list((FindBloc1(A,j)).items())
    D={}#one bloc1=one buffer
    D1={}#dic Affect Buff of all bloc1 of j
    L1=[]#list Affect Buff of all bloc1 of j
    for list1 in ListBloc1:
        D=AffectBuffer(list1,L)
        for valeur in D.values():
            L.remove(valeur)
        D1.update(D)
        L1.extend(D.values())
    return D1,L1,L

#==================================== AffectBuffer() ===================================
"""
Dét pour un bloc1 quel buffer libre à affecter
(Affecter 1 Buffer à un Bloc de 1)
"""
def AffectBuffer(Bloc1,L):
    NumRow,FirstCol,LastCol,k=Bloc1Details(Bloc1)
    D={(NumRow,FirstCol,LastCol):random.choice(L)}
    return D

#==================================== Bloc1Details() ===================================
"""
Dét NumRow,FirstCol,LastCol,k(=LenBloc1): les détails d'un bloc1
"""
def Bloc1Details(L):
    for i in range(len(L)):
        NumRow=L[0]
        FirstCol=L[1][0]
        LastCol=L[1][1]
        k=LastCol-FirstCol+1
    return NumRow,FirstCol,LastCol,k

#===================================== FreeBuffer() ====================================
"""
Dét L: la liste de Buff a liberer
"""
def FreeBuffer(j,D1):
    L=[]
    for key,value in D1.items():
        if key[2] == j:#-1:
            L.append(value)
    return L




#=======================================================================================
#=======================================================================================
#=======================================================================================




#=======================================================================================
#                               Fonctions Principales
#=======================================================================================
"""
Outputs of EECM: X,Y,Ry (Inputs) & Di,Bi,Ti,N,Z,Sj,Uj,Delta (Outputs)
"""
def EECM(X,Y,Ry,alpha,beta, Z): 
    """ Phase 1: ECM outputs <---> N,Di,Bi0,Z0,Ti,Sj,Uj,Delta """
    Di=PrefetchTile(X,Ry)
    N=len(Di)
    Bi0=DestinationTile0(Di,Z)
    Z0=len(Bi0)
    Ti=PrefetchStartDate(Di,alpha)
    Sj,Uj,Delta=ComputeTile(Y,Ry,Di,Ti,alpha,beta) 
    
    """ Phase 2: min Z (based on KTNS's Idea) """    
    A=FindIncidenceMatrix(Di,Ti,Sj,Uj,Y,Ry,beta)
    Z=FindBufferNumber(A)
    Bi=reduce(lambda x,y:x+y,DestinationTile(A,Z))
    print (A)
    print (Bi)
    return Sj, Uj, Di, Bi, Ti, Z0, Z, N, Delta

#=======================================================================================
"""
# Lower Bounds: lbN,lbZ, lb1Delta & lb2Delta
"""
def LowerBounds(X,Y,Ry,alpha,beta):
    lbN=len(X)
    lbZ=BuffersNb(Ry)
    Xmin=RequiredTileNb(Ry)
    lb1Delta=(alpha*len(X))+beta+1
    lb2Delta=alpha+(beta*len(Y))+1
    lb3Delta=alpha*Xmin+(beta*len(Y))+1
    lbDelta= max(lb1Delta,lb2Delta) 
    lbDelta1= max(lb1Delta,lb3Delta)     
    return lbN,lbZ,lb1Delta,lb2Delta,lb3Delta,lbDelta,lbDelta1

"""
Deprecated method of python 2.7 but necessary for this algorythm as I don't know how to replace it 
"""
def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    
    if initializer is None:         
        try:
            initializer = next(it)
        except StopIteration:
            raise TypeError('reduce() of empty sequence with no initial value')     
    
    accum_value = initializer       
    
    for x in it:
        accum_value = function(accum_value, x)

    return accum_value




