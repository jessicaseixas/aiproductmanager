# Overview

* **Objetivo:** Permitir que corretores visualizem o historico completo de conversas entre o lead e o assistente de IA para compreender o contexto e continuar o relacionamento de forma fluida, sem precisar repetir perguntas já respondidas.
* **Quem é afetado:** Corretores de imóveis que recebem leads qualificados pelo Loft Qualifica Leads e precisam dar continuidade ao atendimento iniciado pela IA.
* **Comportamento atual:** N/A - Nova funcionalidade. Atualmente corretores não tem acesso ao historico de conversas dentro da plataforma standalone.
* **Comportamento desejado:** Ao acessar a aba "Conversa" na visao detalhada do lead, o corretor visualiza todo o historico de mensagens em interface estilo chat, com mensagens do lead a esquerda e mensagens da IA/corretor a direita, em ordem cronológica com auto-scroll para a mensagem mais recente.
* **Por que fazer isso agora:** O acesso ao contexto da conversa e critico para a experiência de handoff IA-humano. Corretores que entendem o que foi discutido conseguem dar continuidade ao atendimento de forma mais eficiente, evitando perguntas redundantes e aumentando a satisfacao do lead.
* **Links úteis:**
    * Figma/Design: https://www.figma.com/design/3iXlzrSi8RJEt8Ae52z1Kq/Qualifica-Leads---Standalone?node-id=80-2339
    * User Stories: /new-features/lead-detailed-view/user-stories.md (Story 3)
    * Documentacao do Produto: /context/our-product/existing-features.md

---

# Definicao de Pronto

* Todos os critérios de aceite completamente satisfeitos
* Testes unitários adicionados com cobertura >80%
* Testes de integração para a API de conversas
* Teste E2E para carregamento e scroll da conversa
* Teste de performance com 200+ mensagens
* Eventos de analytics verificados em staging com propriedades corretas
* Dashboard de observabilidade criado e verificado
* Auditoria de acessibilidade aprovada (WCAG AA)
* Code review aprovado
* QA sign-off obtido
* Feature flag configurada para rollout gradual

---

# Escopo

## Dentro do escopo

* Interface de chat estilo WhatsApp para exibir historico de mensagens
* Mensagens do lead exibidas a esquerda em bolhas cinza escuro
* Mensagens da IA/corretor exibidas a direita em bolhas laranja/coral
* Cabecalho do remetente em cada mensagem (nome do assistente ou "Corretor Loft")
* Timestamp em cada mensagem no formato HH:MM AM/PM
* Carregamento em ordem cronológica (mais antigas primeiro)
* Auto-scroll para mensagem mais recente ao abrir a aba
* Estado vazio quando não há conversas: "Nenhuma conversa registrada"
* Área de input de mensagem visível porem desabilitada (somente leitura)
* Suporte a mensagens de voz (exibir "[Mensagem de voz]" com transcricao)
* Páginacao para conversas longas (500+ mensagens)
* Eventos de analytics para visualizacao e scroll

## Fora do escopo

* Envio de novas mensagens (story separada)
* Reproducao de audio de mensagens de voz
* Visualizacao de imagens em mensagens
* Atualizacoes em tempo real (WebSocket)
* Busca/filtro de mensagens
* Read receipts (checkmarks de leitura)
* Edicao ou exclusão de mensagens

---

# Especificação de UX + Comportamento

## Pontos de entrada

* Navegacao pela aba "Conversa" na visao detalhada do lead (terceira aba)
* Pre-requisito: Story 1 (Header & Tab Navigation) deve estar completa

## Fluxo

1. Corretor acessa a visao detalhada do lead (vindo da lista de Atendimentos)
2. Corretor clica na aba "Conversa"
3. Sistema exibe skeleton loader enquanto carrega mensagens
4. Sistema carrega historico completo de conversas via API
5. Mensagens sao renderizadas em ordem cronológica
6. View faz auto-scroll para a mensagem mais recente
7. Corretor pode fazer scroll para cima para ver mensagens anteriores
8. (Assicrono) Se houver muitas mensagens, sistema carrega em lotes com páginacao

## Estados

* **Loading:** Skeleton de bolhas de chat enquanto carrega (max 3 segundos)
* **Sucesso:** Mensagens exibidas em ordem cronológica com auto-scroll para mais recente
* **Vazio:** Exibir "Nenhuma conversa registrada" centralizado
* **Erro (timeout):** Após 3s de loading, exibir "Erro ao carregar conversa" com botão "Tentar novamente"
* **Erro (API):** Exibir mensagem de erro genérica com opção de retry - retornar HTTP 500 se erro interno
* **Erro (auth):** Requisicao não autorizada - retornar HTTP 401/403; redirecionar para login
* **Mensagem longa:** Word-wrap dentro da bolha, sem scroll horizontal
* **Mensagem de voz:** Exibir "[Mensagem de voz]" seguido da transcricao (se disponível)

---

# Especificações técnicas

## Serviços

* `GET /api/v1/leads/{lead_id}/conversations` - Retorna historico de mensagens do lead
  * Suporta páginacao via cursor para conversas longas
  * Retorna no máximo 100 mensagens por requisicao
  * Ordenacao cronológica (mais antigas primeiro)

## Contrato da API

```json
GET /api/v1/leads/{lead_id}/conversations?cursor={next_cursor}

Response 200:
{
  "messages": [
    {
      "id": "string",
      "sender_type": "lead" | "assistant" | "broker",
      "sender_name": "string | null",
      "content": "string",
      "content_type": "text" | "voice" | "image",
      "timestamp": "ISO8601",
      "metadata": {
        "voice_transcription": "string | null"
      }
    }
  ],
  "págination": {
    "has_more": boolean,
    "next_cursor": "string | null"
  }
}

Response 401: Não autenticado
Response 403: Sem permissao para acessar este lead
Response 404: Lead não encontrado
Response 500: Erro interno do servidor
```

## Mudanças no modelo de dados

* [TBD @Eng] Confirmar se tabela de mensagens já existe com campos necessários
* [TBD @Eng] Verificar indexacao para queries por lead_id ordenadas por timestamp
* Campos obrigatórios: id, lead_id, sender_type, sender_name, content, content_type, timestamp, metadata

## Frontend

* Implementar lista virtualizada para performance em conversas longas
* Lazy loading de mensagens anteriores no scroll para cima
* Componente de bolha de chat reutilizavel
* Manter estado de scroll position ao carregar mais mensagens

## Segurança & privacidade

* Válidar que corretor autenticado tem permissao para acessar o lead específico
* Não logar conteúdo de mensagens (contém dados pessoais do lead)
* Sanitizar conteúdo de mensagens para prevencao de XSS antes de renderizar
* Entradas de audit log para acesso a conversas com: broker_id, lead_id, timestamp, action

---

# Critérios de aceite

* Ao acessar aba "Conversa", historico de mensagens é exibido em interface estilo chat
* Mensagens do lead sao exibidas a esquerda em bolhas cinza escuro (#333)
* Mensagens da IA sao exibidas a direita em bolhas laranja/coral com nome do assistente (ex: "Fe da Foxter")
* Mensagens do corretor sao exibidas a direita em bolhas laranja/coral com nome "Corretor Loft" ou nome do corretor
* Cada mensagem exibe timestamp no formato HH:MM AM/PM
* Mensagens sao exibidas em ordem cronológica (mais antigas primeiro, mais recentes por último)
* View faz auto-scroll para mensagem mais recente ao abrir a aba
* Quando não há mensagens, exibe estado vazio: "Nenhuma conversa registrada"
* Mensagens de voz exibem "[Mensagem de voz]" com transcricao quando disponível
* NFR (performance): Carregamento de até 100 mensagens completa em <2 segundos p95
* NFR (acessibilidade): Contraste de cores das bolhas atende WCAG AA (4.5:1); navegação por teclado funcional
* Analytics: Evento `lead_conversation_viewed` dispara com `{lead_id, broker_id, message_count, load_time_ms}`

---

# Observabilidade & Analytics

## Eventos

* `lead_conversation_viewed` props `{lead_id, broker_id, message_count, load_time_ms, timestamp}` trigger: ao carregar aba Conversa com sucesso
* `conversation_scroll_history` props `{lead_id, broker_id, scroll_depth_percentage, oldest_message_viewed_timestamp}` trigger: ao fazer scroll para mensagens anteriores (alem do fold inicial)
* `conversation_load_error` props `{lead_id, broker_id, error_code, error_message, timestamp}` trigger: quando API retorna erro ao carregar conversas
* `conversation_págination_loaded` props `{lead_id, broker_id, page_number, messages_loaded}` trigger: ao carregar página adicional de mensagens

## Dashboard (DataDog/Observabilidade)

* Taxa de visualizacao de conversas por corretor
* Tempo médio de carregamento de conversas (p50/p95/p99)
* Taxa de sucesso vs erro no carregamento
* Distribuição de tamanho de conversas (número de mensagens)
* Scroll depth médio (quanto do historico corretores leem)

## Alertas

* Taxa de erro no carregamento >5% em 5 minutos (page on-call)
* Latencia p95 >3 segundos por 10 minutos (investigar)
* Zero eventos de visualizacao por >2 horas durante horário comercial (investigar integração)

## Auditoria

* Logar acesso a conversas com: broker_id, lead_id, timestamp, ip_address, user_agent

---

# Plano de Rollout & Riscos

## Rollout

Feature flag `feature_lead_conversation_history` no frontend para habilitar/desabilitar aba Conversa

* **Fase 1:** Testar com contas internas da Loft em staging
* **Fase 2:** Habilitar para 2-3 imobiliárias piloto em producao
* **Fase 3:** Monitorar por 3 dias; se taxa de sucesso >98% e feedback positivo, expandir para 20% dos usuários
* **Fase 4:** Rollout 100% após 1 semana sem incidentes

## Rollback

* Passo 1: Desabilitar feature flag `feature_lead_conversation_history`
* Passo 2: Aba "Conversa" fica oculta/desabilitada na navegação
* Passo 3: Dados de conversas permanecem intactos no backend
* Passo 4: Investigar causa raiz e corrigir antes de re-habilitar

---

# Riscos

1. **Conversas muito longas impactam performance:** Leads com 500+ mensagens podem causar lentidao no carregamento → mitigar com lista virtualizada e páginacao por cursor
2. **Exposicao de PII:** Mensagens contém dados pessoais do lead → mitigar com controles de acesso rigorosos, não logar conteúdo de mensagens, sanitizacao XSS
3. **Dados de conversa incompletos:** Historico pode estar incompleto se houve falha na integração WhatsApp → mitigar com tratamento gracioso de dados ausentes, exibir mensagem informativa se detectado

---

# Questões em aberto

* [PM] Devemos exibir indicadores de leitura (checkmarks duplos) como no WhatsApp? (ate 10/01/2026)
* [PM] Qual o limite de historico de conversas a exibir? Toda a vida do lead ou últimos N meses? (ate 10/01/2026)
* [Eng] Qual a expectativa de tamanho máximo de conversa? Quantas mensagens tipicamente? (ate 08/01/2026)
* [Eng] Transcricoes de mensagens de voz já estão disponiveis na base de dados? (ate 08/01/2026)
* [Design] Input de mensagem deve estar visível mesmo desabilitado, ou devemos ocultar completamente? (ate 08/01/2026)

---

# Premissas

* Conversas sao armazenadas server-side durante a integração com WhatsApp e já estão disponiveis via API
* Mensagens de voz tem transcricoes pre-processadas disponiveis no campo metadata.voice_transcription
* Story 1 (Header & Tab Navigation) esta completa e funcional antes do inicio desta story
* Autenticação e autorização de corretores já existem e funcionam para acesso a leads
* Design system já possui componentes reutilizaveis para tabs, cards e estados de loading
* Limite de 100 mensagens por requisicao e adequado para performance; páginacao cobre conversas maiores
