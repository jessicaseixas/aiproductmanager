# Project Context: Loft PM Workspace

## About This Project

This is a product management workspace for Loft. The project contains product documentation, competitive analysis, context about Loft (the company), and resources for creating PRDs, user stories, and other PM deliverables.

## Project Configuration

These values are product/squad-specific. Skills and commands reference this section instead of hardcoding values.

| Key | Value |
|-----|-------|
| **Product Name** | Loft Qualifica Leads |
| **Jira Project Key** | `SLA` |
| **GitHub Repo (code)** | `loft-br/credai-api` |
| **GitHub Repo (docs/tickets)** | `loft-br/qualifica-leads` |
| **GitHub Search Term** | `lead-qualify-assistant` |

> **For other products:** Update the table above with your product's values. All skills and commands will automatically use the configured values.

## Project Structure

```
qualifica-leads-pm/
├── context/                     # Company and product context
│   ├── our-company/             # Context about our company
│   └── our-product/             # Context about our product
│       ├── features/            # All product features organized by status
│       │   ├── live/            # Features in production
│       │   │   └── [feature-name]/
│       │   │       └── README.md
│       │   ├── in-development/  # Features being developed
│       │   │   └── [feature-name]/
│       │   │       ├── README.md
│       │   │       └── TICKET.md
│       │   └── planned/         # Features planned but not started
│       │       └── [feature-name]/
│       │           ├── README.md
│       │           └── TICKET.md
│       ├── prds/                # Product Requirements Documents
│       │   └── [product-name].md
│       └── ...
└── .claude/
    ├── commands/               # Custom slash commands
    └── skills/                 # Custom skills
```


## Context Loading

Context is organized in tiers to optimize loading. For a quick overview of all available context, read `context/INDEX.md`.

### Tier 0: Core Identity (Always Load)

Before ANY task, read these files:
1. `context/our-company/loft.md` (~72 lines)
2. `context/our-product/product-overview.md` (~154 lines)

### Tier 1: Product Knowledge (PM Work)

Load when creating tickets, writing PRDs, or doing feature work:
- `context/our-product/features/*/README.md` (all status folders)
- `context/our-product/faq.md`

### Tier 2: Deep Dive (On Demand)

| Content | When to Load |
|---------|--------------|
| `features/*/TICKET.md` | Working on that specific feature |
| `prds/*.md` | Planning major initiatives |
| `competition/*` | Competitive analysis tasks |
| `meetings/*` | User references specific meeting |
| `metrics.md` | Analytics/metrics work |

### Task-Specific Loading Profiles

| Task | Context to Load |
|------|-----------------|
| Creating tickets | Tier 0 + All feature READMEs + FAQ |
| Writing PRDs | Tier 0 + All feature READMEs + FAQ |
| Competitive analysis | Tier 0 + competition/* |
| Test planning | Tier 0 + Feature README + TICKET |
| Meeting follow-up | Tier 0 + relevant meeting file |
| Metrics work | Tier 0 + metrics.md |


## Features Documentation

### Folder Organization

Each feature has its own folder with standardized files:

| Folder | Description | Jira Status |
|--------|-------------|-------------|
| `context/our-product/features/live/` | Features in production | `DONE` |
| `context/our-product/features/in-development/` | Features being actively developed | `IN PROGRESS`, `IN REVIEW` |
| `context/our-product/features/planned/` | Features planned but not yet started | `BACKLOG`, `PRIORIZADO` |

### Feature Folder Structure

Every feature must have its own folder containing:

```
[feature-name]/
├── README.md      # Overview with standardized header (required)
└── TICKET.md      # Detailed requirements from Jira (optional)
```

### README.md Format

Every README.md must follow this standardized format:

```markdown
<!-- jira: PROJ-123 -->

# Feature Name

> Short description in 1-2 lines.

| | |
|---|---|
| **Status** | Planejado / Em desenvolvimento / Produção |
| **Jira** | [PROJ-123](https://loftbr.atlassian.net/browse/PROJ-123) |
| **Lançamento** | Abr/2026 |

---

## Problema
Por que essa feature existe? Que dor resolve?

## Solução
O que a feature faz (3-5 bullet points de escopo).

## Usuário
Para quem é? Qual persona?

## Valor
Qual o impacto esperado? Métricas de sucesso?

## Dependências
Outras features ou sistemas necessários (se houver).

## Requisitos
Ver [TICKET.md](./TICKET.md) para especificações detalhadas.
```

For features without a Jira ticket (typically in `live/`), the format is the same but without the Requisitos section linking to TICKET.md.

### Syncing with Jira

Use the `/atualizar` command to sync feature documentation with Jira:
- Reads all README.md files in feature folders
- Queries Jira for current status of each ticket
- Moves feature folders to correct status folder based on Jira status

### Creating New Feature Documentation

When creating tickets for new features:

1. Create a folder in `context/our-product/features/planned/[feature-name]/`
2. Create `README.md` with the standardized header and Jira reference
3. Create `TICKET.md` with detailed requirements
4. After creating the ticket in Jira, the `/atualizar` command will keep it organized


## Working Standards

### Language
- Product names should use their **original Portuguese names** (e.g., "Loft Fiança Aluguel", "Assistente Loft")
- **Always use proper Portuguese accents** when writing in Portuguese (e.g., "qualificação", "integração", "imóveis", "descrição", "solução")

### Documentation Style
- Format properly with markdown (bold for emphasis, bullet points for lists, code blocks for technical details)

### Feature Update Order

**IMPORTANT:** When updating feature documentation (content changes, scope updates, requirement changes), always follow this order:

1. **README.md first** - Update the overview if the change affects problem, solution, or scope
2. **TICKET.md second** - Update detailed requirements, criteria, and specifications
3. **Jira card last** - Update the card description and add a comment documenting what changed

All three documents must stay aligned. When making changes:
- Ensure the README overview matches the TICKET details
- Ensure the Jira card description reflects the current state
- Add comments in Jira to document significant changes for traceability

### Jira Integration
- Project key: Use the **Jira Project Key** from `## Project Configuration` above
- Cloud ID: `loftbr.atlassian.net`
- Always include Jira reference in feature README.md

## Slash Commands

Custom slash commands are in `.claude/commands/`. Always refer to Anthropic's official documentation before creating a custom slash command: https://code.claude.com/docs/en/slash-commands

### Available Commands

| Command | Description |
|---------|-------------|
| `/sync:github <período>` | List PRs/deliveries from the team for a period (e.g., "de hoje", "dessa semana") |
| `/sync:jira` | Sync feature documentation with Jira (moves folders based on ticket status) |
| `/sync:granola [--all]` | Sync Granola meeting transcripts to `context/meetings/` |
| `/new:jira-ticket` | Create a new Jira story using the ticket template |
| `/test:plan <input>` | Generate test scenarios and Playwright scripts from Jira ticket, file, or description |
| `/test:run <folder>` | Execute Playwright tests and generate reports (uses Bash agents) |

## Subagents

This project uses Claude Code's built-in subagents for parallel/background tasks:

| Built-in Agent | Used By | Purpose |
|----------------|---------|---------|
| `Bash` | `/test:run` | Execute `npx playwright test` commands |

### Parallel Execution

The `/test:run --parallel` flag spawns multiple `Bash` agents in a single message to run test categories in parallel:

```
/test:run tests/folder --parallel
    │
    ├─ Main Claude: parse args, read spec files, identify categories
    │
    ├─ [Single message with multiple Task calls]
    │     ├──→ Task(Bash): npx playwright test --grep='FUNC-' ──┐
    │     ├──→ Task(Bash): npx playwright test --grep='SEC-'  ──┼─ Run simultaneously
    │     ├──→ Task(Bash): npx playwright test --grep='RESP-' ──┤
    │     └──→ Task(Bash): npx playwright test --grep='A11Y-' ──┘
    │
    └─ Main Claude: aggregate JSON results, generate test-report.md
```

Documentation: https://code.claude.com/docs/en/sub-agents

## Skills

Custom skills are in `.claude/skills/`. Always use the skill-creator skill to create custom Claude Code skills.

### Available Skills

| Skill | Description |
|-------|-------------|
| `writing-prds` | Writes or reviews PRDs from notes, wireframes, or rough ideas |
| `writing-tickets` | Creates or reviews dev-ready tickets using the world-class template |
| `jira-tickets` | Creates and manages Jira tickets with proper ADF formatting via direct Jira REST API v3 calls. Supports CREATE, UPDATE, and SYNC modes. |
| `defining-user-stories` | Defines or reviews user story breakdowns (INVEST criteria) |
| `defining-metrics` | Defines or reviews success metrics using Mixpanel Measurement Framework |
| `researching-personas` | Researches or reviews persona profiles (behavior-focused, not demographics) |
| `scoping-mvp` | Defines or reviews MVP scope (in-scope/out-of-scope boundaries) |
| `docx` | Document creation, editing, and analysis for .docx files |
| `web-testing` | QA best practices, test scenarios, report templates |
| `playwright-testing` | Playwright patterns, locators, assertions, examples |
