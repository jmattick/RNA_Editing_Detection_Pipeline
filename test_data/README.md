# Test Datasets for REDp: RNA Editing Pipeline 

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

Test the fastq processing pipline using provided dna and rna fastq files. Both samples are from the NA12878 cell line under accessions SRR1258218 and ERR262997. The ERR262997 fastq files are are subsample of the full dataset because of the large size of the original. The genome fasta and annotation files are also provided.

The fastq_alignment.py script will quality check and trim reads. It will also create genome indices for STAR and BWA before aligning the reads. The output of this script should be suitable as input for REDItools.  

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

Select positions with variants by running the selectPositions.py script 

```
nohup python3 REDItools_python3/accessory/selectPositions.py -i outTable_XXXXX -d 12 -c 2 -C 10 -v 2 -V 0 -f 0.1 -F 1.0 -e -u -o candidates.txt&
```

Annotate positions with information from repeat masker.

```
nohup python3 REDItools_python3/accessory/AnnotateTable.py -a rmsk.gtf.gz -i candidates.txt -u -c 1,2,3 -n RepMask -o candidates.rmsk.txt &
```

Filter annotated candidates.

```
nohup python3 REDItools_python3/accessory/FilterTable.py -i candidates.rmsk.txt -f rmsk.gtf.gz -F SINE -E -o candidates.rmsk.alu.txt -p &
```
Annotate candidates with gene information from RefSeq. 

```
nohup python3 REDItools_python3/accessory/AnnotateTable.py -a refGene.sorted.gtf.gz -i candidates.rmsk.alu.txt -u -c 1,2 -n RefSeq -o candidates.rmsk.alu.ann.txt &
```

The result is an annotated table containing RNA editing sites in the provided dataset. 
