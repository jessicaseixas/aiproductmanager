## Overview

* **Objetivo:** Permitir que administradores editem os dados da organização e, em casos específicos, excluam a organização.
* **Quem é afetado:** Administradores que precisam atualizar dados da organização (nome, logo, documento).
* **Comportamento atual:** N/A - Nova funcionalidade. Story 4 permite criar, mas não editar.
* **Comportamento desejado:** Admin pode editar nome fantasia, logo e documento. Pode excluir organização apenas se estiver em branco.
* **Por que fazer isso agora:** Organizacoes precisam poder atualizar seus dados quando mudam de nome, logo, etc.

---

## Contexto Importante

> **AUTORIZACAO DEFINITIVA:** Esta e uma solução definitiva. Investir em modelo de dados robusto, arquitetura extensivel e testes abrangentes. Incluir auditoria completa.

---

## Fluxo do Usuário - Editar Organizacao

```
1. Admin acessa configurações da organização
2. Visualiza dados atuais
3. Edita campos desejados
4. Clica em "Salvar"
5. Dados atualizados
```

## Fluxo do Usuário - Excluir Organizacao (em branco)

```
1. Admin acessa configurações da organização
2. Clica em "Excluir organização"
3. Sistema verifica se organização esta em branco
4. Se em branco: exibe confirmação
5. Admin confirma
6. Organizacao excluida
7. Admin redirecionado para criar nova organização
```

---

## Escopo

### Dentro do escopo

* Tela de configurações da organização
* Editar nome fantasia
* Editar logo (novo upload)
* Editar CNPJ/CPF
* Excluir organização (apenas se em branco)
* Auditoria de alterações

### Fora do escopo

* Alterar tipo de organização (imobiliária ↔ corretor autonomo)
* Excluir organização com dados (deve contatar suporte)
* Transferir organização para outro admin
* Campos opcionais (razão social, endereco, etc.)

---

## Especificação de UX + Comportamento

### Tela: Configuracoes da Organizacao

**Seção: Dados da Organizacao**

**Campos editaveis:**
- Nome fantasia (obrigatório)
- Logo (upload, com preview do atual)
- CNPJ ou CPF (dependendo do tipo, validado)

**Campo readonly:**
- Tipo (Imobiliária ou Corretor Autonomo) - não editavel

**Botão:** "Salvar alterações"

**Seção: Zona de Perigo**

**Excluir organização:**
- Texto explicativo: "Ao excluir a organização, todos os dados serao removidos permanentemente."
- Botão: "Excluir organização" (destrutivo)
- Habilitado apenas se organização estiver em branco

### Validações (frontend)

| Campo | Validação |
|-------|-----------|
| Nome fantasia | Não vazio, min 2, max 100 caracteres |
| CNPJ | 14 dígitos + dígitos verificadores válidos |
| CPF | 11 dígitos + dígitos verificadores válidos |
| Logo | Imagem (JPG, PNG), max 5MB, min 200x200px |

### Definicao de "Organizacao em Branco"

Organizacao e considerada em branco se:
- Não tem outros membros (apenas o admin criador)
- Não tem leads
- Não tem conversas
- Não tem WhatsApp Business conectado

### Modal: Confirmar Exclusao

**Pre-condicao:** Organizacao esta em branco

**Conteúdo:**
- Título: "Excluir organização?"
- Texto: "Esta acao e irreversivel. Todos os dados da organização serao excluidos permanentemente."
- Input: "Digite o nome da organização para confirmar: {nome}"

**Botoes:**
- "Excluir permanentemente" (destrutivo, habilitado apenas se nome digitado corretamente)
- "Cancelar"

### Estado: Organizacao Não Pode Ser Excluida

**Conteúdo:**
- Título: "Organizacao não pode ser excluida"
- Texto: "Esta organização possui dados (membros, leads ou configurações) e não pode ser excluida automaticamente."
- Texto: "Entre em contato com o suporte para solicitar a exclusão."
- Botão: "Entrar em contato com suporte" (link para suporte)

### Estados de Erro

**Erro ao salvar:**
- Mensagem: "Não foi possível salvar as alterações. Tente novamente."

**CNPJ/CPF inválido:**
- Mensagem: "Documento inválido. Verifique os dígitos."

**Logo inválido:**
- Mensagem: "Imagem invalida. Use JPG ou PNG até 5MB."

---

## Especificações Técnicas

### API Endpoints

```
GET /api/v1/organizations/{org_id}
Headers:
  Authorization: Bearer {access_token}

Response 200:
{
  "id": "string",
  "type": "company" | "individual",
  "trade_name": "string",
  "document_type": "cnpj" | "cpf",
  "document_number": "string",
  "logo_url": "string",
  "can_be_deleted": boolean,
  "deletion_blockers": ["members", "leads", "whatsapp"] | null,
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

```
PATCH /api/v1/organizations/{org_id}
Headers:
  Authorization: Bearer {access_token}

Request:
{
  "trade_name": "string", // opcional
  "document_number": "string", // opcional
  "logo_key": "string" // opcional, chave do upload
}

Response 200:
{
  "id": "string",
  "trade_name": "string",
  "document_number": "string",
  "logo_url": "string",
  "updated_at": "ISO8601"
}

Response 400: Dados inválidos
Response 403: Sem permissao (não e admin)
```

```
DELETE /api/v1/organizations/{org_id}
Headers:
  Authorization: Bearer {access_token}

Request:
{
  "confirmation_name": "string" // nome da org para confirmar
}

Response 200:
{
  "message": "Organization deleted"
}

Response 400: Nome de confirmação incorreto
Response 403: Sem permissao ou organização não pode ser excluida
```

```
GET /api/v1/organizations/{org_id}/can-delete
Headers:
  Authorization: Bearer {access_token}

Response 200:
{
  "can_delete": boolean,
  "blockers": [
    {
      "type": "members" | "leads" | "conversations" | "whatsapp",
      "count": number
    }
  ]
}
```

### Modelo de Dados

Usa tabela `organizations` existente (Story 4).

### Logica de Verificação "Pode Excluir"

```sql
-- Organizacao pode ser excluida se:
-- 1. Apenas 1 membro (o admin criador)
SELECT COUNT(*) FROM users WHERE organization_id = ? -- deve ser 1

-- 2. Nenhum lead
SELECT COUNT(*) FROM leads WHERE organization_id = ? -- deve ser 0

-- 3. Nenhuma conversa
SELECT COUNT(*) FROM conversations WHERE organization_id = ? -- deve ser 0

-- 4. WhatsApp não conectado
SELECT whatsapp_connected FROM organizations WHERE id = ? -- deve ser false
```

### Auditoria

**Eventos a registrar:**

| Acao | Dados |
|------|-------|
| Organizacao editada | org_id, edited_by, campos_alterados, valores_antigos, valores_novos, timestamp |
| Logo alterado | org_id, edited_by, old_logo_url, new_logo_url, timestamp |
| Organizacao excluida | org_id, deleted_by, org_data_snapshot, timestamp |

---

## Critérios de Aceite

### Editar Organizacao

* Admin consegue acessar configurações da organização
* Dados atuais exibidos nos campos
* Admin pode editar nome fantasia
* Admin pode fazer upload de novo logo
* Preview do logo atual exibido
* Preview do novo logo exibido após upload
* Admin pode editar CNPJ (se imobiliária) ou CPF (se corretor)
* Tipo de organização não e editavel
* Validações de CNPJ/CPF funcionando
* Validações de logo funcionando (formato, tamanho)
* Ao salvar, dados atualizados
* Auditoria registra alterações

### Excluir Organizacao (em branco)

* Botão "Excluir" visível na zona de perigo
* Sistema verifica se organização pode ser excluida
* Se pode: modal de confirmação exibido
* Confirmacao exige digitar nome da organização
* Botão de excluir desabilitado até nome correto
* Ao confirmar, organização excluida
* Usuário desassociado da organização
* Usuário redirecionado para criar nova organização

### Organizacao Não Pode Ser Excluida

* Se organização tem dados, exibir bloqueadores
* Indicar o que impede exclusão (membros, leads, etc.)
* Oferecer link para contato com suporte

### Controle de Acesso

* Apenas admins podem editar organização
* Apenas admins podem excluir organização
* Corretores não vêem opções de edição/exclusão

### Analytics

* Analytics: evento `organization_edited` com {org_id, fields_changed, timestamp}
* Analytics: evento `organization_logo_changed` com {org_id, timestamp}
* Analytics: evento `organization_deleted` with {org_id, timestamp}
* Analytics: evento `organization_deletion_blocked` with {org_id, blockers, timestamp}

---

## Observabilidade & Analytics

### Eventos

* `organization_settings_viewed` props `{org_id, admin_id, timestamp}` trigger: ao carregar página
* `organization_edit_initiated` props `{org_id, admin_id, timestamp}` trigger: ao começar editar
* `organization_edited` props `{org_id, admin_id, fields_changed, timestamp}` trigger: ao salvar alterações
* `organization_logo_changed` props `{org_id, admin_id, timestamp}` trigger: ao alterar logo
* `organization_delete_attempted` props `{org_id, admin_id, can_delete, blockers, timestamp}` trigger: ao clicar em excluir
* `organization_deleted` props `{org_id, admin_id, timestamp}` trigger: ao confirmar exclusão
* `organization_deletion_blocked` props `{org_id, admin_id, blockers, timestamp}` trigger: quando exclusão bloqueada

### Métricas

* Taxa de edição de organizacoes
* Campos mais editados
* Taxa de exclusão de organizacoes
* Motivos de bloqueio de exclusão

---

## Dependências

* Story 4 (Criar Organizacao) deve estar completa
* Storage para logos configurado (mesmo da Story 4)

---

## Fora do Escopo

* Alterar tipo de organização (imobiliária ↔ corretor)
* Excluir organização com dados (processo via suporte)
* Campos opcionais (razão social, endereco, telefone, CRECI)
* Transferir propriedade da organização

---

## Definition of Done

* Código implementado e revisado
* Testes unitários com cobertura >80%
* Testes de integração para APIs
* Teste E2E dos fluxos (editar e excluir)
* Validações de CNPJ/CPF funcionando
* Upload de logo funcionando
* Verificação de "pode excluir" funcionando
* Auditoria implementada
* Eventos de analytics implementados
* Code review aprovado
* QA sign-off
* Deploy em staging validado

---

## Questões em Aberto

* [Design] Qual o layout/design? Link do Figma?
* [PM] Alterar CNPJ/CPF pode ter implicacoes legais?
* [PM] Processo de suporte para exclusão de org com dados?
* [Eng] Manter historico de logos antigos?

---

## Premissas

* Usuário que edita e admin da organização
* Storage para logos já configurado (mesmo da criação)
* Organizacao em branco pode ser excluida sem intervencao do suporte
* Organizacao com dados requer contato com suporte para exclusão
