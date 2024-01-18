import os
import pandas as pd

# Directorio actual
directorio = os.getcwd()

# Crear una función para determinar el tipo
def determinar_tipo(fila):
    if len(fila['ALT']) == len(fila['REF']):
        return 'SNP'
    elif len(fila['ALT']) > len(fila['REF']):
        return 'Indel(Insertion)'
    else:
        return 'Indel(Deletion)'

# Diccionario para almacenar los DataFrames
dataframes = {}

# Bucle para procesar cada archivo en el directorio actual
for archivo in os.listdir(directorio):
    # Verificar si el archivo es un archivo tsv y seguir si es así
    if archivo.endswith("_parsed.tsv"):
        # Construir el nombre de la variable sin la extensión
        nombre_variable = archivo.replace("_parsed.tsv", "")
        # Leer el contenido del archivo y asignarlo a una variable usando Pandas
        dataframes[nombre_variable] = pd.read_csv(archivo, sep='\t', encoding='utf-8')
        # Aplicar la función para crear la nueva columna 'type'
        dataframes[nombre_variable]['Type'] = dataframes[nombre_variable].apply(determinar_tipo, axis=1)
        # Guardar el DataFrame en un archivo *_type.tsv
        dataframes[nombre_variable].to_csv(f"df_{nombre_variable}_type.tsv", sep='\t', index=False)
