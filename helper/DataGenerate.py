import pandas as pd
import numpy as np
import random
import csv
import os.path


# Generate data for the model

#I need to have a function that creates two csv files
    #one for the virtual machines that will have the following values:
        #VM_ID
        #VM_Cost
        #VM_CPU
        #VM_RAM
    #one for the images run through the virtual machines that will have the following values:
        #Image_ID
        #CPU_Cost
        #RAM_Cost
        
        
NUMBER_OF_VMS = 100
MAX_MEMORY = 100        
        
def generate_vms(num_vm: int) -> pd.DataFrame:
    
        ram = np.random.randint(10, size=num_vm)
        cpu = np.random.randint(10, size=num_vm)
        cost = np.random.randint(100, size=num_vm)

        ids = np.arange(num_vm)

        return pd.DataFrame({
            'VM_ID': ids,
            'Max_Ram': ram,
            'Max_CPU': cpu,
            'Cost': cost
        })
 
def generate_images(num_images: int) -> pd.DataFrame:
     
        ram = np.random.randint(4, size=num_images)
        cpu = np.random.randint(4, size=num_images)

        ids = np.arange(num_images)

        return pd.DataFrame({
            'Image_ID': ids,
            'Max_Ram': ram,
            'Max_CPU': cpu,
        })
        
if __name__ == "__main__":
    vms = generate_vms(NUMBER_OF_VMS)
    images = generate_images(NUMBER_OF_VMS)
    
    #I then need to save these csv's to the csv directory in this local
    vms.to_csv('vms.csv', index=False, header=False)
    images.to_csv('images.csv', index=False, header=False)
    
    
    
    # vms.to_csv(os.path.join('./static/csv', 'vms.csv'), index=False, header=False)
    # images.to_csv(os.path.join('./static/csv/', 'images.csv'), index=False, header=False)
    
    # os.path.join('./csv', 'vms.csv')
    
    

    # print('VMS:\n', vms)
    # print('Images:\n', images)
    


    
        
