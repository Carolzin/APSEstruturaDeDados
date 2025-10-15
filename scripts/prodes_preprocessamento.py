import pandas as pd
import os
from collections import deque

# -------------------------------
# caminho e leitura do CSV
# -------------------------------
dados_path = "../dados"
prodes_file = os.path.join(dados_path, "PRODES_BASE_DE_DESMATAMENTO_POR_ANOS.csv")

prodes = pd.read_csv(prodes_file, sep=";", encoding="latin1")
prodes = prodes.dropna(subset=["year", "state", "areakm"])

#corrige caracteres especiais
prodes["municipality"] = prodes["municipality"].apply(
    lambda x: x.encode("latin1").decode("utf-8") if isinstance(x, str) else x
)
prodes["state"] = prodes["state"].apply(
    lambda x: x.encode("latin1").decode("utf-8") if isinstance(x, str) else x
)

# -------------------------------
# NAO ESQUECER DE AJUSTAR A COLUNA AREA KM QUE TA COM ERRO DE CONVERSÃO
# -------------------------------


# -------------------------------
#salvar CSV tratado completo
# -------------------------------
os.makedirs("../resultados", exist_ok=True)
saida_path = "../resultados/prodes_tratado_completo.csv"
prodes.to_csv(saida_path, sep=";", index=False, encoding="utf-8-sig")
print(f"✅ CSV completo salvo em: {saida_path}")

# -------------------------------
#agregação por estado e ano
# -------------------------------
prodes_agregado = prodes.groupby(["state", "year"], as_index=False)["areakm"].sum()

#salvar CSV agregado
saida_agregado = "../resultados/prodes_agregado_estado_ano.csv"
prodes_agregado.to_csv(saida_agregado, sep=";", index=False, encoding="utf-8-sig")
print(f"✅ CSV agregado salvo em: {saida_agregado}")

# -------------------------------
#estruturas de dados
# -------------------------------

#pilha (LIFO)
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

#fila (FIFO)
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

#TAD 
class TADProdes:
    def __init__(self):
        self.dados = []
    def adicionar(self, registro):
        self.dados.append(registro)
    def listar(self):
        return self.dados
    def tamanho(self):
        return len(self.dados)

# -------------------------------
#carregar dados agregados nas estruturas
# -------------------------------
pilha = Pilha()
fila = Fila()
tad = TADProdes()

for idx, row in prodes_agregado.iterrows():
    registro = {
        "state": row["state"],
        "year": row["year"],
        "areakm": row["areakm"]
    }
    pilha.push(registro)
    fila.enqueue(registro)
    tad.adicionar(registro)

print(f"Pilha contém {pilha.tamanho()} registros")
print(f"Fila contém {fila.tamanho()} registros")
print(f"TAD contém {tad.tamanho()} registros")
