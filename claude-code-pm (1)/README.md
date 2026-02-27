# PM Workspace — Loft

> Workspace de Product Management com Claude Code para PMs da Loft.

Este repositório contém um workspace completo para PMs, com skills customizadas, slash commands, integração com Jira, e estrutura de documentação de produto padronizada. O conteúdo do **Qualifica Leads** está incluído como exemplo de referência.

## O que vem incluído?

- **11 skills de PM** — escrever PRDs, criar tickets, definir métricas, pesquisar personas, e mais
- **6 slash commands** — sincronizar com Jira, listar entregas do GitHub, criar tickets, gerar/executar testes
- **Estrutura de contexto** — organização padronizada para documentação de produto (features, PRDs, competidores)
- **Integração com Jira** — criar/atualizar tickets via API REST, sincronizar status de features
- **Testes E2E** — geração de planos de teste e automação com Playwright

---

## Pré-requisitos

- macOS / Linux / Windows (WSL)
- [Node.js 18+](https://nodejs.org/)
- Conta GitHub com acesso à org `loft-br`
- Conta Atlassian (Jira) da Loft

---

## Instalação do Claude Code

### Passo 1: Instalar o Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

Verifique a instalação:

```bash
claude --version
```

> Para mais detalhes, veja a [documentação oficial](https://docs.anthropic.com/en/docs/claude-code).

### Passo 2: Autenticação

Na primeira execução, o Claude Code vai pedir autenticação:

```bash
claude
```

Opções de autenticação:
- **Claude Max/Pro/Team** — login com conta Anthropic
- **API Key** — se a empresa fornecer uma chave de API

### Passo 3: Configurar MCP Servers (Opcional)

Se quiser usar integrações adicionais:

- **Figma MCP** — para importar designs diretamente
- **Jira MCP** — alternativa à integração via API REST

Consulte a [documentação de MCP](https://docs.anthropic.com/en/docs/claude-code/mcp) para configuração.

---

## Setup do Workspace

### Passo 1: Clonar o repositório

```bash
git clone git@github.com:loft-br/claude-code-pm.git meu-produto-pm
cd meu-produto-pm
```

### Passo 2: Configurar credenciais Jira

```bash
cp .env.example .env
```

Edite o `.env` com suas credenciais:

```
JIRA_BASE_URL=https://loftbr.atlassian.net
JIRA_USER_EMAIL=seu-email@loft.com.br
JIRA_API_TOKEN=seu-token-aqui
```

> Para gerar um API token, acesse: https://id.atlassian.com/manage-profile/security/api-tokens

### Passo 3: Instalar dependências (para testes)

```bash
npm install
npx playwright install
```

### Passo 4: Personalizar para seu produto

1. Edite `CLAUDE.md` > **Project Configuration** com o nome do seu produto, Jira key e repos
2. Atualize `context/our-product/product-overview.md` com a visão do seu produto
3. Crie features em `context/our-product/features/`
4. Atualize `context/our-company/loft.md` se necessário

---

## Estrutura do Projeto

```
meu-produto-pm/
├── CLAUDE.md                        # Instruções do projeto para o Claude
├── README.md                        # Este arquivo
├── .env.example                     # Template de credenciais Jira
├── package.json                     # Dependências (Playwright)
│
├── .claude/
│   ├── commands/                    # Slash commands customizados
│   │   ├── sync/
│   │   │   ├── github.md            # /sync:github
│   │   │   ├── jira.md              # /sync:jira
│   │   │   └── granola.md           # /sync:granola
│   │   ├── new/
│   │   │   └── jira-ticket.md       # /new:jira-ticket
│   │   └── test/
│   │       ├── plan.md              # /test:plan
│   │       └── run.md               # /test:run
│   ├── skills/                      # Skills customizadas
│   │   ├── writing-prds/
│   │   ├── writing-tickets/
│   │   ├── jira-tickets/
│   │   ├── defining-user-stories/
│   │   ├── defining-metrics/
│   │   ├── researching-personas/
│   │   ├── scoping-mvp/
│   │   ├── prompt-engineering/
│   │   ├── docx/
│   │   ├── web-testing/
│   │   └── playwright-testing/
│   ├── scripts/                     # Scripts auxiliares
│   └── settings.json                # Configurações compartilhadas
│
├── context/                         # Documentação de produto
│   ├── INDEX.md                     # Índice de todo o contexto
│   ├── our-company/
│   │   └── loft.md                  # Contexto da empresa
│   └── our-product/
│       ├── product-overview.md      # Visão geral do produto
│       ├── faq.md                   # Perguntas frequentes
│       ├── features/                # Features organizadas por status
│       │   ├── live/                #   Em produção
│       │   ├── in-development/      #   Em desenvolvimento
│       │   └── planned/             #   Planejadas
│       ├── prds/                    # Product Requirements Documents
│       └── competition/             # Análise competitiva
│
├── scripts/                         # Scripts utilitários
├── tests/                           # Testes E2E (Playwright)
└── node_modules/                    # (ignorado pelo git)
```

---

## Skills Disponíveis

### writing-prds

Escreve ou revisa PRDs seguindo boas práticas de Product Management. Suporta imagens de wireframes e mockups.

**Quando usar:** ao transformar notas, ideias ou wireframes em um PRD estruturado, ou ao revisar um PRD existente.

```
"Escreva um PRD para a feature de filtro avançado de leads"
"Revise este PRD e sugira melhorias: [conteúdo]"
```

### writing-tickets

Cria ou revisa tickets dev-ready a partir de notas não-estruturadas usando um template padronizado.

**Quando usar:** ao transformar requisitos em tickets prontos para desenvolvimento, ou ao revisar tickets existentes.

```
"Crie um ticket para implementar a validação de CPF no cadastro"
"Revise este ticket e sugira melhorias"
```

### jira-tickets

Cria, atualiza e gerencia tickets no Jira com formatação ADF (Atlassian Document Format) via API REST v3.

**Quando usar:** após criar um ticket com `writing-tickets`, para enviá-lo diretamente ao Jira.

```
"Crie este ticket no Jira no projeto SLA"
"Atualize o ticket SLA-525 com os novos critérios de aceite"
```

> **Dica:** configure o `.env` com suas credenciais Jira antes de usar.

### defining-user-stories

Define ou revisa quebra de user stories para PRDs e features seguindo o critério INVEST.

**Quando usar:** ao quebrar uma feature em stories menores, ou ao revisar uma quebra existente.

```
"Quebre esta feature em user stories: [descrição da feature]"
"Revise estas user stories e verifique se seguem INVEST"
```

### defining-metrics

Define ou revisa métricas de sucesso usando o Mixpanel Measurement Framework. Faz perguntas de esclarecimento antes de propor métricas.

**Quando usar:** ao definir como medir o sucesso de uma feature, PRD ou iniciativa.

```
"Defina métricas de sucesso para a feature de qualificação automática"
"Revise estas métricas e sugira melhorias"
```

### researching-personas

Pesquisa ou revisa perfis de persona focando em comportamentos, jobs-to-be-done e pain points (não dados demográficos).

**Quando usar:** ao criar personas para um novo produto/feature, ou ao revisar personas existentes.

```
"Pesquise a persona do corretor de imóveis que usa o Qualifica Leads"
"Revise esta persona e sugira melhorias"
```

### scoping-mvp

Define ou revisa escopo de MVP criando listas de in-scope/out-of-scope.

**Quando usar:** ao definir o que entra e o que fica de fora do MVP de uma feature.

```
"Defina o escopo de MVP para a feature de relatórios"
"Revise este escopo de MVP"
```

### prompt-engineering

Referência de técnicas avançadas de prompt engineering para maximizar performance de LLMs.

**Quando usar:** ao desenhar prompts para features de IA, criar system prompts, ou otimizar interações com LLMs.

```
"Me ajude a melhorar este prompt de qualificação de leads"
"Qual a melhor técnica de prompt para classificação de texto?"
```

### docx

Criação, edição e análise de documentos Word (.docx) com suporte a tracked changes, comentários e formatação.

**Quando usar:** ao precisar criar ou editar documentos Word para stakeholders, contratos ou documentação formal.

```
"Crie um documento Word com o resumo executivo deste PRD"
"Analise este documento e extraia os requisitos"
```

### web-testing

Referência de boas práticas de QA e cenários de teste para testes E2E de websites.

**Quando usar:** ao planejar testes de uma feature, criar checklists de QA, ou definir cenários de teste.

```
"Liste os cenários de teste para o fluxo de cadastro"
"Crie um checklist de QA para o formulário de leads"
```

### playwright-testing

Escrita e execução de testes automatizados E2E usando Playwright.

**Quando usar:** ao criar arquivos de teste automatizados, debugar falhas de teste, ou configurar Playwright.

```
"Crie testes Playwright para o fluxo de login"
"Este teste está falhando, me ajude a debugar"
```

---

## Slash Commands

### `/sync:github <período>`

Lista PRs e entregas do time no GitHub para um período específico.

```
/sync:github de hoje
/sync:github dessa semana
/sync:github dos últimos 7 dias
```

### `/sync:jira`

Sincroniza documentação de features com o Jira. Lê os README.md de cada feature, consulta o status no Jira, e move as pastas para o diretório correto (`live/`, `in-development/`, `planned/`).

```
/sync:jira
```

### `/sync:granola`

Sincroniza transcrições de reuniões do Granola para `context/meetings/`.

```
/sync:granola
/sync:granola --all
```

### `/new:jira-ticket`

Cria uma nova story no Jira usando o template padronizado de ticket.

```
/new:jira-ticket
```

### `/test:plan <input>`

Gera plano de testes e scripts Playwright a partir de um ticket Jira, arquivo ou descrição.

```
/test:plan SLA-525
/test:plan tests/minha-feature/
```

### `/test:run <pasta>`

Executa testes Playwright e gera relatórios. Suporta execução paralela por categoria.

```
/test:run tests/sla-525-cadastro/
/test:run tests/sla-525-cadastro/ --parallel
```

---

## Workflows Recomendados

### Nova feature do zero

1. **Pesquisar personas** — entender para quem é a feature
2. **Escrever PRD** — documentar o problema e a solução proposta
3. **Definir métricas** — como medir o sucesso
4. **Definir escopo de MVP** — o que entra e o que fica de fora
5. **Quebrar em user stories** — stories independentes e estimáveis
6. **Criar tickets** — tickets dev-ready com critérios de aceite
7. **Enviar ao Jira** — criar os tickets no Jira via API
8. **Gerar testes** — plano de testes e scripts Playwright

### Review de documentos

Todas as skills de PM suportam modo REVIEW. Passe o conteúdo existente e peça uma revisão:

```
"Revise este PRD e sugira melhorias: [conteúdo]"
"Revise estas user stories: [stories]"
```

### Sync semanal

```
/sync:jira            # Atualizar status das features
/sync:github dessa semana   # Ver entregas do time
```

---

## Personalizando para Seu Produto

### 1. Editar `CLAUDE.md`

Atualize a tabela **Project Configuration** no topo do arquivo:

| Key | O que colocar |
|-----|---------------|
| **Product Name** | Nome do seu produto |
| **Jira Project Key** | Chave do projeto no Jira (ex: `SLA`, `CRM`) |
| **GitHub Repo (code)** | Repo do código-fonte |
| **GitHub Repo (docs/tickets)** | Repo de docs/tickets (se separado) |
| **GitHub Search Term** | Termo para buscar PRs relevantes |

### 2. Criar contexto do produto

Atualize estes arquivos com informações do seu produto:

- `context/our-product/product-overview.md` — visão geral, missão, público-alvo
- `context/our-product/faq.md` — perguntas frequentes sobre o produto
- `context/our-product/features/` — documentação de cada feature

### 3. Estrutura de features

Cada feature deve ter sua própria pasta com:

```
features/planned/minha-feature/
├── README.md      # Overview com header padronizado
└── TICKET.md      # Requisitos detalhados
```

Use `/sync:jira` para mover automaticamente entre `planned/`, `in-development/` e `live/`.

---

## FAQ

**Como gerar um API token do Jira?**

Acesse https://id.atlassian.com/manage-profile/security/api-tokens, clique em "Create API token", e cole o token no seu `.env`.

**Preciso do Playwright para usar o workspace?**

Apenas se quiser usar os comandos `/test:plan` e `/test:run`. As skills de PM funcionam sem Playwright.

**Posso usar com outros editores além do VS Code?**

Sim. O Claude Code funciona no terminal e é independente de editor. A pasta `.vscode/` e `.obsidian/` no `.gitignore` são apenas para evitar configs pessoais no repo.

**Uma skill não está funcionando. O que fazer?**

1. Verifique se o Claude Code está atualizado: `npm update -g @anthropic-ai/claude-code`
2. Verifique se o `.env` está configurado (para skills que usam Jira)
3. Tente recarregar: feche e abra o Claude Code novamente

**Como adicionar uma nova skill?**

Crie uma pasta em `.claude/skills/` com pelo menos um arquivo `SKILL.md`. Consulte a [documentação de skills](https://docs.anthropic.com/en/docs/claude-code/skills) para o formato.

**Como adicionar um novo slash command?**

Crie um arquivo `.md` em `.claude/commands/`. O caminho do arquivo define o nome do comando (ex: `.claude/commands/sync/jira.md` → `/sync:jira`). Consulte a [documentação de commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands).
