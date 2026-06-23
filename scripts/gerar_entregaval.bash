#!/bin/bash

# Trocando de diretório
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR/.." || exit 1

# Criando a pasta entrega
mkdir -p "entrega"

# Gerando programa.py
python ./scripts/empacotar.py ./app ./entrega/programa.py

# Copiando requisitos
cp ./requirements.txt ./entrega/requirements.txt

# Copiando os arquivos LaTeX
cp -r ./docs/artigo/. ./entrega

# Copiando Notebooks
cp ./notebooks/Experimentos_todo_dataset_alternativo.ipynb ./entrega/Experimentos.ipynb
cp ./notebooks/Metricas.ipynb ./entrega/Metricas.ipynb

# Zipando
cd entrega || exit 1
zip -9 -r Trabalho_Pratico_Henrique_Mendonca_Castelar_Campos.zip .