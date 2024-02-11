#!/bin/bash
#cargar modulo
module load bcftools/1.10.2
#abrir el archivo GENES.txt
gene_list=($(cat GENES.txt))

for gene in "${gene_list[@]}"; do
  # filtrando por gen y significancia en clinvar, la opcion grep -w omite palabras que empiezan igual y -E excluye similitudes
  filtrado=$(bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t%ID\t %INFO[%GENEINFO\t%ID%CLNDN\t%CLNHGVS\t%CLNSIG\t%CLNVC\t%AF_ESP\t%AF_EXAC\t%AF_TGP %MC]\n'     clinvar.vcf | grep -w "GENEINFO=$gene")
  echo "$filtrado" > "$gene".vcf
  #quita los ; y agrega tabs
  sed -i 's/;/\t/g' "$gene".vcf
  ## creando el archivo (guardamos el CPRA, 4 primeras columnas)
  awk '{print $1,$2,$3,$4}' "$gene".vcf > "$gene"_clinvar.tsv 
  #corriendo el archivo concatenate columns pero dentro del pipeline
  columns_list=($(cat columns.txt))
  #abre el archivo de donde se obtendrán las columnas deseadas
  archivo="$gene.vcf"
  #archivo vacio que servira para vaciar el archivo  en cada iteracion 
  touch archivo_vacio.tsv
  cp archivo_vacio.tsv temporal.tsv
  columns_list=($(cat columns.txt))
  archivo="$gene".vcf
  #el ciclo for se encarga de obtener las columnas solicitadas
  for column in "${columns_list[@]}"; do
    #se inicializa el archivo 
    cp archivo_vacio.tsv columna.tsv 
    #el while obtiene linea por linea de la columna solicitada y agrega NA si el campo está vacio
    while IFS= read -r linea; do
      resultado=$(grep -o "$column=.*" <<< "$linea" | awk -F'\t' '{print $1}' | sed "s/$column=//")

      if [ -z "$resultado" ]; then
        resultado="NA"
      fi

      echo "$resultado" >> columna.tsv
    done < "$archivo"

    paste "$gene"_clinvar.tsv  columna.tsv > temporal.tsv
    cp temporal.tsv "$gene"_clinvar.tsv
  done
  #unir primeras 4 columnas con ":" iintermedios para crear nuestro CPRA
  awk '{print $1":"$2":"$3":"$4"\t"$5"\t"$6"\t"$7"\t"$8"\t"$9"\t"$10"\t"$11"\t"$12"\t"$13"\t"$14}' "$gene"_clinvar.tsv > "$gene"_Clinvar.tsv
  #vaciamos el archivo para sobreescribirlo
  cp archivo_vacio.tsv "$gene"_clinvar.csv
  ### agregar nombre a las columnas
  echo -e "CPRA\tGENEINFO\tRS_ID\tCLNDN_2\tCLNHGVS\tCLNSIG_2\tCLNVC\tAF_ESP\tAF_EXAC\tAF_TGP\tMC" | cat - "$gene"_Clinvar.tsv > "$gene"_clinvar.csv
  # eliminar el archivo sin encabezado
  rm "$gene"_Clinvar.tsv
  rm "$gene".vcf
  rm columna.tsv
  #lo pasamos a un archivo csv
  sed -i 's/\t/,/g' "$gene"_clinvar.csv
done < GENES.txt
rm archivo_vacio.tsv
rm temporal.tsv

