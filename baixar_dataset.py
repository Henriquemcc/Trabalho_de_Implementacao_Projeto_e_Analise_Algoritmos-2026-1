import os
import urllib.request
import zipfile

url = 'https://www.cs.ucr.edu/%7Eeamonn/time_series_data_2018/UCRArchive_2018.zip'
dataset_dir = 'Dataset'
download_path = os.path.join(dataset_dir, os.path.basename(url))
password = 'someone'

# Criando diretório 'Dataset'
os.makedirs(dataset_dir, exist_ok=True)

# Baixando base de dados
if not os.path.exists(download_path):
    urllib.request.urlretrieve(url, download_path)

# Descompactando arquivo zip
if not os.path.isdir(os.path.join(dataset_dir, 'UCRArchive_2018')):
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall(path=dataset_dir, pwd=password.encode('utf-8'))
