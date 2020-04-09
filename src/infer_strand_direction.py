#!/usr/bin/python3

import os
import sys

params = sys.argv # get list of parameters

bam_dir = None # path to directory containing bams
ref_seq_bed = None # path to refseq bed file

for i in range(len(params)-1):
    if params[i] == '-d' or params[i] == '--bam_dir':
        bam_dir = params[i+1]
        if not bam_dir.endswith('/'):
            bam_dir = bam_dir + '/'
    elif params[i] == '-r' or params[i] == '--ref_seq_bed':
        ref_seq_bed = params[i+1]

if bam_dir == None or ref_seq_bed == None: 
    print('Error: Invalid input parameters. \n Set path to bam directory using -d or --bam_dir. \nSet path to reference directory using -r or --ref_seq_bed.')
else:
    for file in os.listdir(str(bam_dir)):
        if file.endswith('.bam'):
            cmd = 'infer_experiment.py -r ' + str(ref_seq_bed) + ' -s 2000000 -i ' + str(bam_dir) + str(file)
            os.system(cmd)
