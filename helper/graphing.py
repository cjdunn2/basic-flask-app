import os
import pandas
import numpy as np


#I need a function that will take an array of touples where the touples 
#are (cost,time)

def graph_data_helper(data):
    
    # print(data)
    
    print('AAAAAAA', data[0][1])
    print ('BBBBBBB', data[0][2])
    print('length', len(data))
    
    #I need to extract from data the cost and time and then put them into a list
    #I need to do this for all 5 of the data sets
    for_graphing = []
    
    for i in range(len(data)):
        for_graphing.append([data[i][1], data[i][2]])
        
    print('for_graphing', for_graphing)
    
    
        
        
        
    
    
    
    