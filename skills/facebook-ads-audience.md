# Skill: Definir Público-Alvo para Facebook Ads

Quando invocado com `/facebook-ads-audience`, siga este fluxo para criar segmentações de público estratégicas para campanhas de engajamento no Meta Ads.

## 1. Coleta de contexto

Pergunte ao usuário:
- Qual é o nicho ou segmento? (ex: beleza, fitness, gastronomia, negócios locais, infoprodutos)
- Onde fica o público? (cidade, estado, país — ou "Brasil inteiro")
- Faixa etária e gênero preferidos?
- Quais são os principais interesses ou comportamentos do cliente ideal?
- Tem base de clientes existente? (email list, seguidores, visitantes do site)

## 2. Estratégia de 3 públicos (Funil Completo)

Crie os 3 públicos abaixo com base nas respostas:

---

### Público 1 — Frio (Topo do Funil)
> Pessoas que ainda não conhecem a marca. Objetivo: apresentar e gerar primeira impressão.

**Como configurar:**
- Segmentação detalhada: liste 5–8 interesses específicos e relevantes ao nicho
- Comportamentos: ex: "Envolveu-se com conteúdo nos últimos 30 dias", "Administrador de página"
- Dados demográficos: nível de escolaridade, estado civil, cargo (se B2B)
- **Tamanho ideal:** 500 mil a 5 milhões (Brasil) — amplo o suficiente para o algoritmo otimizar
- **Exclusão:** pessoas que já curtiram a página ou interagiram nos últimos 60 dias

**CPM esperado:** R$ 8–18 (público frio tende a ser mais barato)

---

### Público 2 — Morno (Meio do Funil)
> Pessoas que já interagiram com a marca. Objetivo: aprofundar relacionamento e aumentar engajamento.

**Como configurar (Custom Audiences):**
- Pessoas que interagiram com a Página do Facebook nos últimos 60 dias
- Pessoas que visitaram o perfil do Instagram nos últimos 30 dias
- Pessoas que assistiram 50%+ de algum vídeo publicado
- Seguidores atuais (para impulsionar publicações específicas)

**Onde criar:** Meta Ads Manager > Públicos > Criar Público > Público Personalizado > Facebook/Instagram

**CPM esperado:** R$ 12–25 (mais caro, mas maior taxa de engajamento)

---

### Público 3 — Quente / Lookalike (Fundo do Funil)
> Pessoas parecidas com os melhores clientes ou fãs. Objetivo: encontrar novos leads qualificados.

**Como configurar (Lookalike Audiences):**
- Lookalike 1% baseado nos seguidores da página (melhor semelhança)
- Lookalike 1–3% baseado em lista de clientes (se disponível)
- Lookalike baseado em quem interagiu com posts nos últimos 180 dias

**Tamanho:** 1% = ~2 milhões no Brasil; 3% = ~6 milhões

**CPM esperado:** R$ 10–22 (boa relação custo-benefício)

---

## 3. Estratégia de exclusões (evitar sobreposição)

Sempre configure exclusões para cada público:

| Público | Excluir |
|---|---|
| Frio | Quem já curtiu a página + quem interagiu nos últimos 30 dias |
| Morno | Quem já é cliente / comprou (se tiver pixel) |
| Lookalike | Público morno (para não disputar leilão interno) |

**Como verificar sobreposição:** Meta Ads Manager > Públicos > Selecionar 2 públicos > Ações > Mostrar sobreposição de público

## 4. Distribuição de orçamento recomendada

Para campanhas de engajamento com foco em crescimento:

| Público | % do Orçamento | Razão |
|---|---|---|
| Frio (Interesses) | 50% | Escala e descoberta |
| Lookalike 1% | 30% | Qualidade + volume |
| Morno (Remarketing) | 20% | Reativação e fidelização |

## 5. Dicas de público para engajamento

- **Evite públicos muito pequenos** (< 100k): o algoritmo não consegue otimizar
- **Evite públicos muito grandes** (> 20 milhões): muita gente irrelevante, CPM sobe
- **Teste 1 variável por vez:** troque apenas o interesse ou apenas o criativo, nunca os dois juntos
- **Renove públicos a cada 30–45 dias** para evitar saturação
- **Advantage+ Audience** (público automático do Meta) funciona bem após ter dados de pixel suficientes
