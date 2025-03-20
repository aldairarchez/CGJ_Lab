import sys
import pandas as pd

# Obtener argumentos de línea de comandos
OUTPUT_DIRECTORY = sys.argv[1]
TYPE = sys.argv[2]  # 'LOF' o 'GOF'

# Leer la lista de genes
with open('LOF_genes.txt', 'r') as file:
    gene_list = file.read().splitlines()

# Definir palabras clave según el tipo de análisis
if TYPE == "LOF":
    keywords = [
        "exonic;splicing", "splicing", "frameshift deletion",
        "frameshift insertion", "stopgain SNV", "stoploss SNV"
    ]
elif TYPE == "GOF":
    keywords = ["nonsynonymous SNV"]
else:
    print("Error: Tipo inválido. Debe ser 'LOF' o 'GOF'.")
    sys.exit(1)

# Iterar sobre cada gen en la lista
for gene in gene_list:
    # Cargar los datos de Sacbe
    sacbe_file = f'{OUTPUT_DIRECTORY}/sacbe_genes/{gene}_sacbe.tsv'
    sacbe_data = pd.read_csv(sacbe_file, sep='\t', encoding='utf-8')
    
    # Agregar columna de anotación (YES/NO)
    sacbe_data['Annotation_Match'] = sacbe_data.apply(
        lambda row: 'YES' if any(str(value) in keywords for value in row) else 'NO', axis=1
    )
    
    # Cargar datos de ClinVar
    clinvar_file = f'{OUTPUT_DIRECTORY}/ClinVar/{gene}_clinvar.tsv'
    clinvar_data = pd.read_csv(clinvar_file, sep='\t', encoding='utf-8')
    
    # Agregar columna de presencia en ClinVar (YES/NO)
    sacbe_data['ClinVar_Match'] = sacbe_data['ID'].apply(
        lambda variant: 'YES' if variant in clinvar_data['ID'].values else 'NO'
    )
    
    # Filtrar datos según el tipo de análisis
    if TYPE == "LOF":
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
    output_file = f'{OUTPUT_DIRECTORY}/{TYPE}_files/{gene}_{TYPE}_filtered.tsv'
    filtered_data.to_csv(output_file, sep='\t', index=False, encoding='utf-8')
