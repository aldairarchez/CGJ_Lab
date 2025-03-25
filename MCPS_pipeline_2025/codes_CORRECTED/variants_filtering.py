import sys
import os
import pandas as pd

# Obtener el directorio de salida desde los argumentos de línea de comandos
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

    # Filtrar variantes patogénicas en ClinVar
    pathogenic_significance = ["pathogenic", "likely pathogenic", "pathogenic/likely pathogenic"]
    clinvar_data_filtered = clinvar_data[
        clinvar_data.iloc[:, 5].str.lower().isin(pathogenic_significance)  # Suponiendo que la columna 6 (índice 5) es "CLINSIG"
    ]

    # Agregar columna de presencia en ClinVar (YES/NO) para variantes patogénicas
    sacbe_data['ClinVar_Match'] = sacbe_data.iloc[:, 14].apply(
        lambda variant: 'YES' if variant in clinvar_data_filtered.iloc[:, 0].values else 'NO'
    )

    # Combinar datos de Sacbe y ClinVar filtrado
    combined_data = sacbe_data.merge(
        clinvar_data_filtered,
        how='left',  # Unión para incluir todas las filas de Sacbe y los datos de ClinVar coincidentes
        left_on=sacbe_data.columns[14],  # Columna 15 de Sacbe (índice 14)
        right_on=clinvar_data_filtered.columns[0]  # Columna 1 de ClinVar filtrado (índice 0)
    )

    # Filtrar datos según el tipo de análisis y las reglas establecidas
    if analysis_type == "LOF":
        # Para LOF, incluir variantes que cumplan con la anotación o sean patogénicas
        final_data = combined_data[
            (combined_data['Annotation_Match'] == 'YES') | (combined_data['ClinVar_Match'] == 'YES')
        ]
    else:  # GOF
        # Para GOF, incluir variantes que sean patogénicas o probablemente patogénicas en ClinVar,
        # independientemente de la anotación, así como las que cumplen con la anotación y estén en ClinVar
        final_data = combined_data[
            (combined_data['ClinVar_Match'] == 'YES') |  # Variantes patogénicas o probablemente patogénicas
            ((combined_data['Annotation_Match'] == 'YES') & (combined_data['ClinVar_Match'] == 'YES'))
        ]

    # Crear el directorio de salida si no existe
    output_dir = f'{OUTPUT_DIRECTORY}/{analysis_type}_files'
    os.makedirs(output_dir, exist_ok=True)

    # Guardar el archivo combinado y filtrado preliminarmente
    output_file = f'{output_dir}/{gene}_{analysis_type}_final.tsv'
    final_data.to_csv(output_file, sep='\t', index=False, encoding='utf-8')

    # Cargar el archivo final para realizar el filtrado adicional
    try:
        final_data = pd.read_csv(output_file, sep='\t', encoding='utf-8')
    except FileNotFoundError:
        print(f"Advertencia: No se encontró el archivo {output_file}. Saltando este gen.")
        continue

    # Filtrar variantes según la columna 70 (CLINSIG)
    if final_data.shape[1] >= 70:  # Asegurarse de que la columna 70 exista
        pathogenic_significance = ["pathogenic", "likely pathogenic", "pathogenic/likely pathogenic"]
        final_data = final_data[
            (final_data.iloc[:, 69] == '.') |  # Mantener las variantes no reportadas (con ".")
            (final_data.iloc[:, 69].str.lower().isin(pathogenic_significance))  # Clasificaciones patogénicas
        ]
    else:
        print(f"Advertencia: El archivo {output_file} no tiene una columna 70. Saltando el filtrado adicional para este gen.")
        continue

    # Sobrescribir el archivo final con los datos filtrados por CLINSIG
    final_data.to_csv(output_file, sep='\t', index=False, encoding='utf-8')

