IndexFile() {
    FileName=${1}
    # 1.Sort file.
    (zgrep ^"#" ${FileName}; zgrep -v ^"#" ${FileName} | sort  -t $'\t' -k1,1V -k4,4n -k5,5n) | bgzip  > ${FileName/.gtf.gz/.sorted.gtf.gz}
    # 2.Index file.
    tabix -p gff ${FileName/.gtf.gz/.sorted.gtf.gz}
}
# IndexFile GRCh37_latest_genomic.gtf.gz
IndexFile GRCh37_latest_genomic.gff.gz
# IndexFile GRCh38_latest_genomic.gtf.gz
IndexFile GRCh38_latest_genomic.gff.gz