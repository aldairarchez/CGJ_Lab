#!/bin/bash
#abrir el archivo GENES.txt
gene_list=($(cat GOF_GENES.txt))


for gene in "${gene_list[@]}"; do
#INICIA SCRIPT PARA UNIR LOS ARCHIVOS DE MCPS y clinvar cuando hay coincidencias
  #Definimos los archivos a utilizar
  archive_clinvar=/mnt/Timina/cgonzaga/marciniega/Dementia_2024/"$gene"_clinvar.tsv
  archive_sacbe=/mnt/Timina/cgonzaga/marciniega/Dementia_2024/genes_files/"$gene"_sacbe.tsv
  # unimos encabezados para el archivo inclinvar
  encabezado1=$(sed -n 1p "$archive_sacbe")
  encabezado2=$(sed -n 1p "$archive_clinvar")
  echo -e "$encabezado1\t$encabezado2" > /mnt/Timina/cgonzaga/marciniega/Dementia_2024/genes_files/"$gene"_inclinvar1.tsv
  
  # Omite el encabezado del archivo para inciar la busqueda
  tail -n +2 "$archive_sacbe" | while IFS= read -r linea
  do
     #obtenemos el CPRA del archivo de MCPS, linea por linea
     CPRA=$(awk -F'\t' '{print $15}' <<< "$linea")
     #buscamos el CPRA de MCPS en el archivo de clinvar del gen
     coincide=$(grep "$CPRA" "$archive_clinvar")
     #cuando no hay coincidencias los guardamos la linea en el archivo notclinvar
     if [ -n "$coincide" ]; then
        #obtenemos el numero de linea del archivo de clinvar en donde hubo coincidencia
        line_matching=$(grep -n "$CPRA" "$archive_clinvar" | cut -d: -f1)
        #guardamos la linea completa en una variable
        line_clinvar=$(sed -n "$line_matching"p "$archive_clinvar")
        # unimos la linea actual de MCPS (dada por el while) y la linea que coincide de clinvar
        echo -e "$linea"'\t'"$line_clinvar" >> /mnt/Timina/cgonzaga/marciniega/Dementia_2024/genes_files/"$gene"_inclinvar1.tsv
     #cuando hay coincidencia lo unimos con la linea del archivo en clinvar que coincide el CPRA
     fi
  done < <(tail -n +2 "$archive_sacbe") #esta linea hace que el while comience a correr omitiendo el encabezado
  
  # es necesario quitar saltos de linea inesperados
  sed -i 's/\r//g' /mnt/Timina/cgonzaga/marciniega/Dementia_2024/genes_files/"$gene"_inclinvar1.tsv
  
  #COMENZAMOS FILTRADO TANTO DE ANOTACIONES COMO PARA SABER SI ERAN PATOGENICAS/PROBABLEMENTE PATOGENICAS
  #cargamos el modulo de python
  module load python38/3.8.3
  #corremos el script que filtra la columna annotations para quedarnos con variantes de GOF
  python3 filter_GOF.py "$gene"

  #corremos el script que filtra por patogenicidad
  python3 filter_clinvar_GOF.py "$gene"

  #eliminamos archivo sin filtrado de CLNSIG
  rm "$gene"_inclinvar1.tsv
  
done < GOF_GENES.txt
