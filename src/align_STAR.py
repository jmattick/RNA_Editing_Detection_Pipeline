#!/usr/bin/python3

import os
import sys

params = sys.argv #input parameters

fastq_dir = None # path to directory containing fastq files
idx = None # path to genome index
output = None #path to output directory

for i in range(len(params)-1): #loop through parameters
    if params[i] == '-f' or params[i] == '--fastq_dir': #if parameter is fastq directory
        fastq_dir = params[i + 1] #set email
    elif params[i] == '-g' or params[i] == '--genome_idx': #if parameter is genome index
        idx = params[i+1]
    elif params[i] == '-o' or params[i] == '--output': #if parameter is output path
        output = params[i+1]
        if not output.endswith('/'):
            output = output + '/'


if fastq_dir == None or idx == None or output == None:
    print('Error: Invalid input parameters. \nSet fastq directory with -f or --fastq_dir.\nSet path to directory containing genome index with -g or --genome_acc.\nSet path to result output directory with -o or --output.')
else:

    for file in os.listdir(str(fastq_dir)): #loop through files in data directory
        if file.endswith('_1.fastq'): #if file is first read in pair
            base = file.split('_1.fastq')[0] #get basename of file
            r1 = str(fastq_dir) + str(base) + '_1.fastq' #path to read 1
            r2 = str(fastq_dir) + str(base) + '_2.fastq' #path to read 2
            outname = base.split('/')[-1] #get name of file
            cmd = 'STAR --runThreadN 4 --genomeDir ' + str(idx) + ' --genomeLoad NoSharedMemory --outFileNamePrefix ' + str(output) + str(outname) +  '_ --outReadsUnmapped Fastx --outSAMtype BAM SortedByCoordinate --outSAMstrandField intronMotif --outSAMattributes All --outFilterType BySJout --outFilterMultimapNmax 1 --alignSJoverhangMin 8 --alignSJDBoverhangMin 1 --outFilterMismatchNmax 999 --outFilterMismatchNoverLmax 0.04 --alignIntronMin 20 --alignIntronMax 1000000 --alignMatesGapMax 1000000 --readFilesIn ' + str(r1) + ' ' + str(r2) # STAR command
            print('Aligning reads with STAR')
            print(cmd)
            os.system(cmd)
