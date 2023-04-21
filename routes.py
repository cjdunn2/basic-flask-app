import os
import time
import openai
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
#import config
import json as JSON
import TestRun
import helper.graphing as graphing




from flask import Flask, render_template

app = Flask(__name__)
# app.config.from_object(config.config['development'])

# two decorators, same function
@app.route('/')
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    #if post request, get the data from the form and write it to the session file and then redirect to the index page
    if request.method == 'POST':
        
        #take in the form data OG
        # submission = request.form['submission']
        # query = request.form['query']
        
        #take in the csv's from the fomr
        virtualMachines = request.files['virtualMachines']
        images = request.files['images']
        
        
        if virtualMachines:
            #if the file exists, delete it
            if os.path.exists('static/csv/virtualMachines.csv'):
                os.remove('static/csv/virtualMachines.csv')
                print('File deleted')
            #write the file to the csv folder
            virtualMachines.save('static/csv/virtualMachines.csv')
            print('File saved')
            
        #as above so below    
        if images:
            if os.path.exists('static/csv/images.csv'):
                os.remove('static/csv/images.csv')
                print('File deleted')
            images.save('static/csv/images.csv')
            print('File saved')
        
        #this rus the experiment on the uploaded test data and then redirects
        # data = TestRun.run_experiment(images, virtualMachines)
        
        
        #redirect to the index page
        return redirect(url_for('index'))
        
        
          
    if request.method == 'GET':
        #static paths
        ImagePath =  'static/csv/images.csv'
        VM_Path = 'static/csv/virtualMachines.csv'
        
        #this runs the experiment on the uploaded test data and returns the data
        data = TestRun.run_expirement()
        
        #then I need to write this data to a csv file acting as back end for the graphing
        write_to_csv = graphing.data_to_csv(data)
        
        #then I need a graphing helper that takes in static csv and then returns the data
        data_for_graphing = graphing.data_for_graphing()
        # print('data_for_graphing', data_for_graphing)
      
        #this is the data for the graphing  
            # algorithm = data_for_graphing[0]
            # knapsack = data_for_graphing[1]
            # recursive_knapsack = data_for_graphing[2]
            # dynamic = data_for_graphing[3]
            # static = data_for_graphing[4]
        
        #not sure if this is the best way to do this
        # data_for_graphing = graphing.csv_to_json()
        
        create_data_for_graphing = graphing.create_data_for_graphing()
        
        return render_template('index.html', 
                               the_title='AWS MQP', 
                               data=data,
                               data_for_graphing=data_for_graphing,
                               )

@app.route('/symbol.html')
def symbol():
    return render_template('symbol.html', the_title='Tiger As Symbol')

@app.route('/myth.html')
def myth():
    return render_template('myth.html', the_title='Tiger in Myth and Legend')

if __name__ == '__main__':
    app.run(debug=True)
    
