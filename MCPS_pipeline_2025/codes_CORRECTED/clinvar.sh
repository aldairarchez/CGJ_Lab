#!/bin/bash

# Cargar módulo
module load bcftools/1.10.2

# Obtener el directorio desde donde se ejecuta el script
output_directory=$(pwd)

# Crear el directorio Clinvar si no existe
mkdir -p ClinVar

# Verificar si el archivo Genes_list.txt existe
if [ ! -f Genes_list.txt ]; then
  echo "Error: El archivo Genes_list.txt no existe en el directorio actual ($output_directory)."
  exit 1
fi

# Leer la lista de genes (solo la primera columna)
gene_list=($(cut -f1 Genes_list.txt))

# Crear directorio de salida si no existe
mkdir -p "$output_directory"

# Iterar sobre la lista de genes
for gene in "${gene_list[@]}"; do

  # Filtrar por gen y significancia en ClinVar
  # filtrando por gen y significancia en clinvar, la opcion grep -w omite palabras que empiezan igual y -E excluye similitudes
  filtrado=$(bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t%ID\t %INFO[%GENEINFO\t%ID%CLNDN\t%CLNHGVS\t%CLNSIG\t%CLNVC\t%AF_ESP\t%AF_EXAC\t%AF_TGP %MC]\n' /mnt/Timina/cgonzaga/marciniega/Dementia_2024/clinvar.vcf | grep -E "GENEINFO=.*\b${gene}\b.*")
  echo "$filtrado" > "$output_directory"/"$gene".vcf

  # Reemplazar ';' con tabulaciones
  sed -i 's/;/\t/g' "$output_directory"/"$gene".vcf

  # Crear archivo TSV con las primeras 4 columnas
  awk '{print $1,$2,$3,$4}' "$output_directory"/"$gene".vcf > "$output_directory"/"$gene"_clinvar.tsv

  # Leer columnas deseadas desde columns.txt
  columns_list=($(cat /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/columns.txt))
  archivo="$output_directory"/"$gene".vcf
  touch "$output_directory"/archivo_vacio.tsv
  cp "$output_directory"/archivo_vacio.tsv "$output_directory"/temporal.tsv

  for column in "${columns_list[@]}"; do
    cp "$output_directory"/archivo_vacio.tsv "$output_directory"/columna.tsv
    while IFS= read -r linea; do
      resultado=$(grep -o "$column=.*" <<< "$linea" | awk -F'\t' '{print $1}' | sed "s/$column=//")
      if [ -z "$resultado" ]; then
        resultado="NA"
      fi
      echo "$resultado" >> "$output_directory"/columna.tsv
      sed -i 's/,/;/g' "$output_directory"/columna.tsv
    done < "$archivo"
    paste "$output_directory"/"$gene"_clinvar.tsv "$output_directory"/columna.tsv > "$output_directory"/temporal.tsv
    cp "$output_directory"/temporal.tsv "$output_directory"/"$gene"_clinvar.tsv
  done

  # Crear el CPRA y agregar encabezados
  awk '{print $1":"$2":"$3":"$4"\t"$5"\t"$6"\t"$7"\t"$8"\t"$9"\t"$10"\t"$11"\t"$12"\t"$13"\t"$14}' "$output_directory"/"$gene"_clinvar.tsv > "$output_directory"/"$gene"_Clinvar.tsv
  cp "$output_directory"/archivo_vacio.tsv "$output_directory"/"$gene"_clinvar.tsv
  echo -e "CPRA\tGENEINFO\tRS_ID\tCLNDN_2\tCLNHGVS\tCLNSIG_2\tCLNVC\tAF_ESP\tAF_EXAC\tAF_TGP\tMC" | cat - "$output_directory"/"$gene"_Clinvar.tsv > "$output_directory"/ClinVar/"$gene"_clinvar.tsv
  
  # Limpiar archivos temporales
  rm "$output_directory"/"$gene"_Clinvar.tsv
  rm "$output_directory"/"$gene".vcf
  rm "$output_directory"/columna.tsv

done

# Eliminar archivos temporales globales
rm "$output_directory"/archivo_vacio.tsv
rm "$output_directory"/temporal.tsv
