"""
main.py
Pipeline principal — acompanhamento de doações de órgãos no Brasil.

Uso:
    python main.py              # análise + gráficos
    python main.py --sem-plots  # só análise no terminal
    python main.py --opensky    # inclui snapshot de voos em tempo real
    python main.py --tudo       # análise + gráficos + opensky
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from data.dados_rbt import carregar_serie_anual, carregar_espera_por_orgao, carregar_estados
from src.analise import resumo_serie_historica, projecao_linear, analise_por_orgao, analise_regional, imprimir_relatorio
from src.visualizacoes import plot_evolucao_historica, plot_deficit_por_orgao, plot_regional, plot_projecao, plot_correlacao


def rodar_analise():
    print("\n[1/4] Carregando dados RBT/ABTO...")
    df_anual   = carregar_serie_anual()
    df_orgao   = carregar_espera_por_orgao()
    df_estados = carregar_estados()

    print("[2/4] Calculando estatísticas...")
    resumo     = resumo_serie_historica(df_anual)
    df_proj    = projecao_linear(df_anual, anos_futuros=3)
    df_orgao_a = analise_por_orgao(df_orgao)
    df_reg     = analise_regional(df_estados)

    imprimir_relatorio(resumo)

    print("  ANÁLISE POR ÓRGÃO (2023):")
    print("  " + "─" * 75)
    cols = ["orgao", "em_espera", "transplantados", "deficit", "taxa_atendimento_pct", "criticidade"]
    print(df_orgao_a[cols].to_string(index=False))

    print("\n  ANÁLISE REGIONAL:")
    print("  " + "─" * 65)
    print(df_reg.to_string(index=False))

    print("\n  PROJEÇÃO 2024–2026:")
    print("  " + "─" * 45)
    pivot = df_proj.pivot(index="ano", columns="variavel", values="valor_projetado")
    pivot.columns.name = None
    print(pivot.to_string())

    return df_anual, df_orgao_a, df_estados, df_reg, df_proj


def rodar_graficos(df_anual, df_orgao, df_estados, df_regional, df_proj):
    print("\n[3/4] Gerando visualizações...")
    plot_evolucao_historica(df_anual)
    plot_deficit_por_orgao(df_orgao)
    plot_regional(df_estados, df_regional)
    plot_projecao(df_anual, df_proj)
    plot_correlacao(df_anual)
    print("  Gráficos salvos em: outputs/plots/")


def rodar_opensky():
    from src.opensky_api import buscar_aeronaves_brasil, filtrar_candidatos_orgaos, imprimir_snapshot
    print("\n[4/4] Consultando OpenSky Network API...")
    aeronaves  = buscar_aeronaves_brasil()
    candidatos = filtrar_candidatos_orgaos(aeronaves)
    imprimir_snapshot(aeronaves, candidatos)


def main():
    parser = argparse.ArgumentParser(description="Análise de transplantes no Brasil")
    parser.add_argument("--sem-plots", action="store_true", help="Pular gráficos")
    parser.add_argument("--opensky",   action="store_true", help="Snapshot OpenSky API")
    parser.add_argument("--tudo",      action="store_true", help="Tudo junto")
    args = parser.parse_args()

    if args.tudo:
        args.opensky = True

    print("=" * 55)
    print("  TRANSPLANTES BRASIL — Pipeline de Análise")
    print("  Fonte: RBT/ABTO 2023 | OpenSky Network API")
    print("=" * 55)

    resultados = rodar_analise()
    if not args.sem_plots:
        rodar_graficos(*resultados)
    if args.opensky or args.tudo:
        rodar_opensky()

    print("\nPipeline concluído.\n")


if __name__ == "__main__":
    main()
