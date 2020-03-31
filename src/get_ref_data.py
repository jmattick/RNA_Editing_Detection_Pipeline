import os

# Download and unzip the human reference genome hg19 in FASTA format
os.system('mkdir genome_hg19')
os.system('cd genome_hg19/')
os.system('wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_30/GRCh37_mapping/GRCh37.primary_assembly.genome.fa.gz')
os.system('gunzip GRCh37.primary_assembly.genome.fa.gz')
os.system('cd ..')

# Download and unzip Gencode annotations in GTF format
os.system('mkdir Gencode_annotation')
os.system('cd Gencode_annotation')
os.system('wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_30/GRCh37_mapping/gencode.v30lift37.annotation.gtf.gz')
os.system('gunzip gencode.v30lift37.annotation.gtf.gz')
os.system('cd ..')

# Download and unzip hg19 RefSeq annotations in bed format for strand detection
os.system('Strand_detection')
os.system('cd Strand_detection')
os.system('wget --no-check-certificate https://sourceforge.net/projects/rseqc/files/BED/Human_Homo_sapiens/hg19_RefSeq.bed.gz')
os.system('gunzip hg19_RefSeq.bed.gz')
os.system('cd ..')

# Download and unzip RepeatMasker annotations
os.system('mkdir rmsk')
os.system('cd rmsk')
os.system('wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/rmsk.txt.gz')
os.system('gunzip rmsk.txt.gz')
os.system('cd ..')

# Download and unzip dbSNP annotations
os.system('mkdir snp151')
os.system('cd snp151')
os.system('wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/snp151.txt.gz')
os.system('gunzip snp151.txt.gz')
os.system('cd ..')

# Download and unzip REDIportal annotations
os.system('mkdir rediportal')
os.system('cd rediportal')
os.system('wget http://srv00.recas.ba.infn.it/webshare/rediportalDownload/table1_full.txt.gz')
os.system('gunzip table1_full.txt.gz')
os.system('cd ..')
