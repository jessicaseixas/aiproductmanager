
# Integracao Chaves na Mao

## Overview

* **Objetivo:** Permitir que o Loft Qualifica Leads receba leads do portal Chaves na Mão quando imobiliárias receberem submissões de formulários dessa plataforma.
* **Quem é afetado:** Imobiliárias que anunciam imóveis no portal Chaves na Mão e querem seus leads qualificados pelo Loft Qualifica Leads.
* **Comportamento atual:** N/A (integração ainda não existe)
* **Comportamento desejado:** Quando um potêncial comprador/locatário preenche um formulário no portal Chaves na Mão e aquela origem de leads está configurada no backoffice do standalone para enviar leads pro Loft Qualifica Leads, o lead é automaticamente recebido e qualificado com IA.
* **Por que fazer isso agora:** Chaves na Mão é o terceiro portal com mais leads chegando ao ecossistema Loft (9% do volume total); a integração desbloqueia um segmento importante de clientes para a versão inicial standalone do produto.
* **Links úteis:**
    * Integradores parceiros: https://www.chavesnamao.com.br/integradores-parceiros/

---

# Definição de Pronto

* Critérios de aceitação completamente satisfeitos
* Testes automatizados adicionados para validação de webhook, parsing e idempotência
* Integração testada com ambiente de sandbox ou webhooks mock do Chaves na Mão
* Eventos de analytics verificados em staging com propriedades corretas
* Dashboard + alertas criados e verificados
* Clientes piloto recebendo e qualificando leads do Chaves na Mão com sucesso
* Documentação criada com instruções de setup da integração

---

# Escopo

## Dentro do escopo

* Receber chamadas de webhook/API do Chaves na Mão contendo dados de leads
* Criar endpoint(s) de API para aceitar submissões de leads do portal Chaves na Mão
* Válidar e fazer parse dos payloads recebidos de acordo com o schema do Chaves na Mão
* Armazenar leads recebidos no sistema Loft Qualifica Leads
* Mapear campos de lead do Chaves na Mão para o modelo de dados do Loft Qualifica Leads
* Rastrear eventos de analytics chave (lead recebido, sucesso/falha no processamento de lead)

## Fora do escopo

* Mapeamento de campos customizado por cliente (usar schema padrão para MVP)
* Deduplicação de leads entre múltiplos portais (melhoria futura)
* Integração de envio de imóveis para o portal (foco apenas em recebimento de leads)

---

# Especificação de UX + Comportamento

## Pontos de entrada

* **Externo:** Serviço de webhook/API do Chaves na Mão chama nossa API quando um formulário de lead é submetido

## Fluxo

1. Usuário preenche formulário de interesse em imóvel no portal Chaves na Mão
2. Serviço do Chaves na Mão envia dados do lead para endpoint da API do Loft Qualifica Leads (via webhook ou polling)
3. Sistema valida autenticação/assinatura da requisição
4. Sistema faz parse e mapeia campos do lead para formato interno
5. Lead é armazenado e entra no pipeline de qualificação
6. Sistema retorna 200 OK para confirmar recebimento
7. (Assíncrono) Processo de qualificação do lead começa

## Estados

* **Sucesso:** Lead recebido é armazenado; webhook/API retorna 200 OK
* **Erro (validação):** Payload inválido → retornar 400 Bad Request com detalhes do erro
* **Erro (auth):** Credenciais/assinatura invalidas → retornar 401 Unauthorized
* **Erro (sistema):** Falha no processamento → retornar 500 Internal Server Error; retry esperado

---

# Especificações técnicas

## Serviços

* Endpoint [TBD @Eng] — receber leads do Chaves na Mão (método HTTP e path a definir com base na documentação final)
* Endpoint deve ser idempotente (entregas duplicadas de webhook não devem criar leads duplicados)
* [TBD @Eng] Definir se integração será via webhook push ou polling da API deles

## Mudanças no modelo de dados

* Adicionar campo string `external_lead_id` para rastrear ID original do lead no portal (se não existir)
* Adicionar campo JSONB `raw_webhook_payload` para preservar dados originais para debugging (se não existir)
* Adicionar valor `chaves_na_mao` ao enum de `lead_source` para identificar origem

## Segurança & privacidade

* Válidar credenciais/assinaturas de acordo com documentação do Chaves na Mão [TBD @Eng confirmar método de autenticação]
* Não logar PII sensível (ex: telefones, emails, CPF)
* Entradas de audit log para todas as chamadas de webhook recebidas com origem, timestamp e resultado

---

# Critérios de aceite

* Endpoint de webhook/API aceita payloads válidos do Chaves na Mão e retorna 200 OK
* Leads são corretamente parseados e mapeados para o modelo de dados do Loft Qualifica Leads com todos os campos obrigatórios
* Entregas duplicadas (mesmo `external_lead_id`) não criam leads duplicados
* Payloads inválidos retornam 400 Bad Request com logging apropriado de erros (sem PII nos logs)
* Chamadas não autorizadas (credenciais/auth invalida) retornam 401 Unauthorized e são logadas
* NFR (performance): Processamento de webhook/API completa em <2 segundos p95
* NFR (confiabilidade): Endpoint tem 99.9% de uptime; requisições falhadas são logadas com alertas
* Segurança: Credenciais/assinaturas são validadas; requisições não autorizadas são rejeitadas e auditadas
* Analytics: Evento `lead_received` dispara com `{lead_source: 'chaves_na_mao', external_lead_id, client_id, success}`
* Analytics: Evento `lead_processing_failed` dispara com `{lead_source: 'chaves_na_mao', error_code}` em falha
* Integração testada end-to-end com 1–2 clientes piloto recebendo leads reais do Chaves na Mão

---

# Observabilidade & Analytics

## Eventos

* `lead_received` props `{lead_source: 'chaves_na_mao', external_lead_id, timestamp, client_id, success}` trigger: recebimento bem-sucedido de webhook/API
* `lead_processing_failed` props `{lead_source: 'chaves_na_mao', external_lead_id, error_code, error_message}` trigger: erro no processamento de webhook/API
* `webhook_auth_failed` props `{portal: 'chaves_na_mao', ip_address, timestamp}` trigger: falha na validação de autenticação

## Dashboard (DataDog)

* Taxa de ingestão de leads do Chaves na Mão (leads/dia)
* Taxa de sucesso e taxa de erro de webhook/API
* Latência de processamento de leads p50/p95/p99

## Alertas

* Taxa de falha de webhook/API >5% em 10 minutos (page on-call)
* Zero leads recebidos do Chaves na Mão por >2 horas durante horário comercial (investigar)
* Falhas de autenticação >10/hora (potêncial problema de segurança)

## Auditoria

* Logar todas as chamadas de webhook/API com: portal (chaves_na_mao), timestamp, tamanho do payload, resultado (sucesso/falha), client_id se aplicável

---

# Plano de Rollout & Riscos

## Rollout

Feature flag no backend para habilitar/desabilitar integração Chaves na Mão

* **Fase 1:** Testar com contas internas em staging
* **Fase 2:** Habilitar para 1–2 clientes piloto em produção
* **Fase 3:** Monitorar por 1 semana; se taxa de sucesso >95%, habilitar para todos os clientes
* **Fase 4:** Rollout 100%

## Rollback

* Desabilitar feature flag para parar de aceitar novas chamadas de webhook/API
* Leads existentes permanecem no sistema e continuam pelo pipeline de qualificação
* Re-habilitar flag após correção se necessário

---

# Riscos

1. **Confiabilidade de webhook/API Chaves na Mão:** Webhooks podem falhar ou atrasar → mitigar com lógica de retry e alertas de monitoramento
2. **Mudanças de schema:** Chaves na Mão pode mudar schema do payload sem aviso → mitigar preservando `raw_webhook_payload` para debugging e versionamento
3. **Leads duplicados:** Mesmo lead enviado múltiplas vezes → mitigar com chave de idempotência (`external_lead_id`)
4. **Documentação incompleta:** Documentação pública pode estar desatualizada → mitigar solicitando documentação atualizada ao suporte deles

---

# Questões em aberto

* \[PM\] Quais clientes devem ser priorizados para teste piloto? (até [TBD])
* \[Eng\] Integração será via webhook push ou polling da API? Confirmar com documentação oficial do Chaves na Mão (até [TBD])
* \[Eng\] Qual método de autenticação o Chaves na Mão utiliza? (token, assinatura, outro) (até [TBD])
* \[Eng\] Qual é o volume esperado de leads por dia do Chaves na Mão? (até [TBD])
* \[PM\] Solicitar documentação atualizada ao suporte do Chaves na Mão (até [TBD])

---

# Premissas

* Payloads do Chaves na Mão seguem schema documentado (a ser confirmado com documentação oficial atualizada)
* Webhooks/API calls são entregues em tempo quase real (<1 minuto da submissão do formulário)
* Dados de lead incluem campos mínimos obrigatórios: informações de contato, detalhes do imóvel, mensagem de interesse
* Portal fornece algum mecanismo de autenticação (token, assinatura ou similar) para validar requisições
