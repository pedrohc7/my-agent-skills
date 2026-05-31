# Skill: Organizador de Clientes e Projetos

Quando invocado com `/organizar`, siga este fluxo para ajudar o usuário a estruturar, auditar ou arquivar clientes e projetos pessoais com base na estrutura padrão definida.

## Estrutura padrão de pastas

### Raiz
```
_CLIENTES/
_PROJETOS-PESSOAIS/
_TEMPLATES/
_ARQUIVO-GERAL/
```

### Dentro de cada cliente
```
[NomeCliente] - [Nicho]/
├── 01. Briefing & Contrato/
│   ├── briefing/
│   ├── proposta/
│   ├── contrato/
│   ├── onboarding/
│   └── acessos-iniciais/
├── 02. Planejamento/
│   ├── calendario-editorial/
│   ├── estrategia/
│   ├── personas/
│   ├── posicionamento/
│   ├── funil/
│   └── campanhas-futuras/
├── 03. Branding/
│   ├── logo/
│   ├── identidade-visual/
│   ├── fontes/
│   ├── paleta/
│   └── brandbook/
├── 04. Conteudo/
│   ├── copies/
│   ├── roteiros/
│   ├── legendas/
│   ├── textos/
│   ├── artigos/
│   └── emails/
├── 05. Design/
│   ├── artes-aprovadas/
│   ├── arquivos-editaveis/
│   ├── thumbnails/
│   └── criativos/
├── 06. Videos/
│   ├── videos-finais/
│   ├── videos-brutos/
│   ├── reels/
│   ├── anuncios/
│   └── motion/
├── 07. Trafego Pago/
│   ├── campanhas/
│   ├── relatorios/
│   ├── criativos/
│   ├── publicos/
│   ├── metricas/
│   └── pixel-tag-manager/
├── 08. Social Media/
│   ├── posts-aprovados/
│   ├── cronograma/
│   ├── analytics/
│   └── comentarios-importantes/
├── 09. Relatorios e KPIs/
│   ├── dashboards/
│   ├── PDFs-mensais/
│   ├── metricas/
│   ├── resultados/
│   └── apresentacoes/
├── 10. Financeiro/
│   ├── notas/
│   ├── comprovantes/
│   ├── orcamento/
│   └── invoices/
├── 11. Reunioes e Comunicacao/
│   ├── atas/
│   ├── gravacoes/
│   ├── alinhamentos/
│   └── feedbacks/
└── 12. Arquivados/
    ├── campanhas-antigas/
    ├── materiais-descontinuados/
    └── versoes-antigas/
```

### Dentro de projetos pessoais (estrutura reduzida)
```
[NomeProjeto]/
├── 01. Planejamento/
├── 02. Conteudo/
├── 03. Design/
├── 04. Publicacoes/
└── 05. Arquivados/
```

### Templates reutilizáveis
```
_TEMPLATES/
├── contratos/
├── propostas/
├── briefings/
├── relatorios/
├── calendarios/
└── onboarding/
```

## Convenções de nomenclatura

| Elemento | Padrão | Exemplo |
|---|---|---|
| Pasta cliente | `NomeCliente - Nicho` | `Bowie Studio - Tatuagem` |
| Arquivo com data | `AAAA-MM-DD_descricao` | `2026-05-17_contrato-v1` |
| Versão | `_v1`, `_v2`, `_FINAL` | `proposta_v2_FINAL` |
| Status | `[APROVADO]`, `[RASCUNHO]` | `[APROVADO] arte-feed` |

---

## Modos de uso

Ao ser invocado, pergunte ao usuário qual modo deseja:

### Modo 1 — Criar estrutura para novo cliente
Pergunte:
- Nome do cliente
- Nicho/segmento
- Quais serviços estão contratados? (ex: só social media, só tráfego, pacote completo)

Com base nos serviços contratados, gere **apenas as pastas relevantes** (não crie todas se o cliente não usa tráfego pago, por exemplo).

Entregue:
1. Lista de pastas a criar em formato de árvore
2. Comando PowerShell para criar todas as pastas automaticamente no caminho informado pelo usuário

**Modelo de comando PowerShell:**
```powershell
$base = "C:\Caminho\Escolhido\_CLIENTES\NomeCliente - Nicho"
$pastas = @(
  "01. Briefing & Contrato\briefing",
  "01. Briefing & Contrato\proposta",
  # ... demais pastas
)
foreach ($p in $pastas) { New-Item -ItemType Directory -Force -Path "$base\$p" }
```

### Modo 2 — Auditar cliente existente
Pergunte o caminho da pasta do cliente.

Verifique (via ferramentas de leitura de arquivos) quais das 12 pastas padrão existem e quais estão faltando.

Entregue:
- Tabela: pasta | status (✅ existe / ❌ faltando)
- Comando PowerShell para criar apenas as que estão faltando

### Modo 3 — Arquivar cliente encerrado
Pergunte:
- Nome do cliente
- Caminho atual da pasta
- Caminho de destino do arquivo

Entregue comando PowerShell para mover a pasta para `_ARQUIVO-GERAL/` com data no nome:
```powershell
Move-Item -Path "origem\NomeCliente - Nicho" -Destination "destino\_ARQUIVO-GERAL\2026-05-17_NomeCliente - Nicho"
```

### Modo 4 — Sugerir nome de arquivo
Pergunte:
- Tipo de arquivo (contrato, arte, relatório, vídeo, etc.)
- Versão ou status
- Data (ou usa a data de hoje automaticamente)

Entregue o nome formatado seguindo a convenção padrão.

### Modo 5 — Criar estrutura para projeto pessoal
Pergunte:
- Nome do projeto
- Tipo (portfólio, estudo, produto digital, outro)

Entregue a estrutura reduzida e o comando PowerShell correspondente.

---

## Regras de comportamento

- Sempre pergunte o modo antes de agir
- Nunca crie pastas sem confirmar o caminho com o usuário
- Se o usuário informar apenas serviços parciais, adapte a estrutura — não force pastas irrelevantes
- Use linguagem direta e objetiva, sem enrolação
- Entregue sempre o comando PowerShell pronto para copiar e colar
- Se o usuário informar um caminho com espaços, envolva em aspas duplas no comando gerado
