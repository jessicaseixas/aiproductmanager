
# Integracao Portais OLX

## Overview

Objetivo: Permitir que o Loft Qualifica Leads receba leads dos portais do Grupo OLX (OLX, Viva Real, ZAP Imóveis) quando imobiliárias receberem submissões de formulários dessas plataformas.

Quem é afetado: Imobiliárias que anunciam imóveis nos portais do Grupo OLX e querem seus leads qualificados pelo Loft Qualifica Leads.

Comportamento atual: N/A (versão standalone ainda não existe)

Comportamento desejado: Quando um potêncial comprador/locatário preenche um formulário nos portais do Grupo OLX e aquela origem de leads (OLX, Viva Real ou ZAP) está configurada no backoffice do standalone para enviar leads pro Loft Qualifica Leads, o lead é automaticamente recebido e qualificado com IA.

Por que é prioritário: Portais do Grupo OLX (OLX, Viva Real, ZAP Imóveis) são grandes fontes de leads no mercado imobiliário brasileiro; a integração desbloqueia um segmento chave de clientes para a versão inicial standalone.

Links úteis: 

Documentação técnica: https://developers.grupozap.com/webhooks/integration_leads.html#envio-dos-leads 

Prova de conceito: <TBD @Germano da Silva Dos Santos >

Definição de Pronto

Critério de aceitação completamente satisfeito

Testes automatizados adicionados para validação de webhook, parsing e idempotência

Integração testada com sandbox do Grupo OLX ou webhooks mock

Eventos de analytics verificados em staging com propriedades corretas

Dashboard + alertas criados e verificados

Clientes piloto recebendo e qualificando leads dos portais do Grupo OLX com sucesso

Documentação criada com instruções de setup da integração

Escopo

Dentro do escopo

Receber chamadas de webhook dos serviços do Grupo OLX contendo dados de leads

Criar endpoint(s) de API para aceitar submissões de leads do OLX, Viva Real e ZAP Imóveis

Válidar e fazer parse dos payloads de webhook recebidos de acordo com o schema do Grupo OLX

Armazenar leads recebidos no sistema Loft Qualifica Leads

Mapear campos de lead do Grupo OLX para o modelo de dados do Loft Qualifica Leads

Rastrear eventos de analytics chave (lead recebido, sucesso/falha no processamento de lead)

Fora do escopo

Sincronização bidirecional (enviar dados de volta aos portais do Grupo OLX)

Mapeamento de campos customizado por cliente (usar schema padrão OLX para MVP)

Deduplicação de leads entre múltiplos portais (melhoria futura)

Especificação de UX + Comportamento

Pontos de entrada

Externo: Serviços de webhook do Grupo OLX chamam nossa API quando um formulário de lead é submetido

Fluxo

Usuário preenche formulário de interesse em imóvel no OLX, Viva Real ou ZAP Imóveis

Serviço de webhook do Grupo OLX envia dados do lead para endpoint da API do Loft Qualifica Leads

Sistema valida assinatura/autenticação do webhook

Sistema faz parse e mapeia campos do lead para formato interno

Lead é armazenado e entra no pipeline de qualificação

Sistema retorna 200 OK para confirmar recebimento

(Assíncrono) Processo de qualificação do lead começa

Estados

Sucesso: Lead recebido é armazenado; webhook retorna 200 OK

Erro (validação): Payload inválido → retornar 400 Bad Request com detalhes do erro

Erro (auth): Assinatura/credenciais invalidas → retornar 401 Unauthorized

Erro (sistema): Falha no processamento → retornar 500 Internal Server Error; retry esperado

Especificações técnicas

Serviços

Endpoint TBD @Germano da Silva Dos Santos  — receber leads do OLX

Endpoint TBD @Germano da Silva Dos Santos  — receber leads do Viva Real

Endpoint TBD @Germano da Silva Dos Santos  — receber leads do ZAP Imóveis

Todos os endpoints devem ser idempotentes (entregas duplicadas de webhook não devem criar leads duplicados)

Mudanças no modelo de dados

Adicionar campo string external_lead_id para rastrear ID original do lead no portal

Adicionar campo JSONB raw_webhook_payload para preservar dados originais para debugging

Segurança & privacidade

Válidar assinaturas de webhook de acordo com documentação do Grupo OLX

Não logar PII sensível (ex: telefones, emails)

Entradas de audit log para todas as chamadas de webhook recebidas com origem, timestamp e resultado

Critérios de aceite

Endpoint de webhook aceita payloads válidos do OLX, Viva Real e ZAP Imóveis e retorna 200 OK

Leads são corretamente parseados e mapeados para o modelo de dados do Loft Qualifica Leads com todos os campos obrigatórios

Entregas duplicadas de webhook (mesmo external_lead_id) não criam leads duplicados

Payloads inválidos retornam 400 Bad Request com logging apropriado de erros (sem PII nos logs)

Chamadas de webhook não autorizadas (assinatura/auth invalida) retornam 401 Unauthorized e são logadas

NFR (performance): Processamento de webhook completa em <2 segundos p95

NFR (confiabilidade): Endpoint de webhook tem 99.9% de uptime; requisições falhadas são logadas com alertas

Segurança: Assinaturas de webhook são validadas; requisições não autorizadas são rejeitadas e auditadas

Analytics: Evento lead_received dispara com {lead_source, external_lead_id, portal, success}

Analytics: Evento lead_processing_failed dispara com {lead_source, error_code, portal} em falha

Integração testada end-to-end com 1–2 clientes piloto recebendo leads reais dos portais do Grupo OLX

Observabilidade & Analytics

Eventos

lead_received props {lead_source, external_lead_id, portal, timestamp, client_id} trigger: recebimento bem-sucedido de webhook

lead_processing_failed props {lead_source, external_lead_id, portal, error_code, error_message} trigger: erro no processamento de webhook

webhook_auth_failed props {portal, ip_address, timestamp} trigger: falha na validação de autenticação/assinatura

Dashboard (DataDog)

Taxa de ingestão de leads do Grupo OLX (leads/dia por portal: OLX, Viva Real, ZAP Imóveis)

Taxa de sucesso e taxa de erro de webhook por portal

Latência de processamento de leads p50/p95/p99 por portal

Alertas

Taxa de falha de webhook >5% em 10 minutos (page on-call)

Zero leads recebidos de qualquer portal por >2 horas durante horário comercial (investigar)

Falhas de autenticação de webhook >10/hora (potêncial problema de segurança)

Auditoria

Logar todas as chamadas de webhook com: portal, timestamp, tamanho do payload, resultado (sucesso/falha), client_id se aplicável

Plano de Rollout & Riscos

Rollout

Feature flag no backend para habilitar/desabilitar integrações do Grupo OLX

Fase 1: Testar com contas internas em staging

Fase 2: Habilitar para 1–2 clientes piloto em produção

Fase 3: Monitorar por 1 semana; se taxa de sucesso >95%, habilitar para todos os clientes

Fase 4: Rollout 100%

Rollback

Desabilitar feature flag para parar de aceitar novas chamadas de webhook

Leads existentes permanecem no sistema e continuam pelo pipeline de qualificação

Re-habilitar flag após correção se necessário

Riscos

Confiabilidade de webhook OLX: Webhooks podem falhar ou atrasar → mitigar com lógica de retry e alertas de monitoramento

Mudanças de schema: OLX pode mudar schema do payload de webhook sem aviso → mitigar preservando raw_webhook_payload para debugging e versionamento

Leads duplicados: Mesmo lead enviado múltiplas vezes → mitigar com chave de idempotência (external_lead_id)

Questões em aberto

[PM] Quais clientes devem ser priorizados para teste piloto? (até [TBD])

[Eng] Qual é o volume esperado de leads por dia dos portais do Grupo OLX? (até [TBD])

Premissas

Payloads de webhook do Grupo OLX seguem o schema documentado em https://developers.grupozap.com/webhooks/integration_leads.html#envio-dos-leads

Webhooks são entregues em tempo quase real (<1 minuto da submissão do formulário)

Dados de lead incluem campos mínimos obrigatórios: informações de contato, detalhes do imóvel, mensagem de interesse
