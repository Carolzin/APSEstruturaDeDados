
import pandas as pd
import os

dados_path = "../dados"

deter_file = os.path.join(dados_path, "DETER_BASE_DE_ALARMES.csv")
prodes_file = os.path.join(dados_path, "PRODES_BASE_DE_DESMATAMENTO_POR_ANOS.csv")

# Ler os CSVs
deter = pd.read_csv(deter_file, sep=",", encoding="utf-8-sig")
prodes = pd.read_csv(prodes_file, sep=";", encoding="utf-8-sig")  

print("Primeiras linhas do DETER:")
print(deter.head(), "\n")

print("Primeiras linhas do PRODES:")
print(prodes.head())
