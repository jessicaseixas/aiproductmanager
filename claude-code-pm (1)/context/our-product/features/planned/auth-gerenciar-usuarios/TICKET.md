## Overview

* **Objetivo:** Permitir que administradores gerenciem os membros da organização, alterando perfis e desativando/reativando usuários.
* **Quem é afetado:** Administradores que precisam gerenciar sua equipe, e corretores que podem ter seu acesso ou perfil alterado.
* **Comportamento atual:** N/A - Nova funcionalidade. Story 5 permite convidar, mas não gerenciar após entrada.
* **Comportamento desejado:** Admin pode alterar perfil de usuários (admin ↔ corretor) e desativar/reativar usuários, com impacto nos leads atribuidos.
* **Por que fazer isso agora:** Imobiliárias precisam gerenciar sua equipe - promover corretores a admin, remover acesso de quem saiu, etc.

---

## Contexto Importante

> **AUTORIZACAO DEFINITIVA:** Esta e uma solução definitiva. Investir em modelo de dados robusto, arquitetura extensivel e testes abrangentes. Incluir auditoria completa.

---

## Fluxo do Usuário - Alterar Perfil

```
1. Admin acessa área de gerenciamento de usuários
2. Localiza usuário na lista
3. Clica em "Editar" ou acoes do usuário
4. Seleciona novo perfil (Admin ou Corretor)
5. Confirma alteração
6. Perfil atualizado
```

## Fluxo do Usuário - Desativar Usuário

```
1. Admin acessa área de gerenciamento de usuários
2. Localiza usuário na lista
3. Clica em "Desativar"
4. Sistema exibe confirmação com aviso sobre leads
5. Admin confirma
6. Usuário desativado
7. Leads do usuário ficam sem atribuição
8. Admin recebe visibilidade dos leads sem atribuição
```

---

## Escopo

### Dentro do escopo

* Alterar perfil de usuário (admin ↔ corretor)
* Desativar usuário
* Reativar usuário
* Leads de usuário desativado ficam sem atribuição
* Indicador de leads sem corretor atribuido
* Confirmacao antes de desativar
* Auditoria de todas as acoes

### Fora do escopo

* Excluir usuário permanentemente
* Transferir leads para outro corretor automaticamente
* Desativar o próprio usuário (admin não pode se desativar)
* Remover o último admin da organização

---

## Especificação de UX + Comportamento

### Tela: Gerenciamento de Usuários (extensao da Story 5)

**Lista de membros com acoes:**
| Nome | E-mail | Perfil | Status | Acoes |
|------|--------|--------|--------|-------|
| Maria Silva | maria@imob.com | Admin | Ativo | Editar |
| Joao Santos | joao@imob.com | Corretor | Ativo | Editar, Desativar |
| Pedro Costa | pedro@imob.com | Corretor | Inativo | Reativar |

**Indicador de leads sem atribuição:**
- Banner ou card: "X leads sem corretor atribuido" com link para ver leads

**Regras de exibição de acoes:**
- Admin não pode desativar a si mesmo
- Último admin não pode ser desativado/rebaixado
- Usuário desativado mostra apenas "Reativar"

### Modal: Editar Usuário

**Campos:**
- Nome (readonly, apenas exibição)
- E-mail (readonly, apenas exibição)
- Perfil (select): Administrador, Corretor

**Botoes:**
- "Salvar" (principal)
- "Cancelar"

**Validação:**
- Não pode rebaixar o último admin

### Modal: Confirmar Desativacao

**Conteúdo:**
- Título: "Desativar usuário?"
- Texto: "O usuário {nome} será desativado e não podera mais acessar o sistema."
- Se tiver leads: "Este usuário tem {X} leads atribuidos que ficarao sem corretor."
- Checkbox (opcional): "Entendo que os leads ficarao sem atribuição"

**Botoes:**
- "Desativar" (destrutivo)
- "Cancelar"

### Modal: Confirmar Reativacao

**Conteúdo:**
- Título: "Reativar usuário?"
- Texto: "O usuário {nome} podera acessar o sistema novamente com perfil de {perfil}."

**Botoes:**
- "Reativar" (principal)
- "Cancelar"

### Estados de Erro

**Último admin:**
- Mensagem: "Nao e possível desativar ou rebaixar o último administrador da organização."

**Erro genérico:**
- Mensagem: "Não foi possível completar a acao. Tente novamente."

---

## Especificações Técnicas

### API Endpoints

```
PATCH /api/v1/organizations/{org_id}/members/{user_id}
Headers:
  Authorization: Bearer {access_token}

Request:
{
  "role": "admin" | "broker"
}

Response 200:
{
  "id": "string",
  "email": "string",
  "role": "admin" | "broker",
  "updated_at": "ISO8601"
}

Response 400: Dados inválidos
Response 403: Sem permissao ou tentando rebaixar último admin
Response 404: Usuário não encontrado
```

```
POST /api/v1/organizations/{org_id}/members/{user_id}/deactivate
Headers:
  Authorization: Bearer {access_token}

Response 200:
{
  "id": "string",
  "status": "inactive",
  "leads_unassigned": number,
  "deactivated_at": "ISO8601"
}

Response 403: Sem permissao, tentando desativar a si mesmo, ou último admin
Response 404: Usuário não encontrado
```

```
POST /api/v1/organizations/{org_id}/members/{user_id}/reactivate
Headers:
  Authorization: Bearer {access_token}

Response 200:
{
  "id": "string",
  "status": "active",
  "reactivated_at": "ISO8601"
}

Response 404: Usuário não encontrado
```

```
GET /api/v1/organizations/{org_id}/leads/unassigned/count
Headers:
  Authorization: Bearer {access_token}

Response 200:
{
  "count": number
}
```

### Logica de Negocio

**Ao desativar usuário:**
1. Marcar usuário como inactive
2. Invalidar todas as sessões do usuário
3. Buscar leads atribuidos ao usuário
4. Remover atribuição (assigned_to = null)
5. Registrar auditoria
6. Retornar quantidade de leads desatribuidos

**Validações de último admin:**
- Contar admins ativos na organização
- Se count == 1, bloquear desativacao/rebaixamento

### Auditoria

**Eventos a registrar:**

| Acao | Dados |
|------|-------|
| Perfil alterado | org_id, changed_by, user_id, old_role, new_role, timestamp |
| Usuário desativado | org_id, deactivated_by, user_id, leads_unassigned, timestamp |
| Usuário reativado | org_id, reactivated_by, user_id, timestamp |

---

## Critérios de Aceite

### Alterar Perfil

* Admin consegue alterar perfil de outro usuário
* Opções de perfil: Administrador e Corretor
* Alteracao refletida imediatamente
* Não pode rebaixar último admin
* Auditoria registra alteração de perfil

### Desativar Usuário

* Admin consegue desativar outro usuário
* Modal de confirmação exibido antes de desativar
* Se usuário tem leads, modal informa quantidade
* Ao desativar, usuário não consegue mais fazer login
* Ao desativar, sessões existentes sao invalidadas
* Leads do usuário ficam sem atribuição (assigned_to = null)
* Admin não pode desativar a si mesmo
* Último admin não pode ser desativado
* Auditoria registra desativacao

### Reativar Usuário

* Admin consegue reativar usuário desativado
* Usuário reativado consegue fazer login novamente
* Usuário mantém mesmo perfil que tinha antes
* Auditoria registra reativacao

### Indicador de Leads

* Indicador mostra quantidade de leads sem corretor
* Indicador atualiza após desativar usuário
* Link para ver leads sem atribuição (se existir tela)

### Controle de Acesso

* Apenas admins vêem opções de gerenciamento
* Corretores não conseguem alterar perfis ou desativar

### Analytics

* Analytics: evento `member_role_changed` com {org_id, user_id, old_role, new_role, timestamp}
* Analytics: evento `member_deactivated` com {org_id, user_id, leads_unassigned, timestamp}
* Analytics: evento `member_reactivated` with {org_id, user_id, timestamp}

---

## Observabilidade & Analytics

### Eventos

* `member_role_changed` props `{org_id, admin_id, user_id, old_role, new_role, timestamp}` trigger: ao alterar perfil
* `member_deactivation_initiated` props `{org_id, admin_id, user_id, leads_count, timestamp}` trigger: ao abrir modal de desativacao
* `member_deactivated` props `{org_id, admin_id, user_id, leads_unassigned, timestamp}` trigger: ao confirmar desativacao
* `member_reactivated` props `{org_id, admin_id, user_id, timestamp}` trigger: ao reativar usuário
* `unassigned_leads_viewed` props `{org_id, admin_id, count, timestamp}` trigger: ao clicar no indicador de leads

### Métricas

* Taxa de desativacao de usuários
* Media de leads desatribuidos por desativacao
* Taxa de reativacao
* Distribuição de perfis (admin vs corretor)

---

## Dependências

* Story 5 (Convidar Membros) deve estar completa
* Modelo de leads deve ter campo assigned_to
* Sistema de sessões deve permitir invalidação

---

## Fora do Escopo

* Excluir usuário permanentemente
* Transferir leads automaticamente para outro corretor
* Tela de detalhes de leads sem atribuição (pode usar listagem existente com filtro)
* Bulk actions (desativar múltiplos usuários)

---

## Definition of Done

* Código implementado e revisado
* Testes unitários com cobertura >80%
* Testes de integração para APIs
* Teste E2E dos fluxos (alterar, desativar, reativar)
* Logica de último admin implementada
* Desatribuição de leads funcionando
* Invalidação de sessões funcionando
* Auditoria implementada
* Eventos de analytics implementados
* Code review aprovado
* QA sign-off
* Deploy em staging validado

---

## Questões em Aberto

* [Design] Qual o layout/design? Link do Figma?
* [PM] Notificar usuário quando for desativado?
* [PM] Tempo de retencao de dados de usuário desativado?
* [PM] Usuário desativado pode ser excluido permanentemente depois?

---

## Premissas

* Usuário que gerencia e admin da organização
* Leads tem campo assigned_to que pode ser null
* Sistema de sessões permite invalidação por user_id
* Ao desativar, dados do usuário sao mantidos (soft delete)
