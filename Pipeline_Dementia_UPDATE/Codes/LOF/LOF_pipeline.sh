#!/bin/bash
mkdir LOF_files
#cargamos el modulo de python
module load python38/3.8.3
#corremos el script que filtra la columna annotations para quedarnos con variantes de GOF
python3 LOF_annotation.py
#we run the script that merges clinvar with MCPS and filter by pathogenicity
python3 LOF_inclinvar.py
