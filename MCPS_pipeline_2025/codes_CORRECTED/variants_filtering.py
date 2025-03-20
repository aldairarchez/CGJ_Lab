import sys
import os
import pandas as pd

# Obtener argumentos de línea de comandos
OUTPUT_DIRECTORY = sys.argv[1]

# Leer la lista de genes y sus tipos de análisis
with open('Genes_list.txt', 'r') as file:
    lines = file.read().splitlines()
    gene_data = [line.split('\t') for line in lines]  # Dividir en columnas: gen y tipo de análisis

# Iterar sobre cada gen y tipo de análisis
for gene, analysis_type in gene_data:
    # Verificar si el tipo de análisis es válido
    if analysis_type not in ["LOF", "GOF"]:
        print(f"Error: Tipo de análisis inválido '{analysis_type}' para el gen {gene}. Debe ser 'LOF' o 'GOF'.")
        continue

    # Definir palabras clave según el tipo de análisis
    keywords = [
        "exonic;splicing", "splicing", "frameshift deletion", 
        "frameshift insertion", "stopgain SNV", "stoploss SNV"
    ] if analysis_type == "LOF" else ["nonsynonymous SNV"]

    # Cargar los datos de Sacbe
    sacbe_file = f'{OUTPUT_DIRECTORY}/sacbe_genes/{gene}_sacbe.tsv'
    try:
        sacbe_data = pd.read_csv(sacbe_file, sep='\t', encoding='utf-8')
    except FileNotFoundError:
        print(f"Advertencia: No se encontró el archivo {sacbe_file}. Saltando este gen.")
        continue

    # Verificar si la columna 15 existe en Sacbe
    if sacbe_data.shape[1] < 15:
        print(f"Advertencia: El archivo {sacbe_file} no tiene 15 columnas. Saltando este gen.")
        continue

    # Agregar columna de anotación (YES/NO)
    sacbe_data['Annotation_Match'] = sacbe_data.apply(
        lambda row: 'YES' if any(str(value) in keywords for value in row) else 'NO', axis=1
    )

    # Cargar datos de ClinVar
    clinvar_file = f'{OUTPUT_DIRECTORY}/ClinVar/{gene}_clinvar.tsv'
    try:
        clinvar_data = pd.read_csv(clinvar_file, sep='\t', encoding='utf-8')
    except FileNotFoundError:
        print(f"Advertencia: No se encontró el archivo {clinvar_file}. Saltando este gen.")
        continue

    # Verificar si la columna 1 existe en ClinVar
    if clinvar_data.shape[1] < 1:
        print(f"Advertencia: El archivo {clinvar_file} no tiene columnas. Saltando este gen.")
        continue

    # Agregar columna de presencia en ClinVar (YES/NO)
    sacbe_data['ClinVar_Match'] = sacbe_data.iloc[:, 14].apply(
        lambda variant: 'YES' if variant in clinvar_data.iloc[:, 0].values else 'NO'
    )

    # Filtrar datos según el tipo de análisis
    if analysis_type == "LOF":
        filtered_data = sacbe_data[
            (sacbe_data['Annotation_Match'] == 'YES') | (sacbe_data['ClinVar_Match'] == 'YES')
        ]
    else:  # GOF
        filtered_data = sacbe_data[
            ((sacbe_data['Annotation_Match'] == 'YES') & (sacbe_data['ClinVar_Match'] == 'YES')) |
            (sacbe_data['ClinVar_Match'] == 'YES')
        ]

    # Crear el directorio de salida si no existe
    output_dir = f'{OUTPUT_DIRECTORY}/{analysis_type}_files'
    os.makedirs(output_dir, exist_ok=True)

    # Guardar el archivo filtrado
    output_file = f'{output_dir}/{gene}_{analysis_type}_filtered.tsv'
    filtered_data.to_csv(output_file, sep='\t', index=False, encoding='utf-8')
