#!/usr/bin/python3

import os 
import sys

params = sys.argv # get parameters

fasta = None # path to genome fasta file

# Loop through parameters
for i in range(len(params)-1):
    if params[i] == '-f' or params[i] == '--fasta':
        fasta = params[i+1]
    elif params[i] == '-a' or params[i] == '--gtf_annotation':
        gtf = params[i+1]
    elif params[i] == '-o' or params[i] == '--output':
        output = params[i+1]
        if not output.endswith('/'):
            output = output + '/'

print('Indexing genome: ')
cmd = 'bwa index ' +  + str(fasta)
print(cmd)

os.system(str(cmd))
