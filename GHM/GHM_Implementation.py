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
    SN = np.zeros(G.number_nodes)
    for i in range(ItNum):
        if i!=0:
            S = SN
            St = np.vstack((St,SN))
        for j in range(G.number_nodes):
            
            if 0 not in S[k in G.neighbors(G.vertices(j))] & (S[j] == 0):
                SN[j] = 0
            elif 0 not in S[k in G.neighbors(G.vertices(j))] &  (S[j] == 0):
                SN[j] = 1
            else:
                SN[j] = S[j]+1
    return St
        
        
        
        
        

edgelist = [['a','b'],['b','c'],['c','d'],['a','c'],['a','e'],['a','f'],['a','g'],['b','e'],['b','f'],\
            ['c','d'],['c','e'],['c','f'],['d','e'],['d','f'],['d','g'],['e','f'],['e','g']]
G1 = NNT()
G1.add_edges(edgelist)
print(G1.vertices)
State = GHM(G1,[0,2,1,2,3,1,4],10)
