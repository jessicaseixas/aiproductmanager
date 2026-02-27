# PRD: Agente de Fiança Aluguel

**Autor:** Product Team
**Data:** Janeiro 2026
**Status:** Draft
**Última revisão:** 16/Jan/2026

> Agente de IA especializado em simulação de fiança aluguel, habilitando cross-sell do Loft Fiança Aluguel dentro do Qualifica Leads através de arquitetura multi-agente.

---

## 1. Background & Problem Statement

### Situação Atual

O assistente de IA qualifica leads de aluguel e venda via WhatsApp, mas hoje:
- Não oferece produtos financeiros durante a qualificação
- Leads de aluguel passam pelo fluxo sem conhecer a opção de fiança
- Cross-sell de fiança acontece apenas após a qualificação, com o corretor
- Imobiliárias parceiras perdem oportunidades de conversão de fiança

### Problema

Leads que querem alugar um imóvel frequentemente não têm fiador, o que é uma barreira significativa para fechamento do contrato. Atualmente:

| Dor | Impacto | Evidência |
|-----|---------|-----------|
| **Lead não conhece alternativas ao fiador** | Desiste do imóvel ou busca em concorrente | Comum no mercado |
| **Corretor precisa explicar fiança manualmente** | Demora no ciclo de vendas | Feedback de imobiliárias |
| **Simulação de crédito não é instantânea** | Lead perde interesse enquanto espera | Observação de mercado |
| **Cross-sell acontece tarde demais** | Menor taxa de conversão | Hipótese a validar |

### Por Que Agora?

1. **Fiança é 90%+ da receita da Loft** — prioridade estratégica máxima
2. **Cross-sell é pilar estratégico** — aumentar cross-sell de produtos financeiros é uma das estratégias-chave da Loft para os próximos anos
3. **~40% dos atendimentos são de aluguel** — base significativa de leads elegíveis para fiança
4. **Arquitetura multi-agente planejada** — momento técnico ideal para implementar
5. **Benchmark de conversão validado** — Assistente Loft tem 6% de conversão (simulação → contrato)

### Oportunidade de Negócio

#### Volumetria de Aluguel

- **~40% dos atendimentos do Qualifica Leads são de aluguel**
- Volume atual (Jan/2026): ~2.000 atendimentos de aluguel/mês com 40 imobiliárias ativas
- **Projeção Q1/2026**: 300 imobiliárias → ~15.000 atendimentos de aluguel/mês

#### Dados de Mercado: Inquilinos sem Fiador

Pesquisas indicam que uma parcela significativa dos inquilinos não utiliza fiador:

| Fonte | Dado |
|-------|------|
| [Secovi-SP (Jul/2024)](https://secovi.com.br/confira-a-pesquisa-secovi-sp-de-locacao/) | 41% dos contratos usam fiador, 59% optam por alternativas (caução 43,5%, seguro-fiança 14%) |
| [Censo QuintoAndar](https://www.quintoandar.com.br/guias/como-alugar/garantia-locaticia/) | Fiador representa apenas 15% das garantias a nível Brasil |

**Assumption**: ~50% dos leads de aluguel não têm fiador disponível ou preferem alternativas.

#### Cálculo de Impacto Potencial

Usando taxa de conversão de **6%** do Assistente Loft como benchmark:

```
15.000 atendimentos de aluguel/mês (projeção Q1/2026 com 300 imobiliárias)
    × 50% não tem fiador (baseado em dados de mercado)
    = 7.500 elegíveis para simulação

7.500 elegíveis
    × 30% aceita simular (assumption)
    = 2.250 simulações/mês

2.250 simulações
    × 60% aprovado (assumption)
    = 1.350 aprovados/mês

1.350 aprovados
    × 6% converte em contrato (benchmark Assistente Loft)
    = ~81 contratos de fiança/mês
```

**Projeção anual**: ~970 contratos de fiança originados pelo Qualifica Leads

**Ticket médio de fiança**: **R$214/mês (ou R$2500 por contrato de 12 meses)**

---

## 2. Goals & Success Metrics

### Primary Goal

Aumentar a conversão de contratos de fiança aluguel através de cross-sell automatizado durante a qualificação de leads, sem fricção adicional para o lead ou corretor.

### Success Metrics

| Métrica | Target | Benchmark | Método de Medição |
|---------|--------|-----------|-------------------|
| **Taxa de simulações iniciadas** | >30% dos leads de aluguel sem fiador | - | Analytics (eventos no agente) |
| **Taxa de CPF coletado** | >50% dos leads que iniciaram simulação | - | Analytics |
| **Taxa de aprovação de crédito** | >60% | A validar | API CredPago |
| **Taxa de conversão em contrato** | 6% das simulações aprovadas | 6% (Assistente Loft) | CRM + sistema de fiança |
| **Contratos originados/mês** | ~80 contratos | Calculado (300 imob.) | Sistema de fiança |
| **NPS do fluxo de fiança** | >30 | - | Pesquisa pós-atendimento |

### Out of Scope (MVP)

- Contratação da fiança diretamente pelo WhatsApp
- Múltiplas opções de plano para o lead escolher
- Integração com outros produtos financeiros (financiamento)
- Simulação para leads de compra
- Reengajamento de leads não aprovados

---

## 3. Target Users

### Persona Primária: Lead de Aluguel sem Fiador

| Atributo | Descrição |
|----------|-----------|
| **Perfil** | Pessoa buscando imóvel para alugar |
| **Situação** | Não tem fiador disponível ou prefere não pedir para alguém |
| **Dor principal** | Barreira para fechar contrato de aluguel |
| **Comportamento** | Responde a anúncios de aluguel em portais (OLX, ZAP, etc.) |
| **Necessidade** | Alternativa rápida e acessível ao fiador tradicional |

### Persona Secundária: Corretor da Imobiliária

| Atributo | Descrição |
|----------|-----------|
| **Perfil** | Corretor que atende leads qualificados |
| **Situação** | Recebe lead já com simulação de fiança feita |
| **Benefício** | Menos trabalho manual, lead mais preparado para fechar |

### User Motivations

- **Lead**: Resolver o problema do fiador de forma rápida e digital
- **Corretor**: Receber leads mais qualificados e prontos para fechar
- **Imobiliária**: Aumentar taxa de conversão e receita com fiança

---

## 4. Solution & Requirements

### High-Level Solution

Implementar um **Agente de Fiança** especializado dentro da arquitetura multi-agente do Qualifica Leads. Este agente:

1. É acionado pelo Agente de Qualificação quando identifica lead de aluguel sem fiador
2. Coleta dados necessários para simulação (CPF, CEP, valor)
3. Faz simulação via API CredPago
4. Retorna resultado para o Agente de Qualificação comunicar ao lead

**Importante**: O Agente de Fiança **nunca conversa diretamente** com o lead. Toda comunicação é feita pelo Agente de Qualificação.

### Visão de Reuso e Arquitetura

Este agente será construído seguindo a **nova arquitetura multi-agente da Loft**, servindo como referência para futuros agentes especializados.

**Princípios de design para reuso:**

| Princípio | Aplicação |
|-----------|-----------|
| **Desacoplado** | Agente de Fiança é independente do Agente de Qualificação |
| **Interface padronizada** | Protocolo de hand-off definido e documentado |
| **Reutilizável** | Outros produtos Loft podem integrar o mesmo agente |
| **Configurável** | Parâmetros de simulação podem ser ajustados por contexto |

**Produtos que poderão reutilizar este agente:**

- **Assistente Loft**: Já faz simulação de fiança, pode migrar para a nova arquitetura
- **Loft/ CRM**: Oferecer simulação de fiança dentro do CRM
- **Outros produtos futuros**: Qualquer produto que atenda leads de aluguel

**Benefícios da arquitetura multi-agente:**

- Times de produto podem criar novos agentes especializados sem depender do time do Qualifica Leads
- Agentes podem ser versionados e evoluídos independentemente
- Facilita testes e manutenção isolada
- Permite escalar a capacidade de cross-sell para múltiplos produtos financeiros

### Arquitetura Multi-Agente

```
┌─────────────────────────────────────────────────────────────────┐
│                         LEAD (WhatsApp)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AGENTE DE QUALIFICAÇÃO                        │
│                                                                 │
│  • Conversa com o lead                                          │
│  • Identifica tipo de negócio (aluguel)                         │
│  • Pergunta se tem fiador                                       │
│  • Coleta CPF quando necessário                                 │
│  • Comunica resultado da simulação                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                    [Hand-off interno]
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     AGENTE DE FIANÇA                            │
│                                                                 │
│  • Recebe dados do lead (CPF, CEP, valor)                       │
│  • Chama API CredPago para simulação                            │
│  • Processa resultado (aprovado/não aprovado)                   │
│  • Retorna resultado estruturado para Agente de Qualificação    │
│                                                                 │
│  ⚠️  NUNCA conversa diretamente com o lead                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API CREDPAGO                             │
│                                                                 │
│  Input: CPF, CEP, valor do aluguel                              │
│  Output: aprovado/não, planos, valores, coberturas              │
└─────────────────────────────────────────────────────────────────┘
```

### Functional Requirements

#### Gatilho e Verificação

- [ ] Identificar quando o negócio é do tipo aluguel (pelo anúncio ou conversa)
- [ ] Perguntar ao lead se ele já tem fiador
- [ ] Se já tem fiador: não oferecer fiança, continuar fluxo normal
- [ ] Se não tem fiador: oferecer simulação de fiança

#### Coleta de Dados

- [ ] **CPF**: Solicitar ao lead de forma natural
  - Se lead não quiser informar: respeitar, não fazer simulação
- [ ] **CEP do imóvel**:
  - Usar CEP do anúncio quando disponível
  - **[TBD: decisão]** Se não tiver CEP no anúncio, verificar se endereço é suficiente para API
- [ ] **Valor do aluguel**:
  - Usar valor do anúncio quando lead já definiu imóvel
  - Perguntar orçamento quando lead não definiu imóvel específico

#### Simulação de Crédito

- [ ] Chamar API CredPago com parâmetros coletados
- [ ] Obter nome completo do lead via bureau (a partir do CPF)
- [ ] Processar resultado: aprovado ou não aprovado
- [ ] Extrair dados do plano recomendado:
  - Valor mensal
  - Cobertura de custo de saída
  - Cobertura de custo de manutenção
  - Taxa de setup (paga na contratação)
  - Prazo de cobertura (12 meses, renovável)

#### Comunicação do Resultado

- [ ] **Se aprovado**:
  - Informar que foi pré-aprovado para fiança
  - Apresentar **uma única opção de plano** (evitar sobrecarga cognitiva)
  - Explicar valores: mensalidade + taxa de setup
  - Informar que corretor pode apresentar outras opções
  - Explicar o que é fiança de aluguel e como funciona
- [ ] **Se não aprovado**:
  - Informar que no momento não foi possível aprovar
  - Explicar que corretor pode fazer novas simulações após entender melhor o cenário
- [ ] Não mencionar "Loft" — usar "parceiro" ou "serviço de fiança"

#### Contextualização da Fiança

- [ ] Explicar o que é fiança de aluguel quando necessário:
  - Substitui o fiador tradicional
  - É um serviço que garante o pagamento do aluguel ao proprietário
  - Lead paga uma taxa mensal
  - Processo 100% digital
- [ ] Usar linguagem simples e acessível
- [ ] Referenciar como "parceiro" da imobiliária (não mencionar Loft)

### Non-Functional Requirements

| Categoria | Requisito |
|-----------|-----------|
| **Performance** | Simulação deve retornar em <5 segundos |
| **Disponibilidade** | API CredPago deve ter fallback para indisponibilidade |
| **Segurança** | CPF deve ser tratado como dado sensível (LGPD) |
| **UX** | Fluxo não deve adicionar mais que 3 mensagens extras |

---

## 5. MVP

### Hipótese a Validar

> **Acreditamos que** leads de aluguel sem fiador vão aceitar fazer simulação de crédito durante a qualificação **porque** querem resolver o problema do fiador de forma rápida e digital, **e isso resultará em** aumento de conversão de contratos de fiança.

### O Que Precisamos Aprender

1. **Qual % de leads de aluguel não tem fiador?** (dimensionar mercado)
2. **Qual % aceita informar CPF para simulação?** (fricção do fluxo)
3. **Qual % é aprovado na simulação?** (viabilidade)
4. **Leads aprovados têm maior taxa de conversão?** (valor do cross-sell)
5. **O fluxo aumenta ou diminui satisfação do lead?** (NPS)

### MVP Scope

| Feature | Prioridade | Justificativa |
|---------|------------|---------------|
| Identificar lead de aluguel | P0 | Gatilho do fluxo |
| Perguntar sobre fiador | P0 | Filtro de elegibilidade |
| Coletar CPF | P0 | Essencial para simulação |
| Integração API CredPago | P0 | Core da funcionalidade |
| Apresentar resultado (1 plano) | P0 | Entrega de valor ao lead |
| Usar CEP/valor do anúncio | P0 | Reduz fricção |
| Explicar o que é fiança | P0 | Contextualização |
| Analytics de funil | P0 | Medir hipótese |

### Intencionalmente Excluídos do MVP

| Feature | Motivo | Quando considerar |
|---------|--------|-------------------|
| Múltiplas opções de plano | Sobrecarga cognitiva | Após validar interesse |
| Contratação pelo WhatsApp | Complexidade alta | Fase 2 |
| Perguntar CEP quando não tem no anúncio | Fricção alta, lead não sabe | Avaliar se endereço funciona |
| Reengajamento de não aprovados | Foco em aprovados primeiro | Fase 2 |
| Simulação para leads de compra | Foco em aluguel (90% receita) | Avaliar demanda |

### Validation Criteria (4 semanas pós-lançamento)

| Métrica | Sucesso | Fracasso | Benchmark |
|---------|---------|----------|-----------|
| **% leads sem fiador** | >40% | <20% | ~50% (dados de mercado) |
| **% que aceita simular** | >30% | <15% | A validar |
| **% que informa CPF** | >50% das simulações iniciadas | <25% | A validar |
| **Taxa de aprovação** | >60% | <30% | A validar |
| **Conversão (simulação → contrato)** | >4% | <2% | 6% (Assistente Loft) |
| **Contratos originados** | >50/mês | <20/mês | ~80/mês (projetado c/ 300 imob.) |

### Se Validado → Fase 2

- Múltiplas opções de plano
- Contratação iniciada pelo WhatsApp
- Reengajamento de leads não aprovados
- Coleta de CEP quando não disponível no anúncio

---

## 6. User Flow

### Fluxo Principal: Lead Aprovado

```
1. Lead responde anúncio de aluguel
2. Agente de Qualificação inicia conversa
3. Durante qualificação, identifica que é aluguel
4. Pergunta: "Você já tem fiador para o aluguel?"
5. Lead responde: "Não tenho"
6. Agente oferece: "Temos uma parceria com um serviço de fiança
   que substitui o fiador. Posso fazer uma simulação gratuita
   para você. Preciso apenas do seu CPF. Quer fazer?"
7. Lead aceita e informa CPF
8. [Hand-off interno para Agente de Fiança]
9. Agente de Fiança:
   - Obtém CEP e valor do anúncio
   - Chama API CredPago
   - Recebe: aprovado + plano recomendado
   - Retorna resultado para Agente de Qualificação
10. Agente de Qualificação comunica:
    "Ótima notícia! Você foi pré-aprovado para fiança de aluguel.

    Com esse serviço, você não precisa de fiador. Funciona assim:
    você paga uma taxa mensal de R$XX e, em troca, o serviço
    garante o pagamento do aluguel ao proprietário.

    Para esse imóvel:
    • Mensalidade: R$XX
    • Taxa de ativação: R$XX (paga uma vez)
    • Cobertura: 12 meses (renovável)

    O corretor pode te apresentar outras opções de plano quando
    vocês conversarem. Vou continuar com a qualificação..."
11. Continua fluxo normal de qualificação
```

### Fluxo Alternativo: Lead Não Aprovado

```
1-8. [Igual ao fluxo principal]
9. Agente de Fiança:
   - Chama API CredPago
   - Recebe: não aprovado
   - Retorna resultado
10. Agente de Qualificação comunica:
    "No momento não conseguimos a aprovação para fiança,
    mas o corretor pode fazer novas simulações depois de
    entender melhor a sua situação. Vou continuar..."
11. Continua fluxo normal de qualificação
```

### Fluxo Alternativo: Lead Não Quer Informar CPF

```
1-6. [Igual ao fluxo principal]
7. Lead responde: "Prefiro não informar"
8. Agente de Qualificação:
   "Sem problema! O corretor pode te ajudar com isso depois.
   Vamos continuar..."
9. Continua fluxo normal de qualificação
```

### Fluxo Alternativo: Lead Já Tem Fiador

```
1-4. [Igual ao fluxo principal]
5. Lead responde: "Já tenho fiador"
6. Agente de Qualificação:
   "Ótimo! Então vamos continuar..."
7. Continua fluxo normal de qualificação (não oferece fiança)
```

---

## 7. Design Considerations

### UX/UI Principles

- **Não interromper o fluxo**: Fiança é um "desvio" curto, não um novo fluxo
- **Linguagem simples**: Evitar jargões financeiros
- **Uma opção apenas**: Reduzir decisões do lead
- **Respeitar o "não"**: Se lead não quer simular ou dar CPF, seguir em frente
- **Não mencionar Loft**: Usar "parceiro" ou "serviço de fiança"

### Conhecimento do Agente sobre Fiança

O Agente de Qualificação precisa saber explicar:

| Pergunta Comum | Resposta |
|----------------|----------|
| "O que é fiança de aluguel?" | É um serviço que substitui o fiador tradicional. Você paga uma taxa mensal e o serviço garante o pagamento do aluguel ao proprietário. |
| "Como funciona?" | É 100% digital. Fazemos uma análise de crédito rápida e, se aprovado, você já pode usar como garantia no contrato de aluguel. |
| "Quanto custa?" | Depende do valor do aluguel. Posso fazer uma simulação gratuita se você quiser. |
| "Por quanto tempo vale?" | A cobertura é de 12 meses e pode ser renovada. |
| "Preciso pagar algo na hora?" | Tem uma taxa de ativação que é paga na contratação, e depois a mensalidade. |

### Technical Constraints

- **API CredPago**: Dependência externa para simulação
- **Bureau de crédito**: Para obter nome completo a partir do CPF
- **Dados do anúncio**: CEP e valor precisam estar disponíveis

### Risky Assumptions

As assumptions abaixo são ordenadas por nível de risco (da mais arriscada para a menos arriscada). Assumptions de alto risco devem ser validadas antes ou durante o MVP.

#### 🔴 Alto Risco

| Assumption | Por que é arriscada | Como validar | Status |
|------------|---------------------|--------------|--------|
| **Leads vão querer informar CPF** | CPF é dado sensível. Lead pode não confiar em dar para "uma imobiliária" via WhatsApp. Se poucos derem CPF, o funil inteiro quebra. | Teste A/B com copy diferente. Medir % que aceita vs recusa. | A validar |
| **30% dos leads sem fiador aceitam simular** | Assumption sem dados. Se for muito menor (ex: 10%), o impacto cai 3x. | Medir nas primeiras 2 semanas de MVP. | A validar |
| **6% de conversão (simulação → contrato)** | Benchmark vem do Assistente Loft, mas contexto é diferente (leads já são do Loft vs leads de imobiliárias parceiras). | Comparar com dados reais após 4 semanas. | Benchmark: 6% |

#### 🟡 Médio Risco

| Assumption | Por que é arriscada | Como validar | Status |
|------------|---------------------|--------------|--------|
| **60% de aprovação de crédito** | Sem dados do perfil de crédito dos leads do Qualifica Leads. Pode ser menor se público for diferente do Assistente Loft. | Monitorar taxa de aprovação real via API CredPago. | A validar |
| **Lead entende o que é fiança e vê valor** | Muitos leads podem não conhecer fiança digital ou achar que é "golpe". | Monitorar perguntas frequentes e objeções. Ajustar copy. | A validar |
| **Fluxo de fiança não prejudica qualificação** | Adicionar perguntas pode aumentar drop-off ou irritar leads que só querem ver o imóvel. | Comparar taxa de qualificação completa antes/depois. | A validar |
| **CEP está presente na maioria dos anúncios** | Se CEP não estiver, não conseguimos fazer simulação. Lead não sabe o CEP de cabeça. | Análise de dados: % de anúncios com CEP vs só endereço. | A validar |

#### 🟢 Baixo Risco

| Assumption | Por que é arriscada | Como validar | Status |
|------------|---------------------|--------------|--------|
| **~50% dos leads não têm fiador** | Baseado em dados de mercado (Secovi-SP, QuintoAndar). Relativamente confiável. | Medir nas primeiras semanas. | Dados de mercado |
| **API CredPago está disponível e funcional** | CredPago já é parceiro da Loft. API existe e é usada no Assistente Loft. | Spike técnico para validar endpoints. | A validar |
| **Simulação retorna em <5 segundos** | API do CredPago já é usada em outros produtos. Performance conhecida. | Teste de carga durante spike técnico. | A validar |

#### Plano de Validação de Assumptions

| Fase | Assumptions a validar | Método |
|------|----------------------|--------|
| **Pré-desenvolvimento** | API CredPago, CEP nos anúncios | Spike técnico + análise de dados |
| **Semana 1-2 do MVP** | % aceita simular, % informa CPF | Analytics de funil |
| **Semana 3-4 do MVP** | Taxa de aprovação, conversão em contrato | Dados de produção |
| **Pós-MVP** | Impacto na qualificação, entendimento do lead | Comparação de métricas + feedback qualitativo |

### Dependencies

| Dependência | Status | Owner |
|-------------|--------|-------|
| API CredPago | **[TBD: validar endpoints]** | Eng + Time CredPago |
| Arquitetura multi-agente | Em planejamento | Eng |
| CEP nos anúncios | Validar % de cobertura | Data |
| Bureau de crédito | Existente (CredPago) | CredPago |

---

## 8. Open Questions & Decisions

### Decisões Pendentes

| Questão | Owner | Status |
|---------|-------|--------|
| Se não tiver CEP no anúncio, endereço é suficiente para API? | Eng + CredPago | **[TBD]** |
| Qual plano apresentar quando há múltiplas opções? (mais barato? recomendado?) | Product | **[TBD]** |
| Qual o ticket médio de um contrato de fiança? (para cálculo de ROI) | Comercial | **[TBD]** |
| Precisamos de opt-in explícito para LGPD antes de coletar CPF? | Jurídico | **[TBD]** |
| Qual fallback se API CredPago estiver indisponível? | Eng | **[TBD]** |

### Questões Técnicas

| Questão | Owner | Status |
|---------|-------|--------|
| Quais endpoints da API CredPago serão usados? | Eng | A definir |
| Como será o hand-off entre agentes tecnicamente? | Eng | Em spike |
| Onde armazenar resultado da simulação? | Eng | A definir |

---

## 9. Risks & Mitigation

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Leads não querem informar CPF** | Alto | Média | Explicar que é só simulação, não compromete. Aceitar "não" sem insistir. |
| **API CredPago lenta ou instável** | Alto | Baixa | Implementar timeout + fallback (corretor faz depois) |
| **CEP não disponível nos anúncios** | Médio | Média | Validar % de cobertura. Avaliar usar endereço. |
| **Taxa de aprovação muito baixa** | Médio | Média | Monitorar e ajustar comunicação para não aprovados |
| **Fluxo de fiança prejudica qualificação** | Alto | Baixa | Manter fiança como desvio curto (max 3 mensagens) |
| **Lead confunde simulação com contratação** | Médio | Média | Deixar claro que é "pré-aprovação" e contratação é com corretor |

---

## 10. Timeline & Milestones

### Target: Q1/2026

| Fase | Atividades | Duração Estimada |
|------|------------|------------------|
| **Discovery** | Validar API CredPago, definir fluxo detalhado | 1 semana |
| **Design** | Definir copy das mensagens, fluxo conversacional | 1 semana |
| **Development** | Implementar agente de fiança + integração CredPago | 2-3 semanas |
| **Testing** | Testes internos, ajustes de fluxo | 1 semana |
| **Soft Launch** | Rollout para grupo piloto de imobiliárias | 1 semana |
| **GA** | Lançamento geral | - |

### Milestones

- [ ] API CredPago validada e documentada
- [ ] Arquitetura multi-agente implementada
- [ ] Agente de Fiança em staging
- [ ] Soft launch com 5 imobiliárias piloto
- [ ] GA para todos os clientes

---

## 11. Alinhamento Estratégico

### Com Pilares da Loft

| Pilar | Alinhamento |
|-------|-------------|
| **AI-first** | Agente de IA especializado em fiança, arquitetura multi-agente |
| **Integração Financeiro+Tech** | Cross-sell de produto financeiro (fiança) via qualificação de leads |
| **Customer-centric** | Resolve dor real do lead (não ter fiador) de forma instantânea |
| **Excelência Operacional** | Automatiza processo que seria manual do corretor |

### Com Estratégia de Cross-sell

> Aumentar cross-sell de produtos financeiros é uma das estratégias-chave da Loft para os próximos anos.

Esta iniciativa é a **primeira implementação de cross-sell automatizado** dentro do Qualifica Leads, estabelecendo:
- Padrão arquitetural (multi-agente) para futuros produtos
- Fluxo de oferta de produto financeiro durante qualificação
- Integração com APIs de simulação de crédito

Após validação, o mesmo padrão pode ser aplicado para:
- Financiamento imobiliário (leads de compra)
- Seguro residencial
- Outros produtos do portfólio Loft

### Com Objetivos de Negócio

- **90%+ da receita vem de fiança** — prioridade estratégica máxima
- **~80 contratos/mês projetados** — com 300 imobiliárias (meta Q1/2026)
- **~970 contratos/ano** — potencial de originação anual
- **6% de conversão** — benchmark validado no Assistente Loft
- **Reduz carga do corretor** — lead chega pré-aprovado
- **Diferencial competitivo** — concorrentes não oferecem cross-sell automatizado

---

## 12. Changelog

| Data | Alteração |
|------|-----------|
| 16/Jan/2026 | Adicionada seção "Risky Assumptions" com classificação por nível de risco (alto/médio/baixo), justificativa e plano de validação |
| 16/Jan/2026 | Adicionada seção "Visão de Reuso e Arquitetura" — agente será construído para ser reutilizado por outros produtos Loft (Assistente Loft, CRM, etc.), seguindo a nova arquitetura multi-agente |
| 16/Jan/2026 | Projeção de impacto atualizada para 300 imobiliárias (~80 contratos/mês). Adicionado dados de mercado Secovi-SP e QuintoAndar sobre uso de fiador (~50% não usa). Ajustado assumption de "sem fiador" para 50% baseado em pesquisas |
| 16/Jan/2026 | Adicionado dados de volumetria (~40% dos atendimentos são aluguel), benchmark de conversão de 6% do Assistente Loft, alinhamento com estratégia de cross-sell |
| 16/Jan/2026 | Criação do documento |

