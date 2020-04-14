### REDp: RNA Editing Detection Pipeline
* By Jessica Mattick and Xufang Deng

### Abstract
RNA editing is a widespread post-transcriptional mechanism able to modify RNA by the host enzymes. Adenosine-to-Inosine (A-to-I) conversion, one of many RNA editing mechanisms, has been proven to play a pleiotropic role in neuron development and neurological diseases. Detecting the A-to-I event in a large-scale transcriptomic dataset is a very compelling and however, challenging task. Previously a computational tool called REDItools was developed to detect the RNA editing in RNA-seq data. However, this tool requires many preparational files and only accepts sequence data that is pre-processed [1]. We here developed a pipeline to automate the entire process, from downloading the required sequence data to produce the final report. This pipeline will enable users who have no experience in using Linux command lines to use this tool. In addition, we converted the scripts of the tool from python2 to python3 so that it would be compatible with other applications written in python3. We outline the usage, required parameters, and analysis of the application of our tool, which is available at https://github.com/jmattick/RNA_Editing_Detection_Pipeline/wiki. 

### Introduction
Among 150 types of RNA modification, A-to-I RNA editing represents one of the most prominent RNA modifications. A-to-I RNA editing is a deamination process of adenosine to inosine by the host ADAR enzymes (Figure 1). Since inosine is recognized as guanine, this base conversion could result in various biological effects, such as amino acid substitutions and regulation of gene expression, depending on the RNA type and the region being edited. A-to-I RNA editing is tightly regulated as a part of epitranscriptomic modification and hence, its dysregulation has been implicated in many autoimmune disorders and neurodegenerative diseases, etc.
Since A-to-I RNA editing having significant implications in various diseases, discovering the editing sites in RNAs is the first and fundamental step for understanding the pathogenesis of a disease. RNA-seq has been the standard technique to obtain large-scale RNA sequence information. By comparing the transcriptomic sequences with the genomic sequence, A-to-I editing sites could be easily identified. The caveat of this approach is that the genome-encoded single-nucleotide polymorphisms (SNPs) and sequencing or read-mapping errors would also be falsely identified. Previously, Lo Giudice et al have developed a software package, named REDItools, to discover the RNA editing at the genomic scale [1]. This tool incorporates the information of genomic reads, SNPs database, and several additional filters to minimize the detection of false RNA editing sites. However, in order to implement the entire process, the user must complete a complicated preparation step, including manually downloading sequences reads and quality control, preparing intermediate files, and mapping reads, etc (Figure 2). This requires the user are familiar with several bioinformatic tools and Linux and python languages. To aid biologists who lack these knowledges, we aim to develop a pipeline to automate the entire process (Figure 3). With a single python file of the pipeline, the user can readily run the detection program and identify the A-to-I RNA editing events.

### Implementation
REDp combines several bioinformatics tools into a single pipeline to process raw FASTQ files and output a table of candidate RNA editing sites. The pipeline is implemented in python3 to run all of the required steps. The core RNA editing detection is performed by REDItools, which requires BAM file input [1]. This pipeline handles the downloading and pre-processing of required reference data and raw FASTQ files. Sequencing data is downloading using NCBI’s sra-toolkit [2]. Since this step depends on NCBI’s servers, it has the potential to be the rate-limiting step of the pipeline and the time can vary depending on a variety of factors. Raw FASTQ files are quality checked with FastQC [3]. WGS reads are aligned to the genome with BWA [4]. RNAseq reads are quality trimmed using Fastp [5] and aligned to the genome using STAR [6]. After pre-processing, the BAM files are run through a series of REDItools scripts to identify RNA editing candidates as described in Lo Giudice et al [1]. Excluding the downloading of data, the overall time complexity is dependent on the on the mapping of reads to the genome. The time complexity can be represented as O(n * rlog(m)) with n representing the number of samples, r representing the number of reads per sample, and m representing the length of genome.

### Results
This pipeline downloads and processes raw FASTQ files into the BAM file input required by REDItools by aligning reads to the genome using either STAR or BWA. Once aligned, the BAM files are passed through a series of REDItools scripts to compare DNA and RNA sequences and identify potential RNA editing sites. These RNA editing sites undergo additional filters using the REDItools scripts. The final output format of this pipeline is a tab-delimited file containing RNA editing candidates. 




### References

[1] Lo Giudice, C., Tangaro, M.A., Pesole, G. et al. Investigating RNA editing in deep transcriptome datasets with REDItools and REDIportal. Nat Protoc 15, 1098–1131 (2020). https://doi.org/10.1038/s41596-019-0279-7

[2] http://ncbi.github.io/sra-tools/

[3] Andrews S. (2010). FastQC: a quality control tool for high throughput sequence data. Available online at: http://www.bioinformatics.babraham.ac.uk/projects/fastqc

[4] Li Heng. Aligning sequence reads, clone sequences and assembly contigs with BWA-MEM. arXiv 1303.3997v2 (2013). https://arxiv.org/abs/1303.3997v2

[5] Shifu Chen, Yanqing Zhou, Yaru Chen, Jia Gu, fastp: an ultra-fast all-in-one FASTQ preprocessor, Bioinformatics, Volume 34, Issue 17, 01 September 2018, Pages i884–i890, https://doi.org/10.1093/bioinformatics/bty560

[6] Dobin A, et al. STAR: ultrafast universal RNA-seq aligner. Bioinformatics. 2013;29:15–21. doi: 10.1093/bioinformatics/bts635


