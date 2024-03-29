#!/bin/bash
#abrir el archivo GENES.txt
gene_list=($(cat LOF_GENES.txt))

for gene in "${gene_list[@]}"; do
#INICIA SCRIPT PARA UNIR LOS ARCHIVOS DE MCPS y clinvar cuando hay coincidencias
  #guardamos el encabezado tanto para el archivo notclinvar como el inclinvar
  sed -n 1p "$gene"_MCPS1.tsv > "$gene"_notclinvar.tsv
  # unimos encabezados para el archivo inclinvar
  encabezado1=$(sed -n 1p "$gene"_MCPS1.tsv)
  encabezado2=$(sed -n 1p "$gene"_clinvar.tsv)
  echo -e "$encabezado1\t$encabezado2" > "$gene"_inclinvar1.tsv
  

  archive="$gene"_MCPS1.tsv
  # Omite el encabezado del archivo para inciar la busqueda
  tail -n +2 "$archive" | while IFS= read -r linea
  do
     #obtenemos el CPRA del archivo de MCPS, linea por linea
     CPRA=$(awk '{print $1}' <<< "$linea")
     #buscamos el CPRA de MCPS en el archivo de clinvar del gen
     coincide=$(grep "$CPRA" "$gene"_clinvar.tsv)
     #cuando no hay coincidencias los guardamos la linea en el archivo notclinvar
     if [ -z "$coincide" ]; then
        notfound=$(echo "$linea" >> "$gene"_notclinvar.tsv)
     #cuando hay coincidencia lo unimos con la linea del archivo en clinvar que coincide el CPRA
     else 
        #obtenemos el numero de linea del archivo de clinvar en donde hubo coincidencia
        line_matching=$(grep -n "$CPRA" "$gene"_clinvar.tsv | cut -d: -f1)
        #guardamos la linea completa en una variable
        line_clinvar=$(sed -n "$line_matching"p "$gene"_clinvar.tsv)
        # unimos la linea actual de MCPS (dada por el while) y la linea que coincide de clinvar
        echo -e "$linea"'\t'"$line_clinvar" >> "$gene"_inclinvar1.tsv

     fi
  done < <(tail -n +2 "$archive") #esta linea hace que el while comience a correr omitiendo el encabezado
  
  # es necesario cambiar espacios por tabs porque a veces en el filtrado se eliminan
  sed -i 's/\r//g' "$gene"_inclinvar1.tsv
  sed -i 's/\r//g' "$gene"_notclinvar.tsv
  #COMENZAMOS FILTRADO TANTO DE ANOTACIONES COMO PARA SABER SI ERAN PATOGENICAS/PROBABLEMENTE PATOGENICAS
  #cargamos el modulo de python
  module load python38/3.8.3
  #corremos el script que filtra la columna annotations para saber que variantes son LOF
  python3 filter_LOF.py "$gene"
  #corremos el script que filtra por patogenicidad
  python3 filter_clinvar.py "$gene"

  #eliminamos archivo sin filtrado de CLNSIG
  #rm "$gene"_inclinvar1.tsv
  
done < LOF_GENES.txt
