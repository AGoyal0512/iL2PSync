# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 20:55:03 2022

@author: Zihong Xu
"""



from NNetwork.NNetwork import NNetwork as NNT
import numpy as np
import pandas as pd
import networkx as nx
import random

""" Parameter: Graph G, Phase State S, Iteration Number ItNum """

def GHM(G,S,ItNum):
    St = S
    SN = S
    for i in range(ItNum):
        if i!=0:
            S = SN
            St = np.vstack((St,SN))
        for j in range(G.number_nodes):
            Onein = False
            for k in range(len(G.neighbors(G.vertices(j)))):
                if 1 in S[k in G.neighbors(G.vertices(j))]:
                    Onein = True
            if SN[j] == 0 & (not Onein):
                SN[j] = 0
            elif SN[j] == 0 & Onein:
                SN[j] = 1
            else:
                Sn[j] = Sn[j] + 1
    return St     
     
        
        
        

edgelist = [['1','2'],['2','3'],['3','4'],['1','3'],['1','5'],['1','6'],['1','7'],['2','5'],['3','6'],\
            ['3','4'],['3','5'],['3','6'],['4','5'],['4','6'],['4','7'],['5','6'],['5','7']]
G1 = NNT()
G1.add_edges(edgelist)
print(G1.vertices)
print(G1.neighbors('2'))
State = GHM(G1,[0,2,1,2,3,1,4],10)
