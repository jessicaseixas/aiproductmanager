## Overview

* **Objetivo:** Permitir que administradores de imobiliárias conectem sua conta de WhatsApp Business ao Qualifica Leads através do fluxo Embedded Signup da Meta, habilitando o recebimento e qualificação de leads via WhatsApp.
* **Quem é afetado:** Administradores de imobiliárias que estão configurando o Qualifica Leads Standalone pela primeira vez.
* **Comportamento atual:** N/A - Nova funcionalidade. Não existe forma de conectar WhatsApp Business ao produto standalone.
* **Comportamento desejado:** Administrador inicia o fluxo de Embedded Signup, faz login no Facebook, cria/seleciona WABA, vincula número de telefone e o sistema salva os dados da conexão para uso pelo assistente de IA.
* **Por que fazer isso agora:** É pré-requisito para o funcionamento do produto. Sem conexão com WhatsApp Business, não é possível qualificar leads via WhatsApp.
* **Links úteis:**
    * [Meta Embedded Signup Docs](https://developers.facebook.com/docs/whatsapp/embedded-signup)
    * [PRD Back-office](../../../prds/backoffice-qualifica-leads.md)

---

## Definição de Pronto

* Critérios de aceitação completamente satisfeitos
* Testes automatizados adicionados para validação
* Integração testada em staging com conta Meta de teste
* Eventos de analytics verificados em staging com propriedades corretas
* Dashboard de monitoramento criado
* Documentação de suporte criada (manual para usuário)
* Feature flag configurada para controle de rollout

---

## Escopo

### Dentro do escopo

* Botão para iniciar fluxo de Embedded Signup
* Tela de instruções pré-fluxo (o que esperar, requisitos)
* Integração com SDK do Facebook para Embedded Signup
* Callback de sucesso: salvar dados da conexão (WABA ID, phone number ID, display name)
* Callback de erro: exibir mensagem apropriada e orientação
* Exibir status da conexão após conclusão (conectado/erro)
* Endpoint para receber e processar callback da Meta
* Armazenar tokens de acesso de forma segura

### Fora do escopo

* Compra de número de telefone (feito via suporte comercial)
* Configuração do perfil WhatsApp (foto, descrição) - ticket separado
* Configuração do assistente (apelido, nome imobiliária) - ticket separado
* Fluxo totalmente self-service (MVP é guiado pelo comercial)
* Configuração de método de pagamento na Meta (feito durante ativação guiada)

---

## Especificação de UX + Comportamento

### Pontos de entrada

* Menu de configurações > Conexão WhatsApp
* Checklist de setup na tela inicial (item "Conectar WhatsApp")

### Fluxo

1. Admin acessa seção de configuração do WhatsApp
2. Vê tela de instruções com requisitos:
   - "Você precisará de uma conta do Facebook Business"
   - "Tenha em mãos o número de telefone que será usado"
   - "O número deve estar no WhatsApp Business ou disponível para migração"
3. Clica em "Iniciar conexão"
4. SDK da Meta abre popup/modal do Embedded Signup
5. Admin faz login no Facebook (se não estiver logado)
6. Admin seleciona/cria conta Business
7. Admin cria/seleciona WABA (WhatsApp Business Account)
8. Admin vincula número de telefone
9. Admin configura método de pagamento na Meta (durante ativação guiada)
10. Meta retorna callback para nosso sistema
11. Sistema processa callback e salva dados
12. Admin vê tela de sucesso com status da conexão

### Estados

* **Não conectado:** Exibe botão "Conectar WhatsApp" com instruções
* **Conectando:** Loading durante fluxo do Embedded Signup
* **Sucesso:** Card verde com "WhatsApp conectado" + número vinculado
* **Erro (cancelado):** "Conexão cancelada. Clique para tentar novamente."
* **Erro (falha Meta):** "Não foi possível conectar. Erro: {mensagem}. Entre em contato com suporte."
* **Erro (token inválido):** "Sessão expirada. Clique para reconectar." → HTTP 401

---

## Especificações técnicas

### Serviços

* `POST /api/v1/whatsapp/embedded-signup/callback` — Recebe callback da Meta após Embedded Signup
* `GET /api/v1/whatsapp/connection/status` — Retorna status atual da conexão
* `POST /api/v1/whatsapp/connection/disconnect` — Desconecta conta (para reconexão)

### Callback da Meta

```json
POST /api/v1/whatsapp/embedded-signup/callback
Request (da Meta):
{
  "code": "authorization_code",
  "state": "organization_id_encoded"
}

Processamento:
1. Trocar code por access_token via Meta API
2. Obter WABA ID e phone number ID
3. Salvar dados na tabela whatsapp_connections

Response 200:
{
  "success": true,
  "connection_id": "uuid"
}
```

### Mudanças no modelo de dados

**Tabela: whatsapp_connections**
- id (UUID, PK)
- organization_id (UUID, FK, unique) - uma conexão por org
- waba_id (string, not null) - WhatsApp Business Account ID
- phone_number_id (string, not null)
- display_phone_number (string) - ex: "+55 11 99999-9999"
- business_name (string) - nome do business na Meta
- access_token (string, encrypted) - token de acesso da Meta
- token_expires_at (timestamp, nullable) - se token expira
- status (enum: active, disconnected, error)
- error_message (string, nullable) - última mensagem de erro
- connected_at (timestamp)
- disconnected_at (timestamp, nullable)
- created_at (timestamp)
- updated_at (timestamp)

### Segurança & privacidade

* Access token deve ser armazenado criptografado (AES-256)
* Não logar tokens ou códigos de autorização
* Válidar state parameter para prevenir CSRF
* Webhook da Meta deve validar assinatura (X-Hub-Signature-256)
* Audit log para conexões/desconexões com: organization_id, timestamp, status, ip_address

---

## Critérios de aceite

* Admin consegue iniciar fluxo de Embedded Signup a partir do backoffice
* Tela de instruções exibe requisitos antes de iniciar
* Popup/modal da Meta abre corretamente ao clicar "Iniciar conexão"
* Após conclusão do fluxo Meta, callback é recebido e processado
* Dados da conexão (WABA ID, phone number ID, display name) são salvos corretamente
* Status "Conectado" é exibido após sucesso com número vinculado
* Erro de cancelamento exibe mensagem apropriada com opção de retry
* Erro da Meta exibe mensagem descritiva e orienta contato com suporte
* NFR (performance): Callback processado em <3s p95
* NFR (segurança): Tokens armazenados criptografados; state parameter validado
* Analytics: Evento `Embedded Signup Started` dispara ao clicar "Iniciar conexão"
* Analytics: Evento `Embedded Signup Completed` dispara com `{waba_id, has_existing_number}`
* Analytics: Evento `Embedded Signup Failed` dispara com `{error_code, error_message}`

---

## Observabilidade & Analytics

### Eventos

| Evento | Descrição | Trigger | Properties |
|--------|-----------|---------|------------|
| `WhatsApp Setup Screen Viewed` | Admin visualizou tela de configuração | Tela de config WhatsApp carrega | - |
| `Embedded Signup Started` | Admin iniciou fluxo de conexão | Clique em "Iniciar conexão" | - |
| `Embedded Signup Completed` | Conexão realizada com sucesso | Callback processado com sucesso | `waba_id`, `has_existing_number`, `time_to_complete_seconds` |
| `Embedded Signup Failed` | Falha na conexão | Callback com erro ou cancelamento | `error_code`, `error_message`, `step_failed` |
| `Embedded Signup Cancelled` | Admin cancelou o fluxo | Fechou popup sem completar | `step_cancelled` |
| `WhatsApp Disconnected` | Admin desconectou conta | Clique em "Desconectar" | `reason` |

### Event Properties

| Property | Tipo | Descrição |
|----------|------|-----------|
| `waba_id` | string | ID da WhatsApp Business Account |
| `has_existing_number` | boolean | Se usou número existente ou novo |
| `time_to_complete_seconds` | number | Tempo total do fluxo |
| `error_code` | string | Código de erro da Meta ou interno |
| `error_message` | string | Mensagem de erro |
| `step_failed` | string | Em qual etapa falhou (login, waba, phone, payment) |
| `step_cancelled` | string | Em qual etapa cancelou |
| `reason` | string | Motivo da desconexão |

### Dashboard (DataDog/Observabilidade)

* Taxa de sucesso do Embedded Signup (completados/iniciados)
* Tempo médio para completar fluxo
* Distribuição de erros por tipo (error_code)
* Conexões ativas por período

### Alertas

* Taxa de erro >20% em 1 hora → alerta para investigar
* Zero conexões bem-sucedidas em 24h (horário comercial) → investigar
* Callbacks não processados >5/hora → possível problema de integração

---

## Plano de Rollout & Riscos

### Rollout

Feature flag `whatsapp_embedded_signup_enabled` para controle

* **Fase 1:** Testar com contas internas em staging
* **Fase 2:** Habilitar para 2-3 clientes piloto em produção (ativação guiada)
* **Fase 3:** Monitorar por 1 semana; se taxa de sucesso >80%, expandir
* **Fase 4:** Rollout 100% (sempre com ativação guiada no MVP)

### Rollback

1. Desabilitar feature flag `whatsapp_embedded_signup_enabled`
2. Conexões existentes continuam funcionando
3. Novos clientes aguardam correção
4. Re-habilitar após correção

---

## Riscos

1. **API da Meta instável:** Meta pode ter instabilidades que afetam o fluxo → mitigar com retry automático e mensagens claras de erro
2. **Usuário não completa fluxo:** Muitos passos podem causar abandono → mitigar com instruções claras e suporte guiado
3. **Token expira:** Access token pode expirar → mitigar com refresh automático ou alerta para reconexão
4. **Mudanças na API Meta:** Meta pode alterar fluxo → mitigar com monitoramento e testes regulares

---

## Questões em aberto

* [Eng] Qual SDK da Meta usar? (Facebook JS SDK, React SDK?) - até [TBD]
* [Eng] Como lidar com tokens de longa duração vs curta duração? - até [TBD]
* [Design] Qual o layout da tela de instruções pré-fluxo? Link do Figma? - até [TBD]

---

## Premissas

* Admin tem acesso a uma conta do Facebook Business ou pode criar
* Número de telefone está disponível para vincular (WhatsApp Business ou novo)
* Meta API está disponível e funcionando
* Fluxo será guiado pelo comercial no MVP (não totalmente self-service)
