#!/usr/bin/python3

import os
import sys

params = sys.argv #input parameters

genome_dir = None # path to directory containing fa.fai file
sam_dir = None # path to directory containing sam file
output_dir = None # path to store output files
chrNum = None # select the chromosome number

for i in range(len(params)-1): #loop through parameters
    if params[i] == '-g' or params[i] == '--genome_dir': #if parameter is fa.fai file directory
        genome_dir = params[i + 1]
    elif params[i] == '-s' or params[i] == '--sam_dir': #if parameter is the sam file directory
    	sam_dir = params[i+1]
    elif params[i] == '-o' or params[i] == '--output_dir': #if parameter is the sam file directory
    	output_dir = params[i+1] 
    elif params[i] == '-chr' or params[i] == '--chrNum': #if chromosome number is given
    	chrNum = params[i+1]

if genome_dir == None or sam_dir == None or chrNum == None or output_dir == None:
    print('Error: Invalid input parameters. \nSet fai directory with -f or --genome_dir.\nSet sam directory with -s or --sam_dir.\nSet output directory with -o or --out_dir.\nEnter the number of chromosome with -ch or --chrNum (e.g. -ch chr21 or --chrNum chr21).')

else:
	for file in os.listdir(str(genome_dir)): #loop through files in data directory
        if file.endswith('.fai'): #if file is fai file
            base = file.split('.fai')[0] #get basename of file
            r = str(genome_dir) + str(base) + '.fai' #path to fai file
            cmd = 'awk \'/^' + chrNum + '\t/ {printf(\"%s\t0\t%s\n\",$1,$2);}\' ' + r + ' > ' + str(output_dir) + chrNum + '.bed'
            os.system(cmd)

	
	for file in os.listdir(str(sam_dir)): #loop through files in data directory
        if file.endswith('.sam'): #if file is sam file
            base = file.split('.sam')[0] #get basename of file
            r = str(sam_dir) + str(base) + '.sam' #path to sam file
            outname = base.split('/')[-1] #get name of the sam file
            cmd = 'samtools view -b -F4 -L ' + str(output_dir) + chrNum + '.bed ' + '-o' + str(output_dir) + chrNum + '.bam -@ 4 ' + r
			os.system(cmd)
			os.system('samtools sort ' + str(output_dir) + chrNum + '.bam > ' + str(output_dir) + 'sorted_' + chrNum + '.bam')
			os.system('samtools index ' + str(output_dir) + 'sorted_' + chrNum + '.bam')