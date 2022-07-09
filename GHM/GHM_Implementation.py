# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 20:55:03 2022

@author: Zihong Xu
"""



from NNetwork.NNetwork import NNetwork as NNT
import numpy as np
import pandas   as pd
import seaborn as sb
import networkx as nx
import matplotlib.pyplot as plt

""" Parameter: Graph G, Phase State S, Period k,Iteration Number ItNum """
def GHMArr(G,S,kap,ItNum):
    St = S
    SN = np.zeros(G.number_of_nodes())
    NodeNum = G.number_of_nodes()
    for i in range(len(S)):
        SN[i] = S[i]
    for i in range(ItNum):
        if i!=0:
            S = SN
            St = np.vstack((St,SN))
        for j in range(NodeNum):
            Onein = False
            NeighbNum = len(list(G.neighbors(list(G.nodes)[j])))
            NeighbSet = G.neighbors(list(G.nodes)[j])
            NeighbList = list(NeighbSet)
            NeighbState = np.zeros(NeighbNum)
            for k in range(NeighbNum):
                NeighbState[k] = S[int(NeighbList[k])-1]  

            if 1 in NeighbState:
                Onein = True
            if S[j] == 0 and (not Onein):
                SN[j] = 0
            elif S[j] == 0 and Onein:
                SN[j] = 1 % kap
            else:
                if (S[j] + 1) % kap == 0:
                    SN[j]=0
                else:       
                    SN[j] = (SN[j] + 1) % kap
    
    PhaseState = pd.DataFrame(St)
    

    return sb.heatmap(PhaseState, cbar=False, cmap='viridis')     
   
        
        
"""Synchronizing example"""
edgelist = [['1','2'],['2','3'],['3','4'],['1','3'],['1','5'],['1','6'],['1','7'],['1','8'],['2','8'],['2','9'],['1','9'],['2','4'],['2','5'],['3','6'],\
            ['3','4'],['3','5'],['3','6'],['3','8'],['3','9'],['4','5'],['4','6'],['4','7'],['4','9'],['5','6'],['5','7'],['6','8']]
G1 = nx.Graph()
G1.add_edges_from(edgelist)
plt.figure(1)
nx.draw(G1, with_labels=True, font_weight='bold')
plt.figure(2)
s = np.random.randint(7,size = 1*9)
GHMArr(G1, s, 12, 15);


Grand2DArr = nx.grid_2d_graph(10, 10)
s = np.random.randint(4, size=10*10)
GHMArr(Grand2DArr, s, 4, 100);

