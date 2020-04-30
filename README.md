# REDp: RNA Editing Detection Pipeline

### Description
RNA editing is a widespread post-transcriptional mechanism able to modify RNA by the host enzymes. Adenosine-to-Inosine (A-to-I) conversion, one of many RNA editing mechanisms, has been proven to play a pleiotropic role in neuron development and neurological diseases. Detecting the A-to-I event in a large-scale transcriptomic dataset is a very compelling and however, challenging task. Previously a computational tool called REDItools was developed to detect the RNA editing in RNA-seq data. However, this tool requires many preparational files and only accepts sequence data that is pre-processed [1]. REDp is a python wrapper that automate the entire process, from downloading the required sequence data to produce the final report. This pipeline will enable users who have no experience in using Linux command lines to use this tool. In addition, the scripts of REDItools were converted from python2 to python3.  

### Softeare/Tools needed
* Linux/Unix
* Python3
* Bash
* Fastq-dump
* Fastp
* Fastqc
* STAR
* BWA
* Pblat
* REDItools
* REDIportal database

### Run Pipeline:
1. Create a tab-delimited file containing the urls to all required reference data keeping the first column identical to the example.

Example ``reference_data.txt``:
```
genome  ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_30/GRCh37_mapping/GRCh37.primary_assembly.genome.fa.gz
genome_annotation       ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_30/GRCh37_mapping/gencode.v30lift37.annotation.gtf.gz
strand_detection        https://sourceforge.net/projects/rseqc/files/BED/Human_Homo_sapiens/hg19_RefSeq.bed.gz
rmsk    http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/rmsk.txt.gz
dbSNP   http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/snp151.txt.gz
rediportal_db   http://srv00.recas.ba.infn.it/webshare/rediportalDownload/table1_full.txt.gz
```
2. Create a txt file containing a list of RNA SRA accession numbers.

Example ``rna_acc.txt``:
```
SRR1258218,SRR1258219
```
3. Create a txt file containing a list of DNA SRA accession numbers.

Example ``dna_acc.txt``:
```
ERR262997
```
4. Run 'main_pipeline.py' to run through the entire pipeline.

Parameters:
* -ru or --reference_urls: path to tab delimited file containing reference data urls
* -o or --output: path to output directory
* -ra or --rna_acc: path to file containing RNA SRA accession numbers
* -da or --dna_acc: path to file containing DNA SRA accession numbers
* -chr or --chr_num: chromosome to filter (must be in format chr#)

Example of running the pipeline:
```
nohup python3 main_pipeline.py -ru reference_data.txt -o REDp_results/ -ra rna_acc.txt -da dna_acc.txt -chr chr4 &
```
### Run individual step separately:
* The usage and required parameters of individual steo are available at https://github.com/jmattick/RNA_Editing_Detection_Pipeline/wiki.
