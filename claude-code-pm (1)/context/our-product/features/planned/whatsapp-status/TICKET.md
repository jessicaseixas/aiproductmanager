## Overview

* **Objetivo:** Exibir o status da conta de WhatsApp Business no backoffice, permitindo que administradores saibam se a integração está funcionando corretamente ou se há problemas que precisam de ação.
* **Quem é afetado:** Administradores de imobiliárias que precisam monitorar a saúde da integração com WhatsApp.
* **Comportamento atual:** N/A para standalone. Não há visibilidade sobre o status da conexão.
* **Comportamento desejado:** Admin vê card/seção com status da conexão (conectado/desconectado/erro), número vinculado, alertas de problemas e orientações para resolver.
* **Por que fazer isso agora:** Reduz chamados de suporte. Admin consegue identificar e resolver problemas proativamente. Faz parte do checklist de setup.
* **Links úteis:**
    * [PRD Back-office](../../../prds/backoffice-qualifica-leads.md)

---

## Definição de Pronto

* Critérios de aceitação completamente satisfeitos
* Testes automatizados adicionados para validação
* Integração testada em staging
* Eventos de analytics verificados em staging
* Card de status integrado ao checklist de setup
* Alertas exibindo corretamente para cenários de erro

---

## Escopo

### Dentro do escopo

* Card/seção mostrando status da conexão WhatsApp
* Exibir número conectado e nome do perfil
* Status: Conectado (verde), Desconectado (vermelho), Erro (amarelo)
* Alertas de problemas conhecidos:
  - Template não aprovado pela Meta
  - Pagamento pendente na Meta
  - Token expirado (precisa reconectar)
  - Qualidade da conta baixa (risco de bloqueio)
* Orientações/links para resolver cada problema
* Integração com checklist de setup

### Fora do escopo

* Fluxo de reconexão completo (usa Embedded Signup existente)
* Troubleshooting detalhado passo a passo
* Histórico de status/problemas
* Notificações push/email sobre problemas

---

## Especificação de UX + Comportamento

### Pontos de entrada

* Dashboard inicial (tela home) - card de status
* Menu de configurações > Status WhatsApp
* Checklist de setup - item "WhatsApp conectado"

### Componentes

**Card de Status (Dashboard)**

```
┌─────────────────────────────────────┐
│ 🟢 WhatsApp Conectado               │
│                                     │
│ +55 11 99999-9999                   │
│ Imobiliária ABC                     │
│                                     │
│ [Configurar perfil]  [Ver detalhes] │
└─────────────────────────────────────┘
```

**Card com Alerta**

```
┌─────────────────────────────────────┐
│ 🟡 WhatsApp - Ação necessária       │
│                                     │
│ +55 11 99999-9999                   │
│                                     │
│ ⚠️ Template pendente de aprovação   │
│    Aguarde aprovação da Meta ou     │
│    [verifique no painel]            │
│                                     │
│ [Ver detalhes]                      │
└─────────────────────────────────────┘
```

**Card Desconectado**

```
┌─────────────────────────────────────┐
│ 🔴 WhatsApp Desconectado            │
│                                     │
│ Conecte seu WhatsApp Business       │
│ para começar a qualificar leads     │
│                                     │
│ [Conectar agora]                    │
└─────────────────────────────────────┘
```

### Estados

* **Conectado (verde):** Tudo funcionando, sem alertas
* **Conectado com alerta (amarelo):** Funcionando, mas há problemas pendentes
* **Desconectado (vermelho):** Não há conexão ativa
* **Erro (vermelho):** Conexão existe mas não está funcional

### Tipos de Alerta

| Alerta | Severidade | Mensagem | Ação |
|--------|------------|----------|------|
| Template pendente | Baixa | "Template aguardando aprovação da Meta" | Link para painel Meta |
| Template rejeitado | Alta | "Template rejeitado. Verifique e reenvie." | Link para painel Meta |
| Pagamento pendente | Alta | "Pagamento pendente na Meta" | Link para painel Meta |
| Token expirado | Crítica | "Conexão expirada. Reconecte sua conta." | Botão reconectar |
| Qualidade baixa | Média | "Qualidade da conta baixa. Risco de bloqueio." | Link para boas práticas |
| Conta bloqueada | Crítica | "Conta bloqueada pela Meta" | Link para suporte |

---

## Especificações técnicas

### Serviços

* `GET /api/v1/whatsapp/status` — Retorna status completo da conexão

### Endpoint

```
GET /api/v1/whatsapp/status
Response 200:
{
  "connected": true,
  "status": "active", // active, warning, error, disconnected
  "phone_number": "+55 11 99999-9999",
  "display_name": "Imobiliária ABC",
  "waba_id": "123456789",
  "connected_at": "2026-01-10T14:30:00Z",
  "alerts": [
    {
      "type": "template_pending",
      "severity": "low", // low, medium, high, critical
      "message": "Template aguardando aprovação da Meta",
      "action_url": "https://business.facebook.com/...",
      "action_label": "Verificar no painel"
    }
  ],
  "health_check": {
    "last_check": "2026-01-14T10:00:00Z",
    "api_status": "ok",
    "message_delivery": "ok"
  }
}

Response 404: Nenhuma conexão encontrada
```

### Verificação de Saúde (Health Check)

Sistema deve verificar periodicamente (a cada 1h ou sob demanda):
- Token ainda válido (via Meta API)
- Status da conta na Meta
- Templates aprovados/pendentes/rejeitados
- Qualidade da conta (quality rating)

### Mudanças no modelo de dados

**Tabela: whatsapp_connections** (adicionar campos)
- last_health_check (timestamp)
- health_status (enum: ok, warning, error)
- quality_rating (enum: green, yellow, red, unknown)
- alerts_json (jsonb) - alertas ativos em formato JSON

**Tabela: whatsapp_alerts** (opcional, para histórico)
- id (UUID, PK)
- connection_id (UUID, FK)
- alert_type (string)
- severity (enum)
- message (string)
- resolved_at (timestamp, nullable)
- created_at (timestamp)

### Segurança & privacidade

* Não expor tokens ou dados sensíveis no endpoint de status
* Mascarar parcialmente número se necessário (ex: +55 11 9****-9999)
* Rate limit: 60 req/min por organização

---

## Critérios de aceite

* Card de status exibido no dashboard inicial
* Status "Conectado" (verde) quando tudo OK
* Status "Desconectado" (vermelho) quando não há conexão
* Status com alerta (amarelo) quando há problemas pendentes
* Número de telefone e nome do perfil exibidos corretamente
* Alertas exibidos com mensagem clara e link de ação
* Botão "Conectar" visível quando desconectado
* Botão "Reconectar" visível quando token expirado
* Integração com checklist de setup (marca como completo quando conectado)
* NFR (performance): Endpoint retorna em <500ms p95
* Analytics: Evento `WhatsApp Status Viewed` dispara ao visualizar
* Analytics: Evento `WhatsApp Alert Clicked` dispara ao clicar em ação do alerta

---

## Observabilidade & Analytics

### Eventos

| Evento | Descrição | Trigger | Properties |
|--------|-----------|---------|------------|
| `WhatsApp Status Viewed` | Admin visualizou status | Card ou página de status carrega | `status`, `has_alerts`, `alert_count` |
| `WhatsApp Alert Clicked` | Admin clicou em ação do alerta | Clique no link/botão do alerta | `alert_type`, `severity` |
| `WhatsApp Reconnect Started` | Admin iniciou reconexão | Clique em "Reconectar" | `previous_status` |

### Event Properties

| Property | Tipo | Descrição |
|----------|------|-----------|
| `status` | string | Status atual (active, warning, error, disconnected) |
| `has_alerts` | boolean | Se há alertas ativos |
| `alert_count` | number | Quantidade de alertas |
| `alert_type` | string | Tipo do alerta clicado |
| `severity` | string | Severidade do alerta |
| `previous_status` | string | Status antes de reconectar |

### Dashboard (DataDog)

* % de conexões por status (active, warning, error)
* Alertas mais frequentes por tipo
* Tempo médio para resolução de alertas
* Taxa de reconexões

### Alertas de Monitoramento

* >10% de conexões com erro → investigar problema sistêmico
* >5% de tokens expirados em 24h → verificar fluxo de refresh
* Aumento de alertas de qualidade baixa → revisar práticas de envio

---

## Plano de Rollout & Riscos

### Rollout

* **Fase 1:** Testar em staging com diferentes cenários de status
* **Fase 2:** Deploy junto com Embedded Signup
* **Fase 3:** Rollout 100%

### Rollback

1. Reverter deploy
2. Card de status não é exibido
3. Usuários usam painel da Meta para verificar status

---

## Riscos

1. **Health check sobrecarrega Meta API:** Muitas verificações podem causar rate limit → mitigar com cache e verificação sob demanda
2. **Alertas desatualizados:** Status pode mudar e não refletir imediatamente → exibir timestamp do último check
3. **Excesso de alertas:** Muitos alertas podem confundir → priorizar por severidade

---

## Questões em aberto

* [Design] Qual o layout do card de status? Link do Figma? - até [TBD]
* [Eng] Qual a frequência ideal do health check? - até [TBD]
* [Eng] Quais endpoints da Meta usar para verificar qualidade/templates? - até [TBD]

---

## Premissas

* Conexão WhatsApp pode ou não existir
* Meta API disponibiliza informações de status e qualidade
* Frequência de health check não causa rate limit
* Alertas têm ações claras que o usuário pode tomar
