<!-- jira: SLA-525 -->

# Cadastro e Login v1

> Permite que usuários acessem o backoffice do Qualifica Leads via Login Loft, com cadastro manual feito pela Squad.

| | |
|---|---|
| **Status** | Em desenvolvimento |
| **Jira** | [SLA-525](https://loftbr.atlassian.net/browse/SLA-525) |
| **Lançamento** | Fev/2026 |

---

## Problema

Para operar o backoffice standalone, usuários precisam se autenticar. Sem fluxo de login, não há como acessar o produto.

## Solução

- Cadastro manual de usuários e imobiliárias via endpoints (operado pela Squad)
- Integração com Login Loft para autenticação
- Primeiro acesso via fluxo de "Recuperar senha" do Login Loft
- Tela de cadastrar nova senha no backoffice
- Redirecionamento automático para área logada após cadastrar senha

## Usuário

Administradores de imobiliárias que contratam o Qualifica Leads Standalone.

## Valor

- Acesso seguro ao backoffice usando infraestrutura existente (Login Loft)
- Onboarding controlado pelo time comercial
- Base para futuras melhorias (self-service, corretores)

## Dependências

- Login Loft disponível e funcional
- Serviço de envio de e-mail configurado (para recuperação de senha)
- Processo comercial definido para solicitar cadastros

## Requisitos

Ver [TICKET.md](./TICKET.md) para especificações detalhadas.
