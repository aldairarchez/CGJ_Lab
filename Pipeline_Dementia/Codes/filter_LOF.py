import sys
import pandas as pd

# Obtener el valor de "gene" del argumento de línea de comandos
gene = sys.argv[1]

# Cargar el archivo CSV en un DataFrame
# data = pd.read_csv('GRN_MCPS1.tsv', sep='\t', encoding='utf-8')
data = pd.read_csv(f'{gene}_inclinvar1.tsv', sep='\t', encoding='utf-8')
pattern = r"frameshift|start_lost|stop_gained|stop_lost|splice_donor|splice_acceptor|splice_region"
# Crear una nueva columna 'LOF' y llenarla con 'yes' o 'no' según el filtro
data['LOF'] = data['Annotations'].str.contains(pattern, regex=True).map({True: 'YES', False: 'NO'})
# Guardar los datos en un nuevo archivo
data.to_csv(f'{gene}_MCPS.tsv', sep='\t', index=False)


#ARCHIVO NOT IN CLINVAR
data = pd.read_csv(f'{gene}_notclinvar.tsv', sep='\t', encoding='utf-8')
pattern = r"frameshift|start_lost|stop_gained|stop_lost|splice_donor|splice_acceptor|splice_region"
# Crear una nueva columna 'LOF' y llenarla con 'yes' o 'no' según el filtro
data['LOF'] = data['Annotations'].str.contains(pattern, regex=True).map({True: 'YES', False: 'NO'})
# Guardar los datos en un nuevo archivo
data.to_csv(f'{gene}_notclinvar.tsv', sep='\t', index=False
