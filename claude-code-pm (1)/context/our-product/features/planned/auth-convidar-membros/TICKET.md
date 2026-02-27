## Overview

* **Objetivo:** Permitir que administradores convidem outros administradores para sua organização, para que possam gerenciar configurações e integracoes.
* **Quem é afetado:** Administradores que precisam adicionar outros admins a organização.
* **Comportamento atual:** N/A - Nova funcionalidade.
* **Comportamento desejado:** Admin envia convite por e-mail, convidado recebe link, completa cadastro e entra na organização como administrador.
* **Por que fazer isso agora:** Imobiliárias podem precisar de múltiplos administradores para gerenciar o sistema.

---

## Contexto Importante

> **AUTORIZACAO DEFINITIVA:** Esta e uma solução definitiva. Investir em modelo de dados robusto, arquitetura extensivel e testes abrangentes. Incluir auditoria completa.

---

## Fluxo do Usuário - Admin Convidando

```
1. Admin acessa área de gerenciamento de usuários
2. Clica em "Convidar membro"
3. Preenche e-mail do convidado
4. Clica em "Enviar convite" (perfil admin automático no MVP)
5. Sistema envia convite por e-mail
6. Admin vê confirmação e lista de convites pendentes
```

## Fluxo do Usuário - Convidado Aceitando

```
1. Convidado recebe e-mail com convite
2. Clica no link do convite
3. Sistema valida token e exibe tela de aceitar convite
4. Convidado preenche: nome, sobrenome, telefone, senha
5. Clica em "Aceitar convite"
6. Usuário criado e associado a organização
7. Convidado redirecionado para o back-office
```

---

## Escopo

### Dentro do escopo

* Tela de gerenciamento de usuários (listagem)
* Formulário de convite (e-mail) - perfil admin automático no MVP
* Envio de convite por e-mail
* Opção de enviar por WhatsApp (canal alternativo, mesmo link)
* Tela de aceitar convite
* Cadastro do convidado (nome, sobrenome, telefone, senha)
* Expiração de convite (7 dias)
* Reenvio de convite
* Lista de convites pendentes
* Auditoria: quem convidou quem

### Fora do escopo

* Convidar como Corretor (Fase 2 - MVP apenas admins)
* Convite em lote (múltiplos e-mails)
* Importacao de lista de usuários
* Convite por link genérico (sem e-mail específico)
* Alterar perfil após convite (Story 6)
* Desativar usuário (Story 6)

---

## Especificação de UX + Comportamento

### Tela: Gerenciamento de Usuários

**Visao geral:**
- Lista de membros da organização
- Lista de convites pendentes
- Botão "Convidar membro"

**Lista de membros:**
| Nome | E-mail | Perfil | Status | Acoes |
|------|--------|--------|--------|-------|
| Maria Silva | maria@imob.com | Admin | Ativo | ... |
| Joao Santos | joao@imob.com | Admin | Ativo | ... |

**Lista de convites pendentes:**
| E-mail | Enviado em | Expira em | Acoes |
|--------|------------|-----------|-------|
| pedro@email.com | 05/01/2026 | 12/01/2026 | Reenviar, Cancelar |

### Modal: Convidar Membro

**Campos:**
- E-mail (obrigatório, formato válido)

**Nota:** No MVP, todos os convidados entram como Administrador. Perfil Corretor será adicionado na Fase 2.

**Botoes:**
- "Enviar convite" (principal)
- "Enviar por WhatsApp" (secundário, mesmo link)
- "Cancelar"

**Validações (frontend):**
- E-mail: formato válido
- E-mail: não pode ser de membro existente
- E-mail: não pode ter convite pendente

### Tela: Aceitar Convite (Convidado)

**Pre-condicao:** Convidado clicou no link do e-mail e token e válido

**Informacoes exibidas:**
- Nome da organização
- Quem convidou

**Campos:**
- Nome (obrigatório)
- Sobrenome (obrigatório)
- Telefone (obrigatório, formato brasileiro)
- Senha (obrigatório)
- Confirmar senha (obrigatório)

**Botão:** "Aceitar convite"

**Validações (frontend):**
- Nome/Sobrenome: min 2 caracteres
- Telefone: formato brasileiro
- Senha: min 8 caracteres, 1 letra, 1 número
- Confirmar senha: igual a senha

### Estados de Erro

**Convite expirado:**
- Título: "Convite expirado"
- Texto: "Este convite expirou. Solicite um novo convite ao administrador."
- Botão: "Solicitar novo convite" (envia notificação ao admin)

**Convite inválido:**
- Título: "Convite inválido"
- Texto: "Este convite não é válido."
- Botão: "Voltar"

**Convite já aceito:**
- Título: "Convite já utilizado"
- Texto: "Este convite já foi aceito. Se você já tem uma conta, faça login."
- Botão: "Ir para login"

**E-mail já cadastrado:**
- Título: "E-mail já cadastrado"
- Texto: "Este e-mail já esta associado a outra conta. Use outro e-mail ou faça login."
- Botão: "Ir para login"

---

## Especificações Técnicas

### API Endpoints

```
GET /api/v1/organizations/{org_id}/members
Headers:
  Authorization: Bearer {access_token}

Response 200:
{
  "members": [
    {
      "id": "string",
      "email": "string",
      "first_name": "string",
      "last_name": "string",
      "role": "admin"  // MVP apenas admin; broker será adicionado na Fase 2,
      "status": "active" | "inactive",
      "joined_at": "ISO8601"
    }
  ],
  "pending_invites": [
    {
      "id": "string",
      "email": "string",
      "role": "admin"  // MVP apenas admin; broker será adicionado na Fase 2,
      "invited_by": {
        "id": "string",
        "name": "string"
      },
      "sent_at": "ISO8601",
      "expires_at": "ISO8601"
    }
  ]
}

Response 401: Não autenticado
Response 403: Sem permissao (não e admin)
```

```
POST /api/v1/organizations/{org_id}/invites
Headers:
  Authorization: Bearer {access_token}

Request:
{
  "email": "string",
  "role": "admin"  // MVP apenas admin; broker será adicionado na Fase 2
}

Response 201:
{
  "id": "string",
  "email": "string",
  "role": "admin"  // MVP apenas admin; broker será adicionado na Fase 2,
  "expires_at": "ISO8601",
  "invite_link": "string"
}

Response 400: E-mail inválido ou já existente
Response 401: Não autenticado
Response 403: Sem permissao (não e admin)
Response 409: Convite pendente já existe para este e-mail
```

```
POST /api/v1/organizations/{org_id}/invites/{invite_id}/resend
Headers:
  Authorization: Bearer {access_token}

Response 200:
{
  "message": "Invite resent",
  "expires_at": "ISO8601" // novo prazo
}

Response 404: Convite não encontrado
```

```
DELETE /api/v1/organizations/{org_id}/invites/{invite_id}
Headers:
  Authorization: Bearer {access_token}

Response 200:
{
  "message": "Invite cancelled"
}
```

```
GET /api/v1/invites/{token}
Response 200:
{
  "valid": true,
  "organization": {
    "id": "string",
    "trade_name": "string"
  },
  "role": "admin"  // MVP apenas admin; broker será adicionado na Fase 2,
  "invited_by": {
    "name": "string"
  },
  "email": "string"
}

Response 400: Token inválido
Response 410: Token expirado
```

```
POST /api/v1/invites/{token}/accept
Request:
{
  "first_name": "string",
  "last_name": "string",
  "phone": "string",
  "password": "string"
}

Response 201:
{
  "user": {
    "id": "string",
    "email": "string",
    "role": "admin"  // MVP apenas admin; broker será adicionado na Fase 2
  },
  "organization": {
    "id": "string",
    "trade_name": "string"
  },
  "access_token": "string",
  "refresh_token": "string"
}

Response 400: Dados inválidos
Response 410: Token expirado
Response 409: E-mail já cadastrado
```

### Modelo de Dados

**Tabela: organization_invites**
- id (UUID, PK)
- organization_id (UUID, FK)
- email (string, not null)
- role (enum: admin)  // MVP apenas admin; broker será adicionado na Fase 2
- token (string, unique, not null)
- invited_by (UUID, FK → users)
- sent_at (timestamp)
- expires_at (timestamp)
- accepted_at (timestamp, nullable)
- cancelled_at (timestamp, nullable)
- created_at (timestamp)

### Auditoria

**Eventos a registrar:**

| Acao | Dados |
|------|-------|
| Convite enviado | org_id, invited_by, email, role, timestamp |
| Convite reenviado | org_id, invite_id, resent_by, timestamp |
| Convite cancelado | org_id, invite_id, cancelled_by, timestamp |
| Convite aceito | org_id, invite_id, user_id, timestamp |
| Convite expirado | org_id, invite_id, timestamp |

---

## Critérios de Aceite

### Admin Convidando

* Admin consegue acessar área de gerenciamento de usuários
* Lista de membros exibe todos os usuários da organização
* Lista de convites pendentes exibe convites não aceitos
* Botão "Convidar membro" abre modal de convite
* Formulário exige e-mail (perfil admin automático no MVP)
* Validação de formato de e-mail
* Não permite convidar e-mail já membro
* Não permite convidar e-mail com convite pendente
* Ao enviar, convite criado com expiração de 7 dias
* E-mail de convite enviado ao convidado
* Convite aparece na lista de pendentes
* Admin pode reenviar convite (renova expiração)
* Admin pode cancelar convite pendente
* Opção de copiar link para enviar por WhatsApp

### Convidado Aceitando

* Link do convite abre tela de aceitar convite
* Tela exibe nome da organização e quem convidou
* Formulário exige nome, sobrenome, telefone, senha
* Validações de campos funcionando
* Convite expirado exibe mensagem apropriada
* Convite inválido exibe mensagem apropriada
* Convite já aceito exibe mensagem apropriada
* E-mail já cadastrado exibe mensagem apropriada
* Ao aceitar, usuário criado como admin
* Usuário associado a organização
* Convidado redirecionado para back-office após aceitar
* Convidado já logado após aceitar

### Auditoria

* Auditoria: convite enviado registrado
* Auditoria: convite aceito registrado
* Auditoria: convite cancelado registrado

### Analytics

* Analytics: evento `invite_sent` com {org_id, role, timestamp}
* Analytics: evento `invite_accepted` com {org_id, user_id, role, time_to_accept_hours, timestamp}
* Analytics: evento `invite_expired` com {org_id, timestamp}

---

## Observabilidade & Analytics

### Eventos

* `members_page_viewed` props `{org_id, admin_id, member_count, pending_count, timestamp}` trigger: ao carregar página
* `invite_modal_opened` props `{org_id, admin_id, timestamp}` trigger: ao abrir modal de convite
* `invite_sent` props `{org_id, admin_id, invitee_email_domain, role, timestamp}` trigger: ao enviar convite
* `invite_resent` props `{org_id, admin_id, invite_id, timestamp}` trigger: ao reenviar convite
* `invite_cancelled` props `{org_id, admin_id, invite_id, timestamp}` trigger: ao cancelar convite
* `invite_link_clicked` props `{org_id, invite_id, timestamp}` trigger: ao clicar no link do convite
* `invite_accepted` props `{org_id, user_id, role, time_to_accept_hours, timestamp}` trigger: ao aceitar convite
* `invite_expired` props `{org_id, invite_id, timestamp}` trigger: quando convite expira sem ser aceito

### Métricas

* Taxa de conversão: convite enviado → aceito
* Tempo médio para aceitar convite
* Taxa de convites expirados
* Taxa de reenvio de convites

---

## Dependências

* Story 1 (Sign Up) deve estar completa
* Story 4 (Criar Organizacao) deve estar completa
* Serviço de envio de e-mail configurado
* Template de e-mail de convite criado

---

## Fora do Escopo

* Convite em lote (múltiplos e-mails de uma vez)
* Importacao de lista de corretores
* Link de convite genérico (sem e-mail específico)
* Alterar perfil após convite aceito (Story 6)
* Desativar usuário (Story 6)

---

## Definition of Done

* Código implementado e revisado
* Testes unitários com cobertura >80%
* Testes de integração para APIs
* Teste E2E do fluxo completo (enviar e aceitar)
* Expiração de convite funcionando (7 dias)
* Auditoria implementada
* Controle de acesso (apenas admin convida)
* Eventos de analytics implementados
* Code review aprovado
* QA sign-off
* Deploy em staging validado

---

## Questões em Aberto

* [Design] Qual o layout/design das telas? Link do Figma?
* [PM] Limite de convites pendentes por organização?
* [PM] Limite de membros por organização?
* [PM] Notificar admin quando convite for aceito?

---

## Premissas

* Usuário que convida e admin da organização
* Serviço de e-mail já configurado
* Convidado tem acesso ao e-mail informado
* Um e-mail só pode pertencer a uma conta (se já existe, não pode aceitar convite)
