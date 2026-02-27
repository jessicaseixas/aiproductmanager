<!-- jira: SLA-590 -->

# Conexao WhatsApp Business (Embedded Signup)

> Permite que administradores conectem sua conta de WhatsApp Business ao Qualifica Leads via fluxo Embedded Signup da Meta.

| | |
|---|---|
| **Status** | Planejado |
| **Jira** | [SLA-590](https://loftbr.atlassian.net/browse/SLA-590) |
| **Lançamento** | Abr/2026 |

---

## Problema

Para que o Qualifica Leads funcione, a imobiliária precisa conectar uma conta de WhatsApp Business. Sem essa conexão, não e possível receber e qualificar leads via WhatsApp.

## Solução

- Fluxo de Embedded Signup da Meta (login Facebook, criar WABA, vincular número)
- Callback de sucesso/erro após conclusao do fluxo
- Salvar dados da conexão no backend (WABA ID, número, etc)
- Exibir status da conexão na interface
- Fluxo guiado pelo comercial no MVP (usuário com número proprio pode tentar sozinho)

## Usuário

Administradores de imobiliárias que precisam conectar WhatsApp Business ao produto.

## Valor

- Habilita o funcionamento core do produto (qualificação via WhatsApp)
- Reduz fricao vs configuração manual no painel da Meta
- Permite rastrear status da conexão

## Dependências

- Nenhuma - feature necessaria para operacao do produto

## Requisitos

Ver [TICKET.md](./TICKET.md) para especificações detalhadas (a ser criado).
