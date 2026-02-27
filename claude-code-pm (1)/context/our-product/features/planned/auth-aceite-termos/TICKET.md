# Overview

* **Objetivo:** Garantir que o usuário aceite os termos de uso e políticas de privacidade antes de utilizar a plataforma, para compliance legal e registro de auditoria.
* **Quem é afetado:** Administradores de imobiliárias no primeiro acesso ao Qualifica Leads Standalone.
* **Comportamento atual:** N/A - Nova funcionalidade. Após fazer login, usuário é redirecionado diretamente para o fluxo de onboarding.
* **Comportamento desejado:** Após fazer login pela primeira vez, usuário vê modal de boas-vindas seguido de termos de uso que deve aceitar para continuar.
* **Por que fazer isso agora:** Precisamos garantir aceite formal dos termos para compliance legal e ter registro de auditoria de quando e por quem os termos foram aceitos.
* **Detalhamento técnico:** [docs/tickets/SLA-556.md](https://github.com/loft-br/qualifica-leads/blob/main/docs/tickets/SLA-556.md)
* **Figma/Design:** [Qualifica Leads - Standalone](https://www.figma.com/design/3iXlzrSi8RJEt8Ae52z1Kq/Qualifica-Leads---Standalone?node-id=315-1121)
* **Links úteis:**
    * [PRD: backoffice-qualifica-leads.md](../../../prds/backoffice-qualifica-leads.md)
    * Termos de Uso: [TBD @Legal]

---

# Definição de Pronto

[ ] Critérios de aceitação completamente satisfeitos
[ ] Testes unitários com cobertura > 80%
[ ] Testes de integração para APIs
[ ] Teste E2E do fluxo completo (criar org -> aceitar termos -> dashboard)
[ ] Integração testada em staging
[ ] Eventos de analytics verificados em staging com propriedades corretas
[ ] Dashboard de métricas criado e verificado
[ ] Alertas configurados e testados
[ ] Code review aprovado
[ ] QA sign-off
[ ] Deploy em staging validado

---

# Escopo

## Dentro do escopo

* Modal de boas-vindas (etapa 1) com mensagem personalizada usando nome do usuário
* Modal de termos e condições (etapa 2) com texto completo dos termos em área com scroll
* Sidebar de navegação entre etapas ("Boas-vindas" / "Termos e condições")
* Checkbox de aceite: "Li e estou de acordo com os termos e condições de uso e com as políticas de privacidade"
* Botão "Aceitar e fechar" (habilitado apenas após marcar checkbox)
* Botão "Cancelar" (volta para etapa anterior ou fecha modal/logout)
* Registro de auditoria do aceite (compliance)
* API para registrar e consultar aceite

## Fora do escopo

* Calculadora de custos (removida do escopo)
* Edição dos termos pelo usuário
* Aceite parcial (deve aceitar tudo ou nada)
* Assinatura digital avançada (ex: DocuSign)
* Notificação quando termos forem atualizados (versão futura)
* Re-aceite de termos atualizados (versão futura)

---

# Especificação de UX + Comportamento

## Pontos de entrada

* Exibição automática do modal no primeiro acesso após login (termos não aceitos)
* Se usuário tentar acessar qualquer rota e termos não aceitos, modal é exibido

## Layout do Modal

**Estrutura:**
- Modal centralizado (840x420px no desktop)
- Overlay escuro (40% opacidade) sobre a tela de onboarding
- Sidebar à esquerda (260px) com navegação entre etapas
- Área de conteúdo à direita (580px) com texto e ações
- Border radius: 12px
- Sombra: Elevation/xl

**Sidebar:**
- Fundo branco com separador à direita
- Indicador de etapa ativa (barra laranja 4px à esquerda)
- Etapas: "Boas-vindas" / "Termos e condições"

## Fluxo

### Etapa 1: Boas-vindas
1. Usuário faz login pela primeira vez (SLA-551)
2. Sistema verifica se termos foram aceitos via `GET /api/v1/organizations/{org_id}/terms-acceptance`
3. Se não aceito, exibe modal de boas-vindas sobre a tela de onboarding
4. Modal exibe ilustração no topo e mensagem: "[Nome], sua conta foi criada com sucesso!"
5. Texto: "Seja muito bem vindo! Você já pode acessar o Qualifica Leads e explorar nossas melhores soluções para você e seus clientes, após aceitar os nossos termos de uso."
6. Botão "Próximo" → avança para etapa 2

### Etapa 2: Termos e condições
7. Modal exibe título "Termos e condições de uso"
8. Área com scroll exibindo texto completo dos termos (máx 300px altura visível)
9. Scrollbar customizada à direita (cinza, border-radius 13px)
10. Checkbox abaixo: "Li e estou de acordo com os termos e condições de uso e com as políticas de privacidade"
11. Botões na área inferior:
    - "Cancelar" (secundário) → volta para etapa 1
    - "Aceitar e fechar" (primário, desabilitado até checkbox marcado)
12. Ao clicar "Aceitar e fechar":
    - Frontend chama `POST /api/v1/organizations/{org_id}/terms-acceptance`
    - Backend registra aceite com auditoria (user_id, org_id, terms_version, IP, user_agent)
    - Modal fecha e usuário continua no fluxo de onboarding

## Estados

* **Etapa 1 (Boas-vindas):** Apenas botão "Próximo" habilitado
* **Etapa 2 (Termos):** Botão "Aceitar e fechar" desabilitado até checkbox marcado
* **Sucesso:** Modal fecha, usuário continua onboarding (Configure seu WhatsApp)
* **Erro (auth):** Token inválido/expirado → retornar 401, redirecionar para login
* **Erro (sistema):** Falha ao registrar → exibir toast "Não foi possível registrar seu aceite. Tente novamente."
* **Loading:** Spinner no botão durante chamada API

---

# Critérios de Aceite

* Modal de boas-vindas é exibido automaticamente no primeiro acesso após login
* Etapa 1 (Boas-vindas) exibe mensagem personalizada com nome do usuário
* Etapa 2 (Termos) exibe texto completo dos termos em área com scroll
* Sidebar indica etapa atual com indicador visual (barra laranja)
* Checkbox "Li e estou de acordo..." é obrigatório para habilitar botão
* Botão "Aceitar e fechar" permanece desabilitado até checkbox marcado
* Botão "Cancelar" na etapa 2 retorna para etapa 1 (Boas-vindas)
* Ao aceitar, registro de auditoria criado com user_id, org_id, terms_version, timestamp, IP, user_agent
* Se termos já aceitos, modal não é exibido (usuário segue direto para onboarding)
* NFR (performance): Modal carrega em <1 segundo p95
* Segurança: Apenas admin da organização pode aceitar (403 para outros)
* Analytics: Eventos `sign_up_terms_welcome_viewed`, `sign_up_terms_page_viewed` e `sign_up_terms_accepted` disparam corretamente
* Responsivo: Modal funciona em desktop (1280px+) — mobile será tratado em versão futura

---

# Observabilidade & Analytics

## Métricas

| Nível | Métrica | Descrição | Fórmula | Justificativa |
|-------|---------|-----------|---------|---------------|
| Focus | Taxa de Aceite de Termos | Percentual de usuários que completam o fluxo de aceite dos termos | `Terms Accepted / Welcome Modal Viewed * 100` | Métrica principal que indica se o fluxo está funcionando e usuários estão conseguindo prosseguir |
| L1 - Activation | Taxa de Conversão Etapa 1→2 | Percentual de usuários que avançam da boas-vindas para os termos | `Terms Modal Viewed / Welcome Modal Viewed * 100` | Indica se a etapa de boas-vindas está clara e não gera abandono |
| L1 - Engagement | Taxa de Scroll Completo | Percentual de usuários que leram os termos até o final | `Terms Scrolled / Terms Modal Viewed * 100` | Indica engajamento real com o conteúdo dos termos |
| L1 - Guardrail | Taxa de Erro | Percentual de tentativas de aceite que falharam | `Terms Acceptance Failed / Terms Acceptance Submitted * 100` | Guardrail para identificar problemas técnicos |
| L2 | Tempo Médio no Modal | Tempo médio que usuários passam no modal (por etapa) | `AVG(time_on_modal_seconds)` | Ajuda a identificar se usuários estão travando em alguma etapa |

## Eventos

| Evento | Descrição | Trigger | Properties |
|--------|-----------|---------|------------|
| `Welcome Modal Viewed` | Usuário visualizou o modal de boas-vindas (etapa 1 do aceite de termos) | Modal de boas-vindas é exibido na tela | `organization_id` |
| `Terms Modal Viewed` | Usuário visualizou o modal de termos e condições (etapa 2) | Usuário clica em "Próximo" e modal de termos é exibido | `organization_id` |
| `Terms Scrolled` | Usuário fez scroll na área de termos | Usuário atinge 90%+ do scroll na área de termos | `organization_id`, `scroll_percentage` |
| `Terms Checkbox Clicked` | Usuário marcou ou desmarcou o checkbox de aceite | Clique no checkbox de aceite dos termos | `organization_id`, `is_checked` |
| `Terms Acceptance Submitted` | Usuário tentou submeter o aceite dos termos | Clique no botão "Aceitar e fechar" (checkbox marcado) | `organization_id`, `terms_version` |
| `Terms Accepted` | Aceite dos termos foi registrado com sucesso | API retorna sucesso (201) ao registrar aceite | `organization_id`, `terms_version`, `time_on_modal_seconds` |
| `Terms Acceptance Failed` | Erro ao registrar aceite dos termos | API retorna erro (4xx/5xx) ao tentar registrar aceite | `organization_id`, `error_code`, `error_message` |
| `Terms Modal Cancelled` | Usuário cancelou o fluxo de aceite | Clique no botão "Cancelar" em qualquer etapa | `organization_id`, `current_step` |

## Event Properties

| Property | Tipo | Descrição | Obrigatória |
|----------|------|-----------|-------------|
| `organization_id` | string | Identificador único da organização (UUID) | Sim |
| `terms_version` | string | Versão dos termos sendo aceitos (ex: "v1.0") | Sim (em eventos de aceite) |
| `time_on_modal_seconds` | number | Tempo total em segundos que o usuário passou no modal | Não |
| `scroll_percentage` | number | Percentual de scroll atingido na área de termos (0-100) | Sim (em Terms Scrolled) |
| `is_checked` | boolean | Se o checkbox está marcado (true) ou desmarcado (false) | Sim (em Terms Checkbox Clicked) |
| `current_step` | string | Etapa atual do modal: "welcome" ou "terms" | Sim (em Terms Modal Cancelled) |
| `error_code` | string | Código HTTP do erro (ex: "500", "403") | Sim (em eventos de erro) |
| `error_message` | string | Mensagem de erro retornada pela API | Não |

## Alertas

| Alerta | Condição | Ação | Severidade |
|--------|----------|------|------------|
| Alta taxa de abandono | Taxa de Aceite < 80% em 24h | Notificar produto para investigar UX | Warning |
| Erros frequentes | Taxa de Erro > 5% em 1h | Page on-call de engenharia | Critical |
| Zero aceites | Nenhum `Terms Accepted` em 4h (horário comercial) | Investigar possível bug no fluxo | Critical |
| Latência alta | p95 da API de aceite > 2s por 15min | Alerta de degradação de performance | Warning |

## Auditoria (Compliance)

* Logar aceite de termos com: `user_id`, `organization_id`, `terms_version`, `timestamp`, `ip_address` (parcial), `user_agent`, `result` (success/error)
* Logs de auditoria retidos por 7 anos (requisito legal)

---

# Questões em Aberto

* [Legal] Versão inicial dos termos (ex: "v1.0")?

---

# Premissas

* Usuário já está autenticado (Story SLA-551) antes de ver o modal
* Termos de uso estarão definidos e versionados antes do lançamento
* Usuário deve ser admin da organização para aceitar termos
* Aceite é obrigatório para prosseguir no onboarding (modal bloqueia interação)
* Um aceite por organização por versão de termos (não por usuário)
* Modal é exibido sobre a tela de onboarding (fluxo "Configure seu WhatsApp")
