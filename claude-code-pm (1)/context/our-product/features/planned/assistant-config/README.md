<!-- jira: SLA-592 -->

# Configuracao do Assistente

> Permite que administradores definam como o assistente de IA se apresenta nas conversas com leads.

| | |
|---|---|
| **Status** | Planejado |
| **Jira** | [SLA-592](https://loftbr.atlassian.net/browse/SLA-592) |
| **Lançamento** | Abr/2026 |

---

## Problema

O assistente de IA precisa se apresentar de forma personalizada para cada imobiliária. Sem configuração, todas as conversas teriam a mesma apresentacao generica.

## Solução

- Campo para definir apelido do assistente (ex: "Ana", "Julia")
- Campo para definir nome da imobiliária
- Dados usados na mensagem inicial: "Ola! Sou a [apelido], assistente da [imobiliária]"
- Salvar configuracoes no backend

## Usuário

Administradores de imobiliárias que querem personalizar a experiencia do lead.

## Valor

- Experiencia personalizada para cada imobiliária
- Leads sabem com quem estao falando
- Configuracao simples e rapida

## Dependências

- Nenhuma - configuração interna do sistema (independente do WhatsApp)

## Requisitos

Ver [TICKET.md](./TICKET.md) para especificações detalhadas (a ser criado).
