import os
import urllib.request

url = 'https://www.cs.ucr.edu/%7Eeamonn/time_series_data_2018/DataSummary.csv'
planilha_dir = 'Dataset'
download_path = os.path.join(planilha_dir, os.path.basename(url))

# Criando diretório 'Dataset'
os.makedirs(planilha_dir, exist_ok=True)

# Baixando a planilha
if not os.path.exists(download_path):
    urllib.request.urlretrieve(url, download_path)