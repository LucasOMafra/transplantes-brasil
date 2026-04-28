"""
analise.py
Análise estatística da relação entre lista de espera e doações de órgãos.
"""

import pandas as pd
import numpy as np
from scipy import stats


def calcular_crescimento_anual(df: pd.DataFrame, coluna: str) -> pd.Series:
    return df[coluna].pct_change() * 100


def resumo_serie_historica(df: pd.DataFrame) -> dict:
    anos = df["ano"].values
    transplantes = df["transplantes"].values
    espera = df["lista_espera"].values
    doadores = df["doadores_efetivos"].values

    corr_doadores_tx, pval_doadores = stats.pearsonr(doadores, transplantes)
    slope_espera, intercept_espera, r_espera, *_ = stats.linregress(anos, espera)
    slope_tx, intercept_tx, r_tx, *_ = stats.linregress(anos, transplantes)

    cresc_tx = (transplantes[-1] / transplantes[0] - 1) * 100
    cresc_espera = (espera[-1] / espera[0] - 1) * 100
    deficit_medio = np.mean(espera - transplantes)

    return {
        "periodo": f"{int(anos[0])}–{int(anos[-1])}",
        "total_transplantes_periodo": int(np.sum(transplantes)),
        "media_anual_transplantes": round(float(np.mean(transplantes)), 0),
        "crescimento_transplantes_pct": round(cresc_tx, 1),
        "crescimento_espera_pct": round(cresc_espera, 1),
        "deficit_medio_anual": round(deficit_medio, 0),
        "deficit_atual_2023": int(espera[-1] - transplantes[-1]),
        "correlacao_doadores_transplantes": round(corr_doadores_tx, 3),
        "pvalor_correlacao": round(pval_doadores, 4),
        "tendencia_espera_por_ano": round(slope_espera, 0),
        "tendencia_transplantes_por_ano": round(slope_tx, 0),
        "impacto_covid_queda_pct": round((transplantes[6] / transplantes[5] - 1) * 100, 1),
        "recuperacao_pos_covid_pct": round((transplantes[-1] / transplantes[6] - 1) * 100, 1),
    }


def projecao_linear(df: pd.DataFrame, anos_futuros: int = 3) -> pd.DataFrame:
    anos = df["ano"].values
    resultados = []
    for col in ["transplantes", "lista_espera", "doadores_efetivos"]:
        slope, intercept, *_ = stats.linregress(anos, df[col].values)
        for i in range(1, anos_futuros + 1):
            ano_proj = int(anos[-1]) + i
            valor = max(0, round(slope * ano_proj + intercept, 0))
            resultados.append({"ano": ano_proj, "variavel": col, "valor_projetado": int(valor)})
    return pd.DataFrame(resultados)


def analise_por_orgao(df_orgao: pd.DataFrame) -> pd.DataFrame:
    df = df_orgao.copy()
    df["criticidade"] = pd.cut(
        df["taxa_atendimento_pct"],
        bins=[0, 50, 80, 110, float("inf")],
        labels=["Crítico", "Deficitário", "Equilibrado", "Superávit"]
    )
    return df.sort_values("deficit", ascending=False)


def analise_regional(df_estados: pd.DataFrame) -> pd.DataFrame:
    return (
        df_estados
        .groupby("regiao")
        .agg(
            estados=("uf", "count"),
            doadores_total=("doadores_total", "sum"),
            transplantes_total=("transplantes_total", "sum"),
            doadores_pmp_medio=("doadores_pmp", "mean"),
        )
        .round(1)
        .reset_index()
        .sort_values("doadores_pmp_medio", ascending=False)
    )


def imprimir_relatorio(resumo: dict) -> None:
    sep = "─" * 55
    print(f"\n{'═'*55}")
    print("  SUMÁRIO EXECUTIVO — TRANSPLANTES NO BRASIL")
    print(f"  Período: {resumo['periodo']}")
    print(f"{'═'*55}")
    print(f"\n  VOLUME:")
    print(sep)
    print(f"  Total de transplantes no período : {resumo['total_transplantes_periodo']:>10,}")
    print(f"  Média anual de transplantes      : {resumo['media_anual_transplantes']:>10,.0f}")
    print(f"  Crescimento (transplantes)       : {resumo['crescimento_transplantes_pct']:>+9.1f}%")
    print(f"  Crescimento (lista de espera)    : {resumo['crescimento_espera_pct']:>+9.1f}%")
    print(f"\n  DÉFICIT:")
    print(sep)
    print(f"  Déficit médio anual              : {resumo['deficit_medio_anual']:>10,.0f}")
    print(f"  Déficit atual (2023)             : {resumo['deficit_atual_2023']:>10,}")
    print(f"  Tendência: espera cresce         : {resumo['tendencia_espera_por_ano']:>+10,.0f} /ano")
    print(f"  Tendência: transplantes crescem  : {resumo['tendencia_transplantes_por_ano']:>+10,.0f} /ano")
    print(f"\n  CORRELAÇÃO & COVID:")
    print(sep)
    print(f"  Corr. doadores ↔ transplantes    : {resumo['correlacao_doadores_transplantes']:>10.3f}")
    print(f"  p-valor                          : {resumo['pvalor_correlacao']:>10.4f}")
    print(f"  Queda COVID-19 (2020 vs 2019)    : {resumo['impacto_covid_queda_pct']:>+9.1f}%")
    print(f"  Recuperação pós-COVID (2023/2020): {resumo['recuperacao_pos_covid_pct']:>+9.1f}%")
    print(f"\n{'═'*55}\n")
