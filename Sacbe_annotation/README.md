## Pipeline Sacbe annotation
This pipeline provides an archive ready to be annotated in Sacbe, here is an example of the **final** format:
| #CHR | START | END | REF	| ALT	| ZYG	| SOURCE	| QUAL	| AC_RAW	| AN_RAW	| AF_RAW	| GQ	| PL | VCF_INFO |
|------|-------|-----|----|----|----|----|----|----|----|----|----|----|----|
| 22 | 10510341 | 10510342 | C	| G	| .	| WGS	| .	| 0	| 19896	| 0	| .	| . | 22:10510341:C:G |

# Archives you need to create 
## Directory where you will save the parsed archives obtained from the vcf from MCPS (*general* archives to different gene lists)
chromosomes.sge #obtains the information that we need from the vcf from MCPS
sacbe_type.py #agregates a column "Type" to know if a SNP is a deletion or insertion


## Directory where the finals archives will be save (*individual* gene list)
### In this directory we must have an archive called "Genes.csv" in the following format:
| GENE,CHR,START,END |
|-------|
| CALM1,14,90397029,90408268 |

sacbe_padded.py #add the start and end position of each variant

sacbe_annotation.sge #generates the final archives
