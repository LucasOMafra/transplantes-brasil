"""
visualizacoes.py
Gera todos os gráficos do projeto com matplotlib + seaborn.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "plots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CORES = {
    "vermelho":    "#C0392B",
    "vermelho_cl": "#E57373",
    "azul":        "#1A5276",
    "azul_cl":     "#5DADE2",
    "verde":       "#1E8449",
    "verde_cl":    "#58D68D",
    "cinza":       "#7F8C8D",
    "fundo":       "#F4F6F7",
    "texto":       "#1C2833",
}

def _setup_estilo():
    plt.rcParams.update({
        "font.family":      "DejaVu Sans",
        "axes.facecolor":   CORES["fundo"],
        "figure.facecolor": "white",
        "axes.grid":        True,
        "grid.linestyle":   "--",
        "grid.alpha":       0.4,
        "axes.spines.top":  False,
        "axes.spines.right":False,
        "axes.labelcolor":  CORES["texto"],
        "xtick.color":      CORES["texto"],
        "ytick.color":      CORES["texto"],
        "axes.titlepad":    14,
        "axes.titlesize":   13,
        "axes.labelsize":   11,
    })

_setup_estilo()


def plot_evolucao_historica(df: pd.DataFrame) -> str:
    fig, ax1 = plt.subplots(figsize=(11, 6))
    fig.suptitle("Evolução Histórica: Transplantes vs. Lista de Espera (2014–2023)",
                 fontsize=15, fontweight="bold", color=CORES["texto"], y=0.98)
    anos = df["ano"].values

    ax1.fill_between(anos, df["transplantes"], df["lista_espera"],
                     alpha=0.12, color=CORES["vermelho"], label="Déficit (gap)")
    ax1.plot(anos, df["lista_espera"], "o--", color=CORES["vermelho"],
             linewidth=2.2, markersize=7, label="Lista de espera")
    ax1.plot(anos, df["transplantes"], "o-", color=CORES["azul"],
             linewidth=2.5, markersize=8, label="Transplantes realizados")

    ax1.axvspan(2019.5, 2020.5, alpha=0.08, color="orange")
    ax1.annotate("COVID-19\n−18%", xy=(2020, 19692), xytext=(2020.3, 23500),
                 fontsize=9, color="darkorange",
                 arrowprops=dict(arrowstyle="->", color="darkorange", lw=1.4))
    ax1.annotate("Recorde\n29.261", xy=(2023, 29261), xytext=(2022.1, 31000),
                 fontsize=9, color=CORES["azul"],
                 arrowprops=dict(arrowstyle="->", color=CORES["azul"], lw=1.4))

    ax1.set_xlabel("Ano")
    ax1.set_ylabel("Número de procedimentos")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax1.set_xticks(anos)
    ax1.legend(loc="upper left", framealpha=0.9)

    ax2 = ax1.twinx()
    ax2.plot(anos, df["taxa_atendimento_pct"], "s:", color=CORES["verde"],
             linewidth=1.8, markersize=6, alpha=0.85, label="Taxa de atendimento (%)")
    ax2.set_ylabel("Taxa de atendimento (%)", color=CORES["verde"])
    ax2.tick_params(axis="y", colors=CORES["verde"])
    ax2.set_ylim(0, 90)
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color(CORES["verde"])
    ax2.legend(loc="lower right", framealpha=0.9)

    plt.tight_layout()
    caminho = OUTPUT_DIR / "01_evolucao_historica.png"
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Salvo: {caminho.name}")
    return str(caminho)


def plot_deficit_por_orgao(df: pd.DataFrame) -> str:
    df = df.sort_values("deficit", ascending=True)
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    fig.suptitle("Lista de Espera vs. Transplantes por Órgão — 2023",
                 fontsize=15, fontweight="bold", color=CORES["texto"])

    ax = axes[0]
    orgaos = df["orgao"].values
    y = np.arange(len(orgaos))

    bars_tx = ax.barh(y, df["transplantados"], color=CORES["azul_cl"],
                      label="Transplantados", height=0.55)
    bars_esp = ax.barh(y, df["deficit"].clip(lower=0), left=df["transplantados"],
                       color=CORES["vermelho_cl"], label="Déficit", height=0.55)
    ax.set_yticks(y)
    ax.set_yticklabels(orgaos, fontsize=11)
    ax.set_xlabel("Número de pacientes")
    ax.set_title("Transplantados × Déficit", fontsize=12)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.legend(framealpha=0.9)

    for bar in bars_esp:
        w = bar.get_width()
        if w > 100:
            ax.text(bar.get_x() + w / 2, bar.get_y() + bar.get_height() / 2,
                    f"{int(w):,}", ha="center", va="center",
                    fontsize=8.5, color="white", fontweight="bold")

    ax2 = axes[1]
    cores_taxa = [
        CORES["vermelho"] if t < 50 else
        CORES["cinza"] if t < 90 else
        CORES["verde"]
        for t in df["taxa_atendimento_pct"]
    ]
    bars = ax2.barh(y, df["taxa_atendimento_pct"], color=cores_taxa, height=0.55)
    ax2.axvline(100, color=CORES["texto"], linestyle="--", linewidth=1.2, alpha=0.6,
                label="Equilíbrio (100%)")
    ax2.set_yticks(y)
    ax2.set_yticklabels(orgaos, fontsize=11)
    ax2.set_xlabel("Taxa de atendimento (%)")
    ax2.set_title("% de Pacientes em Espera Atendidos", fontsize=12)
    ax2.legend(framealpha=0.9)

    for bar, val in zip(bars, df["taxa_atendimento_pct"]):
        ax2.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height() / 2,
                 f"{val:.0f}%", va="center", fontsize=9.5, color=CORES["texto"])

    leg_patches = [
        mpatches.Patch(color=CORES["vermelho"], label="Crítico (<50%)"),
        mpatches.Patch(color=CORES["cinza"],    label="Deficitário (50–90%)"),
        mpatches.Patch(color=CORES["verde"],    label="Equilibrado/Superávit"),
    ]
    ax2.legend(handles=leg_patches, loc="lower right", fontsize=8.5, framealpha=0.9)

    plt.tight_layout()
    caminho = OUTPUT_DIR / "02_deficit_por_orgao.png"
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Salvo: {caminho.name}")
    return str(caminho)


def plot_regional(df_estados: pd.DataFrame, df_regional: pd.DataFrame) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    fig.suptitle("Desigualdade Regional — Doadores e Transplantes (2023)",
                 fontsize=15, fontweight="bold", color=CORES["texto"])

    ax = axes[0]
    top10 = df_estados.nlargest(10, "doadores_pmp")
    cores_barra = [
        CORES["azul"] if r in ["Sul", "Sudeste"] else
        CORES["verde"] if r == "Nordeste" else
        CORES["cinza"]
        for r in top10["regiao"]
    ]
    bars = ax.barh(top10["uf"][::-1], top10["doadores_pmp"][::-1],
                   color=cores_barra[::-1], height=0.6)
    ax.set_xlabel("Doadores efetivos por milhão de população (pmp)")
    ax.set_title("Top 10 Estados — Doadores pmp", fontsize=12)
    ax.axvline(19.9, color=CORES["vermelho"], linestyle="--", linewidth=1.3,
               label="Média Brasil (19,9 pmp)")
    ax.legend(fontsize=9)
    for bar in bars:
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{bar.get_width():.1f}", va="center", fontsize=9)

    ax2 = axes[1]
    regioes = df_estados["regiao"].unique()
    data_box = [df_estados[df_estados["regiao"] == r]["doadores_pmp"].values for r in regioes]
    bp = ax2.boxplot(data_box, labels=regioes, patch_artist=True,
                     medianprops=dict(color="white", linewidth=2))
    cores_box = [CORES["azul"], CORES["verde_cl"], CORES["vermelho_cl"],
                 CORES["cinza"], CORES["azul_cl"]]
    for patch, cor in zip(bp["boxes"], cores_box):
        patch.set_facecolor(cor)
        patch.set_alpha(0.75)

    ax2.set_ylabel("Doadores pmp")
    ax2.set_title("Distribuição de Doadores pmp por Região", fontsize=12)
    ax2.axhline(19.9, color=CORES["vermelho"], linestyle="--", linewidth=1.3,
                label="Média Brasil")
    ax2.legend(fontsize=9)
    ax2.tick_params(axis="x", rotation=15)

    plt.tight_layout()
    caminho = OUTPUT_DIR / "03_regional.png"
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Salvo: {caminho.name}")
    return str(caminho)


def plot_projecao(df_hist: pd.DataFrame, df_proj: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(11, 6))
    fig.suptitle("Projeção 2024–2026: Transplantes e Lista de Espera",
                 fontsize=15, fontweight="bold", color=CORES["texto"])

    for col, cor, label in [
        ("transplantes", CORES["azul"],    "Transplantes realizados"),
        ("lista_espera", CORES["vermelho"], "Lista de espera"),
    ]:
        ax.plot(df_hist["ano"], df_hist[col], "o-", color=cor,
                linewidth=2.5, markersize=7, label=f"{label} (histórico)")
        proj = df_proj[df_proj["variavel"] == col]
        anos_proj = list(df_hist["ano"].values[-1:]) + list(proj["ano"].values)
        vals_proj = list(df_hist[col].values[-1:]) + list(proj["valor_projetado"].values)
        ax.plot(anos_proj, vals_proj, "o--", color=cor,
                linewidth=1.8, markersize=6, alpha=0.7, label=f"{label} (projeção)")
        if len(proj) > 0:
            vals_arr = np.array(vals_proj[1:])
            ax.fill_between(proj["ano"], vals_arr * 0.92, vals_arr * 1.08,
                            color=cor, alpha=0.08)

    ax.axvline(2023.5, color=CORES["cinza"], linestyle=":", linewidth=1.5, alpha=0.7)
    ax.text(2023.6, 15000, "→ Projeção", fontsize=9, color=CORES["cinza"])
    ax.set_xlabel("Ano")
    ax.set_ylabel("Número de procedimentos")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_xticks(list(df_hist["ano"]) + [2024, 2025, 2026])
    ax.legend(loc="upper left", framealpha=0.9, fontsize=9.5)

    plt.tight_layout()
    caminho = OUTPUT_DIR / "04_projecao.png"
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Salvo: {caminho.name}")
    return str(caminho)


def plot_correlacao(df: pd.DataFrame) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Correlação: Doadores Efetivos × Transplantes Realizados",
                 fontsize=14, fontweight="bold", color=CORES["texto"])

    ax = axes[0]
    ax.scatter(df["doadores_efetivos"], df["transplantes"],
               color=CORES["azul"], s=80, zorder=5)
    for _, row in df.iterrows():
        ax.annotate(str(int(row["ano"])),
                    (row["doadores_efetivos"], row["transplantes"]),
                    textcoords="offset points", xytext=(5, 3),
                    fontsize=8, color=CORES["cinza"])
    z = np.polyfit(df["doadores_efetivos"], df["transplantes"], 1)
    p = np.poly1d(z)
    xs = np.linspace(df["doadores_efetivos"].min(), df["doadores_efetivos"].max(), 100)
    ax.plot(xs, p(xs), "--", color=CORES["vermelho"], linewidth=1.8, alpha=0.8, label="Tendência")
    ax.set_xlabel("Doadores efetivos")
    ax.set_ylabel("Transplantes realizados")
    ax.set_title("Dispersão anual", fontsize=11)
    ax.legend()

    ax2 = axes[1]
    cols_corr = ["transplantes", "doadores_efetivos", "lista_espera",
                 "gap_espera_transplante", "taxa_atendimento_pct"]
    corr_mat = df[cols_corr].corr()
    labels = ["Transplantes", "Doadores", "Espera", "Gap", "Taxa atend."]
    sns.heatmap(corr_mat, ax=ax2, annot=True, fmt=".2f", cmap="RdYlGn",
                center=0, linewidths=0.5, square=True,
                xticklabels=labels, yticklabels=labels,
                cbar_kws={"shrink": 0.8})
    ax2.set_title("Matriz de correlação", fontsize=11)
    ax2.tick_params(axis="x", rotation=30)
    ax2.tick_params(axis="y", rotation=0)

    plt.tight_layout()
    caminho = OUTPUT_DIR / "05_correlacao.png"
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Salvo: {caminho.name}")
    return str(caminho)
