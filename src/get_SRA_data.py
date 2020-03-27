#!/usr/bin/python3

import os # import os
import sys # import sys to use parameters

params = sys.argv # get list of parameters

acc_list = None # initialize path to file containing accession numbers
out_path = None # initialize path to output directory

for i in range(len(params)-1): # loop through parameters
    if params[i] == '-a' or params[i] == '--acc_list':
        acc_list = params[i+1] # set acc list
    if params[i] == '-o' or params[i] == '--output':
        out_path = params[i+1] # set output directory

if acc_list == None or out_path == None : #check that parameters have been set
    print('Error: Invalid input parameters. \nSet path to accession list with -a or --acc_list parameters. \nSet output path with -o or --output.') #error to output

else:
    SRR = [] #list to store SRR numbers

    with open(acc_list, 'r') as f: #open file containing accession numbers
        for line in f:
            if line.startswith("SRR") or line.startswith("ERR"):
                SRR.append(line.strip()) #add each accession number to SRR list

    for acc in SRR: #loop through acc numbers
        os.system('fastq-dump -O ' + str(out_path) + ' -I --split-files ' + str(acc)) #call fastq-dump command to output fastq files in data folder

