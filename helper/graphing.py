import os
import pandas as pd
import numpy as np
import csv
import json


#I want this to take the data and then save it to a csv file
def data_to_csv(data):
    
    data_labels = ['Algorithm', 'Knapsack', 'Recursive Knapsack', 'Dynamic', 'Static' ]
    
    
    # print('AAAAAAA', data[0][1])
    # print ('BBBBBBB', data[0][2])
    # print('length', len(data))
    
    #I need to extract from data the cost and time and then put them into a list
    #I need to do this for all 5 of the data sets
    for_graphing = []
    
    for i in range(len(data)):
        for_graphing.append([data_labels[i],data[i][1], data[i][2]])
        
    df = pd.DataFrame(for_graphing, columns = ['Algorithm', 'Cost', 'Time'])
    
    # print('df', df)
    
    
    #This just appends the new data to that same local csv file
    df.to_csv('static/csv/graphing_data.csv', mode='a', index=False, header=False)    
    
    
    
#I need a method that takes in the csv file and then returns the data for the graph
def data_for_graphing():
        
    algorithm_1_arr = []
    knapsack_arr = []
    recursive_knapsack_arr = []
    dynamic_arr = []
    static_arr = []

    with open('static/csv/graphing_data.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        # next(csvreader)  # skip header row

        for row in csvreader:
            algorithm_type = row[0]
            cost = row[1]
            time = row[2]

            if algorithm_type == 'Algorithm':
                algorithm_1_arr.append((cost, time))
            elif algorithm_type == 'Knapsack':
                knapsack_arr.append((cost, time))
            elif algorithm_type == 'Recursive Knapsack':
                recursive_knapsack_arr.append((cost, time))
            elif algorithm_type == 'Dynamic':
                dynamic_arr.append((cost, time))
            elif algorithm_type == 'Static':
                static_arr.append((cost, time))
                

    return [algorithm_1_arr, knapsack_arr, recursive_knapsack_arr, dynamic_arr, static_arr]

#I need to write a method that takes a csv and jsonify's it
def csv_to_json():
    #read the csv file
    df = pd.read_csv('static/csv/graphing_data.csv', usecols=["Algorithm", "Cost", "Time"])
    #convert to json
    json = df.to_json(orient='records')
    #write to file
    # with open('static/csv/graphing_data.json', 'w') as f:
        # f.write(json)
    #return the json
    return json    

def create_data_for_graphing():
    #read the csv file
    df = pd.read_csv('static/csv/graphing_data.csv', usecols=["Algorithm", "Cost", "Time"])
    #but back into csv with just those cols
    if os.path.exists('static/csv/result.csv'):
        os.remove('static/csv/result.csv')
        print('File deleted')
        
    df.to_csv('static/csv/result.csv', index=False, header=True)    
    

    
        
        
        
        
    
    
    
    