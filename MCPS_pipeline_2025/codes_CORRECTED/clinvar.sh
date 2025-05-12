#!/bin/bash

# Cargar módulo
module load bcftools/1.10.2

# Obtener el directorio desde donde se ejecuta el script
output_directory=$(pwd)

# Crear el directorio ClinVar si no existe
mkdir -p "$output_directory"/ClinVar

# Verificar si el archivo Genes_list.txt existe
if [ ! -f Genes_list.txt ]; then
  echo "Error: El archivo Genes_list.txt no existe en el directorio actual ($output_directory)."
  exit 1
fi

# Leer la lista de genes (solo la primera columna)
gene_list=($(cut -f1 Genes_list.txt))

# Iterar sobre la lista de genes
for gene in "${gene_list[@]}"; do

  # Filtrar por gen y significancia en ClinVar
  filtrado=$(bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t%ID\t %INFO[%GENEINFO\t%ID%CLNDN\t%CLNHGVS\t%CLNSIG\t%CLNVC\t%AF_ESP\t%AF_EXAC\t%AF_TGP %MC]\n' /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/clinvar.vcf | grep -E "GENEINFO=.*\b${gene}\b.*")
  echo "$filtrado" > "$output_directory"/ClinVar/"$gene".vcf

  # Reemplazar ';' con tabulaciones
  sed -i 's/;/\t/g' "$output_directory"/ClinVar/"$gene".vcf

  # Crear archivo TSV con las primeras 4 columnas
  awk '{print $1,$2,$3,$4}' "$output_directory"/ClinVar/"$gene".vcf > "$output_directory"/ClinVar/"$gene"_clinvar.tsv

  # Leer columnas deseadas desde columns.txt
  columns_list=($(cat /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/columns.txt))
  archivo="$output_directory"/ClinVar/"$gene".vcf
  touch "$output_directory"/ClinVar/archivo_vacio.tsv
  cp "$output_directory"/ClinVar/archivo_vacio.tsv "$output_directory"/ClinVar/temporal.tsv

  for column in "${columns_list[@]}"; do
    cp "$output_directory"/ClinVar/archivo_vacio.tsv "$output_directory"/ClinVar/columna.tsv
    while IFS= read -r linea; do
      resultado=$(grep -o "$column=.*" <<< "$linea" | awk -F'\t' '{print $1}' | sed "s/$column=//")
      if [ -z "$resultado" ]; then
        resultado="NA"
      fi
      echo "$resultado" >> "$output_directory"/ClinVar/columna.tsv
      sed -i 's/,/;/g' "$output_directory"/ClinVar/columna.tsv
    done < "$archivo"
    paste "$output_directory"/ClinVar/"$gene"_clinvar.tsv "$output_directory"/ClinVar/columna.tsv > "$output_directory"/ClinVar/temporal.tsv
    cp "$output_directory"/ClinVar/temporal.tsv "$output_directory"/ClinVar/"$gene"_clinvar.tsv
  done

  # Crear el CPRA y agregar encabezados
  awk '{print $1":"$2":"$3":"$4"\t"$5"\t"$6"\t"$7"\t"$8"\t"$9"\t"$10"\t"$11"\t"$12"\t"$13"\t"$14}' "$output_directory"/ClinVar/"$gene"_clinvar.tsv > "$output_directory"/ClinVar/"$gene"_Clinvar_temp.tsv
  echo -e "CPRA\tGENEINFO\tRS_ID\tCLNDN_2\tCLNHGVS\tCLNSIG_2\tCLNVC\tAF_ESP\tAF_EXAC\tAF_TGP\tMC" | cat - "$output_directory"/ClinVar/"$gene"_Clinvar_temp.tsv > "$output_directory"/ClinVar/"$gene"_clinvar.tsv

  # Limpiar archivos temporales
  rm "$output_directory"/ClinVar/"$gene"_Clinvar_temp.tsv
  rm "$output_directory"/ClinVar/"$gene".vcf
  rm "$output_directory"/ClinVar/columna.tsv

done

# Eliminar archivos temporales globales
rm "$output_directory"/ClinVar/archivo_vacio.tsv
rm "$output_directory"/ClinVar/temporal.tsv

