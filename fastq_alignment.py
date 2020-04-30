#!/usr/bin/python3

# import libraries
import os
import sys

#path to main script
wd = sys.path[0] + '/'  # get script location
os.system('echo ' + wd)
os.system('echo Starting fastq alignment.')
os.system('date')

# get parameters
params = sys.argv

# initialize parameter variables
genome = None # path to genome fasta file
output = None # path to output directory
rna_fastq = None # path to directory containing RNA fastq files 
dna_fastq = None # path to directory containing DNA fastq files
chrNum = None # chromosome to filter (must be in format chr#)
threads = 4 # number of threads to use for bwa

# loop through parameters
for i in range(len(params)-1):
    if params[i] == '-g' or params[i] == '--genome':
        genome = params[i+1] # set genome fasta
    elif params[i] == '-a' or params[i] == '--genome_annotation':
        genome_ann = params[i+1]
    elif params[i] == '-o' or params[i] == '--output':
        output = params[i+1] # set output
        if not output.endswith('/'):
            output = output + '/' # add / 
    elif params[i] == '-r' or params[i] == '--rna_fastq':
        rna_fastq = params[i+1] # set rna fastq directory
        if not rna_fastq.endswith('/'):
            rna_fastq = rna_fastq + '/'
    elif params[i] == '-d' or params[i+1] == '--dna_fastq':
        dna_fastq = params[i+1] # set dna fastq directory
        if not dna_fastq.endswith('/'):
            dna_fastq = dna_fastq + '/'
    elif params[i] == '-chr' or params[i] == '--chr_num':
        chrNum = params[i+1]
    elif params[i] == '-t' or params[i] == '--threads':
        threads = params[i+1]
         

# usage information
def usage():
    print("""
    Invalid Parameters. Set parameters with: 
    -g or --genome: path to genome fasta file
    -a or --genome_annotation: path to genome annotation file
    -o or --output: path to output directory
    -r or --rna_fastq: path to directory containing rna fastq files
    -d or --dna_fastq: path to directory containing dna fastq files
    -chr or --chr_num: chromosome to filter (must be in format chr#)
    -t or --threads: number of threads to use for BWA (default = 4)
    """)

# check parameters set
if genome is None or output is None or rna_fastq is None or dna_fastq is None:
    os.system('date') # print date
    usage() # call usage function
    sys.exit() # exit program

# Create Directories
rna_fastq_trimmed = rna_fastq + 'trimmed/' # set path to directory containing trimmed rna fastq files
rna_bam = output + 'rna_bam/' # set path to directory containing rna bam files
dna_bam = output + 'dna_bam/' #set path to directory containing dna bam files
fastqc = output + 'fastqc/' # set path to directory containing fastqc reports
genome_dir = os.path.dirname(genome) # set path to genome directory
if not genome_dir.endswith('/'): # check for ending
    genome_dir = genome_dir + '/'
star_index = genome_dir + 'STAR_index/' # set path to directory containng star index

# Make directories
def mk_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

mk_dir(rna_fastq_trimmed)
mk_dir(rna_bam)
mk_dir(dna_bam)
mk_dir(fastqc)
mk_dir(star_index)

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
cmd = 'python3 ' + str(wd) + 'src/index_genome_bwa.py -f ' + str(genome_dir)
os.system('date')
os.system('echo ' + cmd)
os.system(cmd)

# Index genome STAR
cmd = 'python3 ' + str(wd) + 'src/index_genome_STAR.py -f ' + str(genome) + ' -a ' + str(genome_ann) + ' -o ' + str(star_index)
os.system('date')
os.system('echo ' + cmd)
os.system(cmd)

# Align Reads BWA
cmd = 'python3 ' + str(wd) + 'src/align_BWA.py -fq ' + str(dna_fastq) + ' -fa ' + str(genome)
os.system('date')
os.system('echo ' + cmd)
os.system(cmd)

# Select Specific Chromosome
if chrNum is not None:
    cmd = 'python3 ' + str(wd) + 'src/select_map_chr.py -g ' + str(genome) + ' -s ' + str(dna_fastq) + ' -o ' + str(dna_bam) + ' -chr ' + str(chrNum)
    os.system('date')
    os.system('echo ' + cmd)
    os.system(cmd)
else:
    cmd = 'python3 ' + str(wd) + 'src/format_bwa_output.py -g ' + str(genome_dir) + ' -f ' + str(dna_fasstq) + ' -o ' + str(dna_bam)
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

