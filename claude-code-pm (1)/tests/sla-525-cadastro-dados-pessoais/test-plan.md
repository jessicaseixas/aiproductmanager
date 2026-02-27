# Test Plan: Cadastro - Dados pessoais

**Source:** Jira ticket SLA-525
**Date:** 2026-01-13
**Base URL:** (a definir - back-office Qualifica Leads)

---

## Feature Summary

Permitir que administradores de imobiliárias se cadastrem no Qualifica Leads de forma self-service. O fluxo consiste em:
1. Usuário acessa página de cadastro
2. Preenche nome, sobrenome e e-mail
3. Recebe magic link por e-mail
4. Clica no link e é autenticado automaticamente
5. Redirecionado para criar organização

**Características principais:**
- Autenticação via magic link (sem senha)
- Proteção brute force (5 tentativas em 15 min)
- Magic link expira em 24h
- Reenvio de e-mail com cooldown de 60 segundos

---

## Test Scenarios

### FUNC - Functionality Testing

| ID | Scenario | Steps | Expected Result |
|----|----------|-------|-----------------|
| FUNC-001 | Cadastro com dados válidos | Preencher nome, sobrenome, e-mail válidos e submeter | Tela "Verifique seu e-mail" exibida |
| FUNC-002 | Validação de e-mail inválido | Digitar e-mail sem @ ou formato incorreto | Mensagem de erro em tempo real |
| FUNC-003 | Validação de nome curto | Digitar nome com 1 caractere | Mensagem "mínimo 2 caracteres" |
| FUNC-004 | Campos obrigatórios vazios | Submeter formulário sem preencher campos | Validação de campos obrigatórios |
| FUNC-005 | Reenviar e-mail | Na tela de verificação, clicar "Reenviar e-mail" | E-mail reenviado, cooldown de 60s ativado |
| FUNC-006 | Usar outro e-mail | Na tela de verificação, clicar "Usar outro e-mail" | Retorna ao formulário de cadastro |
| FUNC-007 | Magic link válido | Clicar no magic link recebido por e-mail | Usuário autenticado e redirecionado |
| FUNC-008 | Magic link expirado (24h) | Clicar em magic link após 24 horas | Tela "Link expirado" exibida |
| FUNC-009 | Magic link inválido | Acessar URL com token inválido/modificado | Tela "Link inválido" exibida |

### SEC - Security Testing

| ID | Scenario | Steps | Expected Result |
|----|----------|-------|-----------------|
| SEC-001 | Brute force protection | Tentar cadastrar 6 vezes em 15 minutos | Bloqueio após 5ª tentativa |
| SEC-002 | E-mail já cadastrado | Tentar cadastrar e-mail existente | Não expõe informação, envia e-mail de segurança |
| SEC-003 | XSS no formulário | Inserir `<script>alert(1)</script>` nos campos | Script não executa, caracteres escapados |
| SEC-004 | Token manipulation | Modificar token no magic link | Acesso negado, tela de link inválido |
| SEC-005 | SQL injection | Inserir `'; DROP TABLE--` no campo e-mail | Query sanitizada, validação de formato |
| SEC-006 | HTTPS obrigatório | Acessar página via HTTP | Redireciona para HTTPS |

### USAB - Usability Testing

| ID | Scenario | Steps | Expected Result |
|----|----------|-------|-----------------|
| USAB-001 | Labels claros | Observar rótulos dos campos | Labels descritivos: "Nome", "Sobrenome", "E-mail" |
| USAB-002 | Feedback de validação | Digitar dados inválidos | Mensagens de erro claras e próximas ao campo |
| USAB-003 | Loading state | Submeter formulário | Indicador de loading durante envio |
| USAB-004 | Instruções na tela de verificação | Observar tela "Verifique seu e-mail" | Instruções claras sobre próximos passos |
| USAB-005 | Cooldown visível | Clicar "Reenviar e-mail" | Contador de 60s visível |

### RESP - Responsive Testing

| ID | Scenario | Steps | Expected Result |
|----|----------|-------|-----------------|
| RESP-001 | Mobile (375px) | Acessar formulário em iPhone SE | Layout adaptado, campos usáveis |
| RESP-002 | Tablet (768px) | Acessar formulário em iPad | Layout adaptado |
| RESP-003 | Desktop (1920px) | Acessar formulário em monitor Full HD | Layout centralizado e legível |
| RESP-004 | Touch targets | Verificar botões em mobile | Mínimo 44x44px |

### PERF - Performance Testing

| ID | Scenario | Steps | Expected Result |
|----|----------|-------|-----------------|
| PERF-001 | Page load | Medir tempo de carregamento da página | < 2 segundos (NFR) |
| PERF-002 | Envio de e-mail | Medir tempo entre submissão e resposta | < 5 segundos (NFR) |
| PERF-003 | Magic link redirect | Medir tempo de autenticação via link | < 3 segundos |

### A11Y - Accessibility Testing

| ID | Scenario | Steps | Expected Result |
|----|----------|-------|-----------------|
| A11Y-001 | Navegação por teclado | Tab entre campos do formulário | Todos campos acessíveis |
| A11Y-002 | Focus indicator | Tab entre elementos | Focus ring visível |
| A11Y-003 | Labels de formulário | Verificar inputs | Todos têm label associado |
| A11Y-004 | Mensagens de erro | Provocar erro de validação | Erro anunciado para screen reader |
| A11Y-005 | Contraste | Verificar texto e botões | Ratio mínimo 4.5:1 |

---

## Coverage Summary

| Category | Scenarios |
|----------|-----------|
| Functionality | 9 |
| Security | 6 |
| Usability | 5 |
| Responsive | 4 |
| Performance | 3 |
| Accessibility | 5 |
| **Total** | **32** |

---

## Notes

### Assumptions
- Base URL será configurada via variável de ambiente `BASE_URL`
- Magic link tests (FUNC-007) requerem acesso ao serviço de e-mail ou mock
- Brute force test (SEC-001) pode precisar de reset entre execuções

### Dependencies
- Serviço de e-mail configurado para testes de magic link
- Ambiente de teste com proteção brute force resetável

### Recommendations for Manual Testing
- **FUNC-007 (Magic link válido):** Testar manualmente o fluxo completo com e-mail real
- **SEC-002 (E-mail já cadastrado):** Verificar que e-mail de segurança é enviado (não expõe se existe)
- **PERF-002 (Envio de e-mail < 5s):** Medir tempo real de entrega do e-mail

### Areas Needing More Detail
- Template do e-mail de verificação (para validar conteúdo)
- Exata mensagem de erro para cada cenário de validação
- Comportamento específico do cooldown de reenvio (visual countdown?)
