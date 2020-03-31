#!/usr/bin/python3

import os # import os
import sys # import sys to use parameters

params = sys.argv # get list of parameters

data_list = None # initialize path to directory containing fastq files
out_path = None # initialize path to output directory

for i in range(len(params)-1): # loop through parameters
    if params[i] == '-a' or params[i] == '--data_list':
        data_list = params[i+1] # set acc list
    if params[i] == '-o' or params[i] == '--output':
        out_path = params[i+1] # set output directory

if data_list == None or out_path == None : #check that parameters have been set
    print('Error: Invalid input parameters. \nSet path to accession list with -a or --acc_list parameters. \nSet output path with -o or --output.') #error to output

else:
        
    for filename in os.listdir(data_list):
        if filename.endswith(".fastq"): 
            os.system('fastqc -O '+str(out_path) + ' ' + filename) #call fastqc command to perform quality control in data folder 
        else:
            continue
