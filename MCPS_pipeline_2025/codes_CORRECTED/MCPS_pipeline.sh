#!/bin/bash

# Verificar que se proporcione un archivo de entrada
if [ $# -ne 1 ]; then
  echo "Uso: $0 <archivo_de_genes.txt>"
  exit 1
fi

# Archivo de entrada con la lista de genes y su tipo de análisis
GENES_FILE=$1

# Verificar si el archivo de entrada existe
if [ ! -f "$GENES_FILE" ]; then
  echo "Error: El archivo $GENES_FILE no existe."
  exit 1
fi

# Obtener el directorio actual como directorio de salida
OUTPUT_DIRECTORY=$(pwd)

# Ejecutar las dos primeras instrucciones solo una vez
echo "Ejecutando clinvar.sh..."
bash /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/clinvar.sh

echo "Ejecutando sacbe_individual.sh..."
bash /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/sacbe_individual.sh

# Cargar el módulo de Python
module load python38/3.8.3

# Leer el archivo de genes y procesar cada gen según su tipo
while IFS=$'\t' read -r GENE TYPE; do
  # Verificar si el tipo es válido
  if [[ "$TYPE" != "GOF" && "$TYPE" != "LOF" ]]; then
    echo "Error: Tipo inválido para el gen $GENE. Debe ser 'GOF' o 'LOF'."
    continue
  fi

  # Crear el directorio correspondiente (LOF_files o GOF_files)
  mkdir -p "${OUTPUT_DIRECTORY}/${TYPE}_files"

  # Ejecutar el script de filtrado para el gen y tipo actual
  echo "Ejecutando análisis para el gen $GENE ($TYPE)..."
  python3 /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/variants_filtering.py "$OUTPUT_DIRECTORY" "$TYPE"

  echo "Análisis para el gen $GENE ($TYPE) completado. Archivos en: ${OUTPUT_DIRECTORY}/${TYPE}_files"
done < "$GENES_FILE"

echo "Proceso completado."
