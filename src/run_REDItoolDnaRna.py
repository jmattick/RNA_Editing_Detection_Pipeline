#!/usr/bin/python3

import os
import sys

params = sys.argv # get list of parameters

rna_bam_dir = None # path to directory containing rna bam files
dna_bam = None # path dna bam file
output = None # path to output results
genome = None # path to genome fasta 
chr_region = None # chromosome coordinates for analysis (chrX:1-...)

for i in range(len(params)-1):
    if params[i] == '-r' or params[i] == '--rna_bam_dir':
        rna_bam_dir = params[i+1]
        if not rna_bam_dir.endswith('/'):
            rna_bam_dir = rna_bam_dir + '/'
    elif params[i] == '-d' or params[i] == '--dna_bam':
        dna_bam = params[i+1]
    elif params[i] == '-o' or params[i] == '--ouput':
        output = params[i+1]
    elif params[i] == '-g' or params[i] == '--genome':
        genome = params[i+1]
    elif params[i] == '-chr' or params[i] == '--chr_region':
        chr_region = params[i+1]


for file in os.listdir(str(rna_bam_dir)): 
    if file.endswith('.bam'):
        rna_bam = rna_bam_dir + file
        cmd = 'python3 ../REDItools_python3/main/REDItoolDnaRna.py -i ' + str(rna_bam) + ' -j ' + str(dna_bam) + ' -o ' + str(output) + ' -f ' + str(genome) + ' -t10 -c1,1 -m30,255 -v1 -q30,30 -e -n0.0 -N0.0 -u -l -p -s2 -g2 -S -Y ' + str(chr_region)
        os.system(cmd) # run command 

