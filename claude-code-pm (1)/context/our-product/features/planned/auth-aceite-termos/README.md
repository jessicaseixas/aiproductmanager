<!-- jira: SLA-556 -->

# Aceite de Termos de Uso

> Modal de boas-vindas e aceite dos termos de uso exibido no primeiro acesso após login.

| | |
|---|---|
| **Status** | Planejado |
| **Jira** | [SLA-556](https://loftbr.atlassian.net/browse/SLA-556) |
| **Lançamento** | Abr/2026 |

---

## Problema

Clientes chegavam na implantação sem entender o produto e depois cancelavam. Precisamos garantir que o usuário aceite os termos de uso e políticas de privacidade antes de utilizar a plataforma, tanto para compliance quanto para garantir ciência das condições.

## Solução

Modal em 2 etapas exibido sobre o fluxo de onboarding:

1. **Boas-vindas**: Mensagem de boas-vindas personalizada (nome do usuário) confirmando criação da conta
2. **Termos e condições**: Exibição dos termos completos com área de scroll e checkbox de aceite

Elementos da UI:
- Sidebar à esquerda com navegação entre etapas ("Boas-vindas" / "Termos e condições")
- Área de conteúdo à direita com texto e ações
- Checkbox: "Li e estou de acordo com os termos e condições de uso e com as políticas de privacidade"
- Botões: "Cancelar" e "Aceitar e fechar"

## Usuário

Administradores de imobiliárias no primeiro acesso após criar conta no Qualifica Leads Standalone.

## Valor

- Garantir aceite dos termos para compliance legal
- Registro de auditoria do aceite (timestamp, versão dos termos, IP)
- Boas-vindas humanizadas antes de exigir aceite formal
- Fluxo integrado ao onboarding sem redirecionamentos

## Dependências

- Cadastro e Login (SLA-551) - usuário precisa estar autenticado
- Termos de uso definidos pelo jurídico

## Métricas de Sucesso

| Métrica | Target | Descrição |
|---------|--------|-----------|
| Taxa de Aceite de Termos | > 95% | Usuários que completam o fluxo de aceite |
| Taxa de Conversão Etapa 1→2 | > 98% | Usuários que avançam de boas-vindas para termos |
| Taxa de Erro | < 1% | Falhas técnicas no registro do aceite |

## Requisitos

Ver [TICKET.md](./TICKET.md) para especificações detalhadas.
