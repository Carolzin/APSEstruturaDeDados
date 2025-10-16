import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# -------------------------------
# Caminhos dos arquivos
# -------------------------------
input_path = "../resultados/prodes_agregado_estado_ano.csv"
output_path = "../resultados/previsoes_prodes_por_estado.csv"

# -------------------------------
# Carrega os dados
# -------------------------------
prodes = pd.read_csv(input_path, sep=";", encoding="utf-8-sig")

print("Colunas:", prodes.columns.tolist())
print("Primeiras linhas:")
print(prodes.head())

# -------------------------------
# Converte coluna 'year' para int
# -------------------------------
prodes["year"] = prodes["year"].astype(str).str[:4].astype(int)

# -------------------------------
# Criar lista para armazenar previsões
# -------------------------------
todas_previsoes = []

# -------------------------------
# Iterar por estado e treinar modelo separado
# -------------------------------
for estado in prodes["state"].unique():
    dados_estado = prodes[prodes["state"] == estado]
    
    X = dados_estado[["year"]]
    y = dados_estado["areakm"]
    
    # Treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Modelo Linear Regression
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    
    # Avaliação
    y_pred = modelo.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nEstado: {estado}")
    print(f"MSE: {mse:.2f}, R²: {r2:.2f}")
    
    # Previsões para próximos 6 anos
    anos_futuros = np.arange(2025, 2031).reshape(-1, 1)
    previsoes = modelo.predict(anos_futuros)
    
    df_previsoes = pd.DataFrame({
        "Estado": estado,
        "Ano": anos_futuros.flatten(),
        "Área Prevista (km²)": previsoes
    })
    
    todas_previsoes.append(df_previsoes)

# -------------------------------
# Concatenar todas previsões e salvar
# -------------------------------
resultado_final = pd.concat(todas_previsoes, ignore_index=True)
os.makedirs(os.path.dirname(output_path), exist_ok=True)
resultado_final.to_csv(output_path, index=False, sep=";", encoding="utf-8-sig")

print(f"\n✅ Previsões por estado salvas em: {output_path}")
print(resultado_final.head(12))
