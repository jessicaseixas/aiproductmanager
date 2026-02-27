## Overview

* **Objetivo:** Permitir que usuários editem suas próprias informações de perfil e alterem sua senha de forma self-service.
* **Quem é afetado:** Todos os usuários do Qualifica Leads Standalone (admins e corretores).
* **Comportamento atual:** N/A - Nova funcionalidade. Usuários não conseguem editar seus dados após o cadastro.
* **Comportamento desejado:** Usuário acessa página de perfil via Account Menu, visualiza e edita seus dados pessoais, e pode alterar sua senha.
* **Por que fazer isso agora:** Usuários precisam poder atualizar seus dados quando mudam de telefone, corrigir nome, ou alterar senha por segurança.

---

## Contexto Importante

> **AUTORIZACAO DEFINITIVA:** Esta e uma solução definitiva. Investir em modelo de dados robusto, arquitetura extensivel e testes abrangentes.

**Diferenca de Story 6 (Gerenciar Usuários):**
- Story 6: Admin gerencia OUTROS usuários (altera perfil, desativa)
- Story 8 (esta): Usuário edita SEU PROPRIO perfil (self-service)

---

## Fluxo do Usuário

```
1. Usuário clica no Account Menu (canto superior direito)
2. Clica em "Profile"
3. Sistema exibe página de perfil com dados atuais
4. Usuário edita campos desejados
5. Clica em "Salvar"
6. Dados atualizados
```

### Fluxo de Alterar Senha

```
1. Na página de perfil, usuário clica em "Alterar senha"
2. Sistema pede senha atual (confirmação de segurança)
3. Usuário preenche: senha atual, nova senha, confirmar nova senha
4. Clica em "Alterar senha"
5. Senha atualizada
6. (Opcional) Outras sessões podem ser invalidadas
```

---

## Escopo

### Dentro do escopo

* Página de perfil do usuário
* Visualizar dados atuais (nome, sobrenome, e-mail, telefone)
* Editar nome e sobrenome
* Editar telefone
* Alterar senha (com confirmação da senha atual)
* E-mail como campo somente leitura (não editavel)

### Fora do escopo

* Alterar e-mail (requer fluxo de verificação complexo)
* Alterar foto/avatar do usuário
* Excluir própria conta
* Ver historico de alterações
* Configuracoes de notificação

---

## Especificação de UX + Comportamento

### Página: Meu Perfil

**Seção: Informacoes Pessoais**

| Campo | Tipo | Editavel |
|-------|------|----------|
| Nome | Input text | Sim |
| Sobrenome | Input text | Sim |
| E-mail | Input text (readonly) | Não |
| Telefone | Input text (masked) | Sim |

**Botão:** "Salvar alterações"

**Seção: Segurança**

- Texto: "Alterar sua senha"
- Botão: "Alterar senha" → abre modal ou seção expandida

### Modal/Seção: Alterar Senha

**Campos:**
- Senha atual (obrigatório) - para confirmar identidade
- Nova senha (obrigatório)
- Confirmar nova senha (obrigatório)

**Botoes:**
- "Alterar senha" (principal)
- "Cancelar"

**Validações (frontend):**

| Campo | Validação |
|-------|-----------|
| Nome | Não vazio, min 2 caracteres |
| Sobrenome | Não vazio, min 2 caracteres |
| Telefone | Formato brasileiro (DDD + 8-9 dígitos) |
| Senha atual | Não vazio |
| Nova senha | Min 8 caracteres, 1 letra, 1 número |
| Confirmar senha | Igual a nova senha |

**Feedback de senha:**
- Mostrar requisitos antes de digitar
- Válidar em tempo real
- Não permitir nova senha igual a atual

### Estados de Sucesso

**Dados salvos:**
- Toast/notificação: "Perfil atualizado com sucesso"

**Senha alterada:**
- Toast/notificação: "Senha alterada com sucesso"
- (Opcional) Redirecionar para login se invalidar sessões

### Estados de Erro

**Senha atual incorreta:**
- Mensagem: "Senha atual incorreta"

**Nova senha igual a atual:**
- Mensagem: "A nova senha deve ser diferente da atual"

**Erro ao salvar:**
- Mensagem: "Não foi possível salvar as alterações. Tente novamente."

---

## Especificações Técnicas

### API Endpoints

```
GET /api/v1/users/me
Headers:
  Authorization: Bearer {access_token}

Response 200:
{
  "id": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "phone": "string",
  "role": "admin" | "broker",
  "organization": {
    "id": "string",
    "trade_name": "string"
  },
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

```
PATCH /api/v1/users/me
Headers:
  Authorization: Bearer {access_token}

Request:
{
  "first_name": "string", // opcional
  "last_name": "string", // opcional
  "phone": "string" // opcional
}

Response 200:
{
  "id": "string",
  "first_name": "string",
  "last_name": "string",
  "phone": "string",
  "updated_at": "ISO8601"
}

Response 400: Dados inválidos
Response 401: Não autenticado
```

```
POST /api/v1/users/me/change-password
Headers:
  Authorization: Bearer {access_token}

Request:
{
  "current_password": "string",
  "new_password": "string"
}

Response 200:
{
  "message": "Password changed successfully"
}

Response 400: Nova senha não atende requisitos ou igual a atual
Response 401: Senha atual incorreta
```

### Modelo de Dados

Usa tabela `users` existente. Nenhuma alteração necessária.

### Segurança

**Alterar senha:**
- Exigir senha atual para confirmar identidade
- Não permitir nova senha igual a atual
- Aplicar mesmas regras de senha do cadastro (8+ chars, letra + número)
- Considerar invalidar outras sessões após troca de senha

**Proteção:**
- Rate limit em alteração de senha (max 5 tentativas por hora)
- Logar tentativas de alteração de senha (auditoria)

---

## Critérios de Aceite

### Visualizar Perfil

* Usuário acessa página de perfil via Account Menu > Profile
* Página exibe dados atuais: nome, sobrenome, e-mail, telefone
* E-mail exibido como somente leitura (não editavel)

### Editar Dados

* Usuário pode editar nome
* Usuário pode editar sobrenome
* Usuário pode editar telefone
* Validação de nome/sobrenome: min 2 caracteres
* Validação de telefone: formato brasileiro
* Botão "Salvar" salva alterações
* Toast de sucesso exibido após salvar
* Dados atualizados refletem no Account Menu (nome)

### Alterar Senha

* Botão "Alterar senha" disponível na página de perfil
* Modal/seção exige: senha atual, nova senha, confirmar senha
* Senha atual incorreta exibe erro apropriado
* Nova senha validada: min 8 chars, 1 letra, 1 número
* Nova senha não pode ser igual a atual
* Confirmar senha deve ser identica a nova senha
* Sucesso exibe toast de confirmação
* Rate limit: max 5 tentativas de alteração por hora

### Segurança e Auditoria

* Tentativas de alteração de senha sao logadas
* Usuário precisa estar autenticado para acessar
* Usuário só pode editar seu próprio perfil

### Analytics

* Analytics: evento `profile_viewed` com {user_id, timestamp}
* Analytics: evento `profile_updated` com {user_id, fields_changed, timestamp}
* Analytics: evento `password_change_attempted` com {user_id, success, timestamp}
* Analytics: evento `password_change_success` com {user_id, timestamp}
* Analytics: evento `password_change_failed` com {user_id, error_type, timestamp}

---

## Observabilidade & Analytics

### Eventos

* `profile_page_viewed` props `{user_id, timestamp}` trigger: ao carregar página de perfil
* `profile_edit_initiated` props `{user_id, timestamp}` trigger: ao começar editar
* `profile_updated` props `{user_id, fields_changed, timestamp}` trigger: ao salvar alterações
* `password_change_initiated` props `{user_id, timestamp}` trigger: ao abrir modal de senha
* `password_change_attempted` props `{user_id, timestamp}` trigger: ao submeter nova senha
* `password_change_success` props `{user_id, timestamp}` trigger: ao alterar senha com sucesso
* `password_change_failed` props `{user_id, error_type, timestamp}` trigger: ao falhar alteração

### Métricas

* Taxa de usuários que editam perfil
* Campos mais editados
* Taxa de alteração de senha
* Taxa de erro em alteração de senha (senha atual incorreta)

---

## Dependências

* Story 1 (Sign Up) - usuários precisam existir
* Story 2 (Sign In) - usuário precisa estar logado
* Story 2 (Sign In) - Account Menu implementado com link para Profile

---

## Fora do Escopo

* Alterar e-mail (requer verificação)
* Upload de foto/avatar
* Excluir própria conta
* Ver historico de alterações do perfil
* Configuracoes de notificação
* Invalidar todas as sessões após troca de senha (pode ser adicionado depois)

---

## Definition of Done

* Código implementado e revisado
* Testes unitários com cobertura >80%
* Testes de integração para APIs
* Teste E2E do fluxo de editar perfil
* Teste E2E do fluxo de alterar senha
* Validações funcionando
* Rate limit implementado
* Eventos de analytics implementados
* Code review aprovado
* QA sign-off
* Deploy em staging validado

---

## Questões em Aberto

* [Design] Qual o layout/design da página de perfil? Link do Figma?
* [PM] Invalidar outras sessões após troca de senha?
* [PM] Enviar e-mail de notificação quando senha for alterada?
* [PM] Permitir alterar e-mail no futuro? (requer verificação)

---

## Premissas

* Usuário está autenticado
* Account Menu já implementado com link para Profile (Story 2)
* Mesmas regras de senha do cadastro se aplicam
* Alteracao de e-mail não será suportada nesta versão
