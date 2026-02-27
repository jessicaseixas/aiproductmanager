<!-- jira: none -->

# Distribuicao de Leads sem Resposta

> Leads que param de responder sao automaticamente transferidos para corretores.

| | |
|---|---|
| **Status** | Produção |
| **Jira** | - |
| **Lançamento** | Out/2024 |

---

## Problema

Leads podem parar de responder durante a qualificação automatica. Sem um mecanismo de timeout, ficam "travados" indefinidamente no assistente.

## Solução

- Timeout de 60 minutos sem resposta
- Tempo contabilizado apenas em horario comercial (6h-20h)
- Transferencia automatica para corretor humano
- Lead pode retomar conversa com assistente se voltar a responder

## Usuário

Gestores de operacao que precisam garantir que nenhum lead fique sem atendimento.

## Valor

- Nenhum lead fica esquecido no sistema
- Corretor pode tentar contato humano com lead desengajado
- Fluxo operacional previsível e controlado

## Dependências

Integracao Loft CRM (para distribuição ao corretor).
