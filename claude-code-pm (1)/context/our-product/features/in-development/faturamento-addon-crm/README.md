<!-- jira: SLA-370 -->

# Faturamento (Add-on CRM)

> Sistema de cobrança pós-pago para clientes que usam o Qualifica Leads como add-on do Loft/CRM.

| | |
|---|---|
| **Status** | Em desenvolvimento |
| **Jira** | [SLA-370](https://loftbr.atlassian.net/browse/SLA-370), [SLA-377](https://loftbr.atlassian.net/browse/SLA-377), [SLA-378](https://loftbr.atlassian.net/browse/SLA-378), [SLA-379](https://loftbr.atlassian.net/browse/SLA-379) |
| **Lançamento** | Mar/2026 |

---

## Problema

Clientes do Loft/CRM que usam o Qualifica Leads precisam acompanhar seu consumo e pagar pelo uso. O modelo é pós-pago com preço por atendimento que diminui conforme o volume aumenta.

## Solução

O faturamento é composto por 4 versões incrementais:

| Versão | Descrição | Status |
|--------|-----------|--------|
| v1 | Controle de atendimentos executados no ciclo | ✅ Pronto |
| v2 | Precificação e histórico de consumo | ✅ Pronto |
| v3 | Fechamento da fatura com descontos comerciais | 🔄 Em desenvolvimento |
| v4 | Trava de limite com de-para volume e dinheiro | ✅ Pronto |

**Funcionalidades:**
- Tela de consumo no Loft/CRM mostrando atendimentos e valor do ciclo atual
- Histórico de consumo dos ciclos anteriores
- Função de preço com valor máximo e mínimo (preço por atendimento diminui com volume)
- Possibilidade de definir limite de atendimentos (trava)
- Integração com sistema de faturamento da Intranet

## Usuário

Administradores de imobiliárias clientes do Loft/CRM.

## Valor

- Transparência no consumo e custos
- Previsibilidade de gastos com opção de trava
- Cobrança automática junto com fatura do Loft/CRM

## Dependências

- Infraestrutura de qualificação existente
- Sistema de faturamento da Intranet (time CRM)
