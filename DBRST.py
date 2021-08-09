# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 16:17:45 2019

@author: Rana
"""

import pandas as pd
import numpy as np
from itertools import combinations
import time 

def getAlphaSet(Dominating,Dominated):
    AMLower_Approx,AMUpper_Approx,AM_BNC,ALLower_Approx,ALUpper_Approx,AL_BNC=[],[],[],[],[],[]
    maxlen=len(AMClass_Unions) #number of union classes
    
    for i in range(maxlen):
        Tempset1,Tempset2,Tempset3,Tempset4=set(),set(),set(),set()
        for j in range(uni_len):
            if set(Dominated[j])<=set(AMClass_Unions['Union '+str(i+1)]):#get at most lower and upper approx with boundry region
                Tempset1.add(universe[j])
            if set(Dominating[j])&set(AMClass_Unions['Union '+str(i+1)]):
                Tempset2.add(universe[j])
            if set(Dominating[j])<=set(ALClass_Unions['Union '+str(i+1)]):#get at least lower and upper approx with boundry region
                Tempset3.add(universe[j])
            if set(Dominated[j])&set(ALClass_Unions['Union '+str(i+1)]):
                Tempset4.add(universe[j])
        AMLower_Approx.append(Tempset1)
        AMUpper_Approx.append(Tempset2)
        AM_BNC.append((Tempset1-Tempset2)|(Tempset2-Tempset1))
        ALLower_Approx.append(Tempset3)
        ALUpper_Approx.append(Tempset4)
        AL_BNC.append((Tempset3-Tempset4)|(Tempset4-Tempset3))
        
        
    print("at least lower approx",ALLower_Approx, sep='\n')
    print("at least upper approx",ALUpper_Approx, sep='\n')
    print("boundry region for at least class uninos",AL_BNC, sep='\n')
    print("at most lower approx",AMLower_Approx, sep='\n')
    print("at most upper approx",AMUpper_Approx, sep='\n')
    print("boundry region for at most class uninos",AM_BNC, sep='\n')
    
    BNC_Union, Alpha = set(),set()
    for i in range(len(AL_BNC)):
        BNC_Union=BNC_Union|set(AL_BNC[i])
    Alpha=set(universe)-BNC_Union
    print("BNC_Union Set is" , BNC_Union,sep='\n')
    print("Alpha Set is" , Alpha,sep='\n')
    
    return Alpha

def getDominanceSetList(Domi_Mat):
    
    Dominating=[]
    Dominated=[]
    for i in range(uni_len):
        row = Domi_Mat[i]
        #print(row)
        T_pset=set()
        T_nset=set()
        for j in range(uni_len):
            if row[j]==0:
                T_pset.add(universe[j])
                T_nset.add(universe[j])
            elif row[j]==-1:
                T_pset.add(universe[j])
            elif row[j]==1:
                T_nset.add(universe[j])
        Dominating.append(T_pset)
        Dominated.append(T_nset)
    
    return(Dominating,Dominated)
    
    

def getDomimatrix(Ori_Mat):
    
    att_len=len(Ori_Mat[0])
    univ_len=len(Ori_Mat)
    Domi_Mat =np.zeros((uni_len,uni_len))# making 2D matrix
    for i in range(univ_len):
        for j in range(univ_len):
            if i==j:
                Domi_Mat[i][j]=0
            else:
                Greater = False
                Lesser = False
                for k in range(att_len):
                    if Greater==True and Lesser==True: 
                        Domi_Mat[i][j]=5
                        break
                    elif Ori_Mat[i][k]<Ori_Mat[j][k]:
                        Lesser = True
                    elif Ori_Mat[i][k]>Ori_Mat[j][k]:
                        Greater = True 
                
                if Greater==True and Lesser==False: 
                    Domi_Mat[i][j]=1
                elif Greater==False and Lesser==True: 
                    Domi_Mat[i][j]=-1
                elif Greater==True and Lesser==True:
                    Domi_Mat[i][j]=5
                else:
                    Domi_Mat[i][j]=0           
    #print(Domi_Mat)
    return Domi_Mat

def dataframeTo2dmatrix(dt):
    sdf=dt.copy()
    l1=len(sdf.columns)
    sdf.drop(sdf.iloc[:, 0:1], inplace=True, axis=1)
    sdf.drop(sdf.iloc[:, (l1-2):l1], inplace=True, axis=1)
    Ori_Mat=sdf.values
    #print(Ori_Mat)
    return Ori_Mat    

def findUnions(classes,):
    
    AMClass_Unions['Union 1']= Classes["class_1"]# for first class union
    counter = 1
    for i in range(2,length):
        Temp1,Temp2=set(),set()
        current = Classes['class_'+str(i)]
        for j in range(i-1,0,-1):
            Temp1=Temp1|current|Classes['class_'+str(j)] # | is used for unions of sets
            #print("Temp1",Temp1)
        AMClass_Unions['Union '+str(counter+1)]=Temp1 
        for k in range(i+1,length+1):
            Temp2=Temp2|current|Classes['class_'+str(k)]
            #print("Temp2",Temp2)
        ALClass_Unions['Union '+str(counter)]=Temp2
        counter+=1
    ALClass_Unions['Union '+str(len(ALClass_Unions)+1)]= Classes["class_"+str(len(Classes))]#for last class union
    print("at least class unions",  ALClass_Unions, sep='\n' )
    print("at most class unions", AMClass_Unions, sep='\n')
    
def getDRL(AlphaSet,uni_len,att_len):
    
    DRL=set()
    AlphaList=list(AlphaSet)
    Alpha_len=len(AlphaSet)
    for n in range(Alpha_len):  #checking all alpha set elements
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
dt = pd.read_excel("iris_data.xlsx","Sheet1") #loading dataset
Classes={}
AMClass_Unions={}
ALClass_Unions={}

for i, g in dt.groupby('Decision'): #grouping data on the basis of decision classes
    print (i)
    Classes["class_" + str(i+1)]= set(g['Universe'].values.tolist())
    #print(g)
    print(Classes)

columns = list(dt)
last=columns.pop(-1)
labels= dt[last].unique() #getting labels of decision attribute
length=len(labels)

if length==2:
    AMClass_Unions['Union 1']= Classes["class_1"]
    ALClass_Unions['Union 1']= Classes["class_2"]
else:
    findUnions(Classes) #finding of upward and downward unions of classes

Ori_Mat=dataframeTo2dmatrix(dt)
universe=dt['Universe'].values.tolist()
decision=dt['Decision'].values.tolist()
uni_len=len(universe)
at_len=len(Ori_Mat[0])
Domi_Mat=getDomimatrix(Ori_Mat) #extracting dominance matrix

Dominating=[]
Dominated=[]
Dominating,Dominated=getDominanceSetList(Domi_Mat) #extracting dominating and dominated list for every element in the dataset 

print("dominated(smaller) set objects of universe for every object" ,Dominated)
print("dominating(bigger) set objects of universe for every object",Dominating) 
print("at most union classes", AMClass_Unions)
print("at least union classes", ALClass_Unions)

Alpha_Set=getAlphaSet(Dominating,Dominated) #Finding AlphaSet
print("Length of Alpha Set is" , len(Alpha_Set),sep='\n')

Ori_Dep=len(Alpha_Set)/uni_len #calculating original dependency of dataset
print('Original Data Dependency is:',Ori_Dep)

"""DRList=getDRL(Alpha_Set,uni_len,at_len)

Reducts=getReducts(DRList)

print('reducts are:',Reducts)
print('Number of reducts are:',len(Reducts))
"""
end=time.time()

print('execution time is :',end-start)