# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Sobre este repositório

Versiona as skills e configurações do Claude Code para sincronização entre computadores.

Remote: `https://github.com/pedrohc7/my-agent-skills.git`

## O que está versionado

| Caminho | Descrição |
|---|---|
| `.agents/.skill-lock.json` | Registro das skills de terceiros instaladas (fonte + versão) |
| `.claude/settings.json` | Preferências globais (plugins, tema, effort level) |
| `skills/` | Skills customizadas criadas pelo usuário (cada skill = subpasta com `SKILL.md` ou arquivo `.md`) |
| `agents/` | Sub-agentes Claude customizados (cada agente = arquivo `.md` com frontmatter) |
| `commands/` | Comandos slash customizados (`/nome`) |
| `setup.ps1` | Script de instalação em novo computador |

## Instalação em novo computador

```powershell
git clone https://github.com/pedrohc7/my-agent-skills.git $env:TEMP\agent-setup
powershell -ExecutionPolicy Bypass -File "$env:TEMP\agent-setup\setup.ps1"
```

Reinicie o Claude Code após rodar o script.

## Criar uma skill customizada

1. Crie a pasta: `skills\nome-da-skill\`
2. Crie `skills\nome-da-skill\SKILL.md` com o formato:
   ```markdown
   ---
   name: nome-da-skill
   description: O que a skill faz (usado para decidir quando ativá-la)
   ---
   # Título
   ...instruções para o Claude...
   ```
3. Faça commit e push

## Criar um agente customizado

1. Crie `agents\nome-do-agente.md` com o formato:
   ```markdown
   ---
   name: nome-do-agente
   description: Quando usar este agente
   ---
   ...instruções do agente...
   ```

## Criar um comando slash customizado

1. Crie `commands\nome-do-comando.md` com as instruções que o Claude deve executar ao receber `/nome-do-comando`

## Sincronizar após mudanças locais

```powershell
git add .agents/.skill-lock.json .claude/settings.json skills/ agents/ commands/
git commit -m "Update skills/agents/settings"
git push
```
