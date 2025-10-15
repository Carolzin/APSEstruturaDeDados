import pandas as pd
import os
from collections import deque
import time

# -------------------------------
# caminho do CSV
# -------------------------------
dados_path = "../dados"
deter_file = os.path.join(dados_path, "DETER_BASE_DE_ALARMES.csv")

with open(deter_file, "r", encoding="latin1") as f:
    linhas = f.read().splitlines()

# separar cada linha pelo ";"
dados_separados = [linha.split(";") for linha in linhas]

# criar DataFrame
deter = pd.DataFrame(dados_separados, columns=["year", "month", "area", "uf", "className", "numPol"])

# remove espaços extras
deter = deter.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# converte colunas numéricas
deter["area"] = pd.to_numeric(deter["area"], errors="coerce")
deter["month"] = pd.to_numeric(deter["month"], errors="coerce")
deter["numPol"] = pd.to_numeric(deter["numPol"], errors="coerce")

# remove linhas com valores ausentes
deter = deter.dropna(subset=["year", "uf", "area"])

# -------------------------------
# salvar CSV tratado completo
# -------------------------------
os.makedirs("../resultados", exist_ok=True)
saida_path = "../resultados/deter_tratado_completo.csv"
deter.to_csv(saida_path, sep=";", index=False, encoding="utf-8-sig")
print(f"✅ CSV completo salvo em: {saida_path}")

# -------------------------------
# agregação por UF e ano
# -------------------------------
deter_agregado = deter.groupby(["uf", "year"], as_index=False)["area"].sum()
saida_agregado = "../resultados/deter_agregado_uf_ano.csv"
deter_agregado.to_csv(saida_agregado, sep=";", index=False, encoding="utf-8-sig")
print(f"✅ CSV agregado salvo em: {saida_agregado}")

# -------------------------------
# estruturas de dados
# -------------------------------
class Pilha:
    def __init__(self):
        self.itens = []
    def push(self, item):
        self.itens.append(item)
    def pop(self):
        return self.itens.pop() if self.itens else None
    def is_empty(self):
        return len(self.itens) == 0
    def tamanho(self):
        return len(self.itens)

class Fila:
    def __init__(self):
        self.itens = deque()
    def enqueue(self, item):
        self.itens.append(item)
    def dequeue(self):
        return self.itens.popleft() if self.itens else None
    def is_empty(self):
        return len(self.itens) == 0
    def tamanho(self):
        return len(self.itens)

class TADDETER:
    def __init__(self):
        self.dados = []
    def adicionar(self, registro):
        self.dados.append(registro)
    def listar(self):
        return self.dados
    def tamanho(self):
        return len(self.dados)

# -------------------------------
# carregar dados agregados nas estruturas
# -------------------------------
pilha = Pilha()
fila = Fila()
tad = TADDETER()

for idx, row in deter_agregado.iterrows():
    registro = {"uf": row["uf"], "year": row["year"], "area": row["area"]}
    pilha.push(registro)
    fila.enqueue(registro)
    tad.adicionar(registro)

print(f"Pilha contém {pilha.tamanho()} registros")
print(f"Fila contém {fila.tamanho()} registros")
print(f"TAD contém {tad.tamanho()} registros")

# -------------------------------
# algoritmos de ordenação
# -------------------------------
def bubble_sort(lista):
    n = len(lista)
    comparacoes = 0
    inicio = time.time()
    for i in range(n):
        for j in range(0, n - i - 1):
            comparacoes += 1
            if lista[j]["area"] > lista[j + 1]["area"]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    fim = time.time()
    return lista, comparacoes, round(fim - inicio, 4)

def quick_sort(lista):
    comparacoes = [0]
    def _quick_sort(items):
        if len(items) <= 1:
            return items
        pivo = items[len(items)//2]["area"]
        menores = [x for x in items if x["area"] < pivo]
        iguais = [x for x in items if x["area"] == pivo]
        maiores = [x for x in items if x["area"] > pivo]
        comparacoes[0] += len(items) - 1
        return _quick_sort(menores) + iguais + _quick_sort(maiores)
    inicio = time.time()
    ordenado = _quick_sort(lista)
    fim = time.time()
    return ordenado, comparacoes[0], round(fim - inicio, 4)

# -------------------------------
# aplicar algoritmos
# -------------------------------
dados_para_ordenar = tad.listar()
bubble_dados, bubble_comp, bubble_tempo = bubble_sort(dados_para_ordenar.copy())
quick_dados, quick_comp, quick_tempo = quick_sort(dados_para_ordenar.copy())

# -------------------------------
# gerar CSV de desempenho
# -------------------------------
resultados = pd.DataFrame([
    {"Algoritmo": "Bubble Sort", "Comparações": bubble_comp, "Tempo (s)": bubble_tempo},
    {"Algoritmo": "Quick Sort", "Comparações": quick_comp, "Tempo (s)": quick_tempo},
])
saida_performance = "../resultados/desempenho_algoritmos_deter.csv"
resultados.to_csv(saida_performance, sep=";", index=False, encoding="utf-8-sig")
print(f"✅ CSV de desempenho salvo em: {saida_performance}")
