import sys
import pandas as pd

    # Obtener el valor de "gene" del argumento de línea de comandos
    #gene = sys.argv[1]

# Leer la lista de genes desde LOF_genes.txt
with open('LOF_genes.txt', 'r') as file:
        gene_list = file.read().splitlines()

# Iterar sobre cada gen en la lista
for gene in gene_list:
    # Cargar el archivo TSV en un DataFrame
    input_file = f'/mnt/Timina/cgonzaga/marciniega/Dementia_MCPS/sacbe_genes/{gene}_sacbe.csv'
    data = pd.read_csv(input_file, sep='\t', encoding='utf-8')

    # Lista de palabras clave exactas
    keywords = [
        "exonic;splicing",
        "splicing",
        "frameshift deletion",
        "frameshift insertion",
        "stopgain SNV",
        "stoploss SNV"
    ]

    # Función para verificar si una celda contiene alguna palabra clave exacta
    def contains_exact_keyword(cell, keywords):
        return any(cell == keyword for keyword in keywords)

    # Filtrar las filas que contienen alguna palabra clave exacta en alguna celda
    filtered_data = data[data.apply(lambda row: any(contains_exact_keyword(str(value), keywords) for value in row), axis=1)]

    # Especificar el archivo de salida
    output_file = f'/mnt/Timina/cgonzaga/marciniega/Dementia_MCPS/LOF_files/{gene}_LOF_annotation.tsv'

    # Guardar el DataFrame filtrado como un archivo TSV
    filtered_data.to_csv(output_file, sep='\t', index=False, encoding='utf-8')
