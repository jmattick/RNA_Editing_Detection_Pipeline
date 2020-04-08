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
rediportal2recoding = None # path to rediportal2recoding.py

#loop through input parameters 
for i in range(len(params)-1):
    if params[i] == '-i' or params[i] == '--input':
        in_file = params[i+1]
    elif params[i] == '-o' or params[i] == '--output':
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
           elif k == "rediportal2recoding":
               rediportal2recoding = v

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
download_data(strand_detection_dir, strand_detection)

download_data(genome_annotation_dir, genome_annotation)

genome_annotation_gtf_file_name = genome_annotation.split('/')[-1] #gets text after last / in url 
genome_annotation_splicesites_file_name = genome_annotation_gtf_file_name.split('.annotation.gtf')[0] + '.splicesites.txt'

os.system("gtf_splicesites" + str(genome_annotation_dir) + str(genome_annotation_gtf_file_name) + " > splicesites")
os.system('awk -F\" \" \'{split($2,a,\":\"); split(a[2],b,\".\"); if (b[1]>b[3]) print a[1],b[3],b[1],toupper(substr($3,1,1)),\"-\"; else print a[1],b[1],b[3],toupper(substr($3,1,1)),\"+\"}\' ' + str(genome_annotation_dir) + 'splicesites' + ' > ' + str(genome_annotation_dir) + str(genome_annotation_splicesites_file_name)) # creates gtf file  

download_data(rmsk_dir, rmsk)

rmsk_file_name = rmsk.split('/')[-1] #gets text after last / in url (rmsk.txt)
rmsk_gtf_file_name = rmsk_file_name.split('.txt')[0] + '.gtf' # creates gtf file name from txt file name
rmsk_sorted_gtf_file_name = rmsk_file_name.split('.txt')[0] + '.sorted.gtf'
rmsk_sorted_gtf_gz_file_name = rmsk_file_name.split('.txt')[0] + '.sorted.gtf.gz'

os.system('awk \'OFS=\"\t\"{print $6, \"rmsk_hg19\",$12,$7+1,$8,\".\",$10,\".\",\"gene_id \"\"$11\"\"; transcript_id \"\"$13\"\";\"}\' ' + str(rmsk_dir) + str(rmsk_file_name) + " > " + str(rmsk_dir) + str(rmsk_gtf_file_name)) # creates gtf file  
os.system("sort -k1,1 -k4,4n " + str(rmsk_dir) + str(rmsk_gtf_file_name) + ' > ' + str(rmsk_dir) + str(rmsk_sorted_gtf_file_name)) # creates sorted gtf file
os.system("bgzip -p gff " + str(rmsk_dir) + str(rmsk_sorted_gtf_file_name))
os.system("tabix -p gff " + str(rmsk_dir) + str(rmsk_sorted_gtf_gz_file_name))

download_data(dbSNP_dir, dbSNP)

dnSNP_file_name = dbSNP.split('/')[-1] #gets text after last / in url
dbSNP_gtf_file_name = dbSNP_file_name.split('.txt')[0] + '.gtf' # creates gtf file name from txt file name
dbSNP_sorted_gtf_file_name = dbSNP_file_name.split('.txt')[0] + '.sorted.gtf'
dbSNP_sorted_gtf_gz_file_name = dbSNP_file_name.split('.txt')[0] + '.sorted.gtf.gz'

os.system('awk \'OFS=\"\t\"{if ($11==\"genomic\" && $12==\"single\") print $2,\"ucsc_snp151_hg19\",\"snp\",$4,$4,\".\",$7,\".\",\"gene_id \"\"$5\"\"; transcript_id \"\"$5\"\";\"}\' ' + str(dbSNP_dir) + str(dbSNP_file_name) + " > " + str(dbSNP_dir) + str(dbSNP_sorted_gtf_file_name)) # creates gtf file  
os.system("sort -k1,1 -k4,4n " + str(dbSNP_dir) + str(dbSNP_gtf_file_name) + ' > ' + str(dbSNP_dir) + str(dbSNP_sorted_gtf_file_name)) # creates sorted gtf file
os.system("bgzip -p gff " + str(dbSNP_dir) + str(dbSNP_sorted_gtf_file_name))
os.system("tabix -p gff " + str(dbSNP_dir) + str(dbSNP_sorted_gtf_gz_file_name))

download_data(rediportal_db_dir, rediportal_db)
rediportal_db_file_name = rediportal_db.split('/')[-1] #gets text after last / in url
atlas_gtf_file_name = 'atlas.gtf'
atlas_gtf_gz_file_name = atlas_gtf_file_name + '.gz'

os.system('awk \'OFS=\"\t\"{sum+=1; print $1,\"rediportal\",\"ed\",$2,$2,\".\",$5,\".\"gene_id \"\"sum\"\"; transcript_id \"\"sum\"\";\"}\' ' + str(rediportal_db_dir) + str(rediportal_db_file_name) + " > " + str(rediportal_db_dir) + str(atlas_gtf_file_name))
os.system('python3 ' + str(rediportal2recoding) + 'rediportal2recoding.py' + ' ' + str(rediportal_db_dir) + str(rediportal_db_file_name) + ' > ' + str(rediportal_db_dir) + 'atlas_recoding.gff')
os.system("sort -k1,1 -k4,4n " + str(rediportal_db_dir) + 'atlas_recoding.gff' + ' > ' + str(rediportal_db_dir) + 'srtd_atlas_recoding.gff') # creates sorted gtf file
os.system("bgzip" + str(rediportal_db_dir) + 'srtd_atlas_recoding.gff')
os.system("tabix -p gff" + str(rediportal_db_dir) + 'srtd_atlas_recoding.gff')

# Create the nochr file for REDItools
os.system('grep \">\" ' + str(genome_dir) + str(genome) + ' | awk \'{if (substr($1,1,3)==\">GL\" print $2}\'' + ' > ' + str(genome_dir) + 'nochr')
