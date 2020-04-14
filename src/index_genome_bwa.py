#!/usr/bin/python3

import os 
import sys

params = sys.argv # get parameters

fasta_dir = None # path to genome fasta file

# Loop through parameters
for i in range(len(params)-1):
    if params[i] == '-f' or params[i] == '--fasta_dir':
        fasta = params[i+1]

# Confirm parameters set
if fasta_dir == None:
        print('Error: Invalid input parameters. \nSet fasta directory with -f or --fasta_dir.')
        sys.exit()
else:
    for file in os.listdir(str(fasta_dir)): #loop through files in data directory
        if file.endswith('.fa'): #if file is first read in pair
            base = file.split('.fa')[0] #get basename of file
            r = str(fasta_dir) + str(base) + '.fa' #path to genome file
            
    print('Indexing genome for BWA: ')
    cmd = 'bwa index ' + r
    print(cmd)
    os.system(str(cmd))
