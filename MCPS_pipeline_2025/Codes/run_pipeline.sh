#!/bin/bash
#obtains a file for each gene from the GENES.txt file with the variants found in ClinVar
bash /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/clinvar.sh
#obtains a file per gene from the file made by Claudia's script
bash /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/sacbe_individual.sh

# Usar el directorio desde donde se ejecuta el script como output directory
OUTPUT_DIRECTORY=$(pwd)

# Archivo de marcador para verificar si las primeras instrucciones ya se ejecutaron
FLAG_FILE="${OUTPUT_DIRECTORY}/initial_setup_done.flag"

# Verificar si las primeras instrucciones ya se ejecutaron
if [ ! -f "$FLAG_FILE" ]; then
    echo "Ejecutando las primeras instrucciones..."

    # Crea un subdirectorio en el directorio actual para guardar los archivos individuales
    mkdir -p "${OUTPUT_DIRECTORY}/sacbe_genes"

    # Archivo de entrada basado en el patrón (se espera que exista un archivo que coincida con el patrón)
    archivo_entrada=$(ls *_sacbe.varfile.ex.EDITED 2>/dev/null)

    # Verifica si existe un archivo que coincida con el patrón
    if [ -z "$archivo_entrada" ]; then
        echo "Error: No se encontró ningún archivo que coincida con el patrón '*_sacbe.varfile.ex.EDITED' en el directorio actual."
        exit 1
    fi

    # Crear el archivo de marcador para indicar que estas instrucciones ya se ejecutaron
    touch "$FLAG_FILE"
else
    echo "Las primeras instrucciones ya se ejecutaron, omitiendo..."
fi


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

#echo "Directorio de salida: $OUTPUT_DIRECTORY"

# Crear el directorio correspondiente (LOF_files or GOF_files)
mkdir -p "${OUTPUT_DIRECTORY}/${TYPE}_files"

# Cargar el módulo de Python
module load python38/3.8.3

# Ejecutar los scripts correspondientes
if [ "$TYPE" == "GOF" ]; then
  echo "Ejecutando análisis para GOF..."
  python3 /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/GOF_annotation.py "$OUTPUT_DIRECTORY"
  python3 /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/GOF_inclinvar.py "$OUTPUT_DIRECTORY"

elif [ "$TYPE" == "LOF" ]; then
  echo "Ejecutando análisis para LOF..."
  python3 /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/LOF_annotation.py "$OUTPUT_DIRECTORY"
  python3 /mnt/Timina/cgonzaga/resources/MCPS/Clinvar_Jan2025/MCPS_pipeline/LOF_inclinvar.py "$OUTPUT_DIRECTORY"
  
fi

echo "Análisis para $TYPE completado. Archivos en: ${OUTPUT_DIRECTORY}/${TYPE}_files"
