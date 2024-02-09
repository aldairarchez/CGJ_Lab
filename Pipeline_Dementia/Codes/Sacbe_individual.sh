#!/bin/bash
#creates directory to save individual files
mkdir genes_files
archivo="Genes.csv"

# Itera a través de cada línea en el archivo (omitir la primera línea con sed)
tail -n +2 "$archivo" | while IFS=',' read -r GENE CHR START END; do
    chrom=$(echo "$CHR" | tr -cd '[:alnum:]')
    inicio=$(echo "$START" | tr -cd '[:alnum:]')
    fin=$(echo "$END" | tr -cd '[:alnum:]')

    archivo_entrada="/mnt/Timina/cgonzaga/marciniega/Dementia_2024/Marlon_sacbe.varfile.ex.EDITED"
    archivo_salida="/mnt/Timina/cgonzaga/marciniega/Dementia_2024/genes_files/${GENE}_sacbe.tsv"
    #Obtaning the header
    awk NR==1 Marlon_sacbe.varfile.ex.EDITED > "$archivo_salida"

    # Filtra las líneas del archivo de entrada según el intervalo deseado considerando la posicion 
    awk -v inicio="$inicio" -v fin="$fin" '$2 ~ /^[0-9]+$/ && $2 >= inicio && $2 <= fin' "$archivo_entrada" >> "$archivo_salida"
done
