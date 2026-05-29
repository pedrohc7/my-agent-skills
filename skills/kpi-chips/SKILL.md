---
name: kpi-chips
description: >
  Analisa planilha de pedidos de entrega de SIM Cards/chips e gera relatório HTML de KPIs
  com visual CSS Solutions. Use esta skill quando o usuário mencionar: KPI, relatório de
  pedidos, pedidos.xlsx, análise de entregas, taxa de entrega, SLA chips, desempenho de
  transportadores, chips, D+0, D+1, D+2, ou quando mencionar/anexar um arquivo .xlsx de
  pedidos de entrega.
---

# KPI Chips — CSS Solutions

Gera relatório HTML interativo de KPIs para operações de entrega de SIM Cards.

## Como invocar

Quando o usuário fornecer um caminho para o arquivo `.xlsx` de pedidos, execute:

```bash
python "C:\Users\CSS SOLUTION\skills\kpi-chips\scripts\gerar_kpis.py" "<caminho_do_xlsx>"
```

Em seguida, abra o HTML gerado no navegador:

```powershell
Start-Process "<caminho_do_html_gerado>"
```

Informe ao usuário: "Relatório gerado em `<caminho>` e aberto no navegador."

## Dependências

```
pip install pandas openpyxl holidays
```

## O que o script gera

- **Bloco 1 — Cards de resumo:** Total de pedidos, taxa de entrega, SLA ≤D+2, D+0/D+1/D+2/D+3+, média de tentativas, taxa 1ª tentativa, cumprimento de agenda
- **Bloco 2 — Tabela por transportador:** Ordenável por qualquer coluna, com badges coloridos por SLA
- **Bloco 3 — Tabela por cidade:** Cidades com ≥10 pedidos, ordenável

## Regras de negócio

- Dia útil = segunda a sexta, excluindo feriados nacionais brasileiros
- D+X = dias úteis entre `Criado em` e `Fechado em` (apenas data, ignora hora)
- SLA aprovado = D+0, D+1 ou D+2
- "PA não Identificado" conta como não entregue
- Base de cálculo = todos os pedidos do arquivo
