### Esto se corre dentro del directorio donde guardaremos los archivos de cada cromosoma de MCPS
```bash
chmod +x sacbe_type.py
qsub chromosomes.sge
```
* [sacbe_type.py](https://github.com/aldairarchez/CGJ_Lab/blob/main/Sacbe_annotation/Codes/sacbe_padded.py)
* [chromosomes.sge](https://github.com/aldairarchez/CGJ_Lab/blob/main/Sacbe_annotation/Codes/chromosomes.sge)

### Esto se corre dentro del directorio donde guardaremos los archivos de cada gen listo para la anotación sacbe
```bash
chmod +x sacbe_padded.py
qsub sacbe_annotation.sge
```
* [sacbe_padded.py](https://github.com/aldairarchez/CGJ_Lab/blob/main/Sacbe_annotation/Codes/sacbe_padded.py)
* [sacbe_annotation.sge](https://github.com/aldairarchez/CGJ_Lab/blob/main/Sacbe_annotation/Codes/sacbe_annotation.sge)

### Generación de un archivo único concatenando TODOS los archivos finales (1 por cada gen)
primero deberemos crear un directorio a donde se enviará este nuevo archivo, aqui se provee un ejemplo:
```bash
mkdir Sacbe
# Copiar el contenido del primer archivo sin cambios (esto para mantener el encabezado)
cat $(ls *_sacbe.csv | head -n 1) > /mnt/Timina/cgonzaga/marciniega/MCPS_22/Sacbe/Tania_sacbe.csv #aqui se pone la direccion del directorio Sacbe
# Concatenar el contenido de los archivos restantes omitiendo el encabezado
for file in $(ls *_sacbe.csv | tail -n +2); do
    tail -n +2 $file >> /mnt/Timina/cgonzaga/marciniega/MCPS_22/Sacbe/Tania_sacbe.csv
done
```
