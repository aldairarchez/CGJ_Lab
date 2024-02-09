import sys
import pandas as pd

# Obtener el valor de "gene" del argumento de línea de comandos
gene = sys.argv[1]

# Cargar el archivo CSV en un DataFrame
data = pd.read_csv(f'{gene}_inclinvar1.tsv', sep='\t', encoding='utf-8')

pattern = r"missense"

# Crear una nueva columna 'GOF' y llenarla con 'YES' o 'NO' según el filtro
data['GOF'] = data['Annotations'].str.contains(pattern, regex=True).map({True: 'YES', False: 'NO'})

# Guardar los datos en un nuevo archivo
data.to_csv(f'{gene}_MCPS.tsv', sep='\t', index=False)