## Pipeline Sacbe annotation
This pipeline provides an archive ready to be annotated in Sacbe. Here is an example of the **final** format:
| #CHR | START | END | REF	| ALT	| ZYG	| SOURCE	| QUAL	| AC_RAW	| AN_RAW	| AF_RAW	| GQ	| PL | VCF_INFO |
|------|-------|-----|----|----|----|----|----|----|----|----|----|----|----|
| 22 | 10510341 | 10510342 | C	| G	| .	| WGS	| .	| 0	| 19896	| 0	| .	| . | 22:10510341:C:G |

# Archives you need to create 
## Directory where you will save the parsed archives obtained from the vcf from MCPS (*general* archives to different gene lists)
obtains the information that we need from the vcf from MCPS

[![chromosomes.sge](https://img.shields.io/badge/chromosomes.sge-blue)](https://github.com/aldairarchez/CGJ_Lab/blob/main/Sacbe_annotation/Codes/chromosomes.sge)

Aggregates a column "Type" to know if a SNP is a deletion or insertion

[![sacbe_type.py](https://img.shields.io/badge/sacbe_type.py-blue)](https://github.com/aldairarchez/CGJ_Lab/blob/main/Sacbe_annotation/Codes/sacbe_type.py)


## Directory where the final archives will be saved (*individual* gene list)
### In this directory, we must have an archive called "Genes.csv" in the following format:
The positions of the gene were taken from [UCSC Genome browser](https://genome.ucsc.edu/)
| GENE,CHR,START,END |
|-------|
| CALM1,14,90397029,90408268 |

Add the start and end position of each variant

[![sacbe_padded.py](https://img.shields.io/badge/sacbe_padded.py-blue)](https://github.com/aldairarchez/CGJ_Lab/blob/main/Sacbe_annotation/Codes/sacbe_padded.py)

sacbe_annotation.sge #generates the final archives

[![sacbe_annotation.sge](https://img.shields.io/badge/sacbe_annotation.sge-red)](https://github.com/aldairarchez/CGJ_Lab/blob/main/Sacbe_annotation/Codes/sacbe_annotation.sge)

#### Notes:
* **line 35 of sacbe_annotation.sge:** the directory should be changed to the directory where the parsed generated archives from MCPS have been generated
