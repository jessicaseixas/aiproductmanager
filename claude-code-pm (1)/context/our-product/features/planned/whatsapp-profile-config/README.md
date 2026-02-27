<!-- jira: SLA-591 -->

# Configuracao do Perfil WhatsApp

> Permite que administradores configurem o perfil do WhatsApp Business (nome, foto, descrição) diretamente no backoffice.

| | |
|---|---|
| **Status** | Planejado |
| **Jira** | [SLA-591](https://loftbr.atlassian.net/browse/SLA-591) |
| **Lançamento** | Abr/2026 |

---

## Problema

Hoje, para configurar o perfil do WhatsApp Business (foto, nome de exibicao, descrição), o usuário precisa acessar o painel da Meta. Isso gera fricao e dificulta o onboarding.

## Solução

- Formulário para editar nome de exibicao, foto do perfil e descrição
- Preview visual de como vai aparecer no WhatsApp (formato celular)
- Chamada as APIs da Meta para atualizar os dados
- Feedback de sucesso/erro após atualização

## Usuário

Administradores de imobiliárias que querem personalizar o perfil do WhatsApp.

## Valor

- Reduz fricao no onboarding (não precisa ir na Meta)
- Experiencia similar a concorrentes (ex: Lais.ai)
- Leads veem informacoes profissionais da imobiliária

## Dependências

- **Embedded Signup:** Conexao WhatsApp Business precisa estar ativa

## Requisitos

Ver [TICKET.md](./TICKET.md) para especificações detalhadas (a ser criado).
