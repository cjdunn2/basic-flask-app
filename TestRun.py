import pandas as pd
import random
import csv
import numpy as np
import time

#i need to take in the csv files from static and then run the model on them
"""
    Create a list of virtual machines, where each virtual machine is represented as a tuple of (x, y, z), where x is the cost,
    y is the max cpu capabilities, and z is the max ram capabilities.
    
Create a list of images, where each image is represented as a tuple of (y, z), where y is the cpu cost and z is the ram cost.

Initialize a 2-dimensional array of size (n+1) x (m+1), where n is the number of virtual machines and m is the number of images. 
The (i,j)-th element of the array represents the minimum cost to run the first i virtual machines while processing the first j images.

Set the first row and first column of the array to 0.

For each virtual machine i from 1 to n, and each image j from 1 to m, do the following:
    a. If the cpu cost of the j-th image is greater than the max cpu capabilities of the i-th virtual machine or if the ram cost of the j-th image is greater than the max ram capabilities of the i-th virtual machine, set the (i,j)-th element of the array to the value of the (i-1,j)-th element.
    b. Otherwise, set the (i,j)-th element of the array to the minimum of the following:
        i. The (i-1,j)-th element, which represents the cost of not using the i-th virtual machine to process the j-th image.
        ii. The (i-1,j-1)-th element plus the cost of using the i-th virtual machine to process the j-th image, which is the cost of the virtual machine plus the cost of the image.
Return the (n,m)-th element of the array, which represents the minimum cost to run all virtual machines while processing all images.
    """
    
#First a method to parse the csv files into a list of tuples

def parse_csv(file):
    with open(file, 'r') as f:
        #i need to parse the values into integers
        reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        next(reader)    
        listForReturn = [[int(x) for x in row] for row in reader]
        f.close()
        return listForReturn
    
# def parse_csv_old(file):
#     with open(file, 'r') as f:
#         #i need to parse the values into integers
#         reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#         next(reader)    
#         listForReturn = [[int(x) for x in row] for row in reader]
#         return listForReturn
       


#I Keep using workloads and images as the same thing lol

def allocate_vms(vms, workloads):
    #start timer
    sTime = time.time()
    # Sort vms by cost
    vms.sort(key=lambda x: x[3])
    # Create a dictionary to store which vm is allocated to which workload
    allocation = {}
    # Initialize the total cost to 0
    total_cost = 0
    #missed workloads
    missed = []
    # Iterate over each workload
    for workload in workloads:
        # Find the least expensive vm that can accommodate the workload
        best_vm = None
        for vm in vms:
            if vm[1] >= workload[1] and vm[2] >= workload[2]:
                if best_vm is None or vm[3] < best_vm[3]:
                    best_vm = vm
        # If a suitable vm is found, allocate the workload to it
        if best_vm is not None:
            #make copy so we can find it later
            copy = best_vm
            #dictionary of workloads id = best vm id, make better data to figure this out
            allocation[workload[0]] = best_vm[0]
            total_cost += best_vm[3]
            # Decrement the vm's resources
            best_vm = (best_vm[0], best_vm[1] - workload[1], best_vm[2] - workload[2], best_vm[3])
            #this line is wrong below
            # vms[vms.index((best_vm[0], best_vm[1] + workload[1], best_vm[2] + workload[2], best_vm[3]))] = best_vm
            #take the index of the copy and replace it with the new best vm
            vms[vms.index(copy)] = best_vm
        #if no suitable vm is found, return an error
        else:
            missed.append(workload[0])
    # Return the allocation and the total cost
    #this will return a dictionary of workload id = vm id
    #i want it to return a dictionary of vm id = workload id
    #but maybe I should do that in the frontend
    eTime = time.time()
    fTime = eTime - sTime
    allocation = {v: k for k, v in allocation.items()}
    return allocation, total_cost, fTime, missed

#here is the somewhat knapsack version (terrible)
def knapsack_vms(workloads, vms):
    #start timer
    sTime = time.time()
    #missed workloads
    missed = []
    # Create a dictionary to store the cost and resource usage of each vm
    vm_usage = {vm[0]: [vm[3], vm[1], vm[2]] for vm in vms}
    # Create a dictionary to store the vm used for each workload
    workload_vms = {}

    # Sort the vm list by cost in ascending order
    vms_sorted = sorted(vms, key=lambda x: x[3])

    # Iterate through the workloads and assign them to the least expensive vm that has enough resources
    for workload in workloads:
        assigned_vm = None
        for vm in vms_sorted:
            if vm_usage[vm[0]][1] >= workload[1] and vm_usage[vm[0]][2] >= workload[2]:
                assigned_vm = vm[0]
                vm_usage[vm[0]][1] -= workload[1]
                vm_usage[vm[0]][2] -= workload[2]
                break
        if assigned_vm is None:
            missed.append(workload[0])
        workload_vms[workload[0]] = assigned_vm

    # Compute the total cost
    total_cost = sum([vm_usage[vm][0] for vm in vm_usage])
    eTime = time.time()
    fTime = eTime - sTime
    #this returns a dictionary of workload id = vm id, and the total cost
    return workload_vms, total_cost, fTime, missed

#This is the original recursive knapsack version of the algorithm
def recursive_knapsack_vms(workloads, vms):
    #start timer
    sTime = time.time()
    #missed workloads
    missed = []
    # Create a dictionary to store the cost and resource usage of each vm
    vm_usage = {vm[0]: [vm[3], vm[1], vm[2]] for vm in vms}
    # Create a dictionary to store the vm used for each workload
    workload_vms = {}

    def helper(workload_index, vm_usage):
        nonlocal workload_vms

        # Base case: all workloads have been assigned to a VM
        if workload_index >= len(workloads):
            return sum([vm_usage[vm][0] for vm in vm_usage])

        # Recursive case: try to assign the current workload to each available VM
        current_workload = workloads[workload_index]
        min_cost = float('inf')
        for vm_id in vm_usage.keys():
            if vm_usage[vm_id][1] >= current_workload[1] and vm_usage[vm_id][2] >= current_workload[2]:
                new_vm_usage = vm_usage.copy()
                new_vm_usage[vm_id][1] -= current_workload[1]
                new_vm_usage[vm_id][2] -= current_workload[2]
                cost = helper(workload_index + 1, new_vm_usage)
                if cost < min_cost:
                    min_cost = cost
                    workload_vms[current_workload[0]] = vm_id

        return min_cost

    total_cost = helper(0, vm_usage)
    eTime = time.time()
    fTime = eTime - sTime
    #this returns a dictionary of workload id = vm id, and the total cost
    return workload_vms, total_cost, fTime, missed


#Our first attempt at dynamic programming with knapsack to solve the issue
def dynamic_knapsack_vms(workloads, vms):
    #start timer
    sTime = time.time()
    #missed workloads
    missed = []
    # Create a dictionary to store the cost and resource usage of each vm
    vm_usage = {vm[0]: [vm[3], vm[1], vm[2]] for vm in vms}
    # Create a 2D array to store the minimum cost to use a subset of the workloads with a subset of the vms
    min_cost = [[float('inf') for _ in range(len(vms) + 1)] for _ in range(len(workloads) + 1)]
    # Initialize the first row and column to 0 (base cases)
    for i in range(len(vms) + 1):
        min_cost[0][i] = 0
    for i in range(len(workloads) + 1):
        min_cost[i][0] = 0

    # Calculate the minimum cost for all subsets of workloads and vms
    for i in range(1, len(workloads) + 1):
        current_workload = workloads[i - 1]
        for j in range(1, len(vms) + 1):
            current_vm = vm_usage[vms[j - 1][0]]
            # If the current vm has enough resources for the current workload, try to assign it to the vm
            if current_vm[1] >= current_workload[1] and current_vm[2] >= current_workload[2]:
                # If the cost of assigning the current workload to the current vm is less than the minimum cost so far,
                # update the minimum cost for this subset of workloads and vms
                if current_vm[0] + min_cost[i - 1][j - 1] < min_cost[i - 1][j]:
                    min_cost[i][j] = current_vm[0] + min_cost[i - 1][j - 1]
                else:
                    min_cost[i][j] = min_cost[i - 1][j]
            else:
                min_cost[i][j] = min_cost[i - 1][j]

    # Backtrack through the 2D array to determine which vms were used for each workload
    workload_vms = {}
    i, j = len(workloads), len(vms)
    while i > 0 and j > 0:
        current_workload = workloads[i - 1]
        current_vm = vms[j - 1]
        # print('MinCost: ', min_cost[i][j], ' CurrentVM: ', current_vm[3] + min_cost[i - 1][j - 1], ' CurrentWorkload: ', current_workload[1], ' ', current_workload[2])
        #this condidtion is never met ecause min cost i,j is 0 always?
        #I need to figure out why this is happening
        if min_cost[i][j] == current_vm[3] + min_cost[i - 1][j - 1] and current_vm[1] >= current_workload[1] and current_vm[2] >= current_workload[2]:
            workload_vms[current_workload[0]] = current_vm[0]
            i -= 1
            j -= 1
        else:
            i -= 1

    # Reverse the order of the workload_vms dictionary so the workloads are in the original order
    workload_vms = {k: workload_vms[k] for k in reversed(workload_vms)}
    #this returns a dictionary of workload id = vm id, and the total cost
    eTime = time.time()
    fTime = eTime - sTime
    #this is so broken
    return workload_vms, min_cost[-1][-1], fTime, missed

#This is the dynamic approach to the algorithm
def find_least_expensive_vm(vm_list, workload):
    # Given a list of VMs and a workload, find the least expensive VM that can handle the workload.
    valid_vms = [vm for vm in vm_list if vm[1] >= workload[1] and vm[2] >= workload[2]]
    if not valid_vms:
        return None
    return min(valid_vms, key=lambda vm: vm[3])


def assign_workloads(workload_list, vm_list):
    #start timer
    sTime = time.time()
    #missed workloads
    missed = []
    # Assign each workload in the list to the least expensive available VM.
    assigned_vms = []
    total_cost = 0

    for workload in workload_list:
        vm = find_least_expensive_vm(vm_list, workload)
        if vm is None:
            missed.append(workload[0])
            # raise Exception("No valid VM found for workload {}".format(workload[0]))

        assigned_vms.append(vm[0])
        total_cost += vm[3]
        vm_list.remove(vm)
        vm_list.append((vm[0], vm[1]-workload[1], vm[2]-workload[2], vm[3]))
    #this returns a list of vm ids, and the total cost
    eTime = time.time()
    fTime = eTime - sTime
    return assigned_vms, total_cost, fTime, missed

#static attempt balancing two dictionarys
def find_least_expensive_vm_static(vm_list, workload):
    # Given a list of VMs and a workload, find the least expensive VM that can handle the workload.
    valid_vms = [vm for vm in vm_list if vm[1] >= workload[1] and vm[2] >= workload[2]]
    if not valid_vms:
        return None
    return min(valid_vms, key=lambda vm: vm[3])


def assign_workloads_static(workload_list, vm_list):
    # Assign each workload in the list to the least expensive available VM.
    #start timer
    sTime = time.time()
    missed_workloads = []
    assigned_vms = []
    total_cost = 0
    vm_resources = {vm[0]: (vm[1], vm[2]) for vm in vm_list}
    vm_costs = {vm[0]: vm[3] for vm in vm_list}

    for workload in workload_list:
        valid_vms = [(vm_id, resources) for vm_id, resources in vm_resources.items() if resources[0] >= workload[1] and resources[1] >= workload[2]]
        if not valid_vms:
            missed_workloads.append(workload[0])
            continue
            # raise Exception("No valid VM found for workload {}".format(workload[0]))

        vm_id = min(valid_vms, key=lambda vm: vm_costs[vm[0]])[0]
        assigned_vms.append(vm_id)
        total_cost += vm_costs[vm_id]
        vm_resources[vm_id] = (vm_resources[vm_id][0] - workload[1], vm_resources[vm_id][1] - workload[2])
    eTime = time.time()
    fTime = eTime - sTime
    return assigned_vms, total_cost, fTime, missed_workloads

#this is the method the route will call
# def run_experiment(workload_list, vm_list):
def run_expirement():
    # parse the csv files
    vms = parse_csv('static/csv/vms.csv')
    images = parse_csv('static/csv/images.csv')
    
    Algorithm1 = allocate_vms(vms, images)
    Knapsack = knapsack_vms(images, vms)
    Recursive_Knapsack = recursive_knapsack_vms(images, vms)
    Dynamic = assign_workloads(images, vms)    
    Static = assign_workloads_static(images, vms)
    
    answer = [Algorithm1, Knapsack, Recursive_Knapsack, Dynamic, Static]
    
    return answer

   
if __name__ == "__main__":
    #these are the csv files that will be parsed
    vms = parse_csv('static/csv/vms.csv')
    images = parse_csv('static/csv/images.csv')
    
        
    #run the model on the parsed csv files
    Algorithm1 = allocate_vms(vms, images)
    print('\nAlgorithm Working?\n' , Algorithm1)
    
    #run the knapsack model on the parsed csv files
    Knapsack = knapsack_vms(images, vms)
    print('\nKNAPSACK?\n', Knapsack)
    
    #run the recursive knapsack model on the parsed csv files
    Recursive_Knapsack = recursive_knapsack_vms(images, vms)
    print('\nRecursive Knapsack?\n', Recursive_Knapsack)
    
    #run the dynamic knapsack model on the parsed csv files
    # Dynamic_Knapsack = dynamic_knapsack_vms(images, vms)
    # print('Dynamic Knapsack?\n', Dynamic_Knapsack)
    
    Dynamic = assign_workloads(images, vms)
    print('\nDynamic?\n', Dynamic)
    
    Static = assign_workloads_static(images, vms)
    print('\nStatic?\n', Static)
    
    #now I need all of these methods to be usable from the web app
    
    
    
    