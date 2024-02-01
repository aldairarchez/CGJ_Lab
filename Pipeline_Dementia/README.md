Directory of the files:
+ /mnt/Timina/cgonzaga/Sandbox/Annotations_Sacbe

### Annotation file 
The file contains 78 columns separated by tabs, here is an example:
|#CHR|START|END|REF|ALT|ZYG|FILTER|QUAL|RR|VR|TR|RATIO|GQ|PL|VCF_INFO|BAND|ANNOTATION|GENE|GENE_NAME|ACCESSION|EXON|NT_CHANGE|AA_CHANGE|ALL_TRX|dbSNP|TGP_FREQ|ESP_FREQ|EXAC_FREQ|GNOMADEX_FREQ|GNOMADX_POPMAX|GNOMAD312_AF|GERP_SCORE|GERP_PRED|PHYLOP7_SC|PHYLOP20_SC|PHASTCONS7_SC|PHASTCONS20_SC|CONSTRAINT|SIPHY_LOG_ODDS|FATHMM_SC|FATHMM_PRED|FATHMM-MKL_SC|FATHMM-MKL_PRED|META-SVM_SC|META-SVM_PRED|META-LR_SC|META-LR_PRED|LRT_SCORE|LRT_PRED|SIFT_SCORE|SIFT_PRED|PROVEAN_SCORE|PROVEAN_PRED|PPH2-HDIV_SCORE|PPH2-HDIV_PRED|PPH2-VAR_SCORE|PPH2-VAR_PRED|MTT_SCORE|MTT_PRED|MTASS_SCORE|MTASS_PRED|VEST3_SC|DANN_SC|CADD_RAW|CADD_PHRED|INT-FIT_SCORE|INT-FIT_CONFVAL|FAS|OMIM_INFO|CLINSIG|CLNDN|CLINVALLELE|EVE_AF|EVE_HET|EVE_HOM|NCBI_GENE_LINK|GTEX_EXPRESSION|CLINVAR_VAR_LINK|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|chr1|226881956|226881956|C|T|.|WES|.|11|276400|3.98e-05|6944723618.09045|.|.|1:226881956:C:T|1q42.13|nonsynonymous SNV|PSEN2|presenilin 2|NM_000447|exon4|c.C49T|p.R17W|PSEN2:NM_000447:exon4:c.C49T:p.R17W,PSEN2:NM_012486:exon4:c.C49T:p.R17W,|na|na|na|3.297e-05|2.386e-05|0.0002|1.314e-05|0.416|neutral|-0.444|0.036|0.993|0.980|0.39125|14.596|-5.39|deleterious|0.868|deleterious|1.009|deleterious|0.980|deleterious|0.000|deleterious|0.051|tolerated|-2.43|neutral|1.0|probably_damaging|0.906|possibly_damaging|1.000|disease_causing|0.975|nonfunctional:L|0.776|0.999|6.780|32|0.707|0|33.056|PSEN2(600759):Alzheimer disease-4, 606889 (3); Cardiomyopathy, dilated, 1V, 613697 (3)|Uncertain_significance|189386|not_provided|2.90503e-05|11|0|https://www.ncbi.nlm.nih.gov/gene/5664|http://www.gtexportal.org/home/gene/PSEN2|https://www.ncbi.nlm.nih.gov/clinvar/variation/189386|

### Descarga de anotaciones de clinvar
<span style="color:blue; font-weight:bold;">last updated 21/01/24</span>

<span style="color:red; font-weight:bold;">Texto en negrita y rojo</span>

Obtaining the download link (**last updated 21/01/24**):
+ Home page > Downloads/FTP site > vcf_GRCh38 > clinvar.vcf.gz
```bash
wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
gunzip clinvar.vcf.gz #uncompressing the file
```

 
