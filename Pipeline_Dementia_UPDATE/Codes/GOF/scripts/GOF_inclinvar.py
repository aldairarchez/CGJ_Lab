import pandas as pd

# Leer la lista de genes desde LOF_genes.txt
with open('GOF_genes.txt', 'r') as file:
        gene_list = file.read().splitlines()

# Iterar sobre cada gen en la lista
for gene in gene_list:
        # Definir los archivos de entrada y salida
        sacbeGOF_file = f"/mnt/Timina/cgonzaga/marciniega/Dementia_MCPS/GOF_files/{gene}_GOF_annotation.tsv"
        clinvar_file = f"/mnt/Timina/cgonzaga/marciniega/Dementia_MCPS/clinvar_genes/{gene}_clinvar.tsv"
        #output without clinvar significance filter
        output_file_nonfiltered = f"/mnt/Timina/cgonzaga/marciniega/Dementia_MCPS/GOF_files/{gene}_inclinvar_nonfiltered.tsv"
        #output of pathogenic and likely pathogenic variants
        output_file_filtered = f"/mnt/Timina/cgonzaga/marciniega/Dementia_MCPS/GOF_files/{gene}_inclinvar.tsv"

        # Leer los archivos en dataframes
        sacbeGOF_df = pd.read_csv(sacbeGOF_file, sep='\t')
        clinvar_df = pd.read_csv(clinvar_file, sep='\t')

        # Hacer merge de los dataframes usando la columna 15 de sacbeLOF y la columna 1 de clinvar
        #Utiliza pd.merge con how='inner' para hacer una combinación donde se incluyen SOLO las filas de sacbeLOF_df que tienen coincidencias con el archivo de clinvar.
        combined_df = pd.merge(sacbeGOF_df, clinvar_df, left_on=sacbeGOF_df.columns[14], right_on=clinvar_df.columns[0], how='inner')

        # Rellenar NaN con puntos
        combined_df.fillna('.', inplace=True)

        # Guardar el resultado en el archivo de salida
        combined_df.to_csv(output_file_nonfiltered, sep='\t', index=False)

        pattern = r"(Pathogenic|Likely_pathogenic)"
        # Utilizar str.extract para obtener grupos de coincidencia en lugar de str.contains
        filtered_data = combined_df[combined_df['CLNSIG_2'].str.extract(pattern, expand=False).notna()] #CLNSIG_2 es la columna mas actualizada de la significancia en clinvar
        # Guardar el dataframe filtrado
        filtered_data.to_csv(output_file_filtered, sep='\t', index=False)
