## 1. Overview

### Resumo
Permitir que corretores criem, visualizem, editem e excluam anotações pessoais sobre leads para capturar informações obtidas fora da plataforma (ex: durante ligações telefônicas, visitas a imóveis, reuniões presenciais).

### Contexto & Problema
Corretores coletam informações valiosas sobre leads durante interações que acontecem fora do Loft Qualifica Leads - chamadas telefônicas, visitas a imóveis e outras conversas presenciais. Atualmente, não há um local centralizado para registrar essas informações, o que resulta em:
- Perda de contexto importante para o atendimento
- Informações fragmentadas em anotações pessoais, post-its ou memória
- Dificuldade de compartilhar insights com outros corretores da equipe
- Menor qualidade de personalização no atendimento subsequente

### Usuário-Alvo
Corretor de imóveis que acabou de realizar uma visita com um lead e precisa registrar descobertas sobre a situação familiar, flexibilidade de orçamento ou mudanças no cronograma identificadas durante a visita.

### Resultado Esperado
- **Para Usuários:** Corretores conseguem manter perfis completos dos leads com informações de todos os pontos de contato
- **Para o Negócio:** Maior qualidade dos dados de leads resulta em melhor personalização e aumento na taxa de conversão

---

## 2. Definicao de Pronto

* Todos os critérios de aceite verificados (operações CRUD completas)
* Testes unitários escritos com cobertura >80%
* Testes de integração para API de anotações
* Teste E2E para fluxo de criação, edição e exclusão
* Testes de autorização (apenas autor pode editar/excluir)
* Eventos de analytics verificados em staging
* Auditoria de acessibilidade aprovada (WCAG AA)
* Performance verificada (<500ms para salvar)
* UI otimista verificada com rollback em caso de erro
* Code review aprovado
* Design review aprovado
* QA sign-off obtido
* Feature flag configurada para rollout gradual
* Dashboards de monitoramento criados
* Plano de rollback documentado

---

## 3. Escopo

### Em Escopo
- Criar nova anotação com texto livre (max 1000 caracteres)
- Visualizar lista de anotações em ordem cronológica reversa
- Editar anotação existente (apenas pelo autor)
- Excluir anotação com confirmação (apenas pelo autor)
- Toggle "Incluir no resumo do caso" por anotação
- Estado vazio quando não há anotações
- Contador de caracteres durante digitação
- UI otimista com rollback em caso de erro
- Validação de autorização (somente autor pode editar/excluir)

### Fora de Escopo
- Anexos em anotações (imagens, arquivos)
- Menções a outros usuários (@corretor)
- Templates de anotações pré-definidos
- Histórico de revisões/versões
- Controles de visibilidade além do autor
- Busca/filtro de anotações
- Ordenação customizada

---

## 4. Especificação de UX + Comportamento

### 4.1 Layout da Seção

**Cabeçalho da Seção:**
- Título: "Anotações"
- Descrição: "Adicione informações sobre o lead adquiridas além do atendimento da plataforma"
- Botão: "+ Adicionar" (laranja, alinhado à direita)

**Lista de Anotações:**
- Ordem: cronológica reversa (mais recentes primeiro)
- Cada anotação exibe:
  - Avatar do autor (circular, 32px)
  - Label: "ADICIONADO EM: DD/MM/YYYY" (uppercase, cinza)
  - Conteúdo da anotação (texto)
  - Toggle: "Incluir no resumo do caso"
  - Ações: editar (ícone lápis), excluir (ícone lixeira)

**Estado Vazio:**
- Mensagem: "Nenhuma anotação adicionada. Clique em '+ Adicionar' para criar a primeira."

### 4.2 Fluxo de Criação

1. Corretor clica em "+ Adicionar"
2. Formulário de criação expande inline ou abre modal
3. Campo de texto multiline aparece com:
   - Placeholder: "Digite sua anotação..."
   - Contador de caracteres: "0/1000"
   - Limite visual quando próximo do máximo
4. Botões de ação:
   - "Salvar" (primário, laranja) - desabilitado se vazio
   - "Cancelar" (secundário, outline)
5. Ao salvar:
   - UI atualiza imediatamente (otimista)
   - Toast de sucesso: "Anotação salva com sucesso"
   - Se erro: rollback + toast de erro

### 4.3 Fluxo de Edição

1. Corretor clica no ícone de lápis da anotação
2. Anotação entra em modo de edição inline
3. Conteúdo atual aparece no campo de texto
4. Mesmo comportamento de salvamento da criação
5. Ao salvar: mostra data de atualização

### 4.4 Fluxo de Exclusão

1. Corretor clica no ícone de lixeira
2. Dialog de confirmação aparece:
   - Título: "Excluir anotação"
   - Mensagem: "Tem certeza que deseja excluir esta anotação? Esta ação não pode ser desfeita."
   - Botões: "Cancelar" (secundário), "Excluir" (destrutivo, vermelho)
3. Ao confirmar:
   - Anotação some imediatamente (otimista)
   - Toast de sucesso: "Anotação excluída"
   - Se erro: rollback + toast de erro

### 4.5 Toggle "Incluir no Resumo"

- Toggle switch ao lado de cada anotação
- Estado padrão: desligado (off)
- Ao alternar: salva imediatamente via API
- Anotações marcadas serão incluídas no resumo geral do lead (gerado por IA)

### 4.6 Estados de Erro

| Cenário | Comportamento |
|---------|---------------|
| Falha ao salvar | Toast: "Erro ao salvar anotação. Tente novamente." Formulário permanece aberto |
| Falha ao excluir | Toast: "Erro ao excluir anotação." Anotação permanece na lista |
| Falha ao carregar | Mensagem inline: "Erro ao carregar anotações" + botão "Tentar novamente" |
| Offline | Queue local, indicador "Salvando..." até reconexão |

### 4.7 Edge Cases

| Cenário | Comportamento |
|---------|---------------|
| Conteúdo vazio | Botão "Salvar" desabilitado |
| Excede 1000 caracteres | Bloqueia digitação, contador fica vermelho |
| Anotação muito longa | Trunca exibição com "Ver mais" expansível |
| Edições rápidas sucessivas | Debounce de 500ms no salvamento |
| Edições concorrentes | Last-write-wins (sem resolução de conflito no MVP) |
| Usuário não é autor | Ícones de editar/excluir não aparecem |

---

## 5. Especificações Técnicas

### 5.1 API Contract

#### Listar Anotações
```http
GET /api/v1/leads/{lead_id}/notes

Response 200:
{
  "notes": [
    {
      "id": "uuid",
      "content": "string (max 1000 chars)",
      "author": {
        "id": "uuid",
        "name": "string",
        "avatar_url": "string | null"
      },
      "include_in_summary": boolean,
      "created_at": "ISO8601 datetime",
      "updated_at": "ISO8601 datetime"
    }
  ]
}

Response 404:
{ "error": "lead_not_found", "message": "Lead não encontrado" }
```

#### Criar Anotação
```http
POST /api/v1/leads/{lead_id}/notes

Request Body:
{
  "content": "string (required, max 1000 chars)",
  "include_in_summary": boolean (optional, default: false)
}

Response 201:
{
  "id": "uuid",
  "content": "string",
  "author": { ... },
  "include_in_summary": boolean,
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}

Response 400:
{ "error": "validation_error", "message": "Conteúdo é obrigatório" }

Response 429:
{ "error": "rate_limit_exceeded", "message": "Limite de requisições excedido" }
```

#### Atualizar Anotação
```http
PUT /api/v1/leads/{lead_id}/notes/{note_id}

Request Body:
{
  "content": "string (optional)",
  "include_in_summary": boolean (optional)
}

Response 200:
{
  "id": "uuid",
  "content": "string",
  "author": { ... },
  "include_in_summary": boolean,
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}

Response 403:
{ "error": "forbidden", "message": "Apenas o autor pode editar esta anotação" }

Response 404:
{ "error": "note_not_found", "message": "Anotação não encontrada" }
```

#### Excluir Anotação
```http
DELETE /api/v1/leads/{lead_id}/notes/{note_id}

Response 204: (sem corpo)

Response 403:
{ "error": "forbidden", "message": "Apenas o autor pode excluir esta anotação" }

Response 404:
{ "error": "note_not_found", "message": "Anotação não encontrada" }
```

### 5.2 Modelo de Dados

```sql
CREATE TABLE lead_notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  author_id UUID NOT NULL REFERENCES users(id),
  content TEXT NOT NULL CHECK (char_length(content) <= 1000),
  include_in_summary BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

  CONSTRAINT lead_notes_content_not_empty CHECK (char_length(trim(content)) > 0)
);

CREATE INDEX idx_lead_notes_lead_id ON lead_notes(lead_id);
CREATE INDEX idx_lead_notes_author_id ON lead_notes(author_id);
CREATE INDEX idx_lead_notes_created_at ON lead_notes(lead_id, created_at DESC);
```

### 5.3 Componentes Frontend

```
src/
├── components/
│   └── LeadNotes/
│       ├── LeadNotesSection.tsx      # Container principal
│       ├── NotesList.tsx             # Lista de anotações
│       ├── NoteCard.tsx              # Card individual
│       ├── NoteForm.tsx              # Formulário criar/editar
│       ├── DeleteNoteDialog.tsx      # Modal de confirmação
│       └── EmptyNotesState.tsx       # Estado vazio
├── hooks/
│   └── useLeadNotes.ts               # Hook para CRUD
└── api/
    └── leadNotes.ts                  # Chamadas API
```

### 5.4 Segurança

| Controle | Implementação |
|----------|---------------|
| Autorização | Verificar `author_id === current_user_id` antes de UPDATE/DELETE |
| XSS | Sanitizar `content` antes de armazenar e renderizar (DOMPurify) |
| Rate Limiting | Max 10 criações/minuto por usuário |
| Input Válidation | Max 1000 caracteres, content não vazio após trim |
| SQL Injection | Usar prepared statements/ORM |

### 5.5 Performance

| Requisito | Target |
|-----------|--------|
| Tempo de salvamento | < 500ms (P95) |
| Tempo de carregamento lista | < 300ms (P95) |
| Tamanho do bundle do componente | < 15KB gzipped |

---

## 6. Critérios de Aceite

1. [ ] Seção "Anotações" exibe cabeçalho com título, descrição e botão "+ Adicionar" (laranja, alinhado à direita)
2. [ ] Clicar em "+ Adicionar" abre formulário com campo de texto multiline e contador de caracteres "0/1000"
3. [ ] Formulário possui botões "Salvar" (desabilitado se vazio) e "Cancelar"
4. [ ] Anotação salva aparece na lista com: avatar do autor, data "ADICIONADO EM: DD/MM/YYYY", conteúdo e toggle "Incluir no resumo do caso"
5. [ ] Anotações são exibidas em ordem cronológica reversa (mais recentes primeiro)
6. [ ] Cada anotação do usuário atual exibe ícones de editar (lápis) e excluir (lixeira)
7. [ ] Clicar em editar abre o conteúdo em modo de edição inline
8. [ ] Clicar em excluir exibe dialog de confirmação: "Tem certeza que deseja excluir esta anotação?"
9. [ ] Toggle "Incluir no resumo do caso" persiste estado quando alterado
10. [ ] Usuário NÃO consegue editar/excluir anotações de outros autores (ícones não aparecem)
11. [ ] Estado vazio exibe mensagem: "Nenhuma anotação adicionada. Clique em '+ Adicionar' para criar a primeira."
12. [ ] UI atualiza otimisticamente com rollback em caso de erro de API

---

## 7. Observabilidade & Analytics

### 7.1 Eventos de Analytics

| Evento | Propriedades | Trigger |
|--------|--------------|---------|
| `broker_note_created` | `{lead_id, broker_id, note_length, include_in_summary, timestamp}` | Anotação criada com sucesso |
| `broker_note_edited` | `{lead_id, note_id, broker_id, content_changed, summary_changed}` | Anotação editada com sucesso |
| `broker_note_deleted` | `{lead_id, note_id, broker_id}` | Anotação excluída com sucesso |
| `broker_note_summary_toggled` | `{lead_id, note_id, included: boolean}` | Toggle alterado |
| `broker_note_form_opened` | `{lead_id, broker_id, mode: "create" \| "edit"}` | Formulário aberto |
| `broker_note_form_cancelled` | `{lead_id, broker_id, mode, had_content: boolean}` | Formulário cancelado |
| `broker_note_error` | `{lead_id, operation, error_type, error_message}` | Erro em qualquer operação |

### 7.2 Métricas de Sucesso

| Métrica | Target | Medição |
|---------|--------|---------|
| % de leads com pelo menos 1 anotação em 7 dias | 40% | Dashboard semanal |
| Aumento de contexto capturado por lead | +25% | Comparar dados pré/pós feature |

### 7.3 Métricas de Guardrail

| Métrica | Limite | Alerta |
|---------|--------|--------|
| Tempo de salvamento (P95) | < 500ms | Slack + PagerDuty se > 800ms |
| Taxa de erro em operações | < 0.5% | Alerta se > 1% em 5 min |
| Perda de dados | 0 | Alerta imediato se detectado |

### 7.4 Logs

```json
{
  "event": "note_operation",
  "operation": "create|update|delete",
  "lead_id": "uuid",
  "note_id": "uuid",
  "broker_id": "uuid",
  "duration_ms": 123,
  "success": true,
  "error": null
}
```

---

## 8. Plano de Rollout & Riscos

### 8.1 Estrategia de Rollout

| Fase | Audiência | Duração | Critérios de Avanço |
|------|-----------|---------|---------------------|
| 1. Internal | Time interno + beta testers | 3 dias | Zero erros críticos, feedback positivo |
| 2. Canary | 5% dos usuários | 3 dias | Taxa de erro < 0.5%, P95 latência < 500ms |
| 3. Gradual | 25% → 50% → 100% | 1 semana | Métricas estáveis, sem regressões |

### 8.2 Feature Flag

```typescript
// Configuração da feature flag
{
  "feature": "lead_notes_crud",
  "enabled": true,
  "rollout_percentage": 5,
  "allow_list": ["internal_team_org_id"],
  "block_list": []
}
```

### 8.3 Plano de Rollback

**Trigger de Rollback:**
- Taxa de erro > 2% por 5 minutos
- Tempo de resposta P95 > 1s
- Qualquer incidente de perda de dados

**Procedimento:**
1. Desabilitar feature flag (tempo: 30s)
2. Notificar equipe via Slack
3. Investigar causa raiz
4. Anotações existentes permanecem no banco (não são deletadas)

---

## 9. Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Perda de dados ao salvar | Baixa | Alto | UI otimista com rollback, armazenamento local de draft |
| Acesso não autorizado a anotações | Baixa | Médio | Verificação de autorização em todas operações + testes |
| Performance degradada com muitas anotações | Média | Baixo | Páginação no backend, limite de anotações por request |
| Conflito de edições simultâneas | Baixa | Baixo | Last-write-wins (documentado), notificação de conflito em versão futura |
| XSS via conteúdo malicioso | Baixa | Alto | Sanitização server-side e client-side com DOMPurify |

---

## 10. Questões em Aberto

1. **[PM]** As anotações devem ser visíveis para todos os corretores da imobiliária ou apenas para o autor?
   - **Sugestão:** Visíveis para todos, editáveis apenas pelo autor (conforme assumido)

2. **[PM]** O que acontece com as anotações se o lead for reatribuído para outro corretor?
   - **Sugestão:** Anotações permanecem associadas ao lead, não ao corretor

3. **[Design]** A criação de anotação deve ser inline (expandir na própria seção) ou modal?
   - **Aguardando confirmação do Figma**

4. **[Backend]** Qual o limite máximo de anotações por lead?
   - **Sugestão:** Sem limite no MVP, monitorar uso

5. **[PM]** Anotações marcadas como "Incluir no resumo" devem ser processadas pela IA em tempo real ou em batch?
   - **Impacta:** Story de resumo do lead

---

## 11. Premissas

1. **Visibilidade:** Todos os corretores da mesma imobiliária podem visualizar anotações de qualquer corretor, mas apenas o autor pode editar/excluir suas próprias anotações

2. **Persistência:** Anotações persistem indefinidamente junto com o registro do lead

3. **Autenticação:** O sistema de autenticação já fornece `broker_id` e `avatar_url` do usuário logado

4. **Design System:** Componentes de UI (botões, toggles, modals, toasts) já existem no design system

5. **Story 1 Completa:** A navegação por abas (Detalhes, Interesse, Conversa, Anotações) já está implementada

6. **Analytics SDK:** SDK de analytics já está integrado no frontend

7. **Sanitização:** Biblioteca DOMPurify ou equivalente disponível para sanitização de XSS

---

## Dependências

- **Bloqueadora:** Story 1 (Header & Tab Navigation) deve estar completa
- **Backend:** Tabela `users` com campos `id`, `name`, `avatar_url`
- **Backend:** Tabela `leads` existente
- **Frontend:** Design system com componentes: Button, Toggle, Modal, Toast, Avatar, TextÁrea
- **Infra:** Feature flag system configurado

---

## Recursos & Referencias

- **Figma:** https://www.figma.com/design/3iXlzrSi8RJEt8Ae52z1Kq/Qualifica-Leads---Standalone?node-id=78-2294
- **User Story Original:** `/new-features/lead-detailed-view/user-stories.md` (Story 4)
- **Contexto do Produto:** `/context/our-product/existing-features.md`
- **Visão do Produto:** `/context/our-product/product-overview.md`
