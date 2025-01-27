#!/usr/bin/python3

# import libraries
import os
import sys

#path to main script
wd = sys.path[0] + '/'  # get script location
os.system('echo ' + wd)

# get parameters
params = sys.argv

# initialize parameter variables
ref_urls = None # path to tab delimited file containing reference data urls
output = None # path to output directory
rna_acc = None # path to file containing RNA SRA accession numbers
dna_acc = None # path to file containing DNA SRA accession numbners
chrNum = None # chromosome to filter (must be in format chr#)

# loop through parameters
for i in range(len(params)-1):
    if params[i] == '-ru' or params[i] == '--reference_urls':
        ref_urls = params[i+1] # set ref_urls
    elif params[i] == '-o' or params[i] == '--output':
        output = params[i+1] # set output
        if not output.endswith('/'):
            output = output + '/' # add / 
    elif params[i] == '-ra' or params[i] == '--rna_acc':
        rna_acc = params[i+1] # set rna_acc
    elif params[i] == '-da' or params[i+1] == '--dna_acc':
        dna_acc = params[i+1] # set dna_acc
    elif params[i] == '-chr' or params[i] == '--chr_num':
        chrNum = params[i+1]
         

# usage information
def usage():
    print("""
    Invalid Parameters. Set parameters with: 
    -ru or --reference_urls: path to tab delimited file containing reference data urls
    -o or --output: path to output directory
    -ra or --rna_acc: path to file containing RNA SRA accession numbers
    -da or --dna_acc: path to file containing DNA SRA accession numbers
    -chr or --chr_num: chromosome to filter (must be in format chr#)
    """)

# check parameters set
if ref_urls is None or output is None or rna_acc is None or dna_acc is None:
    os.system('date') # print date
    usage() # call usage function
    sys.exit() # exit program

# Create Directories
rna_fastq = output + 'rna_fastq/' # set path to directory containing rna fastq files
rna_fastq_trimmed = rna_fastq + 'trimmed/' # set path to directory containing trimmed rna fastq files
rna_bam = output + 'rna_bam/' # set path to directory containing rna bam files
dna_bam = output + 'dna_bam/' #set path to directory containing dna bam files
dna_fastq = output + 'dna_fastq/' #set path to directory containing dna fastq files
fastqc = output + 'fastqc/' # set path to directory containing fastqc reports
reference = output + 'reference/' # set path to directory containing reference information
star_index = reference + 'STAR_index/' # set path to directory containng star index
redi_table = output + 'redi_table/' # set path to directory containing reditools output tables

# Make directories
def mk_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

mk_dir(rna_fastq)
mk_dir(rna_fastq_trimmed)
mk_dir(rna_bam)
mk_dir(dna_bam)
mk_dir(dna_fastq)
mk_dir(fastqc)
mk_dir(reference)
mk_dir(star_index)
mk_dir(redi_table)


# Download Reference Data
cmd  = 'python3 ' + str(wd) + 'src/get_ref_data_annotations.py -i ' + str(ref_urls) + ' -o ' + str(reference) # command to download reference data
os.system('date') # print date
os.system('echo ' + cmd)
os.system(cmd)

# Update directory paths
genome = reference + 'genome/' # set path to genome directory
genome_annotation = reference + 'genome_annotation/' # get path to genome annotation directory
strand_detection = reference + 'strand_detection/' # get path to strand detection directory
rmsk = reference + 'rmsk/' # set path to rmsk directory
dbSNP = reference + 'dbSNP/'
rediportal = reference + 'rediportal_db/'

# Download RNAseq Reads
cmd = 'python3 ' + str(wd) + 'src/get_SRA_reads.py -a ' + str(rna_acc) + ' -o ' + str(rna_fastq)
os.system('date')
os.system('echo ' + cmd)
os.system(cmd)

# Download DNAseq Reads
cmd = 'python3 ' + str(wd) + 'src/get_SRA_reads.py -a ' + str(dna_acc) + ' -o ' + str(dna_fastq)
os.system('date')
os.system('echo ' + cmd)
os.system(cmd)

# Quality Check RNAseq Reads
cmd = 'python3 ' + str(wd) + 'src/fastqc.py -f ' + str(rna_fastq) + ' -o ' + str(fastqc)
os.system('date')
os.system('echo ' + cmd)
os.system(cmd)

# Quality Check DNAseq Reads
cmd = 'python3 ' + str(wd) + 'src/fastqc.py -f ' + str(dna_fastq) + ' -o ' + str(fastqc)
os.system('date')
os.system('echo ' + cmd)
os.system(cmd)

# Index genome BWA
cmd = 'python3 ' + str(wd) + 'src/index_genome_bwa.py ' + str(genome) + '*.fa'
os.system('date')
os.system('echo ' + cmd)
os.system(cmd)

# Index genome STAR
cmd = 'python3 ' + str(wd) + 'src/index_genome_STAR.py -f ' + str(genome) + '*.fa -a ' + str(genome_annotation) + ' -o ' + str(star_index)
os.system('date')
os.system('echo ' + cmd)
os.system(cmd)

# Align Reads BWA
cmd = 'python3 ' + str(wd) + 'src/align_BWA.py -fq ' + str(dna_fastq) + ' -fa ' + str(genome)
os.system('date')
os.system('echo ' + cmd)
os.system(cmd)

# Select Specific Chromosome
cmd = 'python3 ' + str(wd) + 'src/select_map_chr.py -g ' + str(genome) + ' -s ' + str(dna_fastq) + ' -o ' + str(dna_bam) + ' -chr ' + str(chrNum)
os.system('date')
os.system('echo ' + cmd)
os.system(cmd)

# Quality trim RNA Reads
cmd = 'python3 ' + str(wd) + 'src/fastp.py -f ' + str(rna_fastq) + ' -o ' + str(rna_fastq_trimmed) 
os.system('date')
os.system('echo ' + cmd)
os.system(cmd)

# Align Reads STAR
cmd = 'python3 ' + str(wd) + 'src/align_STAR.py -f ' + str(rna_fastq_trimmed) + ' -g ' + str(star_index) + ' -o ' + str(rna_bam)
os.system('date')
os.system('echo ' + cmd)
os.system(cmd)

# Infer Strand Orientation
cmd = 'python3 ' + str(wd) + 'src/infer_strand_direction.py -d ' + str(rna_bam) + ' -r ' + str(output) + 'strand_detection/'
os.system('date')
os.system('echo ' + cmd)
os.system(cmd)

