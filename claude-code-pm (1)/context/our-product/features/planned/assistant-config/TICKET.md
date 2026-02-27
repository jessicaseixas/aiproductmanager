## Overview

* **Objetivo:** Permitir que administradores definam como o assistente de IA se apresenta nas conversas com leads, personalizando o apelido do assistente e o nome da imobiliária.
* **Quem é afetado:** Administradores de imobiliárias e, indiretamente, os leads que conversam com o assistente.
* **Comportamento atual:** N/A para standalone. No CRM Loft, configuração é feita em outro lugar.
* **Comportamento desejado:** Admin acessa configurações, define apelido (ex: "Ana") e nome da imobiliária. Assistente usa esses dados na mensagem inicial: "Olá! Sou a Ana, assistente da Imobiliária ABC."
* **Por que fazer isso agora:** Personalização básica necessária para que o assistente represente corretamente cada imobiliária. Sem isso, todas as conversas seriam genéricas.
* **Links úteis:**
    * [PRD Back-office](../../../prds/backoffice-qualifica-leads.md)

---

## Definição de Pronto

* Critérios de aceitação completamente satisfeitos
* Testes automatizados adicionados para validação
* Integração testada em staging
* Eventos de analytics verificados em staging
* Preview da mensagem inicial funcionando
* Assistente de IA usando configurações corretamente

---

## Escopo

### Dentro do escopo

* Campo para definir apelido do assistente (como ele se identifica)
* Campo para definir nome da imobiliária
* Preview de como ficará a mensagem inicial
* Salvar configurações no backend
* Assistente de IA utilizar configurações nas conversas

### Fora do escopo

* Configuração do perfil WhatsApp (foto, descrição) - ticket separado
* Personalização avançada de tom de voz
* Múltiplos assistentes por imobiliária
* Configuração de horário de atendimento
* Regras de qualificação customizadas

---

## Especificação de UX + Comportamento

### Pontos de entrada

* Menu de configurações > Assistente
* Checklist de setup na tela inicial (item "Configurar assistente")

### Fluxo

1. Admin acessa seção de configuração do assistente
2. Vê formulário com campos:
   - Apelido do assistente (ex: "Ana", "Julia", "Carlos")
   - Nome da imobiliária (ex: "Imobiliária ABC", "Foxter Cia")
3. Abaixo do formulário, preview da mensagem inicial:
   - "Olá! Sou a {apelido}, assistente da {imobiliária}. Como posso ajudar?"
4. Preview atualiza em tempo real conforme admin digita
5. Admin clica em "Salvar"
6. Sistema salva configurações
7. Exibe toast de sucesso

### Estados

* **Carregando:** Skeleton enquanto busca configurações atuais
* **Editando:** Formulário habilitado com valores atuais ou defaults
* **Salvando:** Loading no botão, campos desabilitados
* **Sucesso:** Toast "Configurações salvas!"
* **Erro (validação):** Mensagens inline nos campos inválidos
* **Erro (sistema):** "Não foi possível salvar. Tente novamente."

### Valores padrão

* Apelido: "Assistente" (se não configurado)
* Nome imobiliária: Usar nome fantasia da organização (cadastro)

---

## Especificações técnicas

### Serviços

* `GET /api/v1/assistant/config` — Retorna configuração atual do assistente
* `PUT /api/v1/assistant/config` — Atualiza configuração do assistente

### Endpoints

```
GET /api/v1/assistant/config
Response 200:
{
  "assistant_nickname": "Ana",
  "company_name": "Imobiliária ABC",
  "greeting_message_preview": "Olá! Sou a Ana, assistente da Imobiliária ABC. Como posso ajudar?"
}
```

```
PUT /api/v1/assistant/config
Request:
{
  "assistant_nickname": "string (2-50 chars)",
  "company_name": "string (2-100 chars)"
}

Response 200:
{
  "success": true,
  "updated_at": "timestamp"
}

Response 400: Validação falhou
```

### Mudanças no modelo de dados

**Tabela: organizations** (adicionar campos ou criar tabela separada)

Opção A - Adicionar à tabela organizations:
- assistant_nickname (string, default "Assistente")
- assistant_company_name (string, nullable) - se null, usa trade_name

Opção B - Nova tabela assistant_config:
- id (UUID, PK)
- organization_id (UUID, FK, unique)
- nickname (string, not null, default "Assistente")
- company_name (string, nullable)
- created_at (timestamp)
- updated_at (timestamp)

> Recomendação: Opção A é mais simples para MVP. Opção B se houver expectativa de mais configurações.

### Segurança & privacidade

* Válidar tamanho dos campos
* Sanitizar inputs (prevenir XSS)
* Apenas admins podem alterar configurações
* Audit log para alterações

---

## Critérios de aceite

* Admin consegue acessar tela de configuração do assistente
* Admin consegue definir apelido do assistente (2-50 caracteres)
* Admin consegue definir nome da imobiliária (2-100 caracteres)
* Preview da mensagem inicial atualiza em tempo real
* Validação inline exibe erros para campos inválidos
* Ao salvar, configurações são persistidas no banco
* Toast de sucesso é exibido após salvar
* Assistente de IA usa apelido e nome nas conversas
* Se não configurado, usa valores padrão ("Assistente" + nome fantasia)
* NFR (performance): Salvar completa em <1s p95
* Analytics: Evento `Assistant Config Screen Viewed` dispara ao acessar tela
* Analytics: Evento `Assistant Config Updated` dispara com `{nickname_changed, company_changed}`

---

## Observabilidade & Analytics

### Eventos

| Evento | Descrição | Trigger | Properties |
|--------|-----------|---------|------------|
| `Assistant Config Screen Viewed` | Admin visualizou tela de config | Tela carrega | - |
| `Assistant Config Updated` | Admin salvou configurações | Clique em Salvar com sucesso | `nickname_changed`, `company_changed`, `is_first_config` |
| `Assistant Config Update Failed` | Falha ao salvar | Erro ao salvar | `error_code` |

### Event Properties

| Property | Tipo | Descrição |
|----------|------|-----------|
| `nickname_changed` | boolean | Se o apelido foi alterado |
| `company_changed` | boolean | Se o nome da empresa foi alterado |
| `is_first_config` | boolean | Se é a primeira vez configurando |
| `error_code` | string | Código de erro (validation, server_error) |

### Dashboard

* % de organizações com assistente configurado vs padrão
* Apelidos mais usados (para insights de produto)
* Taxa de alteração das configurações

---

## Plano de Rollout & Riscos

### Rollout

* **Fase 1:** Testar em staging
* **Fase 2:** Deploy junto com outras configurações do backoffice
* **Fase 3:** Rollout 100%

### Rollback

1. Reverter deploy
2. Assistente usa valores padrão
3. Dados salvos permanecem para quando reativar

---

## Riscos

1. **Valores inapropriados:** Admin pode colocar textos inadequados → mitigar com validação de caracteres especiais e review manual se necessário
2. **Assistente não usa config:** Bug na integração → mitigar com testes E2E

---

## Questões em aberto

* [Design] Qual o layout da tela de configuração? Link do Figma? - até [TBD]
* [Eng] Usar tabela separada ou campos na tabela organizations? - até [TBD]
* [PM] Há limite de caracteres específico para o greeting message? - até [TBD]

---

## Premissas

* Organização já foi criada
* Apenas admins podem configurar
* Assistente de IA já tem mecanismo para buscar e usar essas configurações
* Valores padrão são suficientes para funcionamento inicial
