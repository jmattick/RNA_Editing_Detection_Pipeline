# REDp: RNA Editing Detection Pipeline

### Description
RNA editing is a widespread post-transcriptional mechanism able to modify RNA by the host enzymes. Adenosine-to-Inosine (A-to-I) conversion, one of many RNA editing mechanisms, has been proven to play a pleiotropic role in neuron development and neurological diseases (Figure 1). Detecting the A-to-I event in a large-scale transcriptomic dataset is a very compelling and however, challenging task. Previously a computational tool called REDItools was developed to detect the RNA editing in RNA-seq data (Figure 2). However, this tool requires many preparational files and only accepts sequence data that is pre-processed. REDp is a python wrapper that helps automate the process, from downloading the required sequence data to producing the final report. This pipeline will enable users who have limited experience in using Linux command lines to use this tool. In addition, the scripts of REDItools were converted from python2 to python3.  
![alt text](https://github.com/jmattick/RNA_Editing_Detection_Pipeline/blob/master/images/Slide1.jpeg "Logo Title Text 1")

![alt text](https://github.com/jmattick/RNA_Editing_Detection_Pipeline/blob/master/images/Slide2.jpeg "Logo Title Text 1")

### Software/Tools needed
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

### Run Test datasets for REDp: RNA Editing Pipeline 

A test dataset has been provided in test_data.

Download the reference genome:

```
wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_30/GRCh37_mapping/GRCh37.primary_assembly.genome.fa.gz
gunzip GRCh37.primary_assembly.genome.fa.gz
```


Download the genome annotation:

```
wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_30/GRCh37_mapping/gencode.v30lift37.annotation.gtf.gz
gunzip gencode.v30lift37.annotation.gtf.gz
```

### Test fastq processing

Test the fastq processing pipline using provided dna and rna fastq files. Both samples are from the NA12878 cell line under accessions SRR1258218 and ERR262997. The fastq files are a subsample of the full dataset because of the large size of the original.

The fastq_alignment.py script will quality check and trim reads. It will also create genome indices for STAR and BWA before aligning the reads. The output of this script should be suitable as input for REDItools.  

Parameters: 

- `-g` or `--genome`: path to genome fasta file
- `-a` or `--genome_ann`: path to genome annotation file
- `-r` or `--rna_fastq`: path to directory containing RNA fastq files
- `-d` or `--dna_fastq`: path to directory containing DNA fastq files
- `-o` or `--output`: path to output directory
- `-chr` or `--chrNum`: chromosome location to output (format `-chr chrX`)

Example Run: 
```
nohup python3 fastq_alignment.py -g test_data/GRCh37.primary_assembly.genome.fa -a test_data/gencode.v30lift37.annotation.gtf -r test_data/rna_fastq/ -d test_data/dna_fastq/ -o output_directory/ &
```

Three additional files have been provided containing the RNA accession numbers, the DNA accession numbers, and a file containing the urls of the reference data. The next two steps are not required to test the fastq processing pipeline but can be useful for testing other datasets. 

Download Reference data: 

```
nohup python3 get_ref_data_annotation.py -i reference_data.txt -o output_path &
```

Download fastq files for DNA or RNAseq :

```
nohup python3 get_SRA_data.py -a acc.txt -o output_path &
```

### Test REDItools_python3 scripts

Python3 update to the original REDItools scripts found at https://github.com/BioinfoUNIBA/REDItools

Test the REDItools python3 scripts using the dataset provided by Lo Giudice et al:

http://srv00.recas.ba.infn.it/webshare/testREDItools.tar.gz

Use the following commands to test the scripts:

Unzip dataset:
```
tar xvzf testREDItools.tar.gz
```

Compare DNA and  RNA using the REDItoolDnaRna.py script. 

```
python3 REDItools_python3/main/REDItoolDnaRna.py -i rna.bam -j dna.bam -f reference.fa -o reditool-test -c 10,1 -q 25,25 -m 20,20 -s 2 -g 1 -u -a 6-0 -v 2 -n0.0 -N0.0 -V
```

An output table will be created with the name outTable_XXXXX with XXXXX representing a random number sequence. Use the generated file name for the remaining commands.

Select positions with variants by running the selectPositions.py script within the output directory. 

```
nohup python3 REDItools_python3/accessory/selectPositions.py -i outTable_XXXXX -d 12 -c 2 -C 10 -v 2 -V 0 -f 0.1 -F 1.0 -e -u -o candidates.txt&
```

Annotate positions with information from repeat masker.

```
nohup python3 REDItools_python3/accessory/AnnotateTable.py -a ../../rmsk.gtf.gz -i candidates.txt -u -c 1,2,3 -n RepMask -o candidates.rmsk.txt &
```

Filter annotated candidates.

```
nohup python3 REDItools_python3/accessory/FilterTable.py -i candidates.rmsk.txt -f ../../rmsk.gtf.gz -F SINE -E -o candidates.rmsk.alu.txt -p &
```
Annotate candidates with gene information from RefSeq. 

```
nohup python3 REDItools_python3/accessory/AnnotateTable.py -a ../../refGene.sorted.gtf.gz -i candidates.rmsk.alu.txt -u -c 1,2 -n RefSeq -o candidates.rmsk.alu.ann.txt &
```

The result is an annotated table containing RNA editing sites in the provided dataset. 

### Run individual step separately:
* The usage and required parameters of individual steps are available at https://github.com/jmattick/RNA_Editing_Detection_Pipeline/wiki.
