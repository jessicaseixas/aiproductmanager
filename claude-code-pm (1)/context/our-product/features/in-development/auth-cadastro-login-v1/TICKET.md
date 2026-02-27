# Overview

* **Objetivo:** Permitir que usuários acessem o backoffice do Qualifica Leads Standalone através do Login Loft, com cadastro manual feito pela Squad e primeiro acesso via fluxo de recuperação de senha.
* **Quem é afetado:** Administradores de imobiliárias que contratam o Qualifica Leads Standalone.
* **Comportamento atual:** N/A - Nova funcionalidade. Não existe acesso ao backoffice standalone.
* **Comportamento desejado:** Usuário é pré-cadastrado pela Squad, recebe orientação para acessar "Recuperar senha", cadastra sua senha via Login Loft e é direcionado ao onboarding.
* **Por que fazer isso agora:** É o ponto de entrada obrigatório para usar o produto. Sem autenticação, ninguém consegue acessar o backoffice.
* **Links úteis:**
    * [Login Loft: [TBD @eng]]
    * [Figma/Design: N/A - usaremos telas do Login Loft]

---

# Definição de Pronto

* Endpoints de cadastro manual funcionando e documentados
* Integração com Login Loft funcionando
* Fluxo de recuperação de senha testado end-to-end
* Usuário consegue fazer login após cadastrar nova senha
* Após primeiro login, usuário é redirecionado para onboarding
* Eventos de analytics verificados em staging
* Documentação de como fazer o cadastro manual criada

---

# Escopo

## Dentro do escopo

* Endpoints para cadastro manual de usuário (admin)
* Endpoints para cadastro manual de organização (imobiliária)
* Integração com Login Loft para autenticação
* Usar tela de "Recuperar senha" do Login Loft (funcionalidade existente)
* Usar tela de "Cadastrar nova senha" do Login Loft (funcionalidade existente)
* Redirecionamento para fluxo de onboarding após primeiro login (ver [SLA-556](https://loftbr.atlassian.net/browse/SLA-556))
* Documentação interna de como fazer o pré-cadastro

## Fora do escopo

* Cadastro self-service (usuário se cadastra sozinho)
* Telas próprias de Login (usaremos Login Loft)
* Telas próprias de Recuperar Senha (usaremos Login Loft)
* Telas próprias de Cadastrar Nova Senha (usaremos Login Loft)
* Alterar regras de senha do Login Loft
* Autenticação via magic link
* Validação de CRECI
* Cadastro de corretores (apenas admin no MVP)
* 2FA
* Login social (Google, Apple)

---

# Especificação de UX + Comportamento

## Fluxo completo (cadastro até primeiro login)

```
1. Usuário entra em contato com a Loft demonstrando interesse no produto
2. Time Comercial da Loft faz primeira abordagem (tirar dúvidas, confirmar contratação)
3. Time Comercial abre chamado para nossa Squad cadastrar usuário e imobiliária
4. Nossa Squad faz pré-cadastro do usuário (admin) e sua imobiliária via endpoints
5. Squad envia e-mail para usuário com instruções de primeiro acesso
6. Usuário acessa URL do backoffice → é redirecionado para Login Loft
7. Usuário clica em "Recuperar senha" e preenche seu e-mail
8. Usuário recebe e-mail com link de recuperação de senha
9. Usuário clica no link e cadastra nova senha (tela do Login Loft)
10. Usuário é redirecionado para o primeiro passo do fluxo de onboarding (SLA-556)
```

> **Nota:** Todas as telas de autenticação (login, recuperar senha, cadastrar nova senha) são do Login Loft. Seguiremos os requisitos de senha já existentes do Login Loft - não vamos alterar regras de senha.

## Estados

* **Sucesso:** Senha cadastrada via Login Loft, usuário autenticado e redirecionado para onboarding
* **Erro (token expirado):** Tratado pelo Login Loft
* **Erro (token inválido):** Tratado pelo Login Loft
* **Erro (validação de senha):** Tratado pelo Login Loft (seguindo regras existentes)

---

# Especificações técnicas

## Serviços

### Endpoints de cadastro manual (uso interno da Squad)

```
POST /api/v1/admin/users
Request:
{
  "email": "string",
  "full_name": "string",
  "phone": "string",        // Com DDD
  "role": "admin"
}

Response 201:
{
  "id": "uuid",
  "email": "string",
  "full_name": "string",
  "phone": "string",
  "role": "admin",
  "organization_id": null,
  "created_at": "timestamp"
}

Response 400: Dados inválidos
Response 409: E-mail já cadastrado
```

```
POST /api/v1/admin/organizations
Request:
{
  "name": "string",              // Nome da imobiliária
  "cnpj": "string",              // CNPJ (opcional)
  "admin_user_id": "uuid"        // ID do usuário admin
}

Response 201:
{
  "id": "uuid",
  "name": "string",
  "cnpj": "string",
  "admin_user_id": "uuid",
  "created_at": "timestamp"
}

Response 400: Dados inválidos
Response 404: Usuário não encontrado
```

## Integração com Login Loft

* Redirecionar usuários não autenticados para Login Loft
* Receber callback do Login Loft com token de autenticação
* Validar token e criar sessão no backoffice
* Usar fluxo de "Recuperar senha" existente do Login Loft
* Seguir requisitos de senha já definidos pelo Login Loft
* [TBD @eng] Documentação de integração com Login Loft

## Mudanças no modelo de dados

> **Nota:** Usaremos as tabelas existentes do Login Loft (users, business_user/organization). Precisamos mapear apenas dados adicionais que persistimos do nosso lado.

**Dados adicionais do Qualifica Leads (a definir):**
- [TBD] Campos específicos do produto que não existem no Login Loft

## Segurança & privacidade

* Endpoints de cadastro manual (`/api/v1/admin/*`) requerem autenticação interna da Squad
* Não logar tokens completos
* Requisitos de senha gerenciados pelo Login Loft (não alteramos)

---

# Critérios de aceite

* Squad consegue cadastrar usuário via endpoint `/api/v1/admin/users`
* Squad consegue cadastrar organização via endpoint `/api/v1/admin/organizations`
* Organização é associada corretamente ao usuário admin
* Usuário não autenticado é redirecionado para Login Loft
* Usuário consegue usar "Recuperar senha" do Login Loft
* E-mail de recuperação é enviado pelo Login Loft
* Usuário consegue cadastrar nova senha via Login Loft
* Após cadastrar senha, usuário é autenticado automaticamente
* Após autenticar, usuário é redirecionado para onboarding (SLA-556)
* NFR: Redirecionamento para Login Loft em <2 segundos
* Analytics: Eventos implementados conforme seção "Observabilidade"

---

# Observabilidade & Analytics

## Eventos

| Evento | Descrição | Trigger | Properties |
|--------|-----------|---------|------------|
| `User Created (Admin)` | Usuário criado via endpoint admin | Squad cria usuário com sucesso | `user_id`, `email_domain` |
| `User Creation Failed (Admin)` | Falha ao criar usuário via endpoint admin | Erro no endpoint de criação | `error_type`, `error_message` |
| `Organization Created (Admin)` | Organização criada via endpoint admin | Squad cria organização com sucesso | `organization_id`, `user_id` |
| `Organization Creation Failed (Admin)` | Falha ao criar organização via endpoint admin | Erro no endpoint de criação | `error_type`, `error_message` |
| `Password Reset Requested` | Usuário solicitou recuperação de senha | Clique em "Esqueci minha senha" no Login Loft | `email_domain` |
| `Password Reset Email Sent` | E-mail de recuperação de senha enviado | Login Loft confirma envio | `email_domain` |
| `First Login Completed` | Usuário completou primeiro login após cadastro | Primeiro login bem-sucedido | `user_id`, `time_since_creation_hours` |
| `Onboarding Redirect` | Usuário redirecionado para onboarding | Após primeiro login | `user_id` |

## Métricas

| Level | Métrica | Descrição | Fórmula |
|-------|---------|-----------|---------|
| **Focus** | Taxa de Ativação de Usuários | % de usuários cadastrados que completam primeiro login | `First Login Completed / User Created (Admin)` |
| **L1 - Activation** | Time-to-First-Login | Tempo entre cadastro e primeiro login | `Mediana de horas entre User Created e First Login Completed` |
| **L1 - Activation** | Taxa de Conclusão de Senha | % de usuários que cadastraram senha após solicitar recuperação | `First Login Completed / Password Reset Requested` |
| **L1 - Funnel** | Taxa de Envio de E-mail | % de solicitações de senha que resultaram em e-mail enviado | `Password Reset Email Sent / Password Reset Requested` |
| **L1 - Operations** | Taxa de Sucesso no Cadastro Admin | % de cadastros de usuário bem-sucedidos pela Squad | `User Created / (User Created + User Creation Failed)` |
| **L1 - Operations** | Taxa de Sucesso na Criação de Org | % de organizações criadas com sucesso | `Org Created / (Org Created + Org Creation Failed)` |

## Funil de Onboarding

```
User Created → Password Reset Requested → Email Sent → First Login Completed → Onboarding Redirect
```

## Alertas

* Taxa de erro nos endpoints admin >10% em 1 hora (investigar)
* Zero novos usuários criados por >7 dias (verificar processo comercial)
* Taxa de falha no envio de e-mail de recuperação >5% (investigar)

---

# Riscos

1. **Dependência do Login Loft:** Se Login Loft tiver instabilidade, usuários não conseguem acessar → mitigar com monitoramento e comunicação rápida
2. **Processo manual:** Cadastro manual pode ser gargalo se volume aumentar → mitigar documentando bem o processo e planejando self-service futuro
3. **Integração com Login Loft:** Complexidade técnica desconhecida → mitigar com spike técnico antes do desenvolvimento

---

# Questões em aberto

* [Eng] Como funciona a integração com Login Loft? Documentação disponível?
* [Eng] Login Loft suporta o fluxo de "primeiro acesso" (usuário sem senha)?
* [Eng] Quais dados persistimos do nosso lado vs. dados já capturados pelo Login Loft (users e organizations/business_user)?
* [Eng] Qual a estrutura de tabelas do Login Loft que vamos usar?
* [PM] Qual o processo exato que o time comercial vai seguir para solicitar cadastros?

---

# Premissas

* Não criaremos novas telas para Login, Recuperar Senha ou Cadastrar Nova Senha - usaremos as do Login Loft
* Não alteraremos regras de senha - seguiremos os requisitos já existentes do Login Loft
* Não validaremos se o usuário é mesmo daquela imobiliária (validação manual pelo time comercial)
* Login Loft está disponível e funcional para integração
* Volume inicial de cadastros é baixo (processo manual é aceitável no MVP)
