##### Codigo para unir la informacion de 3 tablas diferentes para tener en una tabla las frecuencias,cantidad de homocigotos y heterocigotos, y la lista de portadores

#Archivos input para correr el codigo:
    #file .frq is a basic allele frequency report
    #file .frqx is a genotype count report
    #file .rlist is a rare genotype list file

#Archivos output:
    #file .csv que contenga CPRA, CHR, POS, REF, ALT, MAF, HET, HOM, N-Miss, N-CHROBS, HET_CARR, HOM_CARR, NIL_CARR

######################## C O D I G O ########################################

#Iniciamos importando las paqueterias necesarias para correr el codigo
import pandas as pd #importing package that will help us to read the csv file, create dataframes, exporting the vcf file, etc.


#Cargamos los archivos input

## Basic Allele Frequency Report
### Para el reporte de frecuencias alelicas basicas necesitamos reformatear el documento. Esto debido a que el archivo parece tener
### 6 columnas, donde la informacion esta centrada, lo que resulta en variacion de tabs y espacios que separan la informacion.
frq=[]
with open("plink.frq", 'r') as file:
    for i, line in enumerate(file): #Aqui enumeramos la fila para no llevarnos el header
        # Separamos cada linea por espacio
        partes = line.strip().split(' ')
        # Eliminamos los elementos de la lista que esten vacios
        while("" in partes):
            partes.remove("")
        linea_reformateada = partes
        #añadimos la linea reformateada a la lista de lineas
        if i!=0: #Con excepcion del header, ese lo pondremos despues...
            frq.append(linea_reformateada)
## Transformamos la linea generada y formateada en Data Frame
allele_frq = pd.DataFrame(frq, columns=['CHR', 'CPRA', 'ALT', 'REF', 'MAF', 'NCHROBS'])

## Genotype Count Report
### Para el reporte del conteo de genotipo, solo tenemos que leer la tabla ya que esta si esta bien delimitada por tabs
genotype_count = pd.read_table("plink.frqx")

## Rare Genotype List
### Para la lista de genotipos raros tenemos que reformatear el documento. Esto debido a que la informacion esta delimitada por
### espacios, pero las columnas son variables. Se deben tener 4 columnas obligatorias: CPRA, Genotipo, Ref, Alt. Despues de esta
### informacion vienen los IDs de los portadores; las cuales tenemos que unir por ';' y asegurarnos que no se repitan los IDs.
frqx=[]
with open("plink.rlist", 'r') as file:
    for line in file:
        # Separamos cada linea por espacio
        partes = line.strip().split(' ')
        # Creamos la lista de los id de portadores separados por ';'
        ## Primero nos quedamos con la lista de los IDs, que estan despues del CPRA, Genotipo, Ref, Alt; es decir de la columna 4 para delante
        id_portadores= partes[4:]
        ## Nos quedamos con los valores unicos; esto lo podemos hacer utilizando el formato set, que volvemos a convertir en lista para nuestro formato
        id_portadores=list(set(id_portadores))
        ## Unimos la lista como string separado por ';'
        id_portadores = ';'.join(id_portadores)
        # A la linea reformateada agregamos la columna de CPRA, Genotipo y los ids de los portadores
        linea_formateada = [partes[0], partes[1], id_portadores]
        # Añadimos la linea reformateada a la lista de lineas
        frqx.append(linea_formateada)
genotype_list = pd.DataFrame(frqx, columns=['CPRA', 'GENOTYPE', 'CARR'])


# CREAMOS LA TABLA QUE CONTENGA INFORMACION DE LAS 3 tablas
data=[]
## Utilizaremos el archivo de reporte de frecuencias alelicas basicas como base para de ahi añadir el resto de columnas necesarias
for i in range(len(allele_frq)):
    #vamos a obtener la linea donde se encuentre la variante de la linea i del archivo frq en el archivo frqx
    k_frqx=genotype_count.index[genotype_count.SNP==allele_frq.CPRA[i]]
    #debido a que este archivo solo contiene una fila por variante, solo encontrara una posicion. Por eso, nos quedamos con la primera posicion de la lista
    k_frqx=k_frqx.tolist()[0]

    #vamos a obtener la linea donde se encuentre la variante de la linea i del archivo frq en el archivo rlist
    k_rlist=genotype_list.index[genotype_list.CPRA==allele_frq.CPRA[i]]
    print(k_rlist)
    #debido a que el archivo de genotipos puede tener mas de una fila con la variante, nos quedaremos con la lista de opciones
    k_rlist=k_rlist.tolist()
    #ahora exploraremos cada de esas opciones para ver el genotipo que es (HET, HOM, NIL)
    ## para saber si no tienen una categoria, pondremos una banderita y asi lo podremo llenar con '.'
    flag_het=0
    flag_hom=0
    flag_nil=0
    for j in range(len(k_rlist)):
        #si es heterocigoto lo agregamos a una variable que representa a los portadores heterocigotos
        if genotype_list.GENOTYPE[k_rlist[j]]=='HET':
            HET_CARR=genotype_list.CARR[k_rlist[j]]
            flag_het=1
        #si es homocigoto lo agregamos a una variable que representa a los portadores homocigotos
        elif genotype_list.GENOTYPE[k_rlist[j]]=='HOM':
            HOM_CARR=genotype_list.CARR[k_rlist[j]]
            flag_hom=1
        #si es NIL lo agregamos a una variable que representa a los portadores de missing variant
        elif genotype_list.GENOTYPE[k_rlist[j]]=='NIL':
            NIL_CARR=genotype_list.CARR[k_rlist[j]]
            flag_nil=1
    #si no pasaron por las categorias, tendran un valor de '.'
    if flag_het==0:
        HET_CARR='.'
    if flag_hom==0:
        HOM_CARR='.'
    if flag_nil==0:
        NIL_CARR='.'
    #despues vamos a obtener el cromosoma, posicion, referencia y alternativo del CPRA
    cpra_i=allele_frq.CPRA[i].split(':')
    chr_i=cpra_i[0]
    pos_i=cpra_i[1]
    ref_i=cpra_i[2]
    alt_i=cpra_i[3]

    #ya que tenemos la informacion que necesitamos, la agruparemos en una lista que representara nuestra fila en el dataframe
    nueva_fila=[allele_frq.CPRA[i], chr_i, pos_i, ref_i, alt_i, allele_frq.MAF[i],
    genotype_count['C(HET)'][k_frqx], genotype_count['C(HOM A1)'][k_frqx], genotype_count['C(MISSING)'][k_frqx], allele_frq.NCHROBS[i],
    HET_CARR, HOM_CARR, NIL_CARR]

    # agregamos la fila a nuestra lista de data
    data.append(nueva_fila)

## Creamos el DataFrame
tabla_portadores=pd.DataFrame(data, columns=['CPRA', 'CHR', 'POS', 'REF', 'ALT', 'MAF', 'HET', 'HOM(ALT)', 'N_MISS', 'N_CHROBS', 'HET_CARR', 'HOM_CARR', 'NIL_CARR'])

##Imprimimos tabla
print(tabla_portadores)
##Guardamos tabla
tabla_portadores.to_csv('portadores.csv', index=False)
