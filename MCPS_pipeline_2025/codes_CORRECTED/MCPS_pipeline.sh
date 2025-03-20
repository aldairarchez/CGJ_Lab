#!/bin/bash

#obtains a file for each gene from the GENES.txt file with the variants found in ClinVar
bash /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/clinvar.sh
#obtains a file per gene from the file made by Claudia's script
bash /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/sacbe_individual.sh


# Usar el directorio desde donde se ejecuta el script como output directory
OUTPUT_DIRECTORY=$(pwd)

# Verificar que se proporcione un argumento
if [ $# -ne 1 ]; then
  echo "Uso: $0 <GOF|LOF>"
  exit 1
fi

# Obtener el tipo (GOF o LOF)
TYPE=$1

# Verificar si el argumento es válido
if [[ "$TYPE" != "GOF" && "$TYPE" != "LOF" ]]; then
  echo "Error: El argumento debe ser 'GOF' o 'LOF'."
  exit 1
fi

# Crear el directorio correspondiente (LOF_files o GOF_files)
mkdir -p "${OUTPUT_DIRECTORY}/${TYPE}_files"

# Cargar el módulo de Python
module load python38/3.8.3

# Ejecutar el script unificado de filtrado
echo "Ejecutando análisis para $TYPE..."
python3 /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/variants_filtering.py "$OUTPUT_DIRECTORY" "$TYPE"

echo "Análisis para $TYPE completado. Archivos en: ${OUTPUT_DIRECTORY}/${TYPE}_files"
