# Overview

* **Objetivo:** Permitir que imobiliárias recebam leads gerados por campanhas de Facebook/Instagram Ads diretamente no Loft Qualifica Leads, iniciando qualificação automática via WhatsApp em segundos após o lead preencher o formulário do anúncio.
* **Quem é afetado:** Imobiliárias que investem em campanhas de mídia paga no Facebook/Instagram e utilizam o Loft Qualifica Leads (add-on CRM ou standalone).
* **Comportamento atual:** Leads de Facebook Ads precisam ser exportados manualmente ou integrados via ferramentas terceiras, causando atraso na qualificação e perda de oportunidades.
* **Comportamento desejado:** Leads submetidos em formulários de Facebook Lead Ads são automaticamente recebidos pelo Qualifica Leads, que inicia qualificação via WhatsApp em tempo real.
* **Por que fazer isso agora:**
  - Facebook/Instagram são canais importantes de geração de leads para imobiliárias brasileiras
  - Concorrentes (Lais.ai, Morada.ai) já oferecem integrações similares
  - Lançamento do standalone (Mar/2026) exige múltiplas fontes de leads
  - Integração já existe no Loft/CRM, podendo ser reaproveitada
* **Links úteis:**
    * [Documentação Facebook Lead Ads API](https://developers.facebook.com/docs/marketing-api/guides/lead-ads/)
    * [PRD Back-office Qualifica Leads](../../../prds/backoffice-qualifica-leads.md)
    * [Feature README](./README.md)

---

# Definição de Pronto

* Critérios de aceitação completamente satisfeitos
* Testes automatizados adicionados para validação (unitários + integração)
* Integração testada em staging com conta de teste do Facebook
* Eventos de analytics verificados em staging com propriedades corretas
* Dashboard + alertas criados e verificados no DataDog
* Documentação de setup para time de implantação criada
* Fluxo de configuração no back-office funcional (se aplicável)

---

# Escopo

## Dentro do escopo

* Integração com Facebook Lead Ads API via webhooks
* Recepção automática de leads submetidos em formulários de anúncios
* Mapeamento de campos do formulário Facebook para formato padrão do Qualifica Leads
* Validação de dados do lead (telefone válido, campos obrigatórios)
* Início automático de qualificação via WhatsApp após recebimento
* Suporte a múltiplas páginas/contas do Facebook por imobiliária
* Autenticação via Facebook Login (OAuth) para conectar páginas

## Fora do escopo

* Criação ou gestão de campanhas de Facebook Ads (usuário faz no Facebook)
* Integração com Instagram Direct Messages (apenas Lead Ads)
* Integração com Facebook Messenger (apenas Lead Ads)
* Relatórios de performance de campanhas (usuário consulta no Facebook)
* Sincronização bidirecional (apenas Facebook → Qualifica Leads)

---

# Especificação de UX + Comportamento

## Pontos de entrada

* **Configuração:** Back-office > Integrações > Facebook Ads > Conectar página
* **Recebimento:** Webhook do Facebook quando lead preenche formulário

## Fluxo de configuração

1. Usuário acessa Back-office > Integrações > Facebook Ads
2. Clica em "Conectar página do Facebook"
3. É redirecionado para Facebook Login (OAuth)
4. Autoriza acesso às páginas e Lead Ads
5. Seleciona qual(is) página(s) conectar ao Qualifica Leads
6. Sistema registra webhook no Facebook para cada página
7. Exibe confirmação de sucesso com páginas conectadas

## Fluxo de recebimento de lead

1. Lead preenche formulário de Lead Ad no Facebook/Instagram
2. Facebook envia webhook para endpoint do Qualifica Leads
3. Sistema valida assinatura do webhook (segurança)
4. Sistema extrai dados do lead do payload
5. Sistema mapeia campos para formato padrão (nome, telefone, email, etc.)
6. Sistema valida telefone (formato brasileiro válido)
7. Sistema cria lead no Qualifica Leads associado à imobiliária
8. Sistema inicia qualificação automática via WhatsApp
9. (Assíncrono) Lead é notificado e conversa começa

## Estados

* **Sucesso:** Lead criado e qualificação iniciada → retornar HTTP 200
* **Erro (validação):** Telefone inválido ou campo obrigatório ausente → retornar HTTP 400 com detalhes; lead não criado
* **Erro (auth):** Assinatura do webhook invalida → retornar HTTP 401; logar tentativa suspeita
* **Erro (duplicado):** Lead com mesmo telefone já existe em conversa ativa → retornar HTTP 200 (idempotente); não criar duplicado
* **Erro (sistema):** Falha interna → retornar HTTP 500; Facebook fará retry automático

---

# Especificações técnicas

## Serviços

* `POST /webhooks/facebook/leads` — Endpoint para receber webhooks do Facebook Lead Ads
* `GET /webhooks/facebook/verify` — Endpoint de verificação do webhook (challenge do Facebook)
* `POST /integrations/facebook/connect` — Iniciar fluxo OAuth para conectar página
* `GET /integrations/facebook/callback` — Callback do OAuth após autorização
* `DELETE /integrations/facebook/pages/{page_id}` — Desconectar página
* Rate limiting: 1000 req/min por imobiliária (alinhado com limites do Facebook)

## Mudanças no modelo de dados

* Adicionar tabela `facebook_page_connections` com campos:
  - `id` (UUID)
  - `organization_id` (FK para imobiliária)
  - `page_id` (string, ID da página no Facebook)
  - `page_name` (string)
  - `access_token` (string, criptografado)
  - `webhook_subscribed` (boolean)
  - `created_at`, `updated_at`
* Adicionar campo `source` = 'facebook_ads' na tabela de leads
* Adicionar campo `source_metadata` (JSON) para armazenar dados originais do Facebook

## Segurança & privacidade

* Válidar assinatura SHA256 do webhook usando app secret do Facebook
* Access tokens armazenados criptografados (AES-256)
* Não logar PII sensível (telefones, emails) em logs de aplicação
* Tokens do Facebook têm validade; implementar refresh automático
* Audit log para: conexão de página, desconexão, falhas de autenticação

---

# Critérios de aceite

* Leads submetidos em formulários de Facebook Lead Ads são recebidos e processados em <30 segundos
* Campos do formulário são corretamente mapeados para formato padrão do Qualifica Leads
* Leads com telefone inválido são rejeitados com erro 400 e não iniciam qualificação
* Webhooks com assinatura invalida são rejeitados com erro 401 e logados
* Leads duplicados (mesmo telefone em conversa ativa) não criam nova conversa (idempotência)
* Múltiplas páginas podem ser conectadas por uma mesma imobiliária
* Desconectar página remove webhook e para de receber leads daquela página
* NFR (performance): Processamento de webhook completa em <2 segundos p95
* NFR (confiabilidade): Endpoint de webhook tem 99.9% de uptime; falhas são logadas com alertas
* Segurança: Tokens são armazenados criptografados; requisições sem assinatura valida são rejeitadas
* Analytics: Evento `facebook_lead_received` dispara com `{organization_id, page_id, lead_id, source}`
* Analytics: Evento `facebook_lead_error` dispara com `{organization_id, error_code, error_message}` em falha

---

# Observabilidade & Analytics

## Eventos

* `facebook_lead_received` props `{organization_id, page_id, lead_id, form_id, timestamp}` trigger: Lead recebido e processado com sucesso
* `facebook_lead_error` props `{organization_id, page_id, error_code, error_message, timestamp}` trigger: Erro no processamento do lead
* `facebook_page_connected` props `{organization_id, page_id, page_name, timestamp}` trigger: Página conectada com sucesso
* `facebook_page_disconnected` props `{organization_id, page_id, timestamp}` trigger: Página desconectada
* `facebook_webhook_auth_failed` props `{ip_address, timestamp, reason}` trigger: Falha na validação de assinatura

## Dashboard (DataDog)

* Taxa de leads recebidos por hora/dia (por imobiliária e total)
* Taxa de sucesso vs erro no processamento
* Latência de processamento p50/p95/p99
* Número de páginas conectadas por imobiliária
* Volume de leads por página/formulário

## Alertas

* Taxa de erro >5% em 5 minutos → page on-call
* Zero leads recebidos por >4 horas durante horário comercial (8h-20h) → investigar
* Latência p95 >5 segundos → investigar degradação
* Falhas de autenticação >10/hora → potêncial ataque, investigar

## Auditoria

* Logar conexão/desconexão de páginas com: organization_id, page_id, user_id, timestamp, resultado
* Logar falhas de autenticação com: ip_address, timestamp, payload_hash (sem PII)

---

# Plano de Rollout & Riscos

## Rollout

Feature flag `facebook_ads_integration_enabled` no backend para habilitar/desabilitar integração

* **Fase 1:** Testar com conta interna da Loft em staging (1 semana)
* **Fase 2:** Habilitar para 2-3 imobiliárias piloto em produção (1 semana)
* **Fase 3:** Monitorar por 1 semana; se taxa de sucesso >95%, habilitar para todas imobiliárias do standalone
* **Fase 4:** Rollout para clientes add-on CRM (se aplicável)

## Rollback

* Desabilitar feature flag `facebook_ads_integration_enabled`
* Leads já recebidos permanecem no sistema e continuam qualificação normalmente
* Novos leads do Facebook não serão processados até reabilitação
* Páginas conectadas mantêm conexão; webhook apenas não processa

---

# Riscos

1. **Rate limiting do Facebook:** API tem limites de requisições → mitigar com cache de tokens e backoff exponencial em retries
2. **Mudanças na API do Facebook:** Facebook pode deprecar endpoints → mitigar com monitoramento de changelogs e versionamento
3. **Tokens expirados:** Access tokens têm validade limitada → mitigar com refresh automático e alertas de tokens próximos de expirar
4. **Dados incompletos:** Formulários podem não ter telefone → mitigar com validação e rejeição clara; orientar imobiliárias sobre campos obrigatórios

---

# Questões em aberto

* [Eng] Qual o limite de páginas que uma imobiliária pode conectar? (até 17/Jan)
* [Eng] Reaproveitar implementação existente do Loft/CRM ou criar nova? (até 17/Jan)
* [PM] Precisa de UI no back-office para configuração ou será feito manualmente pelo time de implantação? (até 20/Jan)
* [Comercial] Quais imobiliárias piloto para Fase 2? (até 24/Jan)

---

# Premissas

* Facebook Lead Ads API permanece estável e disponível
* Imobiliárias já possuem páginas do Facebook configuradas com Lead Ads
* Formulários de Lead Ads incluem campo de telefone (obrigatório para qualificação via WhatsApp)
* Implementação será baseada na integração já existente no Loft/CRM
* Leads recebidos seguem o mesmo fluxo de qualificação dos demais canais
