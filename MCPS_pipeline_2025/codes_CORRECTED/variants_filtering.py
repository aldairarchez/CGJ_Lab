import sys
import pandas as pd

# Obtener argumentos de línea de comandos
OUTPUT_DIRECTORY = sys.argv[1]

# Leer la lista de genes y el tipo de análisis
with open('Genes_list.txt', 'r') as file:
    lines = file.read().splitlines()
    gene_list = [line.split('\t')[0] for line in lines]  # Primera columna: nombres de los genes
    analysis_type = lines[0].split('\t')[1].strip()  # Segunda columna: tipo de análisis (LOF o GOF)

# Verificar si el tipo de análisis es válido
if analysis_type not in ["LOF", "GOF"]:
    print("Error: El tipo de análisis en Genes_list.txt debe ser 'LOF' o 'GOF'.")
    sys.exit(1)

# Definir palabras clave según el tipo de análisis
if analysis_type == "LOF":
    keywords = [
        "exonic;splicing", "splicing", "frameshift deletion",
        "frameshift insertion", "stopgain SNV", "stoploss SNV"
    ]
elif analysis_type == "GOF":
    keywords = ["nonsynonymous SNV"]

# Iterar sobre cada gen en la lista
for gene in gene_list:
    # Cargar los datos de Sacbe
    sacbe_file = f'{OUTPUT_DIRECTORY}/sacbe_genes/{gene}_sacbe.tsv'
    try:
        sacbe_data = pd.read_csv(sacbe_file, sep='\t', encoding='utf-8')
    except FileNotFoundError:
        print(f"Advertencia: No se encontró el archivo {sacbe_file}. Saltando este gen.")
        continue

    # Verificar si la columna 15 existe en Sacbe
    if sacbe_data.shape[1] < 15:  # Verificar que haya al menos 15 columnas
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
    if clinvar_data.shape[1] < 1:  # Verificar que haya al menos 1 columna
        print(f"Advertencia: El archivo {clinvar_file} no tiene columnas. Saltando este gen.")
        continue

    # Agregar columna de presencia en ClinVar (YES/NO)
    sacbe_data['ClinVar_Match'] = sacbe_data.iloc[:, 14].apply(  # Columna 15 (índice 14)
        lambda variant: 'YES' if variant in clinvar_data.iloc[:, 0].values else 'NO'  # Columna 1 (índice 0)
    )
    
    # Filtrar datos según el tipo de análisis
    if analysis_type == "LOF":
        # Para LOF, las variantes deben cumplir con la anotación O estar en ClinVar
        filtered_data = sacbe_data[(sacbe_data['Annotation_Match'] == 'YES') | (sacbe_data['ClinVar_Match'] == 'YES')]
    else:  # GOF
        # Para GOF, las variantes deben cumplir con la anotación Y estar en ClinVar, 
        # o estar en ClinVar aunque no cumplan con la anotación
        filtered_data = sacbe_data[
            ((sacbe_data['Annotation_Match'] == 'YES') & (sacbe_data['ClinVar_Match'] == 'YES')) |
            (sacbe_data['ClinVar_Match'] == 'YES')
        ]
    
    # Guardar el archivo filtrado
    output_file = f'{OUTPUT_DIRECTORY}/{analysis_type}_files/{gene}_{analysis_type}_filtered.tsv'
    filtered_data.to_csv(output_file, sep='\t', index=False, encoding='utf-8')
