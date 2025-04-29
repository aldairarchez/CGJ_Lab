 ```
 ███╗   ███╗ ██████╗██████╗ ███████╗    ██████╗ ██╗██████╗ ███████╗██╗     ██╗███╗   ██╗███████╗
████╗ ████║██╔════╝██╔══██╗██╔════╝    ██╔══██╗██║██╔══██╗██╔════╝██║     ██║████╗  ██║██╔════╝
██╔████╔██║██║     ██████╔╝███████╗    ██████╔╝██║██████╔╝█████╗  ██║     ██║██╔██╗ ██║█████╗  
██║╚██╔╝██║██║     ██╔═══╝ ╚════██║    ██╔═══╝ ██║██╔═══╝ ██╔══╝  ██║     ██║██║╚██╗██║██╔══╝  
██║ ╚═╝ ██║╚██████╗██║     ███████║    ██║     ██║██║     ███████╗███████╗██║██║ ╚████║███████╗
╚═╝     ╚═╝ ╚═════╝╚═╝     ╚══════╝    ╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝
 ```
# Step 1
## Create sacbe annotation file from MCPS data and run it with Claudias Script
### Files you need to create in the directory where you want to save the files:
#### an archive called "Genes.csv" in the following format:
The positions of the gene were taken from [UCSC Genome browser](https://genome.ucsc.edu/)
+ Example:
  
| GENE,CHR,START,END |
|-------|
| CALM1,14,90397029,90408268 |

Then run this command to generate the file needed to create the Sacbe annotation
```bash
# Concatenar todos los archivos *sacbe.csv en uno solo, conservando solo el encabezado del primero
head -n 1 $(ls *sacbe.csv | head -n 1) > Marlon2_sacbe.csv
tail -n +2 *sacbe.csv >> Marlon2_sacbe.csv
# crear un archivo tsv en .txt para claudia
sed 's/,/\t/g' Marlon2_sacbe.csv > Marlon2_sacbe.txt
```

##### concatenate archives into a single file which will be given to Claudia
```bash

```
#### Important note: In order to continue FIRST you need to give this archives to Claudia so she can run the sacbe script and with that file then you can continue

### Annotation file provided by Claudia's script
The file contains 78 columns separated by tabs, here is an example:
|#CHR|START|END|REF|ALT|ZYG|FILTER|QUAL|RR|VR|TR|RATIO|GQ|PL|VCF_INFO|BAND|ANNOTATION|GENE|GENE_NAME|ACCESSION|EXON|NT_CHANGE|AA_CHANGE|ALL_TRX|dbSNP|TGP_FREQ|ESP_FREQ|EXAC_FREQ|GNOMADEX_FREQ|GNOMADX_POPMAX|GNOMAD312_AF|GERP_SCORE|GERP_PRED|PHYLOP7_SC|PHYLOP20_SC|PHASTCONS7_SC|PHASTCONS20_SC|CONSTRAINT|SIPHY_LOG_ODDS|FATHMM_SC|FATHMM_PRED|FATHMM-MKL_SC|FATHMM-MKL_PRED|META-SVM_SC|META-SVM_PRED|META-LR_SC|META-LR_PRED|LRT_SCORE|LRT_PRED|SIFT_SCORE|SIFT_PRED|PROVEAN_SCORE|PROVEAN_PRED|PPH2-HDIV_SCORE|PPH2-HDIV_PRED|PPH2-VAR_SCORE|PPH2-VAR_PRED|MTT_SCORE|MTT_PRED|MTASS_SCORE|MTASS_PRED|VEST3_SC|DANN_SC|CADD_RAW|CADD_PHRED|INT-FIT_SCORE|INT-FIT_CONFVAL|FAS|OMIM_INFO|CLINSIG|CLNDN|CLINVALLELE|EVE_AF|EVE_HET|EVE_HOM|NCBI_GENE_LINK|GTEX_EXPRESSION|CLINVAR_VAR_LINK|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|chr1|226881956|226881956|C|T|.|WES|.|11|276400|3.98e-05|6944723618.09045|.|.|1:226881956:C:T|1q42.13|nonsynonymous SNV|PSEN2|presenilin 2|NM_000447|exon4|c.C49T|p.R17W|PSEN2:NM_000447:exon4:c.C49T:p.R17W,PSEN2:NM_012486:exon4:c.C49T:p.R17W,|na|na|na|3.297e-05|2.386e-05|0.0002|1.314e-05|0.416|neutral|-0.444|0.036|0.993|0.980|0.39125|14.596|-5.39|deleterious|0.868|deleterious|1.009|deleterious|0.980|deleterious|0.000|deleterious|0.051|tolerated|-2.43|neutral|1.0|probably_damaging|0.906|possibly_damaging|1.000|disease_causing|0.975|nonfunctional:L|0.776|0.999|6.780|32|0.707|0|33.056|PSEN2(600759):Alzheimer disease-4, 606889 (3); Cardiomyopathy, dilated, 1V, 613697 (3)|Uncertain_significance|189386|not_provided|2.90503e-05|11|0|https://www.ncbi.nlm.nih.gov/gene/5664|http://www.gtexportal.org/home/gene/PSEN2|https://www.ncbi.nlm.nih.gov/clinvar/variation/189386|

# Step 2
MCPS files and ClinVar merged and filtered by pathogenicity (pathogenic/likely pathogenic)

### Files you need to have in the directory in order to run the script
+ Genes_list.txt (list of ALL genes, no matter if they are LOF or GOF) *must be tab separated*
 ```bash
GRN LOF
PSEN1 LOF
PSEN2 LOF
MAPT GOF
APP GOF
```

+ Sacbe annotation file of the exonic variants: example of name: Marlon_sacbe.varfile.ex.EDITED
+ Genes.csv (previously made in the first step)

### Running the pipeline
```
bash /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/MCPS_pipeline.sh Genes_list.txt
```

