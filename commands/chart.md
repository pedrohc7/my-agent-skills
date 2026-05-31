# Analise e Criacao de Graficos

Siga este fluxo completo de analise e visualizacao de dados.

## 1. Coleta de contexto

Se o usuario nao fornecer dados, pergunte:
- Qual e a fonte dos dados? (CSV, JSON, banco de dados, DataFrame ja carregado, etc.)
- Qual e o objetivo? (comparar, mostrar tendencia, distribuicao, correlacao, proporcao)
- O grafico sera exibido em: notebook Jupyter, aplicacao web, arquivo de imagem?

## 2. Analise dos dados

Antes de gerar o grafico:
- Identifique os tipos de cada variavel: numerica, categorica ou temporal
- Verifique valores nulos, outliers e a escala dos dados
- Sugira transformacoes se necessario (log scale, normalizacao, agrupamento)

## 3. Escolha do tipo de grafico

| Objetivo | Tipo de grafico recomendado |
|---|---|
| Tendencia ao longo do tempo | Line chart |
| Comparar categorias | Bar chart (vertical ou horizontal) |
| Distribuicao de valores | Histogram ou Box plot |
| Relacao entre duas variaveis | Scatter plot |
| Correlacao entre multiplas variaveis | Heatmap |
| Proporcao de partes | Pie chart ou Treemap |
| Hierarquia / composicao | Treemap ou Sunburst |
| Dados geograficos | Choropleth map |
| Multiplas metricas juntas | Dashboard com subplots |

## 4. Geracao do codigo

Gere codigo completo e pronto para executar. Escolha a biblioteca com base no contexto:

### Python - Plotly Express (interativo, preferido para dashboards)
```python
import plotly.express as px
import pandas as pd

df = pd.read_csv("dados.csv")
fig = px.line(df, x="data", y="valor", title="Titulo do Grafico")
fig.show()
```

### Python - Seaborn (estatistico, publicacoes academicas)
```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")
sns.lineplot(data=df, x="data", y="valor")
plt.title("Titulo")
plt.show()
```

### Python - Matplotlib (controle total)
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df["data"], df["valor"])
ax.set_title("Titulo")
plt.tight_layout()
plt.show()
```

### Jupyter Notebook (prototipagem rapida)
```python
# Uma linha com pandas
df.plot(x="data", y="valor", kind="line", figsize=(10, 5), title="Titulo")
```

## 5. Insights obrigatorios

Apos gerar o codigo, sempre comente:
- Tendencias principais identificadas
- Outliers ou anomalias encontradas
- Padroes sazonais ou ciclicos (se serie temporal)
- Recomendacoes para exploracao adicional

## 6. Ferramentas recomendadas por contexto

### Para Python / Data Science
- **Plotly Express** — graficos interativos em uma linha, ideal para Jupyter e web
- **Seaborn** — graficos estatisticos elegantes sobre Matplotlib
- **Matplotlib** — controle total, graficos para publicacoes
- **Altair** — visualizacoes declarativas e responsivas
- **Bokeh** — dashboards interativos com servidor Python

### Para Web / Frontend
- **Chart.js** — simples, leve, responsivo
- **D3.js** — visualizacoes customizadas e complexas
- **Recharts** — graficos para projetos React
- **ApexCharts** — dashboards modernos e bonitos
- **ECharts (Apache)** — alta performance com grandes volumes de dados

### Para Dashboards completos
- **Streamlit** — transforma scripts Python em apps web rapidamente
- **Dash (Plotly)** — dashboards analiticos profissionais em Python
- **Power BI / Tableau** — ferramentas no-code/low-code para negocios

## 7. Boas praticas sempre aplicadas

- Incluir titulo descritivo e labels nos eixos
- Usar paleta de cores acessivel (evitar vermelho/verde juntos)
- Adicionar fonte dos dados quando relevante
- Preferir graficos simples a complexos quando o objetivo e comunicar
- Salvar em alta resolucao se for para relatorio (dpi=300 no matplotlib)
