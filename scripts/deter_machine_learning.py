import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# -------------------------------
# carregar dados tratados do DETER
# -------------------------------
dados_path = "../resultados"
arquivo_agregado = os.path.join(dados_path, "deter_agregado_uf_ano.csv")

df = pd.read_csv(arquivo_agregado, sep=";", encoding="utf-8-sig")

# tratar a coluna "year" (pegar o último ano do intervalo, ex: 2015/2016 -> 2016)
df["year"] = df["year"].astype(str).str.split("/").str[-1]
df["year"] = pd.to_numeric(df["year"], errors="coerce")

# remover linhas com ano nulo
df = df.dropna(subset=["year"])

# -------------------------------
# selecionar colunas e preparar dados
# -------------------------------
X = df[["year"]]
y = df["area"]

# dividir treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------------------
# criar e treinar o modelo
# -------------------------------
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# -------------------------------
# avaliar o modelo
# -------------------------------
y_pred = modelo.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"✅ Modelo treinado com sucesso!")
print(f"Erro quadrático médio (MSE): {mse:.4f}")
print(f"Coeficiente de determinação (R²): {r2:.4f}")

# -------------------------------
# prever tendência futura (2025-2030)
# -------------------------------
anos_futuros = pd.DataFrame({"year": [2025, 2026, 2027, 2028, 2029, 2030]})
previsoes = modelo.predict(anos_futuros)

resultado = pd.DataFrame({
    "Ano": anos_futuros["year"],
    "Área Prevista (km²)": previsoes
})

saida_previsoes = "../resultados/previsoes_deter.csv"
resultado.to_csv(saida_previsoes, sep=";", index=False, encoding="utf-8-sig")

print(f"✅ Previsões salvas em: {saida_previsoes}")
print(resultado)
