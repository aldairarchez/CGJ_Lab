This pipeline works using Sacbe annotation which is provided by Claudia's script, the process needed for the annotation is described in the repository:
[Sacbe_annotation](https://github.com/aldairarchez/CGJ_Lab/tree/main/Sacbe_annotation)

Directory of the files:
+ /mnt/Timina/cgonzaga/Sandbox/Annotations_Sacbe

### Annotation file 
The file contains 78 columns separated by tabs, here is an example:
|#CHR|START|END|REF|ALT|ZYG|FILTER|QUAL|RR|VR|TR|RATIO|GQ|PL|VCF_INFO|BAND|ANNOTATION|GENE|GENE_NAME|ACCESSION|EXON|NT_CHANGE|AA_CHANGE|ALL_TRX|dbSNP|TGP_FREQ|ESP_FREQ|EXAC_FREQ|GNOMADEX_FREQ|GNOMADX_POPMAX|GNOMAD312_AF|GERP_SCORE|GERP_PRED|PHYLOP7_SC|PHYLOP20_SC|PHASTCONS7_SC|PHASTCONS20_SC|CONSTRAINT|SIPHY_LOG_ODDS|FATHMM_SC|FATHMM_PRED|FATHMM-MKL_SC|FATHMM-MKL_PRED|META-SVM_SC|META-SVM_PRED|META-LR_SC|META-LR_PRED|LRT_SCORE|LRT_PRED|SIFT_SCORE|SIFT_PRED|PROVEAN_SCORE|PROVEAN_PRED|PPH2-HDIV_SCORE|PPH2-HDIV_PRED|PPH2-VAR_SCORE|PPH2-VAR_PRED|MTT_SCORE|MTT_PRED|MTASS_SCORE|MTASS_PRED|VEST3_SC|DANN_SC|CADD_RAW|CADD_PHRED|INT-FIT_SCORE|INT-FIT_CONFVAL|FAS|OMIM_INFO|CLINSIG|CLNDN|CLINVALLELE|EVE_AF|EVE_HET|EVE_HOM|NCBI_GENE_LINK|GTEX_EXPRESSION|CLINVAR_VAR_LINK|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|chr1|226881956|226881956|C|T|.|WES|.|11|276400|3.98e-05|6944723618.09045|.|.|1:226881956:C:T|1q42.13|nonsynonymous SNV|PSEN2|presenilin 2|NM_000447|exon4|c.C49T|p.R17W|PSEN2:NM_000447:exon4:c.C49T:p.R17W,PSEN2:NM_012486:exon4:c.C49T:p.R17W,|na|na|na|3.297e-05|2.386e-05|0.0002|1.314e-05|0.416|neutral|-0.444|0.036|0.993|0.980|0.39125|14.596|-5.39|deleterious|0.868|deleterious|1.009|deleterious|0.980|deleterious|0.000|deleterious|0.051|tolerated|-2.43|neutral|1.0|probably_damaging|0.906|possibly_damaging|1.000|disease_causing|0.975|nonfunctional:L|0.776|0.999|6.780|32|0.707|0|33.056|PSEN2(600759):Alzheimer disease-4, 606889 (3); Cardiomyopathy, dilated, 1V, 613697 (3)|Uncertain_significance|189386|not_provided|2.90503e-05|11|0|https://www.ncbi.nlm.nih.gov/gene/5664|http://www.gtexportal.org/home/gene/PSEN2|https://www.ncbi.nlm.nih.gov/clinvar/variation/189386|

### Descarga de anotaciones de clinvar
Obtaining the download link (**last updated 21/01/24**):
+ Home page > Downloads/FTP site > vcf_GRCh38 > clinvar.vcf.gz
```bash
wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
gunzip clinvar.vcf.gz #uncompressing the file
```

## Archived needed for the pipeline to work
+ List of the genes realted to dementia

GENES.txt
```bash
GRN
PSEN1
PSEN2
MAPT
APP
```
+ List of columns to filter out from the clinvar.vcf file (besides of the first column:CPRA)

**columns.txt**
```bash
GENEINFO
ID
CLNDN
CLNHGVS
CLNSIG
CLNVC
AF_ESP
AF_EXAC
AF_TGP
MC
```
### Running of [clinvar.sh](https://github.com/aldairarchez/CGJ_Lab/blob/main/Pipeline_Dementia/Codes/clinvar.sh) code to obtain individual clinvar files per gene
```bash
chmod +x clinvar.sh
./clinvar.sh
```
## Filtering of MCPS vcfs
+ directory of the MCPS files: /mnt/Timina/cgonzaga/resources/MCPS/CHRS_June2022

The following codes will parsed the columns needed from the vcf, add headers and filter by annotations if the genes are **loss** or **gain of function**

|Loss of function genes|Annotation|
|-|-|
|PSEN1 <br> PSEN2<br>GRN|exonic;splicing<br>splicing<br>frameshift deletion<br>frameshift insertion<br>stopgain SNV<br>stoploss SNV|


|Gain of function genes|Annotation|
|-|-|
|MAPT<br>APP|nonsynonymous SNV|

|Annotations not used to filter|
|-|
|nonframeshift deletion<br>nonframeshift insertion<br>synonymous SNV|


### creating indiidual archives per gene with the sacbe annotaion (pipeline Claudia)
first you need to create an achiv with the coordinates obtained from UCSC Browser
```bash
GENE,CHR,START,END
GRN,17,44345302,44353106
PSEN1,14,73136507,73223691
PSEN2,1,226870616,226896098
MAPT,17,45894554,46028334
APP,21,25880550,2617077
```
### Creating the file [Sacbe_individual.sh](https://github.com/aldairarchez/CGJ_Lab/blob/main/Pipeline_Dementia/Codes/Sacbe_individual.sh) and running the following codes
```bash
cp /mnt/Timina/cgonzaga/Sandbox/Annotations_Sacbe/Marlon_sacbe.varfile.ex.EDITED /mnt/Timina/cgonzaga/marciniega/Dementia_2024
chmod +x Sacbe_individual.sh
./Sacbe_individual.sh
```
# creating GOF and LOF gene lists
GOF_GENES.txt
```
MAPT
APP
```
### create filter_GOF.py and MCPS_GOF.sh and filter_clinvar.py
Files:


[MCPS_GOF.sh](https://github.com/aldairarchez/CGJ_Lab/blob/main/Pipeline_Dementia/Codes/MCPS_GOF.sh)

[filter_GOF.py](https://github.com/aldairarchez/CGJ_Lab/blob/main/Pipeline_Dementia/Codes/filter_GOF.py)

[filter_clinvar_GOF.py](https://github.com/aldairarchez/CGJ_Lab/blob/main/Pipeline_Dementia/Codes/filter_clinvar_GOF.py)
```bash
chmod +x filter_GOF.py
chmod +x MCPS_GOF.sh
chmod +x filter_clinvar_GOF.py
./MCPS_GOF.sh
```

