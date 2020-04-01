#!/usr/bin/python3

import os
import sys

params = sys.argv # get parameters

fastq_dir = None # path to fastq directory
output = None # path to output directory
se = False # single end data boolean

# Loop through parameters
for i in range(len(params)-1):
        if params[i] == '-f' or params[i] == '--fastq_dir':
                fastq_dir = params[i + 1]
        elif params[i] == '-o' or params[i] == '--output':
                output = params[i + 1]
        elif params[i] == '-se' or params[i] == '--single_end':
                se = True

# Confirm parameters set
if fastq_dir == None or output == None:
        print('Error: Invalid input parameters. \nSet fastq directory with -f or --fastq_dir. \nSet output directory with -o or --output.')
        sys.exit()

# Loop through files in fastq directory
for file in os.listdir(str(fastq_dir)):
        if file.endswith('_1.fastq') and not se: # if first paired-end file
                base = file.split('_1.fastq')[0]
                r1 = str(fastq_dir) + str(base) + '_1.fastq'
                r2 = str(fastq_dir) + str(base) + '_2.fastq'
                os.system('fastqc -o ' + str(output) + ' ' + str(r1) + ' ' + str(r2)) # PE fastqc command
        elif file.endswith('_2.fastq'): # if second paired-end file
                pass # ignore
        elif file.endswith('.fastq'): # if single-end data
                base = file.split('.fastq')[0]
                r1 = str(fastq_dir) + str(base) + '.fastq'
                os.system('fastqc -o ' + str(output) + ' ' + str(r1)) # SE fastqc command
        else:
                print(str(file) + ' is not a fastq file')
