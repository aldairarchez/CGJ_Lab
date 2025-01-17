import sys
import pandas as pd

# Obtener el valor de OUTPUT_DIRECTORY desde el argumento de línea de comandos
OUTPUT_DIRECTORY = sys.argv[1]

# Leer la lista de genes desde LOF_genes.txt
lof_genes_path = f"{OUTPUT_DIRECTORY}/LOF_genes.txt"
with open(lof_genes_path, 'r') as file:
    gene_list = file.read().splitlines()

# Iterar sobre cada gen en la lista
for gene in gene_list:
    # Definir los archivos de entrada y salida
    sacbeLOF_file = f"{OUTPUT_DIRECTORY}/LOF_files/{gene}_LOF_annotation.tsv"
    clinvar_file = f"{OUTPUT_DIRECTORY}/{gene}_clinvar.tsv"
    
    # Output sin el filtro de significancia de ClinVar
    output_file_nonfiltered = f"{OUTPUT_DIRECTORY}/LOF_files/{gene}_inclinvar_nonfiltered.tsv"
    
    # Output de variantes patogénicas y probablemente patogénicas
    output_file_filtered = f"{OUTPUT_DIRECTORY}/LOF_files/{gene}_inclinvar.tsv"

    # Leer los archivos en DataFrames
    sacbeLOF_df = pd.read_csv(sacbeLOF_file, sep='\t')
    clinvar_df = pd.read_csv(clinvar_file, sep='\t')

    # Hacer merge de los DataFrames usando la columna 15 de sacbeLOF y la columna 1 de clinvar
    combined_df = pd.merge(sacbeLOF_df, clinvar_df, left_on=sacbeLOF_df.columns[14], right_on=clinvar_df.columns[0], how='left')

    # Rellenar NaN con puntos
    combined_df.fillna('.', inplace=True)

    # Guardar el resultado en el archivo de salida sin filtrar
    combined_df.to_csv(output_file_nonfiltered, sep='\t', index=False)

    # Filtrar las variantes patogénicas y probablemente patogénicas
    pattern = r"(Pathogenic|Likely_pathogenic|\.)"
    filtered_data = combined_df[combined_df['CLNSIG_2'].str.extract(pattern, expand=False).notna()]

    # Guardar el dataframe filtrado
    filtered_data.to_csv(output_file_filtered, sep='\t', index=False)
