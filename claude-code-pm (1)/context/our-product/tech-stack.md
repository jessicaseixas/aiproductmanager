# Tech Stack - Lead Qualify Assistant

## Overview

O Lead Qualify Assistant é construido em Python 3.12+ e faz parte do monorepo `credai-api`, que hospeda todos os projetos de IA da Loft. A arquitetura segue padroes de clean architecture com ports/adapters e utiliza o framework Pydantic-AI para orquestracao de agentes.

## Stack Principal

### Linguagem e Runtime
| Tecnologia | Versao | Uso |
|------------|--------|-----|
| **Python** | 3.12+ | Linguagem principal |
| **uv** | latest | Gerenciador de pacotes e workspaces |
| **Hatchling** | latest | Build backend |

### Framework de IA
| Tecnologia | Versao | Uso |
|------------|--------|-----|
| **Pydantic-AI** | 1.0.1+ | Framework de agentes com suporte a tools, validacao de output e instrucoes |
| **Pydantic** | 2.0+ | Validacao de dados e modelos |
| **Pydantic-Evals** | 0.7.3+ | Framework de avaliacao de agentes |

### Modelos de LLM
| Modelo | Provider | Uso |
|--------|----------|-----|
| **Gemini 2.5 Pro** | Google | Modelo principal para qualificacao |
| **OpenAI (fallback)** | OpenAI | Modelo de fallback para casos de rate limit |

### API e Web
| Tecnologia | Versao | Uso |
|------------|--------|-----|
| **FastAPI** | 0.115+ | Framework web para APIs REST |
| **Uvicorn** | 0.32+ | Servidor ASGI |
| **aiohttp** | 3.12+ | Cliente HTTP assincrono |

### Persistencia e Cache
| Tecnologia | Uso |
|------------|-----|
| **AWS DynamoDB** | Armazenamento de leads e historico de mensagens |
| **Redis** | Cache e rate limiting |
| **Google BigQuery** | Data lake para metricas e analytics |

### Integracao WhatsApp
| Tecnologia | Uso |
|------------|-----|
| **Meta WhatsApp Business API** | Envio e recebimento de mensagens |
| **Webhooks** | Recebimento de mensagens em tempo real |

### Observabilidade
| Tecnologia | Uso |
|------------|-----|
| **Datadog (ddtrace)** | APM, tracing e logs |
| **Stitch** | Pipeline de metricas para BigQuery |

### UI para Debug
| Tecnologia | Versao | Uso |
|------------|--------|-----|
| **Streamlit** | 1.36+ | Interface para debug e testes |
| **Plotly** | 5.17+ | Visualizacoes |
| **Streamlit-AgGrid** | 1.1+ | Tabelas interativas |

## Arquitetura do Codigo

```
lead-qualify-assistant/
├── src/lead_qualify_assistant/
│   ├── adapters/           # Implementacoes de ports (DynamoDB, APIs)
│   ├── agencies_management/ # Gestao de imobiliarias/parceiros
│   ├── coexistence/        # Logica de coexistencia com outros sistemas
│   ├── evals/              # Casos de teste para avaliacao do agente
│   ├── expiration/         # Logica de expiracao de leads
│   ├── message_debouncing/ # Debouncing de mensagens
│   ├── models_v2/          # Novos modelos de dados
│   ├── onboarding/         # Fluxo de onboarding de leads
│   ├── ports/              # Interfaces/contratos (ports)
│   ├── routes/             # Endpoints FastAPI
│   ├── search/             # Integracao com busca de imoveis
│   ├── services/           # Servicos de dominio
│   ├── utils/              # Utilitarios
│   ├── agent.py            # Agente principal Pydantic-AI
│   ├── agent_prompts.py    # Prompts e instrucoes do agente
│   ├── agent_tools.py      # Ferramentas disponíveis para o agente
│   ├── agent_validators.py # Validadores de output
│   └── models.py           # Modelos de dados (Lead, LeadInsights, etc)
├── docs/                   # Design docs
├── evals/                  # Datasets de avaliacao
├── tests/                  # Testes unitarios e de integracao
└── ui/                     # Interface Streamlit
```

## Ferramentas do Agente (Tools)

O agente possui as seguintes ferramentas disponiveis:

| Tool | Descricao |
|------|-----------|
| `update_lead_insights` | Atualiza informacoes coletadas do lead |
| `lead_insights_collection_completed` | Marca coleta de dados como completa |
| `lead_insights_validation` | Valida informacoes coletadas |
| `human_assistance_requested` | Solicita atendimento humano |
| `search_and_send_whatsapp` | Busca imoveis e envia resultados via WhatsApp |

## Modulo Shared

O projeto utiliza um modulo `shared` que contem funcionalidades comuns:

| Modulo | Funcionalidade |
|--------|----------------|
| `shared.llm` | Configuracoes e utilitarios de LLM |
| `shared.messaging.whatsapp` | Cliente WhatsApp API |
| `shared.aws` | Clientes AWS (DynamoDB, S3) |
| `shared.cache` | Integracao Redis |
| `shared.datalake` | Integracao BigQuery |
| `shared.metrics` | Cliente de metricas (Stitch) |
| `shared.pdf` | Geracao de PDFs (WeasyPrint) |
| `shared.evals` | Framework de avaliacao |

## Dependencias de Desenvolvimento

| Tecnologia | Uso |
|------------|-----|
| **pytest** | Testes |
| **pytest-asyncio** | Testes assincronos |
| **pytest-cov** | Cobertura de codigo |
| **ruff** | Linter e formatter |
| **pyright** | Type checking |
| **pre-commit** | Hooks de pre-commit |
| **moto** | Mocks para AWS |

## Infraestrutura

- **Cloud**: Google Cloud Platform (GCP) + AWS
- **Container**: Docker
- **CI/CD**: GitHub Actions
- **Secrets**: JumpCloud Password Manager

## Links Uteis

- **Repositorio**: `loft-br/credai-api` (monorepo)
- **Subprojeto**: `lead-qualify-assistant/`
