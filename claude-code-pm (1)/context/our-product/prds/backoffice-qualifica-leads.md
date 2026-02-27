# PRD: Back-office Qualifica Leads

**Autor:** Product Team
**Data:** Janeiro 2026
**Status:** Draft
**Última revisão:** 12/Jan/2026

> Plataforma que permite configurar e operar o Qualifica Leads de forma independente de CRM, habilitando o produto standalone para imobiliárias que usam qualquer CRM do mercado.

---

## 1. Background & Problem Statement

### Situação Atual

O Qualifica Leads já qualifica leads via WhatsApp com IA, mas hoje:
- Clientes do Loft/CRM visualizam dados na interface existente do CRM
- Clientes standalone (lançamento Abr/2026) não terão onde gerenciar os leads qualificados
- Concorrentes (Lais.ai, Morada.ai) já oferecem soluções integradas com CRMs

### Problema

Imobiliárias pequenas e médias enfrentam dificuldades críticas na gestão de leads:

| Dor | Impacto | Evidência |
|-----|---------|-----------|
| **Perda de leads para corretores** | Corretores saem da imobiliária e levam contatos | Validada - dor frequente em entrevistas |
| **Falta de visibilidade** | Imobiliária não sabe o que IA conversou com lead | Feedback de clientes |
| **Dados descentralizados** | Info em WhatsApp pessoal, planilhas, CRMs | Observação de mercado |
| **Resposta lenta** | Média 6h para responder vs 5 min ideal | Dados de mercado |

### Por Que Agora?

1. **Lançamento standalone em Abr/2026** exige interface de gestão
2. **Concorrência acelerada**: Lais.ai (+500 imobiliárias, US$15M Series A) e Morada.ai (R$17M captados) já tem tração
3. **Oportunidade de mercado**: ~40% dos corretores (~230 mil) não usam CRM estruturado
4. **Diferenciação possível**: Concorrentes integram com CRM, não substituem

### User Pain Points

1. Corretores que saem da imobiliária levam os leads consigo (WhatsApp pessoal)
2. Sem visibilidade sobre qualidade do atendimento da IA
3. Dificuldade em priorizar leads quentes vs frios
4. Informações fragmentadas entre múltiplos sistemas
5. Distribuição manual de leads e ineficiente e lenta

---

## 2. Goals & Success Metrics

### Primary Goal

Criar uma plataforma que aumente a adoção e stickiness do Qualifica Leads, oferecendo gestão de leads com proteção dos contatos da imobiliária.

### Success Metrics

| Métrica | Target | Método de Medição |
|---------|--------|-------------------|
| **DAU/MAU** | >30% | Analytics (Mixpanel/Amplitude) |
| **Retenção D30** | >50% | Cohort analysis |
| **Taxa de Ativação** | >60% completam setup em 24h | Funnel analytics |
| **NPS** | >30 | Pesquisa in-app |
| **Tempo médio resposta lead** | <1h | Tracking de mensagens |
| **Redução churn Qualifica Leads** | >20% | Comparação com baseline |

### Out of Scope (MVP)

- Regras automáticas de distribuição de leads
- Dashboards de inteligência/insights avançados
- Integrações com CRMs de terceiros
- App mobile nativo
- Gestão de catálogo de imóveis
- Criação de anúncios
- Site builder

---

## 3. Target Users

### Persona Primária: Dono/Gerente de Imobiliária Pequena/Média (com CRM)

| Atributo | Descrição |
|----------|-----------|
| **Perfil** | Imobiliárias que já usam CRM de terceiros (Kenlo, Superlogica, C2S, etc.) |
| **Tamanho** | 2-10 corretores |
| **Dor principal** | Qualificação manual de leads é lenta e ineficiente |
| **Necessidade** | Automatizar triagem de leads antes de enviar ao CRM |
| **Comportamento** | Já tem processo estruturado no CRM, quer otimizar a entrada de leads |

> **Decisão estratégica (08/Jan/2026):** O MVP foca em imobiliárias que já possuem CRM. Imobiliárias sem CRM não são público-alvo desta primeira entrega, pois não teriam onde visualizar os leads qualificados (o back-office MVP não inclui listagem de leads).

### Persona Secundária: Corretor Autônomo (Fase 2+)

| Atributo | Descrição |
|----------|-----------|
| **Perfil** | ~230 mil corretores sem CRM no Brasil |
| **Comportamento** | Usa WhatsApp + planilha para gerenciar leads |
| **Sensibilidade** | Muito sensível a preço |
| **Necessidade** | Simplicidade e organização |
| **Dor principal** | Perder leads por falta de organização |

> **Nota:** Este público só será atendido quando o back-office incluir listagem de leads e chat (Fase 2).

### User Motivations

- **Proteger invéstimento em leads** (custo de aquisição via portais e ads)
- **Ter visibilidade** sobre o que esta acontecendo com cada lead
- **Responder mais rápido** para aumentar conversão
- **Não depender de ferramentas caras** (CRMs com mensalidade alta)

---

## 4. Solution & Requirements

### High-Level Solution

Back-office gratuito com chat centralizado via WhatsApp Business API, onde:
1. Leads são qualificados pela IA e aparecem na listagem
2. Corretor responde pelo sistema (sem acesso ao telefone do lead)
3. Imobiliária mantem controle total dos contatos
4. Historico completo (IA + humano) fica disponível

### Posicionamento vs Concorrência

| Dimensão | Lais.ai | Morada.ai | Qualifica Leads |
|----------|---------|-----------|-----------------|
| Modelo | Complementa CRM | Complementa CRM | **Funciona sem CRM** |
| Preço | ~R$2.000/mes fixo | Variável | Pay-per-use (gratuito back-office) |
| Proteção leads | Não | Não | **Chat centralizado** |
| Target | Quem tem CRM | Incorporadoras | **Quem não tem CRM** |

### Functional Requirements

#### MVP: Set Mínimo

##### Autenticação & Onboarding

> **Decisão (08/Jan/2026):** Email é a chave de acesso (não telefone). Telefone compartilhado entre corretores causa problemas de unicidade.

> **Decisão (09/Jan/2026):** Login via magic link (OTP por email) ao invés de senha. Simplifica MVP eliminando necessidade de "esqueci minha senha" e "trocar senha". Senha e MFA ficam para versão futura.

- [ ] Sign Up com email e confirmação via OTP
- [ ] Sign In via magic link (link enviado por email, sem senha)
- [ ] Criar organização (imobiliária) - fica em status "pendente"
- [ ] Aceitar Termos de Uso do produto ao criar organização (ver seção "Aceite de Termos e Simulação")
- [ ] Convidar outros admins por email (todos com acesso total)

> **Nota:** No MVP, todos os usuários são administradores com mesmas permissões. Não há perfil de corretor - gestão de roles fica para Fase 2.

> **Nota técnica:** Avaliar se a plataforma de identidade da Loft já tem suporte a magic link. Se tiver, usar. Se não, implementar solução simples.

##### Emails Transacionais

> **Decisão (12/Jan/2026):** Definir copy dos emails de segurança. Não expor na tela se email já existe (prevenção de enumeração).

- [ ] Email de confirmação de cadastro (OTP/magic link)
- [ ] Email de login (magic link)
- [ ] Email de segurança: se tentar cadastrar com email que já existe, não mostrar na tela "este email já está cadastrado" - em vez disso, mostrar mensagem genérica ("enviamos um email de verificação") e enviar email informando que já existe conta
- [ ] Email de convite para novos admins

> **Próximo passo:** Definir copy exato dos emails com time de conteúdo/marketing.

##### Cadastro da Organização

> **Decisão (09/Jan/2026):** Campos mínimos para cadastro da empresa. Verificar se CNPJ já existe na base Loft para reaproveitar dados.

> **Decisão (12/Jan/2026):** Incluir campos de responsáveis para questões legais e financeiras. Dados serão armazenados no banco próprio do Qualifica Leads (autenticação será própria, não usa Loft).

- [ ] CNPJ (obrigatório)
- [ ] Razão social
- [ ] Nome fantasia
- [ ] Responsável legal/proprietário (nome, email, telefone)
- [ ] Responsável financeiro (nome, email) - quem recebe notas e trata pagamentos
- [ ] Responsável pela implantação (nome, email) - se diferente do usuário que está cadastrando
- [ ] Se usuário que está cadastrando é um dos responsáveis acima, não pedir dados duplicados
- [ ] Verificar se CNPJ já existe na base Loft (integração com sistema de identidade)
- [ ] Se já existe: reaproveitar dados existentes
- [ ] Se não existe: criar novo registro

> **Nota:** Responsável legal e responsável pela implantação são considerados responsáveis legais pela conta. Responsável financeiro pode ser pessoa diferente (ex: setor financeiro da empresa).

##### Pergunta sobre CRM (Elegibilidade e Cross-sell)

> **Decisão (09/Jan/2026):** Perguntar sobre CRM durante cadastro para validar elegibilidade e gerar oportunidades de cross-sell.

- [ ] Perguntar: "Você já usa algum CRM?"
  - **Sim, uso outro CRM** → Qual? (lista: Kenlo, Superlogica, C2S, Outro)
  - **Sim, uso o CRM Loft** → Direcionar para fluxo do CRM Loft
  - **Não tenho CRM** → Ver tratamento abaixo

- [ ] Se não tem CRM:
  - Produto **não disponível** no MVP (não há onde visualizar leads)
  - Oferecer: "Quer entrar na lista de espera?"
  - Oferecer: "Conheça o CRM Loft Light (gratuito)" → Gerar lead para comercial
  - Registrar interesse para métricas de demanda

> **Oportunidade:** Gerar leads qualificados para o time comercial do CRM Loft. Pode virar métrica de originação de vendas do Qualifica Leads.

##### Validação de Organização

> **Decisão (08/Jan/2026):** O primeiro usuário cria a organização, mas ela fica em status "pendente" até validação pelo time da Loft. Isso garante que apenas pessoas autorizadas (ex: sócios no contrato social) representem a imobiliária.

> **Decisão (09/Jan/2026):** Validação pode ser feita consultando QSA (Quadro de Sócios e Administradores) na Receita Federal. Processo manual pelo time no MVP.

- [ ] Organização criada fica com status "Pendente de Validação"
- [ ] Usuário vê mensagem: "Sua organização está em análise. Nosso time entrará em contato."
- [ ] Time Loft valida se usuário está no QSA do CNPJ (consulta manual na Receita Federal)
- [ ] Após aprovação, organização fica ativa e usuário pode prosseguir com setup

> **Nota:** Validação automática via API de birô (ex: Serasa) tem custo. MVP usa validação manual.

##### Aceite de Termos e Simulação

> **Decisão (12/Jan/2026):** Incluir passo de aceite de termos com resumo dos principais pontos e calculadora de custos. Objetivo é evitar que cliente chegue na implantação sem entender o produto e depois cancele (já aconteceu casos de cliente achar que era "imobiliária no ChatGPT").

- [ ] Tela de aceite com resumo dos principais pontos (não tijolo de texto):
  - Pode cancelar a qualquer momento
  - Pagamento é pós-pago (paga só o que consumir)
  - Não paga por leads que não responderam
  - Quanto mais leads atender, menor o custo unitário
- [ ] Calculadora de custos integrada na tela:
  - Input: "Quantos leads você quer atender por mês?"
  - Output: Estimativa de custo mensal
- [ ] Link para termos completos (TCG Loft + termos específicos do produto)
- [ ] Checkbox de aceite obrigatório para prosseguir
- [ ] Opcional: Link para vídeo explicativo do Qualifica Leads

> **Importante:** Evitar excesso de informação que gere atrito no cadastro. O objetivo é confirmar entendimento, não assustar o usuário. Ser leve e direto.

> **Nota:** Termos específicos do produto referenciam os Termos Gerais de Contratação (TCG) da Loft. Termos específicos são sucintos e cobrem pontos como responsabilidade sobre ações da Meta.

##### Forma de Pagamento

> **Decisão (12/Jan/2026):** Não definir forma de pagamento no MVP por enquanto. Aguardar definição do modelo de faturamento pelo time financeiro. Provavelmente será boleto (padrão dos outros produtos Loft).

- [ ] TBD - Aguardando definição do modelo de faturamento

> **Próximo passo:** Quando modelo de faturamento for definido, voltar aqui e incluir fluxo de cadastro de forma de pagamento no onboarding.

##### Tela Inicial (Dashboard de Consumo)

> **Decisão (08/Jan/2026):** A tela inicial é focada em configurações e consumo. Não há listagem de leads no MVP - cliente visualiza leads no CRM dele.

- [ ] Contadores de atendimentos com linguagem clara:
  - **Leads atendidos pela IA** (total)
  - **Com imóvel definido** (chegaram a identificar preferência de imóvel)
  - **Com interesse de visita** (manifestaram interesse em visitar)
- [ ] Visão de consumo do mês (quanto vai pagar)
- [ ] Destaque de economia gerada:
  - "Você economizou R$X com leads que não responderam"
  - "Você não pagou por X atendimentos incompletos"
- [ ] Indicação clara de gratuidade promocional:
  - "Período gratuito até Mar/2026"
  - "Quanto você pagaria: R$X" (para mostrar valor)
- [ ] Atendimentos abonados (não cobrados):
  - Lead nunca respondeu
  - Lead não alcançado (número errado, mensagem não entregue pela Meta)
- [ ] Alerta de setup incompleto (ex: "Você ainda não configurou meio de pagamento na Meta")

> **Nota sobre linguagem:** Evitar termo "qualificado" isolado, pois causa confusão. Algumas pessoas entendem como "lead quente" quando na verdade significa "passou pelo processo de triagem".

##### Configuração do Assistente
- [ ] Definir apelido do assistente (como ele se identifica)
- [ ] Definir nome da imobiliária (aparece na mensagem inicial: "Sou assistente da [nome]")

##### Configuração do Perfil WhatsApp

> **Decisão (08/Jan/2026):** Trazer configurações do WhatsApp para a própria plataforma, reduzindo fricção de ter que acessar o painel da Meta. Similar à experiência da Lais.ai que tem tela com preview de como vai aparecer no WhatsApp.

- [ ] Nome de exibição (display name) do perfil WhatsApp
- [ ] Foto do perfil
- [ ] Descrição/sobre do perfil
- [ ] Preview visual de como vai aparecer no WhatsApp (formato celular)

> **Nota técnica:** Usar APIs da Meta para atualizar esses dados. A Lais.ai já faz isso - referência de UX.

##### Configuração das Regras de Distribuição

> **Em aberto (08/Jan/2026):** Talvez não seja necessário no MVP. A configuração de canais de origem e tipos de negócio pode já estar disponível na configuração do portal (ex: Portal Pro do Grupo OLX). Precisamos validar com os portais antes de implementar.

- [ ] ~~Selecionar canais de origem de leads (quais portais/fontes direcionam para o Qualifica)~~ - **TBD**
- [ ] ~~Selecionar tipos de negócio qualificados (venda, aluguel, ou ambos)~~ - **TBD**

> **Próximo passo:** Conversar com Grupo OLX para entender o que já é possível configurar no portal e o que precisamos fazer do nosso lado.

##### Pergunta sobre Número de Telefone

> **Decisão (09/Jan/2026):** Perguntar sobre número durante cadastro para preparar o time comercial. Importante deixar claro que o número deve ser exclusivo para qualificação de leads.

- [ ] Perguntar: "Você já tem um número de telefone para usar?"
  - **Sim, tenho número** → Perguntar: "Esse número já está no WhatsApp Business?"
    - **Sim** → Fluxo de coexistência (pode fazer sozinho ou com suporte)
    - **Não** → Precisa migrar para WhatsApp Business primeiro
  - **Não, preciso de número novo** → Compra de número via suporte (não automatizado no MVP)

- [ ] Exibir aviso: "Importante: esse número será usado exclusivamente para qualificação de leads. Todas as conversas ficarão visíveis na plataforma."

> **Nota:** A compra automática de número foi descartada do MVP devido à complexidade (reserva de número, custos antes da assinatura, cancelamento).

##### Conexão WhatsApp Business (Embedded Signup)

> **Decisão (09/Jan/2026):** Embedded Signup não será self-service no MVP. Usuário faz cadastro e comercial guia o processo de ativação. Isso reduz complexidade e garante sucesso na configuração.

**Fluxo MVP (Guiado):**
- [ ] Usuário completa cadastro (conta + empresa + preferências de número)
- [ ] Sistema exibe: "Nosso time entrará em contato para ativar sua conta"
- [ ] Comercial recebe notificação de novo cadastro
- [ ] Comercial agenda reunião de ativação
- [ ] Durante reunião, comercial guia usuário pelo Embedded Signup
- [ ] Se usuário precisa comprar número: comercial faz a compra na Salve/Twilio

**Usuário com número próprio (coexistência):**
- [ ] Pode iniciar Embedded Signup sem esperar comercial (opcional)
- [ ] Tela com instruções passo a passo antes de iniciar
- [ ] Link para manual/documentação de apoio
- [ ] Se travar, aguardar suporte

**Requisitos técnicos:**
- [ ] Fluxo de login no Facebook Business
- [ ] Criar nova WhatsApp Business Account (WABA)
- [ ] Vincular número de telefone (coexistência)
- [ ] Configurar método de pagamento na Meta (cartão de crédito)
- [ ] Validar conexão ativa

> **Melhoria futura:** Automatizar mais etapas do Embedded Signup, trazer configuração de cartão para dentro da plataforma (evitar usuário ir para Meta).

##### Sincronização de Catalogo
- [ ] Configurar URL do XML de imóveis
- [ ] Visualizar status da última sincronização
- [ ] Visualizar quantidade de imóveis ativos

> **Nota:** Frequencia de sincronização sera padrão do sistema (a cada 12-24h).

##### Integração com Portais (Entrada de Leads)
- [ ] Configurar integração com Grupo OLX (OLX, ZAP, Viva Real)
- [ ] Configurar integração com Chaves na Mão
- [ ] Configurar integração com Facebook Ads
- [ ] Visualizar status da integração
- [ ] Endpoint para receber leads dos portais

##### Integração com CRMs (Saida de Leads)
- [ ] Configurar integração com Kenlo
- [ ] Configurar integração com Superlogica
- [ ] Configurar integração com C2S
- [ ] Mapear campos do lead para formato do CRM
- [ ] Visualizar status da integração
- [ ] Log de leads enviados (sucesso/erro)

---

#### Fase 2: Gestão de Leads (pós-validação)

##### Gestão de Leads
- [ ] Listagem páginada de todos os atendimentos
- [ ] Filtros por status, tipo de negócio, origem, data
- [ ] Busca por nome/telefone
- [ ] Ordenação por data, status, relevância
- [ ] Visualizar detalhes do lead (resumo IA, contato)
- [ ] Visualizar histórico completo da conversa (IA + humano)
- [ ] Visualizar imóveis de interesse do lead
- [ ] Adicionar anotações sobre o lead

##### Chat Centralizado (Diferencial de Retenção)
- [ ] Corretor responde lead via interface do back-office
- [ ] Integração com WhatsApp Business API
- [ ] Mensagem chega no WhatsApp do lead de forma transparente
- [ ] Lead nunca ve que corretor mudou (experiência continua)
- [ ] Corretor NAO tem acesso ao telefone do lead
- [ ] Historico unificado (conversa IA + conversa humana)
- [ ] Notificação de nova mensagem recebida

##### Gestão de Usuários
- [ ] Convidar membros (corretores)
- [ ] Gerenciar usuários (admin)
- [ ] Editar perfil pessoal
- [ ] Recuperação de senha via email

##### Distribuição de Leads
- [ ] Admin visualiza leads não distribuidos
- [ ] Admin distribui lead para corretor especifico (manual)
- [ ] Corretor so ve leads atribuidos a ele
- [ ] Notificação quando lead e atribuido

### Non-Functional Requirements

| Categoria | Requisito |
|-----------|-----------|
| **Performance** | Listagem carrega em <2s com 1000+ leads |
| **Disponibilidade** | 99.5% uptime |
| **Seguranca** | Autenticação JWT, HTTPS obrigatório |
| **Escalabilidade** | Suportar 10.000 usuários simultâneos |
| **Responsividade** | Funcionar em desktop e mobile (web responsivo) |

---

## 5. MVP

### Hipótese a Validar

> **Acreditamos que** imobiliárias que usam CRMs de terceiros vao contratar o Qualifica Leads standalone **porque** a qualificação automatizada via IA resolve a dor de resposta lenta e triagem manual, e o modelo pay-per-use e mais acessível que soluções com mensalidade fixa.

### O Que Precisamos Aprender

1. **O fluxo de integração funciona?** (leads chegam no CRM do cliente corretamente)
2. **O cadastro self-service é simples o suficiente?** (usuário completa sem desistir)
3. **A ativação guiada é eficiente?** (tempo de ativação, sucesso na primeira tentativa)
4. **O assistente performa bem com catálogos externos?** (qualidade da busca)
5. **Há demanda real por standalone?** (conversão de interessados)
6. **Quantos usuários precisam comprar número vs já têm?** (dimensionar esforço comercial)

### Estratégia: Set Mínimo Primeiro

Ao invés de construir um back-office completo, comecaremos com o **set mínimo** necessário para operar o Qualifica Leads de forma standalone. Isso permite:

1. Validar demanda real antes de invéstir em features adicionais
2. Lancar mais rápido (Mar/2026)
3. Aprender com clientes reais quais features agregam valor
4. Evitar construir funcionalidades que usuários de CRM já tem

### MVP Scope: Set Mínimo

> **Atualizado (09/Jan/2026):** Foco em configuração + consumo. Modelo híbrido (cadastro self-service + ativação guiada). Público-alvo são imobiliárias com CRM.

| Feature | Prioridade | Justificativa |
|---------|------------|---------------|
| Cadastro de usuário (magic link) | P0 | Login sem senha, simplifica MVP |
| Cadastro da imobiliária (CNPJ, razão social, nome fantasia) | P0 | Com validação manual pela Loft |
| Pergunta sobre CRM | P0 | Validar elegibilidade + cross-sell CRM Loft |
| Pergunta sobre número de telefone | P0 | Preparar comercial para ativação |
| Múltiplos admins | P0 | Convidar por email, todos com acesso total |
| Tela inicial (dashboard de consumo) | P0 | Visão de atendimentos, consumo e economia |
| Configuração do assistente | P0 | Apelido e nome da imobiliária |
| Configuração do perfil WhatsApp | P0 | Nome, foto, descrição (durante ativação guiada) |
| Conexão WhatsApp Business (guiada) | P0 | Embedded Signup com suporte do comercial |
| Sincronização de catálogo (XML) | P0 | Base para buscas do assistente |
| Integração com portais | P0 | Receber leads (fonte de entrada) |
| Integração com CRMs | P0 | Enviar leads qualificados (destino) |
| Checklist de setup | P0 | Indicadores visuais de progresso |
| Manual/instruções do Embedded Signup | P0 | Apoio para usuários que tentam sozinhos |
| Assistente de ajuda | P1 | Reduz carga no time de implantação |
| ~~Regras de distribuição~~ | TBD | Validar se portais já oferecem isso |

#### Integração com Portais (MVP)

| Portal | Prioridade | Observação |
|--------|------------|------------|
| Grupo OLX | P0 | Inclui OLX, ZAP, Viva Real |
| Chaves na Mão | P0 | |
| Facebook Ads | P0 | Leads de campanhas |

#### Integração com CRMs (MVP)

| CRM | Prioridade | Observação |
|-----|------------|------------|
| Kenlo | P0 | |
| Superlogica | P0 | |
| C2S | P0 | |

### Intentionally Excluded from MVP (Set Mínimo)

> **Atualizado (09/Jan/2026):** Essas features serão validadas via pesquisa/testes de usabilidade com clientes antes de serem desenvolvidas.

| Feature | Motivo | Quando considerar |
|---------|--------|-------------------|
| Login com senha | Magic link mais simples, evita "esqueci senha" | Quando escalar |
| Recuperação de senha | Não há senha no MVP | Quando implementar senha |
| Embedded Signup self-service | Complexidade alta, muitas variáveis | Melhorar progressivamente |
| Compra automática de número | Complexidade (reserva, custos, cancelamento) | Quando validar demanda |
| Listagem de leads | Cliente já tem no CRM dele | Fase 2: validar demanda primeiro via pesquisa |
| Chat centralizado | Complexidade alta; diferencial futuro | Fase 2: principal upsell |
| Cadastro de corretores | Foco em admins no MVP | Fase 2 |
| Distribuição de leads | Cliente já faz no CRM dele | Fase 2/3 |
| Gestão de permissões | Apenas admins no MVP | Fase 2 |
| Edição de perfil | Nice-to-have | Fase 2 |
| Notificações | Sem listagem de leads, não há o que notificar | Fase 2 |
| Dashboards de insights | Diferencial futuro | Fase 3 |
| App mobile nativo | Web responsivo suficiente | Fase 4 |

> **Importante:** Mesmo que não entre em Mar/2026, a descoberta de Listagem de Leads e Chat deve começar em paralelo para validar hipóteses.

### Validation Criteria (4 semanas pós-lançamento)

| Métrica | Sucesso | Fracasso |
|---------|---------|----------|
| **Taxa de ativação** | >70% completam setup em 48h | <50% |
| **Leads qualificados/dia** | >10 por cliente ativo | <3 |
| **Taxa de erro integração** | <5% | >15% |
| **NPS** | >30 | <0 |
| **Leads enviados ao CRM** | >90% chegam corretamente | <70% |

### Evolução Pós-MVP

> **Decisão (08/Jan/2026):** Enquanto desenvolvemos o MVP (até Mar/2026), a descoberta de Fase 2 deve acontecer em paralelo para ganhar tempo. Não construir sem validar hipóteses primeiro.

#### Fase 2: Gestão de Leads (requer validação prévia)

**Pré-requisito:** Validar via pesquisa e testes de usabilidade se clientes querem/precisam dessas features ou se o CRM deles já atende.

- Listagem de leads no back-office
- Visualização do histórico de conversas
- Chat centralizado (responder via back-office)
- Cadastro de corretores e gestão de permissões
- Proteção de leads (ocultar telefone do corretor)

#### Fase 3: Inteligencia (Jul/2026)
- Dashboards de demanda
- Insights proativos
- Lead scoring automático
- Sugestoes de captação

#### Fase 4: Escala (Out/2026)
- Mais integrações com CRMs
- Mais integrações com portais
- Distribuição automática de leads
- API pública

---

## 6. User Flow

### MVP: Fluxo de Onboarding (Set Mínimo)

> **Atualizado (09/Jan/2026):** Fluxo híbrido - cadastro self-service + ativação guiada pelo comercial.

**Fase 1: Cadastro Self-Service**

> **Atualizado (12/Jan/2026):** Fluxo simplificado com 3 passos visíveis para o usuário. Passos de configuração do WhatsApp/assistente não aparecem no wizard pois serão feitos com suporte.

```
Passos visíveis no wizard:
1. Crie sua conta
2. Dados da empresa
3. Aceite os termos

Fluxo detalhado:
1. Admin acessa página de cadastro
2. Cria conta com email (recebe magic link para confirmar)
3. Preenche dados da empresa:
   - CNPJ, razão social, nome fantasia
   - Responsável legal/proprietário
   - Responsável financeiro (se diferente)
   - Responsável pela implantação (se diferente)
4. Responde: "Você já usa CRM?" (elegibilidade)
   - Se não tem CRM: produto indisponível, oferecer lista de espera ou CRM Loft
   - Se tem CRM: continua
5. Responde: "Você já tem número de telefone?" (preparação)
   - Sim, já no WhatsApp Business → coexistência
   - Sim, mas não no WhatsApp Business → orientar migração
   - Não → comercial vai ajudar a comprar
6. Tela de aceite dos termos:
   - Resumo dos principais pontos (cancelamento, pós-pago, etc.)
   - Calculadora: "Quantos leads quer atender?" → estimativa de custo
   - Link para termos completos
   - Checkbox de aceite obrigatório
7. Vê mensagem: "Cadastro concluído! Nosso time entrará em contato para ativar sua conta."
```

> **Nota sobre navegação:** Cada passo tem URL própria (ex: /onboarding/step/3) para permitir que usuário retorne ao ponto onde parou.

**Fase 2: Ativação Guiada (com Comercial)**
```
1. Comercial recebe notificação de novo cadastro
2. Comercial agenda reunião de ativação
3. Durante reunião:
   a. Valida dados da empresa (QSA no CNPJ)
   b. Se precisa comprar número: comercial faz a compra
   c. Guia usuário pelo Embedded Signup
   d. Configura perfil do WhatsApp (nome, foto, descrição)
   e. Configura catálogo (URL do XML)
   f. Configura integração com CRM
4. Testa fluxo end-to-end
5. Ativa operação
```

**Variante: Usuário com Número Próprio (Autoatendimento Parcial)**
```
1. Usuário completa cadastro self-service
2. Pode iniciar Embedded Signup sem esperar comercial
3. Segue instruções na tela + manual de apoio
4. Se travar: aguarda suporte
5. Comercial entra para completar configurações restantes
```

### MVP: Fluxo Operacional

```
1. Lead entra via portal (ex: OLX)
2. Portal envia lead para endpoint do Qualifica Leads
3. Assistente IA inicia conversa via WhatsApp
4. Assistente qualifica o lead (interesse, perfil, imóveis)
5. Ao concluir qualificação, envia lead para CRM do cliente
6. Cliente visualiza lead qualificado no CRM dele
7. Cliente atende lead pelo CRM dele
```

> **Nota:** No MVP, o cliente usa o CRM dele para gestão de leads. O back-office e apenas para configuração.

---

### Fase 2: Fluxo com Gestão de Leads

#### Corretor Responde Lead (via back-office)

```
1. Corretor faz login no back-office
2. Ve listagem de leads atribuidos a ele
3. Clica em lead com nova mensagem
4. Ve histórico completo (conversa IA + mensagens anteriores)
5. Digita resposta no campo de chat
6. Mensagem e enviada via WhatsApp API
7. Lead recebe no WhatsApp dele (transparente)
8. Corretor NAO ve telefone do lead em momento algum
```

#### Admin Distribui Leads

```
1. Admin faz login no back-office
2. Ve listagem de leads não distribuidos
3. Seleciona lead
4. Escolhe corretor para atribuir
5. Corretor recebe notificação
6. Lead aparece na listagem do corretor
```

---

## 7. Design Considerations

### UX/UI Principles

> **Atualizado (09/Jan/2026):** MVP usa modelo híbrido (cadastro self-service + ativação guiada). Self-service completo fica para versões futuras.

- **Cadastro self-service**: Usuário consegue criar conta e preencher formulário sozinho. Ativação do WhatsApp é guiada pelo comercial no MVP.
- **Simplicidade first**: Interface limpa, sem complexidade desnecessária
- **Mobile-friendly**: Design responsivo para uso em celular
- **Informação clara**: Destacar dados importantes do lead
- **Checklist de progresso**: Indicadores visuais (faróis/checkmarks) mostrando o que foi configurado e o que falta
- **Instruções claras**: Cada etapa do Embedded Signup deve ter explicação + link para manual

### Assistente de Ajuda (Selfservice)

> **Decisão (08/Jan/2026):** Incluir assistente de IA para tirar dúvidas durante o setup, similar ao que foi implementado no site de marketing. Reduz carga no time de implantação.

- [ ] Chatbot de ajuda integrado na plataforma
- [ ] Base de conhecimento: documentação da Meta + nossa documentação de setup
- [ ] Padrão visual igual ao assistente do site de marketing
- [ ] Histórico de perguntas salvo para análise posterior (identificar principais dúvidas)
- [ ] Para problemas críticos que o usuário não consegue resolver: mensagem direcionando para suporte humano

> **Nota:** Usar mesmo padrão técnico do site de marketing (Botpress ou similar). Avaliar métricas via dashboard do Langfuse.

### Checklist de Setup

> **Decisão (08/Jan/2026):** Implementar indicadores visuais de progresso do setup para reduzir dependência do time de implantação.

- [ ] Lista de etapas do setup com status (pendente/concluído/erro)
- [ ] Indicador visual por etapa (farol verde/amarelo/vermelho)
- [ ] Para etapas com erro: link para artigo de ajuda específico
- [ ] Para problemas críticos (ex: template não aprovado pela Meta): alerta para entrar em contato com suporte
- [ ] Mensagem de sucesso quando setup está 100% completo

### Technical Constraints

- **WhatsApp Business API**: Necessita conta verificada, tem custos por mensagem
- **Rate limits**: API tem limites de mensagens por janela de tempo
- **Webhook reliability**: Mensagens recebidas via webhook precisam de retry logic
- **Multi-tenant**: Arquitetura deve suportar múltiplas organizações

### Assumptions

- [ ] Imobiliárias já tem conta WhatsApp Business ou podem criar
- [ ] Custo da WhatsApp API e absorvido no modelo de precificação
- [ ] Distribuição manual e suficiente para MVP
- [ ] Usuários vao adotar mais um sistema (vs planilha/WhatsApp)

### Dependencies

| Dependencia | Status | Owner |
|-------------|--------|-------|
| WhatsApp Business API | **[TBD: validar viabilidade]** | Eng |
| Infra de backend | Existente | Platform |
| Design system | Existente | Design |
| Analytics (Mixpanel/Amplitude) | Existente | Data |

---

## 8. Open Questions & Decisions

### MVP (Set Mínimo)

| Questao | Owner | Status |
|---------|-------|--------|
| ~~Quais portais entram no MVP?~~ | Product | ✅ Grupo OLX, Chaves na Mão, Facebook Ads |
| ~~Confirmar CRMs priorizados~~ | Product | ✅ Kenlo, Superlogica, C2S |
| ~~Embedded Signup vai ser self-service?~~ | Product | ✅ Não no MVP. Modelo híbrido (cadastro self-service + ativação guiada) |
| ~~Login com senha ou magic link?~~ | Product | ✅ Magic link (sem senha no MVP) |
| ~~Plataforma de identidade Loft já tem magic link?~~ | Eng | ✅ NÃO usar Keycloak no MVP. Autenticação própria. Migração para Login Loft será fase futura (time de identidade não está preparado para novos usuários). |
| Como obter acesso aos CRMs para testar integração? | Eng/Comercial | Em andamento |
| Formato padrão do XML de catálogo? | Eng | A definir |
| Qual provedor usar para compra de números? Salve ou Twilio? | Eng | A definir |

### Fases Futuras

| Questao | Owner | Status |
|---------|-------|--------|
| Chat centralizado: so no back-office ou também no CRM Loft? | Product | A definir |
| Como evitar canibalização do CRM Loft? | Product/Strategy | A definir |
| Custos da WhatsApp Business API são viaveis para chat? | Eng/Finance | A definir |
| Como migrar conversas existentes do Loft/CRM? | Eng | A definir |
| Temperatura do lead / filtro de visita | Product | ✅ Aguardar validação standalone. Esperar feedback antes de implementar filtros de qualificação no CRM (reunião 12/Jan/2026 com time CRM). |

---

## 9. Risks & Mitigation

### Riscos do MVP (Set Mínimo)

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Integração com CRMs complexa** | Alto | Alta | Comecar com CRMs que tem API documentada; contratar contas para testar |
| **Cada CRM tem formato diferente** | Médio | Alta | Criar camada de adaptadores; mapear campos por CRM |
| **Catalogos XML mal formatados** | Médio | Alta | Validação robusta; feedback claro de erros ao usuario |
| **Baixa demanda por standalone** | Alto | Média | Validar interesse antes de construir; set mínimo reduz invéstimento |
| **Concorrência forte (Lais/Morada)** | Médio | Alta | Diferenciação por preço (pay-per-use) e simplicidade |
| **Parceiros CRM não colaborativos** | Médio | Média | Comecar com CRMs menores e mais acessiveis |

### Riscos de Fases Futuras

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Usuários não adotam back-office** | Alto | Média | So construir se validar demanda real na Fase 1 |
| **Canibalização do CRM Loft** | Médio | Média | Monitorar migrações; alinhar com estratégia de produto |
| **Chat centralizado inviável tecnicamente** | Alto | Média | Spike técnico antes de iniciar Fase 2 |
| **Usuários preferem WhatsApp pessoal** | Alto | Média | Entrevistas para entender resistencia |
| **WhatsApp API tem custos altos** | Médio | Média | Validar custos antes da Fase 2 |

---

## 10. Estratégia da Versão Standalone

> **Atualizado (12/Jan/2026):** Estratégia de fases revisada para comunicação executiva. Foco em outcomes de negócio e valor para o cliente.

---

### Fase 1 - Q1/2026

**Objetivo:** Funcionar com outros CRMs de mercado e ser uma nova fonte de cross-sell para a Loft

**O que a imobiliária poderá fazer:**
- Receber leads de portais (OLX, Zap, Viva Real, Chaves na Mão) e Facebook Ads
- Ter leads qualificados automaticamente via IA no WhatsApp
- Enviar leads qualificados direto para seu CRM (Kenlo, Superlógica, C2S, Loft)
- Gerenciar configurações via backoffice

**Outcomes esperados:**
- Aquisição de clientes de outros CRMs
- Cross-sell de produtos Loft (Fiança e Financiamento)

| Componente | Atividades |
|------------|------------|
| Cadastro e Auth | Sign up (magic link), cadastro de empresa (CNPJ), pergunta sobre CRM e número |
| Ativação | Fluxo guiado pelo comercial, Embedded Signup, compra de número (manual) |
| Configuração | Assistente, perfil WhatsApp, catálogo XML |
| Integração Portais | Grupo OLX, Chaves na Mão, Facebook Ads |
| Integração CRMs | Kenlo, Superlógica, C2S |
| Infra | Deploy, monitoramento, logs |

---

### Fase 2 - Q2/2026

**Objetivo:** Criar valor adicional com o backoffice

**O que a imobiliária poderá fazer:**
- Visualizar e filtrar todos os leads em um só lugar
- Conversar com leads e acompanhar histórico - sem expor telefone com corretores
- Reativar leads antigos automaticamente
- Receber insights sobre performance da qualificação

**Outcomes esperados:**
- Aumentar retenção criando defensibilidade e switching costs

**Gatilho:** Demanda validada de clientes por gestão de leads no back-office.

---

### Fase 3 - Q3/2026

**Objetivo:** Expandir mercado e casos de uso

**O que a imobiliária poderá fazer:**
- Conectar outras origens de leads
- Integrar com outros CRMs
- Distribuir leads

**Outcomes esperados:**
- Aumentar aquisição (menos objeções de incompatibilidade)
- Aumentar cross-sell (maior base de leads)

---

## 11. Modelo de Negócio

| Item | Valor |
|------|-------|
| **Back-office (Set Mínimo)** | Gratuito (custo de configuração) |
| **Monetização** | Cobranca por atendimento de IA (R$1,80-4,00/conversa) |
| **Objetivo MVP** | Habilitar Qualifica Leads standalone para clientes de outros CRMs |
| **Objetivo Futuro** | Aumentar stickiness com gestão de leads e inteligência |
| **Cross-sell** | CRM Loft (via cadastro), Fiança Aluguel, Financiamento Imobiliário |
| **Originação CRM Loft** | Leads sem CRM direcionados para comercial do CRM Loft |

---

## 12. Alinhamento Estratégico

### Com Pilares da Loft

| Pilar | Alinhamento |
|-------|-------------|
| **AI-first** | Qualifica Leads standalone leva a IA para clientes de qualquer CRM |
| **Integração Financeiro+Tech** | Habilita cross-sell de produtos financeiros via leads qualificados |
| **Customer-centric** | Resolve dor de qualificação manual e resposta lenta |
| **Excelencia Operacional** | Set mínimo reduz time-to-market e custo de validação |

### Com Objetivos de Negócio

- Expande mercado além dos clientes do CRM Loft (TAM maior)
- Modelo pay-per-use acessível para imobiliárias de todos os tamanhos
- Habilita cross-sell de produtos financeiros
- Cria base para upsell de features premium (chat, inteligência)

---

## 13. Changelog

| Data | Alteração |
|------|-----------|
| 16/Jan/2026 | **Daily Squad AI - Mudanças nos Fluxos de Autenticação:** (1) Autenticação própria no MVP - migração para Login Loft será fase futura (time de identidade não está preparado para novos usuários). (2) CPF como identificador principal no Sign In e Sign Up. (3) Campos de cadastro: CPF, nome completo, telefone, email. (4) Email mascarado nas telas de verificação (anti-enumeração). (5) Criar Organização: remover responsável legal, manter apenas financeiro e implantação. (6) Novo passo de agendamento com 3 opções de horário. (7) Integração com Salesforce para criar chamado de implantação. (8) Sem senha/recuperar senha - apenas Magic Link. (detalhes abaixo) |
| 14/Jan/2026 | **Daily Squad AI - Decisão de Autenticação:** ~~Qualifica Leads usará Keycloak da Loft (primeiro produto sem legado Auth0).~~ **ATUALIZADO em 16/Jan:** Decisão revertida - autenticação própria no MVP. (detalhes abaixo) |
| 12/Jan/2026 | **Estratégia de Fases para Comunicação Executiva:** Seção 10 reescrita com foco em outcomes de negócio. Estrutura: Objetivo + O que a imobiliária poderá fazer + Outcomes esperados. Fases alinhadas com metas corporativas (cross-sell, retenção, aquisição). |
| 12/Jan/2026 | **Reunião Times CRM x AI:** Decisão de aguardar validação do standalone antes de implementar filtros de temperatura/visita no CRM. Evita criar complexidade desnecessária. |
| 12/Jan/2026 | **Reunião Product Trio - Detalhes do Cadastro:** Campos de responsáveis (legal, financeiro, implantação). Fluxo de onboarding com 3 passos visíveis. Tela de aceite com calculadora e resumo dos termos. Emails de segurança. (detalhes abaixo) |
| 09/Jan/2026 | **Reunião Product Trio - Fluxo de Ativação:** Modelo híbrido (cadastro self-service + ativação guiada). Login com magic link. Pergunta sobre CRM para elegibilidade e cross-sell. (detalhes abaixo) |
| 08/Jan/2026 | **Reunião Product Trio - Estratégia Standalone:** Múltiplas decisões estratégicas (detalhes abaixo) |
| 08/Jan/2026 | Revisão pós-daily: redefinição do MVP para "set mínimo" (configuração + integrações). Gestão de leads e chat movidos para Fase 2. Foco em validar demanda antes de construir back-office completo. |
| 08/Jan/2026 | Definição de portais (Grupo OLX, Chaves na Mão, Facebook Ads) e CRMs (Kenlo, Superlogica, C2S) para MVP. Data ajustada para Mar/2026. |

### Detalhes da Reunião Product Trio (08/Jan/2026)

**Decisões de Escopo:**
- **Público-alvo refinado:** Foco em imobiliárias que já têm CRM. Sem CRM = sem listagem de leads = produto não funciona para eles no MVP.
- **Sem cadastro de corretor:** Apenas administradores no MVP. Gestão de corretores fica para Fase 2.
- **Regras de distribuição como TBD:** Validar se portais (ex: Portal Pro do OLX) já oferecem essa configuração antes de implementar.
- **Notificações removidas:** Sem listagem de leads, não há o que notificar.

**Decisões de UX/Onboarding:**
- **Email como chave de acesso:** Não telefone (problema de telefone compartilhado entre corretores).
- **Validação de organização:** Usuário cria, mas fica pendente até aprovação pela Loft (CNPJ, contrato social).
- **Configurações do WhatsApp na plataforma:** Trazer nome/foto/descrição do perfil para a própria plataforma (reduz fricção com Meta). Referência: Lais.ai.
- **Checklist de setup com faróis:** Indicadores visuais de progresso para estimular selfservice.
- **Assistente de ajuda integrado:** Similar ao do site de marketing, para tirar dúvidas durante setup.

**Decisões de Dashboard:**
- **Tela inicial = consumo:** Não há listagem de leads. Dashboard focado em atendimentos e economia.
- **Linguagem clara:** Evitar "qualificado" isolado (confunde). Usar "leads atendidos", "com imóvel definido", "interesse de visita".
- **Destaque de economia:** Mostrar valor do modelo pay-per-use (não cobrar quem não responde).
- **Gratuidade visível:** Destacar "gratuito até Mar/2026" e "quanto você pagaria".

**Decisões de Processo:**
- **Descoberta em paralelo:** Enquanto MVP é desenvolvido, validar Listagem e Chat via pesquisa/testes de usabilidade.
- **Não construir sem validar:** Fase 2 só entra em desenvolvimento após confirmar demanda real.

**Próximos Passos:**
- Conversar com Grupo OLX sobre configurações de portal
- Definir processo de validação de organização com time de operações
- Design começar telas de configuração do WhatsApp e Embedded Signup

---

### Detalhes da Reunião Product Trio (09/Jan/2026)

**Decisões de Autenticação:**
- **Login via magic link:** Sem senha no MVP. Usuário recebe link por email para acessar. Evita ter que implementar "esqueci minha senha" e "trocar senha".
- **Senha e MFA ficam para depois:** Quando escalar, avaliar necessidade.

**Decisões de Cadastro:**
- **Campos da empresa:** CNPJ (obrigatório), razão social, nome fantasia. Verificar se já existe na base Loft.
- **Pergunta sobre CRM:** Obrigatória. Valida elegibilidade (sem CRM = produto indisponível no MVP) e gera oportunidades de cross-sell para o CRM Loft.
- **Pergunta sobre número:** Preparar comercial para ativação. Três opções: já tem no WhatsApp Business (coexistência), tem mas não no WhatsApp Business, precisa comprar.

**Decisões de Validação:**
- **Validação de CNPJ:** Consulta manual no QSA (Quadro de Sócios e Administradores) na Receita Federal. Validação automática via birô tem custo.

**Decisões de Ativação:**
- **Modelo híbrido:** Cadastro self-service + ativação guiada pelo comercial.
- **Embedded Signup não é self-service no MVP:** Muita complexidade (compra de número, variações de fluxo, cartão de crédito na Meta).
- **Compra de número via suporte:** Comercial faz a compra na Salve/Twilio durante reunião de ativação.
- **Usuário com número próprio:** Pode tentar Embedded Signup sozinho seguindo instruções. Se travar, aguarda suporte.
- **Somente coexistência:** Para números próprios, só oferecer opção de coexistência (número já no WhatsApp Business).

**Decisões de Cross-sell:**
- **CRM Loft Light:** Se usuário não tem CRM, oferecer plano gratuito do CRM Loft. Gera lead para comercial.
- **Métrica de originação:** Qualifica Leads pode gerar vendas do CRM Loft como métrica de valor.

**O que foi descartado do MVP:**
- Compra automática de número (complexidade de reserva, custos, cancelamento)
- Embedded Signup totalmente self-service
- Login com senha (magic link é mais simples)

**Próximos Passos:**
- Revisar histórias de usuário de cadastro e login
- Montar fluxo visual do onboarding híbrido
- Avaliar se plataforma de identidade Loft já tem magic link
- Criar manual/instruções para Embedded Signup

---

### Detalhes da Reunião Product Trio (12/Jan/2026)

**Decisões de Cadastro:**
- **Responsáveis da empresa:** Incluir campos para responsável legal/proprietário, responsável financeiro e responsável pela implantação. São papéis diferentes que podem ser pessoas diferentes.
- **Responsável financeiro:** Quem recebe notas e trata pagamentos (pode ser setor financeiro da empresa).
- **Responsável pela implantação:** Quem vai fazer a configuração técnica (pode ser TI, não necessariamente responsável legal).
- **Evitar dados duplicados:** Se usuário que está cadastrando é um dos responsáveis, não pedir para preencher novamente.
- **Armazenamento:** Dados serão salvos no banco próprio do Qualifica Leads (autenticação será própria, não integrada com Loft).

**Decisões de Fluxo de Onboarding:**
- **3 passos visíveis:** Simplificar wizard para mostrar apenas: (1) Crie sua conta, (2) Dados da empresa, (3) Aceite os termos.
- **Passos de WhatsApp/assistente removidos do wizard:** Serão feitos com suporte, não aparecem no cadastro self-service.
- **URL por passo:** Cada etapa tem URL própria (ex: /onboarding/step/3) para permitir retorno ao ponto onde parou.

**Decisões de Termos e Aceite:**
- **Tela de aceite obrigatória:** Evitar que cliente chegue na implantação sem entender o produto (casos de cancelamento por expectativa errada).
- **Resumo dos principais pontos:** Não tijolo de texto. Mostrar: pode cancelar, pós-pago, não paga leads que não respondem.
- **Calculadora integrada:** "Quantos leads quer atender?" → estimativa de custo mensal.
- **Link para termos completos:** TCG Loft + termos específicos do produto.
- **Termos específicos:** Referenciando TCG, são sucintos e cobrem pontos como responsabilidade sobre ações da Meta.

**Decisões de Pagamento:**
- **Não definir agora:** Aguardar definição do modelo de faturamento pelo time financeiro.
- **Provável boleto:** Padrão dos outros produtos Loft, mas não confirmar ainda.

**Decisões de Emails:**
- **Segurança:** Se email já existe, não expor na tela ("este email já está cadastrado"). Mostrar mensagem genérica e enviar email informando.
- **Copy dos emails:** Precisa ser definido (confirmação, login, convite, segurança).

**Decisões de Analytics:**
- **Cuidado com auto-tracking:** Evitar virar bagunça. Identificar componentes corretamente.
- **Amplitude/Mixpanel:** Configurar SDK e definir eventos com nomes padronizados.

**Status do Desenvolvimento:**
- Front-end já sendo desenvolvido (código rodando local).
- Próximo passo: deploy no ambiente de desenvolvimento.
- Design system da Loft será utilizado.

**Próximos Passos:**
- Definir copy exato dos emails com time de conteúdo
- Configurar analytics (Amplitude) com eventos nomeados
- Deploy em ambiente de desenvolvimento
- Conectar com design system da Loft

---

### Detalhes da Daily Squad AI (16/Jan/2026)

**Decisão de Autenticação - Autenticação Própria:**
- **Keycloak descartado para o MVP** - time de identidade não está preparado para novos usuários
- Autenticação própria no MVP, migração para Login Loft será fase futura
- CPF é o identificador principal (não email)
- Sem senha - apenas Magic Link

**Mudanças no Sign Up (SLA-525):**
- Campos: CPF (novo), nome completo (ao invés de nome + sobrenome), telefone (novo), email
- Email mascarado na tela de verificação (ex: s***@g***.com) - proteção anti-enumeração
- Nova tela de sucesso: "Seu cadastro está feito!" com botão para criar organização

**Mudanças no Sign In (SLA-526):**
- Login por CPF ao invés de email
- Sistema busca email associado ao CPF e envia magic link
- Email mascarado + email fictício se CPF não existe (anti-enumeração)

**Mudanças no Criar Organização (SLA-521):**
- **Removido responsável legal/proprietário** - não é mais necessário
- Mantidos: responsável financeiro e responsável pela implantação
- Checkboxes "Sou eu" vêm marcados por padrão (formulário simplificado)
- **Nova etapa: Agendamento de implantação** - usuário escolhe 3 opções de dia/horário
- **Nova integração: Salesforce** - cria chamado para time de implantação
- Proteção anti-enumeração de CNPJ

**Features que NÃO se aplicam no MVP:**
- Recuperação de Senha (SLA-527) - não tem senha
- Editar Perfil - Alterar Senha (SLA-528) - não tem senha

---

### Detalhes da Daily Squad AI (14/Jan/2026)

**Decisão de Autenticação - Keycloak:** *(REVERTIDA em 16/Jan/2026)*
- ~~Qualifica Leads será o primeiro produto da Loft a conectar diretamente no Keycloak~~ (decisão revertida)
- ~~A solução padrão da Loft já provisiona frontend para sign up/sign in~~ (decisão revertida)
- **NOVA DECISÃO (16/Jan):** Autenticação própria no MVP. Time de identidade não está preparado.

**Configuração do WhatsApp - User Stories identificadas:**
- **Embedded Signup (M):** Fluxo de conexão WhatsApp Business via Meta
- **Configuração do Perfil WhatsApp (S):** Foto, nome de exibição, descrição
- **Configuração do Assistente (XS):** Apelido do bot, nome da imobiliária
- **Status da Conta WhatsApp (XS):** Card de status no backoffice

**Outras discussões:**
- Prioridades enquanto bloqueados em auth: continuar OLX, iniciar Chaves na Mão
- Refatoração do agente de IA para arquitetura multi-agente (discussão iniciada, spike técnico planejado)
- Integrações de fiança e financiamento previstas para Q1/2026

**Próximos Passos:**
- ~~JP: continuar investigação com time de identidade~~ (descartado - auth própria)
- Dani/Rodrigo: continuar integração OLX, iniciar Chaves na Mão
- Criar tickets detalhados para user stories de configuração do WhatsApp
