
# Visão Detalhada do Lead - Aba Detalhes (Resumo e Informações de Contato)

---

# Overview

* **Objetivo:** Implementar a aba "Detalhes" da visão detalhada do lead no Loft Qualifica Leads Standalone, permitindo que corretores visualizem o resumo gerado por IA e as informações de contato do lead para compreender rapidamente o contexto antes do atendimento.
* **Quem é afetado:** Corretores e gestores de imobiliárias que utilizam o Loft Qualifica Leads e precisam acessar rapidamente informações de leads qualificados pela IA para dar continuidade ao atendimento.
* **Comportamento atual:** N/A - Nova funcionalidade para a versão standalone do produto (lançamento previsto para Abr/2026).
* **Comportamento desejado:** Corretores podem acessar a visão detalhada de um lead a partir da listagem de atendimentos, visualizando o cabeçalho com nome/status, navegação por abas, resumo gerado pela IA com disclaimer, e todas as informações de contato do lead com ações rápidas (ligar/email).
* **Por que fazer isso agora:** A versão standalone do Loft Qualifica Leads será lançada em Abr/2026. Esta tela é crítica para que os corretores tenham acesso centralizado a todas as informações coletadas pela IA durante a qualificação, reduzindo o tempo de preparação antes de contatar o lead. Dados de mercado mostram que leads atendidos em menos de 5 minutos têm taxa de conversão 2.6x maior.
* **Links úteis:**
    * [Figma - Aba Detalhes](https://www.figma.com/design/3iXlzrSi8RJEt8Ae52z1Kq/Qualifica-Leads---Standalone?node-id=55-2167)
    * [User Story completa](./user-stories.md)

---

# Definição de Pronto

* Critérios de aceitação completamente satisfeitos
* Testes automatizados adicionados (unitários com cobertura >80% e integração)
* Teste E2E para o happy path de navegação
* Integração testada em staging com dados reais
* Eventos de analytics verificados em staging com propriedades corretas
* Dashboard de observabilidade criado e verificado
* Performance validada (<2s p95 para carregamento da página)
* Auditoria de acessibilidade WCAG AA aprovada
* Code review aprovado
* Design review completado
* QA sign-off obtido
* Feature flag configurada para rollout gradual
* Plano de rollback documentado

---

# Escopo

## Dentro do escopo

* Cabeçalho do lead com nome, badge de status e timestamp de última atualização
* Breadcrumb de navegação: "Atendimentos > [Nome do Lead]"
* Seta de voltar (navegação para lista de Atendimentos)
* Navegação por abas: Detalhes, Interesse, Conversa, Anotações (aba Detalhes como padrão)
* Card "Resumo Geral" com:
  * Texto do resumo gerado pela IA
  * Timestamp "Atualizado em"
  * Disclaimer sobre conteúdo gerado por IA
* Card "Informações do Lead" com:
  * Nome
  * Telefone (clicável)
  * E-mail (clicável)
  * Origem do lead
  * Mensagem de contato inicial
  * Tipo de negócio
  * Contato inicial (data/hora)
  * Último contato (data/hora)
  * Status de Integração CRM
* Tratamento de estados: loading, erro, dados parciais

## Fora do escopo

* Conteúdo das abas Interesse, Conversa e Anotações (tickets separados)
* Edição de informações do lead
* Ações de sincronização com CRM
* Mudança de status do lead a partir desta tela
* Integração direta com WhatsApp (será tratada na aba Conversa)
* Versão mobile/tablet

---

# Especificação de UX + Comportamento

## Pontos de entrada

* Clique em uma linha da listagem de Atendimentos
* URL direta: `/atendimentos/{lead_id}`
* Link na notificação de novo lead (WhatsApp)

## Fluxo

1. Corretor clica em um lead na listagem de Atendimentos
2. Sistema carrega a visão detalhada com aba Detalhes ativa
3. Cabeçalho exibe nome do lead, badge de status e última atualização
4. Breadcrumb exibe "Atendimentos > [Nome do Lead]"
5. Card "Resumo Geral" exibe resumo da IA com timestamp e disclaimer
6. Card "Informações do Lead" exibe todos os dados de contato
7. Corretor pode clicar no telefone para iniciar chamada ou copiar
8. Corretor pode clicar no e-mail para abrir cliente de e-mail
9. Corretor pode navegar entre abas clicando nos tabs
10. Corretor pode voltar à listagem clicando na seta ou no breadcrumb

## Estados

### Carregando
* Skeleton placeholders para ambos os cards
* Skeleton no cabeçalho (nome e status)
* Tabs visíveis mas desabilitados durante carregamento

### Lista preenchida (Happy path)
* Cabeçalho com dados do lead
* Cards preenchidos com todas as informações
* Tabs navegáveis

### Erro
* Mensagem "Erro ao carregar dados do lead"
* Botão "Tentar novamente"
* Manter cabeçalho e navegação visíveis se possível

### Lead não encontrado
* Mensagem "Lead não encontrado"
* Botão para voltar à listagem

### Dados parciais
* Campos sem dados exibem "-"
* Resumo não disponível: "Resumo ainda não disponível"

### Edge cases
* Nome muito longo: truncar com ellipsis após 40 caracteres
* Lead sem e-mail: exibir "-" no campo
* Lead sem resumo IA: exibir "Resumo ainda não disponível" no card

## Componentes do Cabeçalho

| Elemento | Descrição | Comportamento |
|----------|-----------|---------------|
| Seta voltar | Ícone de seta para esquerda | Navega para listagem de Atendimentos |
| Breadcrumb | "Atendimentos > [Nome]" | "Atendimentos" é clicável |
| Nome do lead | Título principal (H1) | Truncado se >40 caracteres |
| Badge de status | Tag colorida | Ex: "Novo" em verde |
| Última atualização | Timestamp | Formato: "Última atualização: DD/MM/YYYY - HH:MM" |

## Status e cores (Badge)

| Status | Cor | Descrição |
|--------|-----|-----------|
| Novo | #20A483 (verde) | Lead recém qualificado |
| Em atendimento | #697077 (cinza) | Corretor assumiu o atendimento |
| Qualificado | #20A483 (verde) | Lead qualificado com sucesso |
| Descartado | #697077 (cinza) | Lead descartado |

## Navegação por Tabs

| Tab | Estado padrão | Descrição |
|-----|---------------|-----------|
| Detalhes | Ativo | Resumo e informações de contato |
| Interesse | Inativo | Preferências de imóvel (ticket separado) |
| Conversa | Inativo | Histórico de conversas (ticket separado) |
| Anotações | Inativo | Notas do corretor (ticket separado) |

## Card "Resumo Geral"

| Elemento | Descrição |
|----------|-----------|
| Título | "Resumo Geral" |
| Texto do resumo | Parágrafo gerado pela IA |
| Timestamp | "Atualizado em DD/MM/YYYY - HH:MM" |
| Disclaimer | "Resumo gerado por IA e pode ter informações erradas ou faltantes. Revise os dados analisando os dados de origem." |

## Card "Informações do Lead"

| Campo | Formato | Ação |
|-------|---------|------|
| Nome | Texto | - |
| Telefone | (XX) XXXXX-XXXX | Clique inicia chamada ou copia |
| E-mail | email@domínio.com | Clique abre cliente de e-mail |
| Origem do lead | Texto (ex: "Portal ZAP") | - |
| Mensagem de contato inicial | Texto multilinha | - |
| Tipo de negócio | "Locação" ou "Venda" | - |
| Contato inicial | DD/MM/YYYY - HH:MM | - |
| Último contato | DD/MM/YYYY - HH:MM | - |
| Integração CRM | Status badge | "Não pronto", "Sincronizado", "Erro de sincronização" |

---

# Especificações técnicas

## Serviços

* **Frontend:** Aplicação web standalone (stack a definir com Eng)
* **Backend:** API REST para dados do lead
* **Analytics:** SDK de analytics integrado

## Contrato de API

```
GET /api/v1/leads/{lead_id}

Response 200:
{
  "id": "string",
  "name": "string",
  "status": "novo" | "em_atendimento" | "qualificado" | "descartado",
  "updated_at": "ISO8601 datetime",
  "summary": {
    "text": "string",
    "generated_at": "ISO8601 datetime"
  },
  "contact": {
    "phone": "string | null",
    "email": "string | null",
    "source": "string",
    "initial_message": "string",
    "business_type": "locacao" | "venda",
    "first_contact_at": "ISO8601 datetime",
    "last_contact_at": "ISO8601 datetime"
  },
  "crm_integration": {
    "status": "not_ready" | "synced" | "error",
    "synced_at": "ISO8601 datetime | null"
  }
}

Response 404:
{
  "error": "lead_not_found",
  "message": "Lead não encontrado"
}

Response 500:
{
  "error": "internal_error",
  "message": "Erro interno do servidor"
}
```

## Mudanças no modelo de dados

* [TBD @Eng] - Confirmar se modelo de dados existente suporta todos os campos necessários
* [TBD @Eng] - Confirmar schema de `summary` (text + generated_at)
* [TBD @Eng] - Confirmar mapeamento de status CRM para strings de exibição

## Segurança & privacidade

* Autenticação via token JWT obrigatória
* Autorização: usuário deve ter permissão de acesso ao lead (mesmo tenant da imobiliária)
* Sanitização do texto do resumo IA para prevenção de XSS antes de renderização
* Validação de formato UUID para lead_id no frontend e backend
* Não logar dados PII (telefone, e-mail) em logs de aplicação
* Rate limiting: 100 requests/minuto por usuário

---

# Critérios de aceite

## Cabecalho e Navegacao
* Cabeçalho exibe nome do lead em destaque (H1)
* Badge de status exibe status correto com cor correspondente ("Novo" em verde)
* Timestamp de última atualização exibe no formato "Última atualização: DD/MM/YYYY - HH:MM"
* Breadcrumb exibe "Atendimentos > [Nome do Lead]" com link funcional
* Seta de voltar navega corretamente para lista de Atendimentos
* Navegação por tabs exibe 4 tabs: Detalhes, Interesse, Conversa, Anotações
* Tab Detalhes está selecionado por padrão ao abrir a visão detalhada
* Troca de tab é instantânea (sem reload de página)

## Card Resumo Geral
* Card "Resumo Geral" exibe texto do resumo gerado pela IA
* Card exibe timestamp "Atualizado em DD/MM/YYYY - HH:MM"
* Disclaimer sobre IA é visível: "Resumo gerado por IA e pode ter informações erradas ou faltantes. Revise os dados analisando os dados de origem."
* Resumo não disponível exibe mensagem "Resumo ainda não disponível"

## Card Informacoes do Lead
* Card exibe todos os 9 campos: Nome, Telefone, E-mail, Origem do lead, Mensagem de contato inicial, Tipo de negócio, Contato inicial, Último contato, Integração CRM
* Telefone é clicável (inicia chamada ou copia para clipboard)
* E-mail é clicável (abre cliente de e-mail padrão)
* Campos sem dados exibem "-"
* Datas formatadas no padrão brasileiro (DD/MM/YYYY - HH:MM)

## Estados e Erros
* Loading state exibe skeleton placeholders para cards
* Erro de API exibe mensagem "Erro ao carregar dados" com botão "Tentar novamente"
* Lead não encontrado (404) exibe mensagem "Lead não encontrado" com botão para voltar
* Timeout de API (>3s) exibe skeleton, depois estado de erro

## NFRs
* Página carrega em <2 segundos (P95)
* Taxa de erro <0.5%
* Acessibilidade WCAG AA: contraste de cores 4.5:1
* Todos os elementos interativos navegáveis por teclado
* Screen reader anuncia nome do lead e status ao carregar página

## Analytics
* Evento `lead_detail_viewed` dispara ao carregar página com props: {lead_id, tab: "detalhes", broker_id, timestamp, load_time_ms}
* Evento `lead_contact_initiated` dispara ao clicar telefone com props: {lead_id, contact_type: "phone", broker_id}
* Evento `lead_contact_initiated` dispara ao clicar e-mail com props: {lead_id, contact_type: "email", broker_id}
* Evento `lead_detail_tab_changed` dispara ao navegar tabs com props: {lead_id, from_tab, to_tab, broker_id}
* Evento `lead_detail_error` dispara em erros de API com props: {lead_id, error_type, error_message}

---

# Observabilidade & Analytics

## Eventos

| Evento | Propriedades | Trigger |
|--------|--------------|---------|
| `lead_detail_viewed` | `{tenant_id, user_id, lead_id, tab: "detalhes", load_time_ms, timestamp}` | Ao carregar a página com sucesso |
| `lead_contact_initiated` | `{tenant_id, user_id, lead_id, contact_type: "phone" \| "email"}` | Ao clicar no telefone ou e-mail |
| `lead_detail_tab_changed` | `{tenant_id, user_id, lead_id, from_tab, to_tab}` | Ao trocar de aba |
| `lead_detail_error` | `{tenant_id, user_id, lead_id, error_type, error_code}` | Ao ocorrer erro de carregamento |
| `lead_detail_back_clicked` | `{tenant_id, user_id, lead_id, navigation_method: "arrow" \| "breadcrumb"}` | Ao clicar para voltar |

## Dashboard (DataDog/Observabilidade)

* Taxa de visualização da visão detalhada por tenant
* Latência de carregamento (p50/p95/p99)
* Taxa de cliques em telefone vs. e-mail
* Distribuição de uso das tabs
* Taxa de erros por tipo
* Taxa de leads sem resumo disponível

## Alertas

| Alerta | Condição | Severidade |
|--------|----------|------------|
| Latência alta | >3s P95 por >5 minutos | Warning |
| Taxa de erro alta | >5% em 5 minutos | Critical (page on-call) |
| Zero acessos | Nenhum acesso por >1h em horário comercial | Warning |

## Auditoria

* Logar acessos com: tenant_id, user_id, lead_id, timestamp
* Não logar dados PII (telefone, e-mail do lead)

---

# Plano de Rollout & Riscos

## Rollout

Feature flag: `standalone_lead_detail_view`

* **Fase 1:** Deploy em staging com testes internos e dados sintéticos
* **Fase 2:** Habilitar para 2-3 imobiliárias piloto do programa beta standalone
* **Fase 3:** Monitorar por 1 semana; se taxa de erro <0.5% e feedback positivo, expandir para 20% dos usuários beta
* **Fase 4:** Rollout 100% para todos os usuários do standalone

## Rollback

* Desabilitar feature flag `standalone_lead_detail_view`
* Cliques em leads na listagem exibem mensagem "Funcionalidade em desenvolvimento"
* Dados permanecem intactos no backend
* Re-habilitar após correção do problema

---

# Riscos

| Risco | Probabilidade | Impacto | Mitigacao |
|-------|---------------|---------|-----------|
| Resumo IA não disponível para leads antigos | Média | Baixa | Exibir mensagem fallback "Resumo ainda não disponível" |
| API lenta em picos de uso | Baixa | Média | Implementar cache, skeleton loaders, timeout com retry |
| Dados de contato incompletos | Média | Baixa | Exibir "-" para campos ausentes, não quebrar layout |
| XSS via resumo gerado por IA | Baixa | Alta | Sanitizar HTML/scripts antes de renderizar |
| Falha na integração CRM | Baixa | Baixa | Exibir status "Erro de sincronização" sem bloquear funcionalidade |

---

# Questões em aberto

* [PM] Clique no telefone deve iniciar WhatsApp ou chamada telefônica tradicional?
* [PM] Quais status de integração CRM além de "Não pronto" devemos suportar? (Sincronizado, Erro, Pendente?)
* [Eng] O resumo da IA é gerado sob demanda ou pré-computado durante qualificação?
* [Eng] Qual framework/component library será utilizado no frontend?
* [Design] Confirmar comportamento de truncamento do nome do lead (40 caracteres?)
* [Design] Confirmar se mensagem de contato inicial deve ter limite de caracteres visíveis

---

# Premissas

* API de detalhes do lead (`GET /api/v1/leads/{lead_id}`) já existe ou será desenvolvida em paralelo
* Autenticação e autorização do standalone já estão implementadas
* Design system e componentes base (tabs, cards, badges, skeleton loaders) já existem
* Resumo da IA é pré-gerado durante o processo de qualificação é armazenado no backend
* Dados do lead são persistidos durante o fluxo de qualificação via WhatsApp
* Story 1 é pré-requisito para Stories 2, 3 e 4 (tabs Interesse, Conversa, Anotações)
* Componentes de acessibilidade (ARIA labels, navegação por teclado) estão disponíveis no design system

---

# Métricas de Sucesso

## Objetivo primario

| Métrica | Meta | Formula |
|---------|------|---------|
| Redução no tempo para primeira ação do corretor | -30% | Comparar tempo médio entre atribuição do lead e primeira ação (ligação/e-mail) antes vs. depois |
| Taxa de acesso aos detalhes do lead | 90% em <5 min | `(Leads com 'lead_detail_viewed' em <5min após atribuição / Total leads atribuídos) × 100` |

## Métricas de engajamento

| Métrica | Descrição | Formula |
|---------|-----------|---------|
| Taxa de uso de contato | % de visualizações que resultam em clique no telefone ou e-mail | `(Eventos 'lead_contact_initiated' / Eventos 'lead_detail_viewed') × 100` |
| Preferência de contato | Distribuição entre telefone vs. e-mail | `COUNT(contact_type) GROUP BY contact_type` |
| Taxa de navegação entre tabs | % de sessões que exploram outras tabs | `(Sessões com 'tab_changed' / Sessões com 'detail_viewed') × 100` |

## Guardrails (Qualidade)

| Métrica | Meta | Formula |
|---------|------|---------|
| Latência p95 | <2s | `PERCENTILE(load_time_ms, 0.95)` |
| Taxa de erro | <0.5% | `(Eventos 'lead_detail_error' / Total requisições) × 100` |
| Taxa de resumos indisponíveis | <10% | `(Leads sem resumo IA / Total leads visualizados) × 100` |
