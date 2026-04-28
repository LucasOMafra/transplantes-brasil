# 🫀 Transplantes Brasil — Análise de Doações de Órgãos

Projeto de análise de dados com Python utilizando **Pandas**, **NumPy**, **Matplotlib**, **Seaborn** e **SciPy** para explorar dados reais do Registro Brasileiro de Transplantes (RBT/ABTO 2014–2023) e rastrear aeronaves em tempo real via OpenSky Network API.

---

## 🗂️ Estrutura do Projeto

```
transplantes-brasil/
├── main.py
├── requirements.txt
├── README.md
├── data/
│   └── dados_rbt.py
├── src/
│   ├── analise.py
│   ├── visualizacoes.py
│   └── opensky_api.py
└── outputs/
    └── plots/
        ├── 01_evolucao_historica.png
        ├── 02_deficit_por_orgao.png
        ├── 03_regional.png
        ├── 04_projecao.png
        └── 05_correlacao.png
```

---

## 📌 O que o projeto faz

1. **Dados reais RBT/ABTO** — série histórica 2014–2023 com transplantes, doadores efetivos e lista de espera
2. **Análise estatística** — correlações de Pearson, regressões lineares, crescimento acumulado e impacto COVID-19
3. **Análise por órgão** — déficit e taxa de atendimento para rim, fígado, córnea, coração, pulmão e pâncreas
4. **Análise regional** — comparativo de doadores pmp entre os 27 estados e 5 regiões do Brasil
5. **Projeção 2024–2026** — tendência linear com intervalo de incerteza para transplantes e lista de espera
6. **Visualizações** — 5 gráficos gerados automaticamente:
   - 📈 Evolução histórica: transplantes vs lista de espera com duplo eixo
   - 📊 Déficit por órgão: barras empilhadas + taxa de atendimento
   - 🗺️ Desigualdade regional: top 10 estados e boxplot por região
   - 🔭 Projeção 2024–2026 com banda de incerteza
   - 🔗 Correlação: dispersão anual + matriz de correlação (heatmap)
7. **OpenSky API** — snapshot em tempo real de aeronaves sobre o Brasil com filtro de candidatos a voos de transporte de órgãos

---

## 🛠️ Tecnologias utilizadas

| Biblioteca | Uso |
|---|---|
| `pandas` | Manipulação e agrupamento de dados |
| `numpy` | Operações numéricas e projeções |
| `matplotlib` | Visualizações customizadas com duplo eixo e anotações |
| `seaborn` | Heatmap de correlação |
| `scipy` | Correlação de Pearson e regressão linear |

---

## 🚀 Como executar

**1. Clone o repositório**
```bash
git clone https://github.com/seuusuario/transplantes-brasil.git
cd transplantes-brasil
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Execute o pipeline**
```bash
python main.py              # análise completa + gráficos
python main.py --sem-plots  # só análise no terminal
python main.py --opensky    # inclui snapshot de voos em tempo real
python main.py --tudo       # tudo junto
```

Os gráficos serão salvos em `outputs/plots/`.

---

## 📈 Destaques da análise

```
Total de transplantes (2014–2023) :    230.560
Crescimento transplantes           :    +48,6%
Crescimento lista de espera        :    +69,7%
Déficit atual (2023)               :    26.739
Tendência espera                   :  +2.388/ano
Tendência transplantes             :    +767/ano
Correlação doadores ↔ transplantes :  r = 0,886 (p < 0,001)
Queda COVID-19 (2020 vs 2019)      :    −18,1%
Recuperação pós-COVID (2023/2020)  :    +48,6%
```

---

## 🔬 Fonte dos dados

- [ABTO — Relatório Brasileiro de Transplantes 2023](https://site.abto.org.br)
- [OpenSky Network API](https://openskynetwork.github.io/opensky-api/)

---

## 👨‍💻 Autor

**Lucas Mafra**
LinkedIn: https://linkedin.com/in/lucasomafra
GitHub: https://github.com/LucasOMafra
