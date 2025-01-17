#!/bin/bash

# Define el directorio de salida dinámicamente usando `pwd`
OUTPUT_DIRECTORY=$(pwd)

# Crea un subdirectorio en el directorio actual para guardar los archivos individuales
mkdir -p "${OUTPUT_DIRECTORY}/sacbe_genes"

# Archivo de entrada basado en el patrón (se espera que exista un archivo que coincida con el patrón)
archivo_entrada=$(ls *_sacbe.varfile.ex.EDITED 2>/dev/null)

# Verifica si existe un archivo que coincida con el patrón
if [ -z "$archivo_entrada" ]; then
    echo "Error: No se encontró ningún archivo que coincida con el patrón '*_sacbe.varfile.ex.EDITED' en el directorio actual."
    exit 1
fi

# Obtener el encabezado del archivo de entrada
encabezado=$(awk 'NR==1' "$archivo_entrada")

# Archivo con la lista de genes
archivo_genes="Genes.csv"

# Verifica si el archivo de genes existe
if [ ! -f "$archivo_genes" ]; then
    echo "Error: No se encontró el archivo 'Genes.csv' en el directorio actual."
    exit 1
fi

# Itera a través de cada línea en el archivo (omitir la primera línea con `tail`)
tail -n +2 "$archivo_genes" | while IFS=',' read -r GENE CHR START END; do
    # Limpia el valor de CHR para asegurarte de que no contenga caracteres inesperados
    chrom=$(echo "$CHR" | tr -cd '[:alnum:]')
    
    # Define la ruta del archivo de salida
    archivo_salida="${OUTPUT_DIRECTORY}/sacbe_genes/${GENE}_sacbe.tsv"
    
    # Agrega el encabezado al archivo de salida
    echo "$encabezado" > "$archivo_salida"
    
    # Filtrar y agregar líneas al archivo de salida
    awk -F'\t' -v GENE="$GENE" '$18 ~ GENE' "$archivo_entrada" >> "$archivo_salida"
done
