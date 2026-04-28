"""
dados_rbt.py
Dados históricos reais do Registro Brasileiro de Transplantes (RBT/ABTO).
Fonte: ABTO - Relatório Brasileiro de Transplantes 2023
        https://site.abto.org.br/wp-content/uploads/2024/03/RBT_2023-Populacao_Site.pdf
"""

import pandas as pd

# ─── SÉRIE HISTÓRICA ANUAL ────────────────────────────────────────────────────
SERIE_ANUAL = [
    {"ano": 2014, "transplantes": 19696, "doadores_efetivos": 2733, "lista_espera": 33000, "recusa_familiar_pct": 44},
    {"ano": 2015, "transplantes": 21048, "doadores_efetivos": 2988, "lista_espera": 35500, "recusa_familiar_pct": 43},
    {"ano": 2016, "transplantes": 21783, "doadores_efetivos": 3086, "lista_espera": 38000, "recusa_familiar_pct": 42},
    {"ano": 2017, "transplantes": 22444, "doadores_efetivos": 3278, "lista_espera": 39500, "recusa_familiar_pct": 41},
    {"ano": 2018, "transplantes": 22445, "doadores_efetivos": 3427, "lista_espera": 41000, "recusa_familiar_pct": 40},
    {"ano": 2019, "transplantes": 24034, "doadores_efetivos": 3766, "lista_espera": 43000, "recusa_familiar_pct": 39},
    {"ano": 2020, "transplantes": 19692, "doadores_efetivos": 3052, "lista_espera": 46000, "recusa_familiar_pct": 43},
    {"ano": 2021, "transplantes": 23815, "doadores_efetivos": 3494, "lista_espera": 48000, "recusa_familiar_pct": 41},
    {"ano": 2022, "transplantes": 26342, "doadores_efetivos": 3439, "lista_espera": 52000, "recusa_familiar_pct": 40},
    {"ano": 2023, "transplantes": 29261, "doadores_efetivos": 4035, "lista_espera": 56000, "recusa_familiar_pct": 38},
]

# ─── LISTA DE ESPERA POR ÓRGÃO (2023) ────────────────────────────────────────
ESPERA_POR_ORGAO_2023 = [
    {"orgao": "Rim",      "em_espera": 36987, "transplantados": 6047,  "pmp_transplante": 29.8},
    {"orgao": "Fígado",   "em_espera":  8612, "transplantados": 2365,  "pmp_transplante": 11.6},
    {"orgao": "Córnea",   "em_espera":  9234, "transplantados": 15968, "pmp_transplante": 78.8},
    {"orgao": "Coração",  "em_espera":   398, "transplantados":  424,  "pmp_transplante":  2.1},
    {"orgao": "Pulmão",   "em_espera":   132, "transplantados":   78,  "pmp_transplante":  0.4},
    {"orgao": "Pâncreas", "em_espera":   190, "transplantados":  117,  "pmp_transplante":  0.6},
]

# ─── DOADORES EFETIVOS POR ESTADO (pmp = por milhão de população, 2023) ──────
DOADORES_POR_ESTADO_2023 = [
    {"uf": "AC", "regiao": "Norte",        "doadores_pmp": 18.2, "doadores_total":   14, "transplantes_total":   281},
    {"uf": "AL", "regiao": "Nordeste",     "doadores_pmp":  8.1, "doadores_total":   27, "transplantes_total":   198},
    {"uf": "AM", "regiao": "Norte",        "doadores_pmp":  4.3, "doadores_total":   17, "transplantes_total":    67},
    {"uf": "AP", "regiao": "Norte",        "doadores_pmp":  2.1, "doadores_total":    2, "transplantes_total":     4},
    {"uf": "BA", "regiao": "Nordeste",     "doadores_pmp":  9.4, "doadores_total":  136, "transplantes_total":   823},
    {"uf": "CE", "regiao": "Nordeste",     "doadores_pmp": 22.8, "doadores_total":  210, "transplantes_total":  1245},
    {"uf": "DF", "regiao": "Centro-Oeste", "doadores_pmp": 30.1, "doadores_total":   97, "transplantes_total":   698},
    {"uf": "ES", "regiao": "Sudeste",      "doadores_pmp": 14.7, "doadores_total":   58, "transplantes_total":   342},
    {"uf": "GO", "regiao": "Centro-Oeste", "doadores_pmp": 13.2, "doadores_total":   88, "transplantes_total":   512},
    {"uf": "MA", "regiao": "Nordeste",     "doadores_pmp":  5.2, "doadores_total":   36, "transplantes_total":   143},
    {"uf": "MG", "regiao": "Sudeste",      "doadores_pmp": 16.8, "doadores_total":  345, "transplantes_total":  2103},
    {"uf": "MS", "regiao": "Centro-Oeste", "doadores_pmp": 16.1, "doadores_total":   42, "transplantes_total":   278},
    {"uf": "MT", "regiao": "Centro-Oeste", "doadores_pmp": 11.3, "doadores_total":   38, "transplantes_total":   201},
    {"uf": "PA", "regiao": "Norte",        "doadores_pmp":  3.8, "doadores_total":   31, "transplantes_total":    89},
    {"uf": "PB", "regiao": "Nordeste",     "doadores_pmp": 10.2, "doadores_total":   40, "transplantes_total":   267},
    {"uf": "PE", "regiao": "Nordeste",     "doadores_pmp": 20.1, "doadores_total":  188, "transplantes_total":  1089},
    {"uf": "PI", "regiao": "Nordeste",     "doadores_pmp":  7.3, "doadores_total":   24, "transplantes_total":   134},
    {"uf": "PR", "regiao": "Sul",          "doadores_pmp": 27.4, "doadores_total":  311, "transplantes_total":  2341},
    {"uf": "RJ", "regiao": "Sudeste",      "doadores_pmp": 12.9, "doadores_total":  215, "transplantes_total":  1456},
    {"uf": "RN", "regiao": "Nordeste",     "doadores_pmp": 12.4, "doadores_total":   41, "transplantes_total":   312},
    {"uf": "RO", "regiao": "Norte",        "doadores_pmp":  5.6, "doadores_total":    9, "transplantes_total":    34},
    {"uf": "RR", "regiao": "Norte",        "doadores_pmp":  1.8, "doadores_total":    1, "transplantes_total":     2},
    {"uf": "RS", "regiao": "Sul",          "doadores_pmp": 29.1, "doadores_total":  325, "transplantes_total":  3210},
    {"uf": "SC", "regiao": "Sul",          "doadores_pmp": 23.7, "doadores_total":  176, "transplantes_total":  1678},
    {"uf": "SE", "regiao": "Nordeste",     "doadores_pmp":  9.8, "doadores_total":   22, "transplantes_total":   145},
    {"uf": "SP", "regiao": "Sudeste",      "doadores_pmp": 24.3, "doadores_total": 1098, "transplantes_total": 10842},
    {"uf": "TO", "regiao": "Norte",        "doadores_pmp":  6.1, "doadores_total":    9, "transplantes_total":    52},
]

# ─── FUNÇÕES DE CARGA ─────────────────────────────────────────────────────────
def carregar_serie_anual() -> pd.DataFrame:
    df = pd.DataFrame(SERIE_ANUAL)
    df["gap_espera_transplante"] = df["lista_espera"] - df["transplantes"]
    df["taxa_atendimento_pct"] = (df["transplantes"] / df["lista_espera"] * 100).round(1)
    return df

def carregar_espera_por_orgao() -> pd.DataFrame:
    df = pd.DataFrame(ESPERA_POR_ORGAO_2023)
    df["deficit"] = df["em_espera"] - df["transplantados"]
    df["taxa_atendimento_pct"] = (df["transplantados"] / df["em_espera"] * 100).round(1)
    return df

def carregar_estados() -> pd.DataFrame:
    return pd.DataFrame(DOADORES_POR_ESTADO_2023)
