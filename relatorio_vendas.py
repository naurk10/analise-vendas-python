import os
import pandas as pd

ARQUIVO_ENTRADA = "entrada/vendas.xlsx"
PASTA_SAIDA = "saida"

def categorizar(valor: float) -> str:
    if valor >= 300:
        return "Alto"
    elif valor >= 200:
        return "Médio"
    return "Baixo"

def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    # 1) Ler
    df = pd.read_excel(ARQUIVO_ENTRADA)
    df.columns = df.columns.str.strip().str.lower()

    # 2) Limpar
    for col in ["cliente", "cidade"]:
        if col not in df.columns:
            raise ValueError(f"Coluna obrigatória não encontrada: {col}")
        df[col] = df[col].astype(str).str.strip()

    if "valor" not in df.columns:
        raise ValueError("Coluna obrigatória não encontrada: valor")

    df["valor"] = (
        df["valor"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df = df.dropna(subset=["cliente", "cidade", "valor"])

    # 3) Transformar
    df["categoria"] = df["valor"].apply(categorizar)

    # 4) Relatórios
    rel_cliente = (
        df.groupby("cliente", as_index=False)["valor"].sum()
        .rename(columns={"valor": "total_gasto"})
        .sort_values("total_gasto", ascending=False)
    )

    rel_cidade = (
        df.groupby("cidade", as_index=False)["valor"].sum()
        .rename(columns={"valor": "total_gasto"})
        .sort_values("total_gasto", ascending=False)
    )

    resumo = pd.DataFrame({
        "metricas": ["linhas", "clientes_unicos", "cidades_unicas", "valor_total", "ticket_medio"],
        "valor": [
            len(df),
            df["cliente"].nunique(),
            df["cidade"].nunique(),
            df["valor"].sum(),
            df["valor"].mean(),
        ],
    })

    # 5) Exportar
    df.to_csv(f"{PASTA_SAIDA}/vendas_limpa.csv", index=False)
    rel_cliente.to_csv(f"{PASTA_SAIDA}/total_por_cliente.csv", index=False)
    rel_cidade.to_csv(f"{PASTA_SAIDA}/total_por_cidade.csv", index=False)
    resumo.to_csv(f"{PASTA_SAIDA}/resumo.csv", index=False)

    with pd.ExcelWriter(f"{PASTA_SAIDA}/relatorio_final.xlsx", engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="base_limpa", index=False)
        rel_cliente.to_excel(writer, sheet_name="total_por_cliente", index=False)
        rel_cidade.to_excel(writer, sheet_name="total_por_cidade", index=False)
        resumo.to_excel(writer, sheet_name="resumo", index=False)

    print("✅ Relatórios gerados em:", PASTA_SAIDA)

if __name__ == "__main__":
    main()
