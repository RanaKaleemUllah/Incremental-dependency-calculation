# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 16:50:53 2019

@author: Rana
"""
import pandas as pd
import numpy as np
from itertools import combinations
import time

def dataframeTo2dmatrix(dt):
    sdf=dt.copy()
    l1=len(sdf.columns)
    sdf.drop(sdf.iloc[:, 0:1], inplace=True, axis=1)
    sdf.drop(sdf.iloc[:, (l1-2):l1], inplace=True, axis=1)
    Ori_Mat=sdf.values
    #print(Ori_Mat)
    return Ori_Mat

def getDomimatrix(Ori_Mat):
    
    uni_len= len(Ori_Mat)
    att_len= len(Ori_Mat[0])
    Domi_Mat =np.zeros((uni_len,uni_len))
    
    for i in range(uni_len):
        for j in range(i,uni_len):
            if i==j:
                Domi_Mat[i][j]=0
            else:
                Greater = False
                Lesser = False
                for k in range(att_len):
                    if Greater==True and Lesser==True: 
                        Domi_Mat[i][j]=5
                        Domi_Mat[j][i]=5
                        break
                    elif Ori_Mat[i][k]<Ori_Mat[j][k]:
                        Lesser = True
                    elif Ori_Mat[i][k]>Ori_Mat[j][k]:
                        Greater = True 
                
                if Greater==True and Lesser==False: 
                    Domi_Mat[i][j]=1
                    Domi_Mat[j][i]=-1
                elif Greater==False and Lesser==True: 
                    Domi_Mat[i][j]=-1
                    Domi_Mat[j][i]=1
                elif Greater==True and Lesser==True:
                    Domi_Mat[i][j]=5
                    Domi_Mat[j][i]=5
                else:
                    Domi_Mat[i][j]=0
                    Domi_Mat[j][i]=0
    #print(Domi_Mat)
    return Domi_Mat

def getAlphaSet(Mat):
    
    univ_len=len(Mat)
    Selected=np.ones(univ_len)
    print(Selected)
    AlphaSet=set()
    Checked=set()
    Decision=dt['Decision'].values.tolist()
    
    for i in range(univ_len):
        cl=len(Checked)
        if cl==0:# check that if the object is first one from universe
            Checked.add(universe[i])
            AlphaSet.add(universe[i])
            Selected[i]=1
        else:
            for j in range(cl):
                if Domi_Mat[i][j]==5:
                    Checked.add(universe[i])
                    if Selected[i]==1:
                        Selected[i]=1
                        AlphaSet.add(universe[i])
                elif (Domi_Mat[i][j]==1 and Decision[i]>=Decision[j]) or (Domi_Mat[i][j]==-1 and Decision[i]<=Decision[j]):
                    Checked.add(universe[i])
                    if Selected[i]==1:
                        Selected[i]=1
                        AlphaSet.add(universe[i])
                elif Domi_Mat[i][j]==0 and (Decision[i]==Decision[j]):
                    Checked.add(universe[i])
                    if Selected[i]==1:
                        Selected[i]=1
                        AlphaSet.add(universe[i])
                elif Domi_Mat[i][j]==0 and (Decision[i]!=Decision[j]):
                    Checked.add(universe[i])
                    Selected[i]=0
                    Selected[j]=0
                    AlphaSet.discard(universe[i])
                    AlphaSet.discard(universe[j])
                elif (Domi_Mat[i][j]==1 and Decision[i]<Decision[j]) or (Domi_Mat[i][j]==-1 and Decision[i]>Decision[j]):
                    Checked.add(universe[i])
                    Selected[i]=0
                    Selected[j]=0
                    AlphaSet.discard(universe[i])
                    AlphaSet.discard(universe[j])
        
            
    print("Selected array is:",Selected)
    print("Checked array is:",Checked)
    
    
    #AlphaSet=set()
    #for i in range(univ_len):
    #    if Selected[i]==1:
    #        AlphaSet.add(universe[i])
    print("Alpha Set is:",sorted(AlphaSet))
    Alpha_Len=len(AlphaSet)
    dependency = Alpha_Len/univ_len
    print('Length of Alphaset:',Alpha_Len)
    print("Dependency of this dataset is:",dependency)
    return(AlphaSet)


def getDRL(AlphaSet,uni_len,att_len):
    
    DRL=set()
    AlphaList=list(AlphaSet)
    Alpha_len=len(AlphaSet)
    for n in range(Alpha_len):  #checking all alpha set elements
        print("Turn no. =",n)
        for m in range(uni_len):
            if AlphaList[n]==universe[m]: #comparing to Domi_Row
                Domi_Row=Domi_Mat[m]
                #print("Domi Row",Domi_Row)
                for i in range(uni_len): 
                    if decision[m]!=decision[i] and Domi_Row[i]==5:
                        tempset=set()
                        if decision[m]>decision[i]:
                            for k in range(att_len):
                                if Ori_Mat[m][k]>Ori_Mat[i][k]:
                                    tempset.add(k)
                        elif decision[m]<decision[i]:
                            for k in range(att_len):
                                if Ori_Mat[m][k]<Ori_Mat[i][k]:
                                    tempset.add(k)
                        
                        #print('tempset',tempset)
                        Critical_att=tuple(list(tempset))
                        DRL.add(Critical_att)
    print('Sorted Absorbed Dominance Retaining List = ',sorted(DRL))
    print('Length of ADRL',len(DRL))
    return DRL

def getReducts(DRList):
    
    strlist,sublist,reduct=[],[],[]
    for value in DRList:
        strlist.extend(value)
    
    strset=set(strlist)
    length=len(strset)
    #print('String List',strset)
    
    count=0
    for i in range(length):
        comb = combinations(strset,i)
        for k in list(comb):
            if count==0:
                count=count+1
            else:
                sublist.append(k)
    #Print the obtained combinations 
    #print('sublist',sublist)
    for value in sublist:
        match=True
        for value2 in DRList:
            val=set(value).intersection(set(value2))
            if not val:
                match=False
                break
        if match:
            reduct.append(value)
    
    return(reduct)

start=time.time()
dt = pd.read_excel("iris_data.xlsx","Sheet1")
Classes={}

for i, g in dt.groupby('Decision'):
    #print (i)
    Classes["class_" + str(i)]= set(g['Universe'].values.tolist())
    #print(g)
    #print(sorted(Classes['class_'+str(i)]))
          
#print(dt)

Ori_Mat=dataframeTo2dmatrix(dt)
#print(Ori_Mat)

universe=dt['Universe'].values.tolist()
decision=dt['Decision'].values.tolist()
uni_len=len(universe)
at_len=len(Ori_Mat[0])
Domi_Mat=getDomimatrix(Ori_Mat)
print(Domi_Mat)

AlphaSet=getAlphaSet(Domi_Mat)
#print("Decision",decision)
#DRList=getDRL(AlphaSet,uni_len,at_len)

#Reducts=getReducts(DRList)

#print('reducts are:',Reducts)
#print('Number of reducts are:',len(Reducts))

end=time.time()

print('execution time is :',end-start)

        