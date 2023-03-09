# AnnotateGene (Version 0.1)
## Introduction
### Discovering a potential causal variant is exciting, but we also want to see the location of this mutation in the gene. We can go to NCBI gene or UCSC genome browser to see where the mutation is located. However, if we want to save those figures from NCBI or UCSC and use them in the publication or presentation, the only way is taking a screenshot. Unfortunatly, we cannot control the colors, cannot add precise annotations (for example, add a copy number variant to show the exons affected), and cannot control the resolution of the figures.
&nbsp;
### Here, utilizing the gtf/gff files from NCBI RefSeq, I developed a tool that can plot the genes and transcripts. Precise annotations with customized colors could be add into the figure.
&nbsp;
### If you use this tool in your publication, please cite this repository.
&nbsp;

## gtf/gff files used from NCBI RefSeq: 
### GRCh37: https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh37_latest/refseq_identifiers/GRCh37_latest_genomic.gtf.gz https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh37_latest/refseq_identifiers/GRCh37_latest_genomic.gff.gz (Latest modified: 2022-03-12 12:43)
### GRCh38: https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh38_latest/refseq_identifiers/GRCh38_latest_genomic.gtf.gz https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh38_latest/refseq_identifiers/GRCh38_latest_genomic.gff.gz (Latest modified: 2022-04-12 08:00)
&nbsp;

## Dependencies
### Matplotlib
&nbsp;

## Tutorial
### Python was used to develop this tool.