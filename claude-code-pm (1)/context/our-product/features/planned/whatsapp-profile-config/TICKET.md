## Overview

* **Objetivo:** Permitir que administradores configurem o perfil do WhatsApp Business (nome de exibição, foto e descrição) diretamente no backoffice, sem precisar acessar o painel da Meta.
* **Quem é afetado:** Administradores de imobiliárias que querem personalizar a aparência do WhatsApp Business usado pelo assistente de IA.
* **Comportamento atual:** Configuração do perfil WhatsApp só é possível acessando o painel da Meta diretamente.
* **Comportamento desejado:** Admin acessa seção de configuração no backoffice, preenche nome/foto/descrição, vê preview em tempo real e salva. Sistema atualiza via API da Meta.
* **Por que fazer isso agora:** Reduz fricção no onboarding (usuário não precisa ir na Meta). Referência competitiva: Lais.ai já oferece essa funcionalidade.
* **Links úteis:**
    * [Meta Business Profile API](https://developers.facebook.com/docs/whatsapp/business-management-api/profile)
    * [PRD Back-office](../../../prds/backoffice-qualifica-leads.md)
    * Referência UX: Lais.ai

---

## Definição de Pronto

* Critérios de aceitação completamente satisfeitos
* Testes automatizados adicionados para validação
* Integração testada em staging com conta Meta de teste
* Eventos de analytics verificados em staging com propriedades corretas
* Preview visual funcionando corretamente
* Documentação de limites da Meta incluída (tamanho foto, caracteres)

---

## Escopo

### Dentro do escopo

* Formulário para editar nome de exibição (display name)
* Upload de foto do perfil com preview
* Campo para descrição/sobre do perfil
* Preview visual em formato de celular (como aparece no WhatsApp)
* Validação de limites da Meta (tamanho foto, caracteres)
* Chamada à API da Meta para atualizar dados
* Feedback de sucesso/erro após salvar

### Fora do escopo

* Embedded Signup (ticket separado - pré-requisito)
* Configuração do assistente (apelido, nome imobiliária) - ticket separado
* Edição de templates de mensagem
* Configuração de horário comercial
* Alteração do número de telefone

---

## Especificação de UX + Comportamento

### Pontos de entrada

* Menu de configurações > Perfil WhatsApp
* Checklist de setup na tela inicial (item "Configurar perfil")

### Fluxo

1. Admin acessa seção de configuração do perfil WhatsApp
2. Sistema carrega dados atuais do perfil (se existirem)
3. Admin visualiza formulário com campos:
   - Nome de exibição (texto, max 512 chars)
   - Foto do perfil (upload, max 5MB, formatos: JPG, PNG)
   - Descrição (texto, max 256 chars)
4. Ao lado do formulário, preview em formato celular mostra como ficará
5. Preview atualiza em tempo real conforme admin digita/faz upload
6. Admin clica em "Salvar alterações"
7. Sistema valida campos e chama API da Meta
8. Exibe feedback de sucesso ou erro

### Estados

* **Carregando:** Skeleton/loading enquanto busca dados atuais
* **Editando:** Formulário habilitado com dados preenchidos
* **Salvando:** Loading no botão "Salvar", campos desabilitados
* **Sucesso:** Toast "Perfil atualizado com sucesso!"
* **Erro (validação):** Mensagens inline nos campos inválidos
* **Erro (Meta API):** "Não foi possível atualizar o perfil. Erro: {mensagem}. Tente novamente."
* **Sem conexão:** "Conecte o WhatsApp Business primeiro" com link para Embedded Signup

---

## Especificações técnicas

### Serviços

* `GET /api/v1/whatsapp/profile` — Retorna dados atuais do perfil
* `PUT /api/v1/whatsapp/profile` — Atualiza perfil via Meta API
* `POST /api/v1/whatsapp/profile/photo` — Upload de foto (retorna URL temporária para preview)

### Endpoints

```
GET /api/v1/whatsapp/profile
Response 200:
{
  "display_name": "Imobiliária ABC",
  "about": "Sua casa dos sonhos está aqui!",
  "photo_url": "https://...",
  "phone_number": "+55 11 99999-9999"
}

Response 404: Conexão WhatsApp não existe
```

```
PUT /api/v1/whatsapp/profile
Request:
{
  "display_name": "string (max 512)",
  "about": "string (max 256)",
  "photo_base64": "string (opcional, se nova foto)"
}

Response 200:
{
  "success": true,
  "updated_at": "timestamp"
}

Response 400: Validação falhou (campos inválidos)
Response 502: Erro na API da Meta
```

### Integração com Meta API

```
PATCH https://graph.facebook.com/v18.0/{phone_number_id}/whatsapp_business_profile

Headers:
  Authorization: Bearer {access_token}

Body:
{
  "messaging_product": "whatsapp",
  "about": "Descrição do perfil",
  "profile_picture_handle": "handle_da_foto"
}
```

### Mudanças no modelo de dados

**Tabela: whatsapp_connections** (adicionar campos)
- profile_display_name (string, nullable)
- profile_about (string, nullable)
- profile_photo_url (string, nullable)
- profile_updated_at (timestamp, nullable)

### Segurança & privacidade

* Válidar tamanho máximo de upload (5MB)
* Válidar tipo de arquivo (apenas JPG, PNG)
* Sanitizar inputs de texto
* Rate limit no endpoint de upload: 10 req/min por organização
* Audit log para alterações de perfil

---

## Critérios de aceite

* Admin consegue visualizar dados atuais do perfil WhatsApp
* Admin consegue editar nome de exibição (max 512 caracteres)
* Admin consegue fazer upload de foto (max 5MB, JPG/PNG)
* Admin consegue editar descrição (max 256 caracteres)
* Preview em formato celular exibe alterações em tempo real
* Validação de campos exibe mensagens inline apropriadas
* Ao salvar, API da Meta é chamada e dados são atualizados
* Sucesso exibe toast de confirmação
* Erro da Meta exibe mensagem descritiva
* Tela exibe alerta se WhatsApp não estiver conectado
* NFR (performance): Upload de foto processa em <5s p95
* NFR (performance): Atualização na Meta completa em <10s p95
* Analytics: Evento `Profile Update Started` dispara ao iniciar edição
* Analytics: Evento `Profile Update Completed` dispara com `{fields_updated[]}`
* Analytics: Evento `Profile Update Failed` dispara com `{error_code}`

---

## Observabilidade & Analytics

### Eventos

| Evento | Descrição | Trigger | Properties |
|--------|-----------|---------|------------|
| `WhatsApp Profile Screen Viewed` | Admin visualizou tela de perfil | Tela de perfil carrega | - |
| `Profile Update Started` | Admin começou a editar | Primeiro campo modificado | - |
| `Profile Photo Uploaded` | Admin fez upload de foto | Upload concluído | `file_size_kb`, `file_type` |
| `Profile Update Completed` | Perfil atualizado com sucesso | API Meta retorna sucesso | `fields_updated[]`, `time_to_save_seconds` |
| `Profile Update Failed` | Falha ao atualizar | API Meta retorna erro | `error_code`, `error_message`, `field_failed` |

### Event Properties

| Property | Tipo | Descrição |
|----------|------|-----------|
| `fields_updated` | array | Campos que foram alterados: ["display_name", "about", "photo"] |
| `file_size_kb` | number | Tamanho da foto em KB |
| `file_type` | string | Tipo do arquivo (jpg, png) |
| `time_to_save_seconds` | number | Tempo entre clicar salvar e conclusão |
| `error_code` | string | Código de erro |
| `field_failed` | string | Campo que causou erro |

### Dashboard

* Taxa de sucesso de atualizações de perfil
* Tempo médio para atualizar perfil
* Campos mais editados (display_name, about, photo)
* Erros por tipo

### Alertas

* Taxa de erro na API Meta >30% em 1 hora → investigar
* Uploads rejeitados por tamanho >20% → verificar UX/comúnicação

---

## Plano de Rollout & Riscos

### Rollout

* **Fase 1:** Testar em staging com conta Meta de teste
* **Fase 2:** Habilitar para clientes piloto junto com Embedded Signup
* **Fase 3:** Rollout 100% junto com funcionalidades de configuração

### Rollback

1. Desabilitar acesso à tela de perfil
2. Dados existentes permanecem (apenas leitura na Meta)
3. Admin pode configurar diretamente na Meta como fallback

---

## Riscos

1. **Rate limit da Meta:** API pode ter limites de requisições → mitigar com debounce no save e cache de dados
2. **Foto rejeitada pela Meta:** Validações adicionais da Meta → exibir mensagem clara e orientar
3. **Delay na propagação:** Alterações podem demorar para aparecer no WhatsApp → informar usuário sobre delay

---

## Questões em aberto

* [Design] Qual o layout do preview em formato celular? Link do Figma? - até [TBD]
* [Eng] Quais são os rate limits exatos da Meta para esta API? - até [TBD]
* [Eng] Foto precisa ser redimensionada antes do upload? Qual tamanho ideal? - até [TBD]

---

## Premissas

* Conexão WhatsApp já foi estabelecida (Embedded Signup concluído)
* Access token da Meta está válido
* API da Meta para atualização de perfil está disponível
* Usuário tem permissão de admin na organização
