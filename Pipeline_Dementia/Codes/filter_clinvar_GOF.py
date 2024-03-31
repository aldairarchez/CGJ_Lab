# -*- coding: utf-8 -*-
import sys
import pandas as pd

# Obtener el valor de "gene" del argumento de línea de comandos
gene = sys.argv[1]

# Cargar el archivo CSV en un DataFrame
data = pd.read_csv('/mnt/Timina/cgonzaga/marciniega/Dementia_2024/genes_files/'+f'{gene}_GOF.tsv', sep='\t', encoding='utf-8')

pattern = r"(Pathogenic|Likely_pathogenic)"

# Utilizar str.extract para obtener grupos de coincidencia en lugar de str.contains
filtered_data = data[data['CLNSIG_2'].str.extract(pattern, expand=False).notna()] #CLNSIG_2 es la columna mas actualizada de la significancia en clinvar

# Guardar los datos filtrados en un nuevo archivo
filtered_data.to_csv('/mnt/Timina/cgonzaga/marciniega/Dementia_2024/genes_files/'+f'{gene}_inclinvar_pathogenic.tsv', sep='\t', index=False) 


