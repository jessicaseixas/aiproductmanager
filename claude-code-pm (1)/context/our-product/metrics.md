# Metricas do Produto

Documento de discussao e definicao de metricas para Loft Qualifica Leads.

## Contexto

- **Estagio do produto**: Entre MVP e Crescimento (lancou out/2025 como add-on, standalone abr/2026)
- **Modelo de negocio**: B2B2C passivo (imobiliaria paga, lead interage com IA)
- **Monetizacao**: Pay-per-conversation (R$1,80 - R$4,00 por conversa)
- **Base atual**: 87 contratadas, 57 implantadas/ativadas (Jan/2026)
- **Promocao**: Gratuidade ate fim de marco/2026

---

## Metricas Atuais

### O que ja medimos

| Metrica | Descricao | Baseline |
|---------|-----------|----------|
| Taxa de resposta | % de leads que respondem a primeira mensagem da IA | 46-70% |
| Taxa de qualificacao | % de leads qualificados entre os que responderam | ~75% |
| CSAT do lead | Satisfacao do lead ao final do atendimento (1-5) | A definir |
| Total de atendimentos | Volume absoluto de conversas | Crescendo (330-1.48k/semana) |

### O que ainda nao medimos

| Metrica | Por que importa | Bloqueio |
|---------|-----------------|----------|
| Feedback da imobiliaria por lead | Valida se lead entregue gerou valor | Back-office v2 nao implementado |
| Retencao de imobiliarias | Clientes B2B continuam usando? | Gratuidade distorce dados ate abr/2026 |
| Activation / Aha moment | Quando imobiliaria experimenta valor | Precisa analise de cohort (dados insuficientes) |
| NPS da imobiliaria | Satisfacao do cliente B2B | Pesquisa mensal em planejamento |

---

## Framework de Metricas para B2B2C

### Por que o AARRR tradicional nao funciona diretamente

O framework AARRR assume que o usuario "usa" o produto ativamente. No Loft Qualifica Leads:

```
Imobiliaria (B2B)     Produto        Lead (C)
      |                  |               |
   Paga            Conecta os dois   Interage com IA
   Recebe valor                      Gera valor
   PASSIVO                           ATIVO
```

A imobiliaria nao "engaja" — ela **recebe** valor. O volume de leads depende dos portais, nao de acoes da imobiliaria.

### Categorias adaptadas

| Categoria | Aplicacao no contexto | Responsavel |
|-----------|----------------------|-------------|
| Acquisition | Novas imobiliarias contratando | Sales |
| Activation | Imobiliaria experimenta proposta de valor | Produto + CS |
| Eficacia da IA | Qualidade da qualificacao | Produto |
| Valor entregue | Lead gerou resultado para imobiliaria | Produto |
| Retention | Imobiliaria continua usando/pagando | Produto + CS |
| **Expansion** | Imobiliaria usando mais ao longo do tempo | Produto + CS |

---

## Discussao: North Star Metric

### Candidatas avaliadas

| Candidata | Pros | Contras | Decisao |
|-----------|------|---------|---------|
| Leads qualificados entregues (volume) | Correlaciona com receita | Sobe automaticamente com mais clientes, pouco controlavel pelo produto | Rejeitada para Produto |
| Taxa de qualificacao completa | Controlavel pelo produto | Pode ser gamificada (capturar menos dados = taxa sobe) | Aceita para Produto |
| Taxa de contato efetivo | Mede valor real entregue | Depende de feedback da imobiliaria (cobertura parcial) | Candidata futura |
| Volume de atendimentos | Diretamente ligado a receita | Pouco controlavel pelo produto | Aceita para Negocio |
| Net Volume Retention (NVR) | Mede saude da expansion | Depende de base existente | Aceita para Negocio |

### Conclusao: Dois niveis de Focus

O modelo de monetizacao e **pay-per-conversation**. Uma imobiliaria grande com 1.000 atendimentos vale mais que 10 pequenas com 50 cada. Por isso, separamos:

#### Focus Metric de Negocio

> **Volume de Atendimentos por Mes**
>
> Total de conversas realizadas no periodo

Ou, para medir saude da expansion:

> **Net Volume Retention (NVR)**
>
> Volume M0 / Volume M-1 (mesmos clientes)

**Justificativa**:
- Diretamente ligado a receita (pay-per-conversation)
- Reflete valor total gerado
- Imobiliarias grandes pesam mais (correto para o negocio)

**Responsavel**: Sales + CS + Produto (todos contribuem)

#### Focus Metric de Produto

> **Taxa de Qualificacao Completa**
>
> `Leads qualificados / Leads que responderam ao menos 1x`

**Justificativa**:
- Diretamente controlavel pelo produto (qualidade da IA, fluxo de conversa)
- Nao infla automaticamente com mais clientes
- Baseline conhecido: ~75%

**Responsavel**: Produto

### Relacionamento entre as Focus Metrics

```
FOCUS NEGOCIO:    Volume de Atendimentos / NVR
                         |
                         | depende de
                         |
        +----------------+----------------+
        |                                 |
        v                                 v
   Quantidade de              Qualidade do
   imobiliarias ativas        atendimento
   (Sales + CS)               (Produto)
                                 |
                                 v
FOCUS PRODUTO:           Taxa de Qualificacao
```

### Guardrails

| Guardrail | Threshold | Protege contra |
|-----------|-----------|----------------|
| CSAT do lead | >= 4.0 | Piorar experiencia do lead |
| Taxa de resposta inicial | >= 40% | Primeira mensagem ruim |
| Taxa de Expansion | >= 50% | Base contraindo |

**Limitacao conhecida**: Taxa de qualificacao pode ser otimizada capturando menos dados. O CSAT do lead funciona como guardrail, mas idealmente precisamos do feedback da imobiliaria para validar se leads com menos dados ainda sao uteis.

---

## Discussao: Activation (Aha Moment)

### O problema

Nao sabemos qual evento/comportamento prediz retencao. Candidatos:

- Primeiro lead qualificado recebido
- X leads qualificados na primeira semana
- Primeiro lead com interesse de visita
- Combinacao de volume + qualidade

### Por que ainda nao da para medir

1. **Gratuidade ate marco/2026**: Retencao esta artificialmente alta (~94%, apenas 5 churns em 57 implantadas)
2. **Base pequena**: 57 imobiliarias ativas nao da significancia estatistica
3. **Tempo insuficiente**: Produto lancou out/2025, poucos meses de dados

### Metodologia para descobrir (quando tivermos dados)

1. Definir "sucesso" = imobiliaria ativa apos 60 dias (recebeu lead no mes)
2. Listar candidatos a aha moment (eventos na primeira semana)
3. Calcular correlacao: retencao de quem fez X vs quem nao fez
4. Escolher evento com maior poder preditivo e volume razoavel

### Proxy disponivel agora

**Time-to-First-Lead**: Tempo entre criacao da imobiliaria no sistema e primeiro lead qualificado recebido.

- Data de criacao = registro criado durante embedded sign-up
- Primeiro lead = primeiro lead qualificado entregue
- Metrica = mediana de dias entre os dois eventos

Isso mede velocidade de entrega de valor, mas nao valida se e o aha moment.

---

## Discussao: Feedback da Imobiliaria

### Necessidade

Hoje so temos feedback do lead (CSAT). Falta feedback do cliente B2B (imobiliaria) para validar:
- O lead entregue gerou valor?
- A qualificacao estava correta?
- Conseguiu contato/agendou visita?

### Abordagem proposta

**Pergunta factual (nao subjetiva)**:

> "Conseguiu contato com esse lead?"
> [Sim] [Nao] [Ainda vou tentar]

Se sim:
> "Agendou visita?"
> [Sim] [Nao, mas em negociacao] [Sem interesse]

**Por que factual**: Evita interpretacao subjetiva ("foi util?"). Alinha com linguagem ja usada no produto (status do lead: abandonou, respondeu, qualificado, interesse de visita).

### Canal de coleta

| Fase | Canal | Cobertura |
|------|-------|-----------|
| Curto prazo | WhatsApp (follow-up 24h apos lead) | Parcial (so quem responde) |
| Medio prazo | Back-office v2 (ao visualizar lead) | Alta |
| Longo prazo | Integracao CRM (status do lead no funil) | Total |

### Metrica derivada

> **Taxa de Contato Efetivo** = Leads com contato confirmado / Leads com feedback recebido

Calculada apenas sobre a amostra que respondeu (vies de selecao aceito no curto prazo).

---

## Discussao: Expansion (Engagement B2B)

### O problema

Retencao mede se a imobiliaria **ficou**, mas nao se **esta usando mais**. Precisamos medir expansion — a imobiliaria esta confiando mais no produto?

### Conceito: Retencao vs Expansion

| Metrica | O que mede | Pergunta |
|---------|------------|----------|
| **Retencao** | Cliente continua usando | "Ela ainda esta aqui?" |
| **Expansion** | Cliente usa mais ao longo do tempo | "Ela esta confiando mais em nos?" |

### Sinais de expansion em B2B2C passivo

A imobiliaria nao "usa" ativamente, mas ela **decide** quanto do fluxo de leads passa pelo produto:

| Sinal | Como interpretar |
|-------|------------------|
| Volume de leads aumentando | Mais canais configurados ou mais confianca |
| Mais integracoes ativas | Decisao consciente de expandir uso |
| Mais corretores recebendo leads | Operacao crescendo com o produto |

### Metricas de Expansion propostas

#### 1. Taxa de Expansion (democratica)

> **% de imobiliarias com volume crescente**
>
> = Imobiliarias onde `leads M0 > leads M-1` / Total de imobiliarias ativas

Cada imobiliaria = 1 voto, independente do tamanho.

Segmentacao por tendencia:

| Segmento | Criterio |
|----------|----------|
| **Expanding** | Volume M0 > M-1 (cresceu >10%) |
| **Stable** | Volume M0 ≈ M-1 (variacao +/-10%) |
| **Contracting** | Volume M0 < M-1 (caiu >10%) |

#### 2. Net Volume Retention - NVR (ponderada)

> **NVR = Volume total de leads M0 / Volume total de leads M-1**
>
> (considerando apenas clientes que existiam em M-1)

Imobiliarias grandes pesam mais. Reflete impacto na receita.

| NVR | Interpretacao |
|-----|---------------|
| >100% | Base esta expandindo uso |
| =100% | Estavel |
| <100% | Base esta contraindo |

#### 3. Canais por Cliente

> **Media de canais/integracoes por imobiliaria**

Se uma imobiliaria comeca com 1 portal e depois configura 3, ela esta expandindo.

### Exemplo: Por que ter as duas metricas

| Imobiliaria | Leads M-1 | Leads M0 | Tendencia |
|-------------|-----------|----------|-----------|
| LOBO (grande) | 1.000 | 800 | Caiu 20% |
| Heras (media) | 100 | 150 | Cresceu 50% |
| Trend (pequena) | 50 | 60 | Cresceu 20% |

**Taxa de Expansion**: 2 de 3 cresceram = **67%** ✅
**NVR**: 1.010 / 1.150 = **88%** ⚠️

Historias diferentes:
- Taxa de Expansion: "A maioria dos clientes esta confiando mais"
- NVR: "Mas o volume total caiu porque o maior cliente contraiu"

**Quando divergem**: Sinal de risco concentrado em cliente grande.

---

## Discussao: Segmentacao por Volume

Segmentar imobiliarias por volume de uso.

### Dados reais (Jan/2026)

Analise de 34 imobiliarias ativas:

| Faixa | Quantidade | % da base | Exemplos |
|-------|------------|-----------|----------|
| >=5 leads/dia | ~12 | 35% | LOBO (38/dia), TONINHO (27/dia), BB (9.8/dia) |
| 2-5 leads/dia | ~12 | 35% | Real Estate SP (3.7/dia), HARANO (3.6/dia) |
| 1-2 leads/dia | ~6 | 18% | Trend (1.8/dia), Corporativa (1.2/dia) |
| <1 lead/dia | ~4 | 12% | SIGNATA (0.9/dia), Vivence MT (0.6/dia) |

**Observacoes**:
- Base bem ativa: 70% tem mais de 2 leads/dia
- Outliers no topo: LOBO e TONINHO muito acima da media
- Range de atendimentos/mes: 18 a 1.155
- Apenas 12% com <1 lead/dia (possivel risco de churn ou operacao pequena)

### Segmentacao proposta

| Segmento | Criterio | % da base | Perfil |
|----------|----------|-----------|--------|
| **Power users** | >=5 leads/dia (~150+/mes) | ~35% | Imobiliarias grandes, alto volume de portais |
| **Core users** | 2-5 leads/dia (~60-150/mes) | ~35% | Uso tipico, operacao media |
| **Light users** | 1-2 leads/dia (~30-60/mes) | ~18% | Operacao menor ou menos integracoes |
| **Low-volume** | <1 lead/dia (<30/mes) | ~12% | Monitorar: risco de churn ou operacao muito pequena |

**Metrica**: Distribuicao de clientes por faixa de volume

Isso ajuda a entender perfil da base, nao "engagement" no sentido tradicional.

---

## Metricas Propostas (Consolidado)

### Focus Metrics

| Level | Metrica | Formula | Responsavel | Status |
|-------|---------|---------|-------------|--------|
| **Focus Negocio** | Volume de Atendimentos | Total de conversas/mes | Todos | Ativo |
| **Focus Negocio** | Net Volume Retention (NVR) | Volume M0 / Volume M-1 (mesmos clientes) | Todos | A implementar |
| **Focus Produto** | Taxa de Qualificacao Completa | Leads qualificados / Leads que responderam | Produto | Ativo, baseline 75% |

### Guardrails

| Level | Metrica | Formula | Threshold | Status |
|-------|---------|---------|-----------|--------|
| **Guardrail** | CSAT do Lead | Media das avaliacoes (1-5) | >= 4.0 | Ativo |
| **Guardrail** | Taxa de Resposta Inicial | Leads que responderam / Leads contactados | >= 40% | Ativo, baseline 46-70% |
| **Guardrail** | Taxa de Expansion | % imobiliarias com volume crescente | >= 50% | A implementar |

### L1 Metrics

| Level | Metrica | Formula | Status |
|-------|---------|---------|--------|
| **L1 - Activation** | Time-to-First-Lead | Mediana de dias entre criacao e 1o lead | A implementar |
| **L1 - Retention** | Retencao Mensal | Imobiliarias ativas M0 e M1 / Ativas M1 | A medir apos abr/2026 |
| **L1 - Expansion** | Taxa de Expansion | % imobiliarias com volume M0 > M-1 | A implementar |
| **L1 - Expansion** | Canais por Cliente | Media de integracoes por imobiliaria | A implementar |
| **L1 - Value** | Taxa de Contato Efetivo | Leads com contato / Leads com feedback | A implementar (depende coleta) |
| **L1 - Profile** | Distribuicao por Volume | % imobiliarias em cada faixa | A implementar |
| **L1 - Satisfaction** | NPS Imobiliaria | NPS mensal | Em planejamento |

---

## Proximos Passos

1. [ ] Implementar calculo de NVR (Net Volume Retention) no dashboard
2. [ ] Implementar calculo de Taxa de Expansion (% imobiliarias crescendo)
3. [ ] Implementar coleta de feedback da imobiliaria via WhatsApp (mensagem 24h apos lead)
4. [ ] Criar dashboard com Time-to-First-Lead
5. [ ] Apos fim da gratuidade (abr/2026): rodar analise de cohort para descobrir aha moment
6. [ ] Apos back-office v2: migrar coleta de feedback para interface
7. [ ] Definir targets para cada metrica baseado em baselines
8. [ ] Rastrear numero de canais/integracoes por imobiliaria

---

## Metricas de Performance da IA

### Tempo de Primeira Resposta

Tempo entre o lead chegar (ser criado no sistema) e a IA enviar a primeira mensagem.

**Dados coletados**: Jan/2026 (ultimos 30 dias, 5.282 leads analisados)

#### Resultado Geral

| Metrica | Valor |
|---------|-------|
| **Media** | 1.5 segundos |
| **% respondidos em ate 15 seg** | 97.4% |

#### Por Canal de Origem

| Canal | Media (seg) | Total Leads | Respondidos ate 3seg | % ate 3seg |
|-------|-------------|-------------|----------------------|------------|
| OLX | 0.4 | 2.188 | 2.188 | 100% |
| Facebook Ads | 0.2 | 1.250 | 1.250 | 100% |
| Chaves na Mao | 0.3 | 733 | 733 | 100% |
| WhatsApp | 24.4 | 263 | 1 | 0.4% |
| ImovelWeb | 0.2 | 220 | 220 | 100% |
| Portal 62imoveis.com.br | 0.5 | 211 | 211 | 100% |
| Site | 0.4 | 136 | 136 | 100% |
| CliqueiMudei | 0.2 | 93 | 93 | 100% |
| Website | 0.5 | 86 | 86 | 100% |
| SP Imovel | 0.3 | 54 | 54 | 100% |
| Quires | 0.3 | 22 | 22 | 100% |
| Portal Loft | 0.5 | 20 | 20 | 100% |
| Google Ads | 0.5 | 6 | 6 | 100% |

**Observacao**: WhatsApp tem tempo maior (24.4 seg) porque o lead ja inicia a conversa - nao e a IA que faz o primeiro contato.

#### Percentis (excluindo WhatsApp)

| Total Leads | Media (seg) | P50 (mediana) | P80 | P95 |
|-------------|-------------|---------------|-----|-----|
| 5.019 | 0.3 | 0 | 1 | 1 |

**Interpretacao**: 95% dos leads recebem resposta em ate 1 segundo (excluindo WhatsApp). Performance excelente.

---

## Historico de Discussoes

| Data | Topico | Conclusao |
|------|--------|-----------|
| Jan/2026 | Tempo de Primeira Resposta | P95 de 1 segundo (excl. WhatsApp), 97.4% respondidos em ate 15 seg |
| Jan/2026 | North Star Metric | Taxa de Qualificacao como Focus, volume rejeitado por ser pouco controlavel |
| Jan/2026 | Feedback imobiliaria | Abordagem factual ("conseguiu contato?") melhor que subjetiva ("foi util?") |
| Jan/2026 | Aha moment | Impossivel medir agora (gratuidade + base pequena), revisitar apos abr/2026 |
| Jan/2026 | Engagement B2B2C | Conceito tradicional nao aplica; usar segmentacao por volume |
| Jan/2026 | Segmentacao por volume | Ajustado com dados reais: 70% tem >2 leads/dia, thresholds revisados |
| Jan/2026 | Expansion metrics | Adicionado NVR e Taxa de Expansion para medir se imobiliarias estao usando mais |
| Jan/2026 | Focus Metric de Negocio | Volume de atendimentos/NVR como Focus de Negocio (receita), separado de Focus de Produto (taxa) |
| Jan/2026 | Queries de Expansion | Criadas queries BigQuery para NVR e Taxa de Expansion, normalizadas por dia para evitar distorcao MTD |

---

## Queries BigQuery

### Nota sobre MTD (Month-to-Date)

Ao comparar meses, o mes atual pode estar incompleto. Para evitar distorcao (ex: comparar 12 dias de janeiro com 31 dias de dezembro), as queries abaixo **normalizam por dia** - ou seja, comparam media diaria ao inves de volume bruto.

### Query 1: Evolucao por Imobiliaria (M0, M1, M2...)

Mostra o volume de cada mes desde o inicio da imobiliaria, com taxa media de crescimento MoM.

- **M0** = primeiro mes da imobiliaria
- **M1** = segundo mes
- **M2** = terceiro mes, etc.

```sql
-- =====================================================
-- EVOLUCAO: Volume mensal por imobiliaria desde o inicio
-- =====================================================

WITH phone_unable_to_reach_due_to_payment_issue AS (
  SELECT lead_phone_number, created_at
  FROM `loft-datalake.ds_import_api_gcp.lead_qualify_metrics`,
  UNNEST(data.errors) AS _error
  WHERE metric_name = 'webhook_message_failed'
    AND _error.value.message LIKE '%payment%'
),

agency_lead_and_phone_unable_to_reach_due_to_payment_issue AS (
  SELECT CONCAT(DATE(TIMESTAMP(a.created_at)), '|', CAST(a.lead_id AS STRING), '|', CAST(a.agency_id AS STRING)) atendimento_id
  FROM `loft-datalake.ds_import_api_gcp.lead_qualify_metrics` a
  JOIN phone_unable_to_reach_due_to_payment_issue b
    ON a.lead_phone_number = b.lead_phone_number
    AND a.metric_name = 'lead_qualify_started'
    AND b.created_at > a.created_at
    AND TIMESTAMP_DIFF(TIMESTAMP(b.created_at), TIMESTAMP(a.created_at), MINUTE) <= 1
),

-- Base de atendimentos por imobiliaria e mes
atendimentos_por_mes AS (
  SELECT
    DATE_TRUNC(DATE(TIMESTAMP(JSON_VALUE(lead_data, '$.created_at'))), MONTH) AS mes,
    agency_id AS imobiliaria_id,
    CASE
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') IN ('BM CLASS', 'GRECCO CHERUBINI E AZEVEDO LTDA') THEN 'BM Class'
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') IN ('Especifica', 'Especifica Imobiliária') THEN 'Especifica Imobiliária'
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') IN ('Heras', 'Heras Imóveis') THEN 'Heras Imóveis'
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') IN ('CORPORATIVA DIGITAL IMOBILIÁRIA LTDA', 'Corporativa imobiliária') THEN 'Corporativa Imobiliária'
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') IN ('ESPECIFICA ASSESSORIA IMOBILIARIA LTDA', 'Especifica Plataforma Imobiliária') THEN 'Especifica Assessoria Imobiliária'
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') = 'EDER VIEIRA IMÓVEIS' THEN 'Eder Vieira Imóveis'
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') = 'HOME21LTDA' THEN 'Home21 Imóveis'
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') = 'Cristina Milanez Imóveis' THEN 'Cristina Milanez'
      ELSE JSON_VALUE(lead_data, '$.agency_data.agency_name')
    END AS imobiliaria_nome,
    COUNT(*) AS total_atendimentos
  FROM `loft-dl-fintech.bronze_dynamo_credpago_dados_production_gcp.lead_qualify_leads`
  WHERE agency_id NOT IN (
      'f47ac10b-58cc-4372-a567-0e02b2c3d479',
      '3cb167fb-13df-4129-942b-c415034d9ec7',
      'a414f744-b0fa-414a-8a2d-2470ad1e6154',
      'eb78caa7-5fcb-4ae3-a509-82355a57c3fe',
      '4f6261ad-e50c-445e-b9ed-3b997d3eb5a8'
    )
    AND REGEXP_CONTAINS(agency_id, r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    AND CONCAT(DATE(TIMESTAMP(JSON_VALUE(lead_data, '$.created_at'))), '|', CAST(lead_id AS STRING), '|', CAST(agency_id AS STRING)) NOT IN (
      SELECT * FROM agency_lead_and_phone_unable_to_reach_due_to_payment_issue
    )
    AND JSON_VALUE(lead_data, '$.agency_data.agency_name') IS NOT NULL
  GROUP BY 1, 2, 3
),

-- Primeiro mes de cada imobiliaria
primeiro_mes AS (
  SELECT
    imobiliaria_id,
    MIN(mes) AS mes_inicio
  FROM atendimentos_por_mes
  GROUP BY 1
),

-- Numerar os meses de cada imobiliaria (M0, M1, M2...)
meses_numerados AS (
  SELECT
    a.imobiliaria_id,
    a.imobiliaria_nome,
    a.mes,
    a.total_atendimentos,
    DATE_DIFF(a.mes, p.mes_inicio, MONTH) AS numero_mes
  FROM atendimentos_por_mes a
  JOIN primeiro_mes p ON a.imobiliaria_id = p.imobiliaria_id
),

-- Pivotar para ter uma coluna por mes
evolucao_pivot AS (
  SELECT
    imobiliaria_id,
    imobiliaria_nome,
    MAX(CASE WHEN numero_mes = 0 THEN total_atendimentos END) AS M0,
    MAX(CASE WHEN numero_mes = 1 THEN total_atendimentos END) AS M1,
    MAX(CASE WHEN numero_mes = 2 THEN total_atendimentos END) AS M2,
    MAX(CASE WHEN numero_mes = 3 THEN total_atendimentos END) AS M3,
    MAX(CASE WHEN numero_mes = 4 THEN total_atendimentos END) AS M4,
    MAX(CASE WHEN numero_mes = 5 THEN total_atendimentos END) AS M5,
    MAX(numero_mes) AS total_meses
  FROM meses_numerados
  GROUP BY 1, 2
),

-- Calcular taxas de crescimento mes-a-mes
taxas_crescimento AS (
  SELECT
    m.*,
    CASE WHEN M0 > 0 AND M1 IS NOT NULL THEN ROUND((M1 - M0) * 100.0 / M0, 1) END AS taxa_m0_m1,
    CASE WHEN M1 > 0 AND M2 IS NOT NULL THEN ROUND((M2 - M1) * 100.0 / M1, 1) END AS taxa_m1_m2,
    CASE WHEN M2 > 0 AND M3 IS NOT NULL THEN ROUND((M3 - M2) * 100.0 / M2, 1) END AS taxa_m2_m3,
    CASE WHEN M3 > 0 AND M4 IS NOT NULL THEN ROUND((M4 - M3) * 100.0 / M3, 1) END AS taxa_m3_m4,
    CASE WHEN M4 > 0 AND M5 IS NOT NULL THEN ROUND((M5 - M4) * 100.0 / M4, 1) END AS taxa_m4_m5
  FROM evolucao_pivot m
)

SELECT
  imobiliaria_nome,
  M0, M1, M2, M3, M4, M5,
  total_meses + 1 AS meses_ativos,
  taxa_m0_m1,
  taxa_m1_m2,
  taxa_m2_m3,
  taxa_m3_m4,
  taxa_m4_m5,
  -- Taxa media MoM
  ROUND(
    (COALESCE(taxa_m0_m1, 0) + COALESCE(taxa_m1_m2, 0) + COALESCE(taxa_m2_m3, 0) + COALESCE(taxa_m3_m4, 0) + COALESCE(taxa_m4_m5, 0))
    / NULLIF(
        (CASE WHEN taxa_m0_m1 IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN taxa_m1_m2 IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN taxa_m2_m3 IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN taxa_m3_m4 IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN taxa_m4_m5 IS NOT NULL THEN 1 ELSE 0 END)
      , 0)
  , 1) AS taxa_media_mom
FROM taxas_crescimento
ORDER BY M0 DESC;
```

### Query 2: NVR e Taxa de Expansion (normalizado por dia)

Compara mes atual vs anterior usando **media diaria** para evitar distorcao MTD.

**Nota**: Esta versao usa CTEs separadas para filtrar os meses ANTES do JOIN, evitando problemas com FULL OUTER JOIN.

```sql
-- =====================================================
-- NVR e TAXA DE EXPANSION (normalizado por dia)
-- =====================================================

WITH phone_unable_to_reach_due_to_payment_issue AS (
  SELECT lead_phone_number, created_at
  FROM `loft-datalake.ds_import_api_gcp.lead_qualify_metrics`,
  UNNEST(data.errors) AS _error
  WHERE metric_name = 'webhook_message_failed'
    AND _error.value.message LIKE '%payment%'
),

agency_lead_and_phone_unable_to_reach_due_to_payment_issue AS (
  SELECT CONCAT(DATE(TIMESTAMP(a.created_at)), '|', CAST(a.lead_id AS STRING), '|', CAST(a.agency_id AS STRING)) atendimento_id
  FROM `loft-datalake.ds_import_api_gcp.lead_qualify_metrics` a
  JOIN phone_unable_to_reach_due_to_payment_issue b
    ON a.lead_phone_number = b.lead_phone_number
    AND a.metric_name = 'lead_qualify_started'
    AND b.created_at > a.created_at
    AND TIMESTAMP_DIFF(TIMESTAMP(b.created_at), TIMESTAMP(a.created_at), MINUTE) <= 1
),

atendimentos_por_mes AS (
  SELECT
    DATE_TRUNC(DATE(TIMESTAMP(JSON_VALUE(lead_data, '$.created_at'))), MONTH) AS mes,
    agency_id AS imobiliaria_id,
    CASE
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') IN ('BM CLASS', 'GRECCO CHERUBINI E AZEVEDO LTDA') THEN 'BM Class'
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') IN ('Especifica', 'Especifica Imobiliária') THEN 'Especifica Imobiliária'
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') IN ('Heras', 'Heras Imóveis') THEN 'Heras Imóveis'
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') IN ('CORPORATIVA DIGITAL IMOBILIÁRIA LTDA', 'Corporativa imobiliária') THEN 'Corporativa Imobiliária'
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') IN ('ESPECIFICA ASSESSORIA IMOBILIARIA LTDA', 'Especifica Plataforma Imobiliária') THEN 'Especifica Assessoria Imobiliária'
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') = 'EDER VIEIRA IMÓVEIS' THEN 'Eder Vieira Imóveis'
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') = 'HOME21LTDA' THEN 'Home21 Imóveis'
      WHEN JSON_VALUE(lead_data, '$.agency_data.agency_name') = 'Cristina Milanez Imóveis' THEN 'Cristina Milanez'
      ELSE JSON_VALUE(lead_data, '$.agency_data.agency_name')
    END AS imobiliaria_nome,
    COUNT(*) AS total_atendimentos,
    MIN(DATE(TIMESTAMP(JSON_VALUE(lead_data, '$.created_at')))) AS primeiro_dia,
    MAX(DATE(TIMESTAMP(JSON_VALUE(lead_data, '$.created_at')))) AS ultimo_dia
  FROM `loft-dl-fintech.bronze_dynamo_credpago_dados_production_gcp.lead_qualify_leads`
  WHERE agency_id NOT IN (
      'f47ac10b-58cc-4372-a567-0e02b2c3d479',
      '3cb167fb-13df-4129-942b-c415034d9ec7',
      'a414f744-b0fa-414a-8a2d-2470ad1e6154',
      'eb78caa7-5fcb-4ae3-a509-82355a57c3fe',
      '4f6261ad-e50c-445e-b9ed-3b997d3eb5a8'
    )
    AND REGEXP_CONTAINS(agency_id, r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    AND CONCAT(DATE(TIMESTAMP(JSON_VALUE(lead_data, '$.created_at'))), '|', CAST(lead_id AS STRING), '|', CAST(agency_id AS STRING)) NOT IN (
      SELECT * FROM agency_lead_and_phone_unable_to_reach_due_to_payment_issue
    )
    AND JSON_VALUE(lead_data, '$.agency_data.agency_name') IS NOT NULL
  GROUP BY 1, 2, 3
),

atendimentos_normalizado AS (
  SELECT
    *,
    DATE_DIFF(ultimo_dia, primeiro_dia, DAY) + 1 AS dias_ativos,
    ROUND(total_atendimentos * 1.0 / (DATE_DIFF(ultimo_dia, primeiro_dia, DAY) + 1), 2) AS media_diaria
  FROM atendimentos_por_mes
),

-- Identificar os dois ultimos meses
meses_referencia AS (
  SELECT
    MAX(mes) AS mes_atual,
    MAX(CASE WHEN mes < (SELECT MAX(mes) FROM atendimentos_por_mes) THEN mes END) AS mes_anterior
  FROM atendimentos_por_mes
),

-- SEPARAR os dados por mes ANTES do join (evita problemas com FULL OUTER JOIN)
dados_mes_atual AS (
  SELECT *
  FROM atendimentos_normalizado
  WHERE mes = (SELECT mes_atual FROM meses_referencia)
),

dados_mes_anterior AS (
  SELECT *
  FROM atendimentos_normalizado
  WHERE mes = (SELECT mes_anterior FROM meses_referencia)
),

-- Agora o FULL OUTER JOIN funciona corretamente
comparacao AS (
  SELECT
    COALESCE(atual.imobiliaria_id, anterior.imobiliaria_id) AS imobiliaria_id,
    COALESCE(atual.imobiliaria_nome, anterior.imobiliaria_nome) AS imobiliaria_nome,
    anterior.total_atendimentos AS atendimentos_mes_anterior,
    atual.total_atendimentos AS atendimentos_mes_atual,
    anterior.dias_ativos AS dias_mes_anterior,
    atual.dias_ativos AS dias_mes_atual,
    anterior.media_diaria AS media_diaria_anterior,
    atual.media_diaria AS media_diaria_atual,
    CASE
      WHEN anterior.media_diaria IS NULL THEN 'Nova'
      WHEN atual.media_diaria IS NULL THEN 'Churned'
      WHEN atual.media_diaria > anterior.media_diaria * 1.1 THEN 'Expanding'
      WHEN atual.media_diaria < anterior.media_diaria * 0.9 THEN 'Contracting'
      ELSE 'Stable'
    END AS tendencia,
    CASE
      WHEN anterior.media_diaria IS NULL OR anterior.media_diaria = 0 THEN NULL
      ELSE ROUND((atual.media_diaria - anterior.media_diaria) * 100.0 / anterior.media_diaria, 1)
    END AS variacao_media_diaria_pct
  FROM dados_mes_atual atual
  FULL OUTER JOIN dados_mes_anterior anterior
    ON atual.imobiliaria_id = anterior.imobiliaria_id
)

SELECT
  (SELECT mes_anterior FROM meses_referencia) AS mes_anterior,
  (SELECT mes_atual FROM meses_referencia) AS mes_atual,
  COUNT(*) AS total_imobiliarias,
  COUNT(CASE WHEN tendencia = 'Nova' THEN 1 END) AS novas,
  COUNT(CASE WHEN tendencia = 'Churned' THEN 1 END) AS churned,
  COUNT(CASE WHEN tendencia IN ('Expanding', 'Stable', 'Contracting') THEN 1 END) AS existentes,
  -- Taxa de Expansion
  COUNT(CASE WHEN tendencia = 'Expanding' THEN 1 END) AS expanding,
  COUNT(CASE WHEN tendencia = 'Stable' THEN 1 END) AS stable,
  COUNT(CASE WHEN tendencia = 'Contracting' THEN 1 END) AS contracting,
  ROUND(COUNT(CASE WHEN tendencia = 'Expanding' THEN 1 END) * 100.0 /
        NULLIF(COUNT(CASE WHEN tendencia IN ('Expanding', 'Stable', 'Contracting') THEN 1 END), 0), 1) AS taxa_expansion_pct,
  -- NVR baseado em media diaria
  ROUND(SUM(CASE WHEN tendencia IN ('Expanding', 'Stable', 'Contracting') THEN media_diaria_atual END), 2) AS media_diaria_total_atual,
  ROUND(SUM(CASE WHEN tendencia IN ('Expanding', 'Stable', 'Contracting') THEN media_diaria_anterior END), 2) AS media_diaria_total_anterior,
  ROUND(SUM(CASE WHEN tendencia IN ('Expanding', 'Stable', 'Contracting') THEN media_diaria_atual END) * 100.0 /
        NULLIF(SUM(CASE WHEN tendencia IN ('Expanding', 'Stable', 'Contracting') THEN media_diaria_anterior END), 0), 1) AS nvr_pct
FROM comparacao;
```

### Query 3: Detalhamento por Imobiliaria (normalizado)

Para investigar quais imobiliarias estao expandindo ou contraindo.

Usar as mesmas CTEs da Query 2, substituir o SELECT final por:

```sql
-- =====================================================
-- DETALHAMENTO: Tendencia por imobiliaria (normalizado)
-- =====================================================

SELECT
  imobiliaria_nome,
  atendimentos_mes_anterior,
  dias_mes_anterior,
  media_diaria_anterior,
  atendimentos_mes_atual,
  dias_mes_atual,
  media_diaria_atual,
  variacao_media_diaria_pct,
  tendencia
FROM comparacao
WHERE tendencia != 'Churned'
ORDER BY media_diaria_atual DESC;
```
