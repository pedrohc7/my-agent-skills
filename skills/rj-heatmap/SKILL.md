---
name: rj-heatmap
description: >
  Cria dashboards interativos de mapa de calor (choropleth + heatmap) para regiões do Rio de Janeiro
  usando Python + Folium, gerando um arquivo HTML standalone sem necessidade de servidor.
  Use esta skill SEMPRE que o usuário mencionar: mapa do Rio, calor por bairro, visualização
  geográfica no RJ, distribuição por região, concentração de entregas, análise por zona, 
  mapa de ocorrências RJ, ou qualquer dado numérico que precise ser visualizado por localidade
  no Rio de Janeiro — mesmo que não use as palavras "heatmap", "choropleth" ou "dashboard".
  Também aciona quando o usuário fornece um CSV/Excel com colunas de bairro, zona ou
  município do RJ e quer ver onde os dados se concentram no mapa.
---

# Dashboard de Mapa de Calor — Rio de Janeiro

Esta skill gera mapas interativos choropleth (regiões coloridas por intensidade) e/ou
camadas de heatmap de pontos para dados do Rio de Janeiro, exportando um HTML navegável
e offline com zoom, tooltips e legenda.

---

## 1. Capturar o contexto

Antes de gerar o mapa, colete (pergunte apenas o que ainda não foi informado):

| O que coletar | Por que importa |
|---|---|
| Arquivo de dados (CSV/Excel) | Fonte principal dos dados |
| Coluna de região | Nome do bairro, zona, município ou lat/lon |
| Coluna de métrica | O valor a ser mapeado (entregas, pedidos, tempo, etc.) |
| Título do dashboard | Exibido no topo do mapa |
| Nível geográfico | bairro · zona · município — ou detectar automaticamente |
| Coluna de lat/lon (opcional) | Para camada de heatmap de pontos além do choropleth |

Se o arquivo foi fornecido, leia as primeiras linhas com `pandas` para inferir as colunas
disponíveis antes de perguntar — isso evita perguntas desnecessárias.

---

## 2. Detectar o nível geográfico

Use este critério para detectar automaticamente quando o usuário não especificar:

1. **Municípios**: coluna contém nomes como "Niterói", "Duque de Caxias", "Nova Iguaçu" — provavelmente nível municipal
2. **Zonas**: coluna contém "Zona Norte", "Zona Sul", "Zona Oeste", "Centro", "Barra" — nível de zona
3. **Bairros**: nomes como "Copacabana", "Tijuca", "Méier" — nível de bairro (mais granular)
4. **Coordenadas**: colunas `lat`/`lon`, `latitude`/`longitude` → heatmap de pontos

É possível combinar choropleth (região colorida) + heatmap de pontos no mesmo mapa.

---

## 3. Fontes de GeoJSON

Leia `references/fontes_geojson.md` para os endpoints e arquivos corretos por nível.
O script Python faz o download automaticamente se o arquivo local não existir.

---

## 4. Gerar o mapa — usar o script bundled

Execute o script em `scripts/gerar_mapa.py` passando os parâmetros via CLI:

```bash
python scripts/gerar_mapa.py \
  --arquivo    "caminho/para/dados.csv" \
  --coluna_geo "bairro" \
  --coluna_val "qtd_entregas" \
  --nivel      "bairro" \
  --titulo     "Entregas por Bairro — RJ" \
  --saida      "mapa_entregas_rj.html"
```

**Parâmetros opcionais:**
- `--coluna_lat lat --coluna_lon lon` → adiciona camada heatmap de pontos
- `--paleta YlOrRd` → paleta de cores (padrão: YlOrRd; outras: Blues, Greens, RdYlGn, plasma)
- `--bins 6` → número de intervalos na legenda (padrão: 6)
- `--opacidade 0.7` → transparência das regiões (padrão: 0.7)
- `--sem_dados_cor #cccccc` → cor para regiões sem dado (padrão: cinza claro)

---

## 5. O que o mapa gerado contém

O HTML final inclui:
- **Choropleth**: regiões coloridas proporcionalmente ao valor da métrica
- **Tooltips ao passar o mouse**: nome da região + valor formatado
- **Popups ao clicar**: detalhes completos (todas as colunas do dado)
- **Legenda interativa** com escala de cores e intervalo de valores
- **Camada heatmap de pontos** (se lat/lon fornecidos)
- **Controle de camadas** (toggle choropleth / heatmap)
- **Mini-mapa de navegação** no canto inferior direito
- **Escala de distância** no canto inferior esquerdo
- **Título e subtítulo** no topo do mapa

---

## 6. Pré-requisitos Python

Instale se necessário (mencione ao usuário caso não esteja instalado):

```bash
pip install folium pandas geopandas requests branca openpyxl
```

`geopandas` é usado apenas para leitura de GeoJSON complexos; se não disponível,
o script usa `json` + `requests` como fallback.

---

## 7. Resolução de problemas comuns

| Problema | Solução |
|---|---|
| Bairro não encontrado no GeoJSON | Usar `--fuzzy` para matching aproximado de nomes |
| GeoJSON muito lento para baixar | Usar arquivo local; ver `references/fontes_geojson.md` |
| Encoding do CSV com acentos | Adicionar `--encoding latin-1` ou `utf-8-sig` |
| Regiões fora do RJ no dado | O script ignora automaticamente; avisa no log |
| Muitos pontos no heatmap (>50k) | Usar `--amostra 10000` para amostrar aleatoriamente |

---

## 8. Entregar o resultado

Após gerar o arquivo HTML:

1. Informe o caminho completo do arquivo gerado
2. Mencione que ele pode ser **aberto direto no navegador** (sem servidor)
3. Se possível, abra automaticamente: `python -m webbrowser mapa_entregas_rj.html`
4. Descreva resumidamente o que o mapa mostra (região com maior concentração, outliers)
5. Ofereça variações: filtro por período, comparativo entre dois períodos, etc.
