# Skill: Analisar Métricas de Campanha no Facebook Ads

Quando invocado com `/facebook-ads-metrics`, siga este fluxo para diagnosticar o desempenho de campanhas de engajamento e gerar um plano de otimização.

## 1. Coleta de dados

Peça ao usuário os números atuais da campanha (pode ser de um conjunto ou da campanha toda):

- Alcance e Impressões
- CPM (Custo por Mil Impressões)
- CTR (Taxa de Cliques — se houver link)
- Custo por Engajamento (CPE) ou Custo por Curtida/Seguidor
- Frequência
- Engajamentos totais (curtidas, comentários, compartilhamentos, salvamentos)
- Orçamento diário e total gasto até agora
- Há quantos dias a campanha está rodando?
- Objetivo da campanha (curtidas na página, engajamento, alcance)

## 2. Benchmarks de referência (Brasil, 2024–2025)

Compare os números fornecidos com estas referências:

### Campanha de Engajamento / Conteúdo

| Métrica | Ruim | Aceitável | Bom | Excelente |
|---|---|---|---|---|
| CPM (R$) | > R$ 35 | R$ 20–35 | R$ 10–20 | < R$ 10 |
| CTR (Feed) | < 0,5% | 0,5–1% | 1–2% | > 2% |
| CTR (Stories/Reels) | < 0,3% | 0,3–0,6% | 0,6–1,2% | > 1,2% |
| Custo por Curtida (R$) | > R$ 1,50 | R$ 0,70–1,50 | R$ 0,20–0,70 | < R$ 0,20 |
| Custo por Seguidor (R$) | > R$ 3,00 | R$ 1,50–3,00 | R$ 0,50–1,50 | < R$ 0,50 |
| Frequência | > 5 | 3–5 | 2–3 | 1–2 |
| Taxa de Engajamento | < 1% | 1–3% | 3–6% | > 6% |

## 3. Diagnóstico dos problemas

Com base nos números, identifique o gargalo principal:

### CPM muito alto (> R$ 30)
- Público muito pequeno ou muito específico
- Nicho competitivo (alta temporada, feriados)
- Frequência alta (leilão interno = mais caro)
- **Solução:** ampliar público, usar Advantage+ Placements, testar horários de menor concorrência

### CTR baixo (< 0,5%)
- Criativo não atrai atenção (hook fraco)
- Imagem ou vídeo pouco relevante para o público
- Copy genérica ou sem proposta de valor clara
- **Solução:** trocar criativo, testar novo hook nos primeiros 3 segundos (vídeo) ou imagem mais chamativa

### Frequência alta (> 3,5)
- Público saturado — as mesmas pessoas vendo o mesmo anúncio repetidamente
- **Solução:** renovar criativo imediatamente, expandir público ou criar exclusão dos que já engajaram

### CPE alto com CTR bom
- Público está clicando mas não engajando (mismatch entre expectativa e conteúdo)
- Página ou perfil com poucos seguidores ou publicações antigas (baixa credibilidade)
- **Solução:** melhorar página/perfil antes de escalar; revisar copy do anúncio

### Fase de aprendizado prolongada (> 7 dias sem sair)
- Orçamento muito baixo (< R$ 10/dia por conjunto)
- Muitas edições no conjunto nos primeiros dias
- **Solução:** aumentar orçamento ou consolidar conjuntos similares

## 4. Plano de otimização (3–5 ações priorizadas)

Com base no diagnóstico, gere um plano de ação ordenado por impacto:

**Formato:**
1. [Ação] — [Por quê resolver isso primeiro] — [Como fazer no Meta Ads Manager]
2. ...

Exemplo de ações possíveis:
- Duplicar conjunto vencedor com orçamento +30%
- Pausar conjunto com frequência > 4 e substituir por novo criativo
- Testar público Lookalike 1% para substituir público de interesses saturado
- Ativar Advantage+ Creative para otimização automática de criativos
- Ajustar horário de veiculação para 18h–23h (pico de engajamento no BR)

## 5. Decisões de escala, pausa ou manutenção

| Situação | Decisão |
|---|---|
| CPE < meta E frequência < 2 E em aprendizado | Aguardar — não mexer |
| CPE < meta E frequência < 3 E saiu do aprendizado | Escalar +20–30% do orçamento |
| CPE 1,5x a meta E frequência < 2,5 | Testar novo criativo mantendo público |
| CPE > 2x a meta após 7 dias | Pausar conjunto e reavaliar público |
| Frequência > 4 em qualquer situação | Renovar criativo imediatamente |

## 6. Relatório de desempenho semanal

Ao final da análise, gere um resumo estruturado:

```
RELATÓRIO SEMANAL — [Nome da Campanha]
Data: [data]

RESUMO:
- Alcance: [X] pessoas
- Impressões: [X]
- Engajamentos: [X] (taxa: X%)
- Custo total: R$ [X]
- CPE médio: R$ [X]

STATUS: Ótimo / Aceitável / Precisa de ajuste / Pausar

AÇÕES PARA ESTA SEMANA:
1. ...
2. ...
3. ...
```
