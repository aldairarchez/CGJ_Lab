#adding the header to the first part of the file taken from plink.frq
echo -e "ID\tCHR\tPOS\tREF\tALT\tSOURCE\tAF\tCHROBS" > MCPS_plink1
#adding line by line of the first 7 columns requiered
awk 'NR > 1 {print $2"\t"$2"\tWES""\t"$5"\t"$6}' plink.frq >> MCPS_plink1
#separating the second column SNP to obtain chromosome, position, reference and alternative separated by tabs and form 4 columns
awk -F'\t' 'BEGIN {OFS="\t"} {gsub(":", "\t", $2); print}' MCPS_plink1 > tmpfile && mv tmpfile MCPS_plink1

#adding the header to the second part of the file taken from plink.frqx
echo -e "ID\tHET_ALT\tHOM_ALT\tHOM_REF" > MCPS_plink2
#adding line by line of the 3 columns requiered
awk 'NR > 1 {print $2"\t"$6"\t"$5"\t"$7}' plink.frqx >> MCPS_plink2

#filtrar quellas que no son variantes de MCPS
awk -F'\t' 'NR == 1 || ($2 != 0 || $3 != 0)' MCPS_plink2 > MCPS_plink2_filtrado

#now we match the two files if the CPRA is in the other one and add the columns to the final archive
echo -e "ID\tCHR\tPOS\tREF\tALT\tSOURCE\tAF\tCHROBS\tHET_ALT\tHOM_ALT\tHOM_REF" > MCPS.tsv
#code that matches the two files
awk 'NR==FNR{a[$1]=$0; next} ($1 in a){print a[$1] "\t" $0}' MCPS_plink1 MCPS_plink2_filtrado > MCPS.tsv
#eliminamos la columna repetida de CPRA despues de generar el match
awk -F'\t' 'BEGIN{OFS="\t"} {for(i=1;i<=NF;i++) if(i!=9) printf("%s%s", $i, (i==NF) ? "\n" : OFS)}' MCPS.tsv > MCPS_sin_col9.tsv
#movemos la columna CHROBS al final
awk -F'\t' 'BEGIN{OFS="\t"} {temp=$8; $8=$9; $9=$10; $10=$11; $11=temp; print $0}' MCPS_sin_col9.tsv > MCPS_final.tsv


