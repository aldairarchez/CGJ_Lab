import sys
import pandas as pd

# Obtener el valor de "gene" del argumento de línea de comandos
archivo = sys.argv[1]
# Extraer la parte del nombre del gen del archivo
nombre_variable = archivo.split('_')[0]
# Cargar el archivo CSV en un DataFrame
cpras_variantes = pd.read_csv(f'{archivo}', sep='\t', encoding='utf-8')
# Crear tabla con el nombre de las columnas que queremos
column_names = ['#CHR', 'START', 'END', 'REF', 'ALT', 'ZYG', 'SOURCE', 'QUAL', 'AC_RAW', 'AN_RAW', 'AF_RAW', 'GQ', 'PL', 'VCF_INFO']
annotation = pd.DataFrame(columns=column_names)
# En esta función vamos a crear la anotación para llenar correctamente la tabla que acabamos de crear
#En esta funcion vamos a crear la anotacion para llenar correctamente la tabla que acabamos de crear
for i in range(len(cpras_variantes)):
    #primero tenemos que separar el cpra que nos dara: cromosoma, posicion, referencia, alternativo.
    cpra_i=cpras_variantes['VCF_INFO'][i].split(':')
    #obtenemos la variable de cromosoma, agregamos 'chr' y el numero de cromosoma que sacamos del cpra
    chromosome_i='chr'+cpra_i[0]
    #ahora, separaremos las acciones dependiendo del tipo de mutacion
    ##como los SNPs es cambio de una base nitrogenada, no se tienen que hacer muchas modificiaciones, entonces si no son SNP, deben entrar a este loop
    if cpras_variantes['Type'][i] != 'SNP':
        #lo primero que hay que hacer es cambiar la posicion, ya que toman en cuenta una base antes de la mutacion
        #es decir, sumamos una posicion para dar con el inicio de la mutacion
        position_i=int(cpra_i[1])+1
        #para obtener la posicion de inicio y final, ref, y alt sera diferente dependiendo para deleciones e inserciones
        ## primero el caso de deleciones
        if cpras_variantes['Type'][i]=='Indel(Deletion)':
            #el alternativo es una delecion, entonces no hay bases
            alt_i= '-'
            #para la referencia vamos a quitar la primera base que esta antes de la mutacion
            ##para eso separamos el string
            ref_i=[*cpra_i[2]]
            ##eliminamos la primer casilla
            ref_i.pop(0)
            #obtenemos la longitud de la delecion
            len_ref=len(ref_i)
            ##volvemos a unir la delecion en un string
            ref_i="".join(ref_i)
            #posicion de inicio
            start_i=position_i
            #posicion de final
            end_i=int(position_i)+int(len_ref)-1
        if cpras_variantes['Type'][i]=='Indel(Insertion)':
            #el alternativo es una delecion, entonces no hay bases
            ref_i= '-'
            #para la referencia vamos a quitar la primera base que esta antes de la mutacion
            ##para eso separamos el string
            alt_i=[*cpra_i[3]]
            ##eliminamos la primer casilla
            alt_i.pop(0)
            ##volvemos a unir la delecion en un string
            alt_i="".join(alt_i)
            #posicion de inicio
            start_i=position_i
            #posicion de final
            end_i=position_i
    else:
        #en caso de que sea un snp, la posicion, ref y alt se mantienen igual
        start_i=cpra_i[1]
        end_i=cpra_i[1]
        ref_i=cpra_i[2]
        alt_i=cpra_i[3]
    #creamos la fila que sera añadida a nuestro data frame con la informacion que queremos, la informacion que no tenemos, sera sustituida por un '.'
    row_i=[chromosome_i, start_i, end_i, ref_i, alt_i, '.', cpras_variantes['SOURCE'][i], '.', cpras_variantes['AC_RAW'][i], cpras_variantes['AN_RAW'][i], cpras_variantes['AF_RAW'][i], '.', '.',cpras_variantes['VCF_INFO'][i]]
    #adjuntamos la fila al data DataFrame, se tiene que transformar la lista en un dataframe para poder unirla con nuestra tabla principal, por eso utilizamos el 'pd.DataFrame'
    annotation=pd.concat([annotation, pd.DataFrame([row_i], columns=column_names)])
#imprimimos la tabla para ver como queda
print(annotation)
#guardamos tabla como archivo csv
annotation.to_csv(f"{nombre_variable}_sacbe.csv", sep=',', index=False)
