#!/usr/bin/python3

import os 
import sys

params = sys.argv # get list of parameters

in_file = None # path to file containing reference files
output = None # path to reference data directory
genome = None # genome file
genome_annotation = None # annotation file
strand_detection = None # refseq annotation file (bed)
rmsk = None # repeat master annotations
dbSNP = None # dbSNP annotations
rediportal_db = None #REDIportal annotations

#loop through input parameters 
for i in range(len(params)-1):
    if params[i] == '-i' or params[i] == '--input':
        in_file = params[i+1]
    if params[i] == '-o' or params[i] == '-output':
        output = params[i+1]
        if not output.endswith('/'):
            output = output + '/'

# Open input file and get file urls
with open(in_file, 'r') as f:
    for line in f:
        path = line.strip().split('\t')
        if len(path) < 2:
            print('Error in input file')
            continue
        else:
           k = path[0] # key of path 
           v = path[1] # value of path
           if k == "genome":
               genome = v
           elif k == "genome_annotation":
               genome_annotation = v
           elif k == "strand_detection":
               strand_detection = v
           elif k == "rmsk":
               rmsk = v
           elif k == "dbSNP":
               dbSNP = v
           elif k == "rediportal_db":
               rediportal_db = v

def make_dir(path):
    """Function to make a directory if it does not exist"""
    if not os.path.exists(path):
        os.makedirs(path)


def download_data(path, url):
    """Funciton to download data using wget"""
    print("Creating directory:")
    print(path)
    make_dir(path) # make directory from path
    print("Downloading data:")
    print(url)
    cmd = 'wget --no-check-certificate -P ' + str(path) + ' ' + str(url) # command to wget data into path
    os.system(cmd)
    cmd = 'gunzip ' + str(path) + '*' # command to unzip compressed data in path
    os.system(cmd)

# Setup directory paths for reference data
print('Creating output directories in ' + str(output))
genome_dir = str(output) + 'genome/'
genome_annotation_dir = str(output) + 'genome_annotation/'
strand_detection_dir = str(output) + 'strand_detection/'
rmsk_dir = str(output) + 'rmsk/'
dbSNP_dir = str(output) + 'dbSNP/'
rediportal_db_dir = str(output) + 'rediportal_db/'

# Make directories to hold reference data
download_data(genome_dir, genome)
download_data(genome_annotation_dir, genome_annotation)
download_data(strand_detection_dir, strand_detection)
download_data(rmsk_dir, rmsk)
download_data(dbSNP_dir, dbSNP)
download_data(rediportal_db_dir, rediportal_db)

