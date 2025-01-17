 ```
 ███╗   ███╗ ██████╗██████╗ ███████╗    ██████╗ ██╗██████╗ ███████╗██╗     ██╗███╗   ██╗███████╗
████╗ ████║██╔════╝██╔══██╗██╔════╝    ██╔══██╗██║██╔══██╗██╔════╝██║     ██║████╗  ██║██╔════╝
██╔████╔██║██║     ██████╔╝███████╗    ██████╔╝██║██████╔╝█████╗  ██║     ██║██╔██╗ ██║█████╗  
██║╚██╔╝██║██║     ██╔═══╝ ╚════██║    ██╔═══╝ ██║██╔═══╝ ██╔══╝  ██║     ██║██║╚██╗██║██╔══╝  
██║ ╚═╝ ██║╚██████╗██║     ███████║    ██║     ██║██║     ███████╗███████╗██║██║ ╚████║███████╗
╚═╝     ╚═╝ ╚═════╝╚═╝     ╚══════╝    ╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝
 ```

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
bash /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/sacbe_annotation.sge Genes.csv
```
#### Important note: In order to continue FIRST you need to give this archives to Claudia so she can run the sacbe script and with that file then you can continue
