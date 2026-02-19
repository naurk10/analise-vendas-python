import pandas as pd
import os

# caminho do arquivo CSV
ARQUIVO = "entrada/vendas.csv"

# pasta de saída
PASTA_SAIDA = "saida"

# criar pasta se não existir
os.makedirs(PASTA_SAIDA, exist_ok=True)

# ler arquivo CSV
df = pd.read_csv(ARQUIVO)

# limpar dados
df["cliente"] = df["cliente"].astype(str).str.strip()
df["cidade"] = df["cidade"].astype(str).str.strip()
df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

# relatório por cliente
relatorio_cliente = (
    df.groupby("cliente")["valor"]
    .sum()
    .reset_index()
    .sort_values("valor", ascending=False)
)

# relatório por cidade
relatorio_cidade = (
    df.groupby("cidade")["valor"]
    .sum()
    .reset_index()
    .sort_values("valor", ascending=False)
)

# salvar relatórios
relatorio_cliente.to_csv("saida/relatorio_cliente_csv.csv", index=False)
relatorio_cidade.to_csv("saida/relatorio_cidade_csv.csv", index=False)

print("Relatórios CSV gerados com sucesso!")
