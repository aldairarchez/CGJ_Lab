import sys
import pandas as pd
import os

# Obtener el valor del archivo de entrada desde los argumentos
archivo = sys.argv[1]

# Extraer el nombre del gen del archivo
nombre_gen = os.path.basename(archivo).split('_')[0]

# Definir el directorio de salida
output_dir = os.path.dirname(archivo)

# Leer el archivo TSV de entrada
cpras_variantes = pd.read_csv(archivo, sep='\t', encoding='utf-8')

# Crear un DataFrame para la anotación
column_names = ['#CHR', 'START', 'END', 'REF', 'ALT', 'ZYG', 'SOURCE', 'QUAL', 'AC_RAW', 'AN_RAW', 'AF_RAW', 'GQ', 'PL', 'VCF_INFO']
annotation = pd.DataFrame(columns=column_names)

# Procesar las variantes
for i in range(len(cpras_variantes)):
    cpra_i = cpras_variantes['VCF_INFO'][i].split(':')
    chromosome_i = 'chr' + cpra_i[0]
    if cpras_variantes['Type'][i] != 'SNP':
        position_i = int(cpra_i[1]) + 1
        if cpras_variantes['Type'][i] == 'Indel(Deletion)':
            alt_i = '-'
            ref_i = ''.join([*cpra_i[2]][1:])
            len_ref = len(ref_i)
            start_i = position_i
            end_i = position_i + len_ref - 1
        elif cpras_variantes['Type'][i] == 'Indel(Insertion)':
            ref_i = '-'
            alt_i = ''.join([*cpra_i[3]][1:])
            start_i = end_i = position_i
    else:
        start_i = end_i = cpra_i[1]
        ref_i, alt_i = cpra_i[2], cpra_i[3]

    row_i = [chromosome_i, start_i, end_i, ref_i, alt_i, '.', cpras_variantes['SOURCE'][i], '.', cpras_variantes['AC_RAW'][i], cpras_variantes['AN_RAW'][i], cpras_variantes['AF_RAW'][i], '.', '.', cpras_variantes['VCF_INFO'][i]]
    annotation = pd.concat([annotation, pd.DataFrame([row_i], columns=column_names)])

# Guardar el archivo CSV de salida con el nombre del gen
output_file = os.path.join(output_dir, f"{nombre_gen}_sacbe.csv")
annotation.to_csv(output_file, sep=',', index=False)
