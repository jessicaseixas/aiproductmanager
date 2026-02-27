# Overview

* **Objetivo:** Permitir que corretores visualizem as preferências de imóveis e os imóveis de interesse de um lead para preparar recomendações relevantes antes do contato
* **Quem é afetado:** Corretores de imobiliárias que utilizam o Loft Qualifica Leads para gerenciar leads qualificados
* **Comportamento atual:** N/A - Funcionalidade nova (os corretores atualmente precisam perguntar novamente ao lead sobre suas preferências)
* **Comportamento desejado:** Ao acessar a aba "Interesse" na visão detalhada do lead, o corretor visualiza todas as preferências de imóveis coletadas pela IA durante a qualificação, observações adicionais capturadas, e os imóveis específicos pelos quais o lead demonstrou interesse
* **Por que fazer isso agora:**
    * Corretores perdem tempo perguntando informações que a IA já coletou, causando frustração nos leads
    * Leads qualificados estão esfriando enquanto corretores não têm acesso rápido às preferências
    * Meta de aumentar taxa de agendamento de visitas em 15%
* **Links úteis:**
    * [Figma - Aba Interesse](https://www.figma.com/design/3iXlzrSi8RJEt8Ae52z1Kq/Qualifica-Leads---Standalone?node-id=59-2741)
    * [User Stories - Lead Detailed View](/new-features/lead-detailed-view/user-stories.md)
    * [Funcionalidades Existentes](/context/our-product/existing-features.md)

---

# Definicao de Pronto

* Todos os critérios de aceitacao satisfeitos e verificados
* Testes unitários escritos com >80% de cobertura
* Testes de integração para a API de interesses
* Teste E2E para visualizacao de preferências e clique em imóvel
* Eventos de analytics verificados em staging com propriedades corretas
* Dashboard de observabilidade criado e verificado
* Auditoria de acessibilidade aprovada (WCAG AA)
* Performance verificada (<1.5s tempo de carregamento da aba)
* Lazy loading de imagens verificado
* Code review aprovado
* QA sign-off obtido
* Feature flag configurada para rollout gradual

---

# Escopo

## Dentro do escopo

* Seção "Detalhes de Interesse" com preferências de imóveis em layout de duas colunas
* Campos de preferências: Tipo de negócio, Cidade, Bairro(s), Tipo de imóvel, Valor de locacao desejado, Valor total desejado, Quartos, Suites, Banheiros, Vagas, Mobiliado, Pet-friendly
* Seção "Observacoes Adicionais" com lista de notas capturadas pela IA
* Seção "Imóveis de Interesse" com cards de imóveis
* Card de imóvel com: imagem, badge "Principal", tipo de transacao, tipo de imóvel, preco formatado, endereco, específicações (m2, quartos, banheiros, vagas), datas
* Botão "Ver detalhes" em cada card de imóvel
* Estados de erro, loading e empty state
* Eventos de analytics para rastreamento de uso

## Fora do escopo

* Adicionar/remover imóveis de interesse manualmente
* Editar preferências do lead
* Funcionalidade de comparacao de imóveis
* Enviar sugestoes de imóveis ao lead diretamente da tela
* Integracao em tempo real com atualizacoes de preferências

---

# Especificação de UX + Comportamento

## Pontos de entrada

* Navegacao via abas na Visao Detalhada do Lead > Clicar na aba "Interesse"
* Deep link direto: `/leads/{lead_id}/interesse`

## Fluxo

1. Corretor navega para a aba "Interesse" na visao detalhada do lead
2. Sistema exibe loading skeleton enquanto carrega os dados
3. Sistema carrega preferências de imóveis coletadas durante qualificacao via IA
4. Sistema exibe seção "Detalhes de Interesse" com preferências em grid de duas colunas
5. Sistema exibe seção "Observacoes Adicionais" com lista de notas da IA (se houver)
6. Sistema carrega e exibe seção "Imóveis de Interesse" com cards de imóveis
7. Corretor pode clicar em "Ver detalhes" para abrir a página de detalhes do imóvel
8. (Assincrono) Imagens dos imóveis sao carregadas via lazy loading conforme scroll

## Estados

* **Sucesso:** Todas as secoes exibem dados corretamente; imóvel principal destacado com badge "Principal"
* **Loading:** Skeleton placeholders para cards de preferências e cards de imóveis
* **Empty (sem preferências):** Exibir "Preferências não coletadas durante qualificacao" na seção de detalhes
* **Empty (sem imóveis):** Exibir "Nenhum imóvel de interesse registrado" na seção de imóveis
* **Empty (sem observacoes):** Seção "Observacoes Adicionais" não é exibida
* **Erro (API timeout):** Exibir mensagem "Erro ao carregar interesses" com botão "Tentar novamente" após 3s de loading
* **Erro (404):** Exibir "Lead não encontrado" com botão para voltar a lista
* **Erro (imagem):** Exibir placeholder de imagem genérica para imóveis sem imagem disponível
* **Parcial:** Exibir campos disponiveis; campos ausentes mostram "-"

---

# Especificações técnicas

## Serviços

* `GET /api/v1/leads/{lead_id}/interests` - Retorna preferências, observacoes e imóveis de interesse do lead
* Endpoint deve suportar páginacao para lista de imóveis (query params: `limit`, `offset`)
* Cache no cliente com invalidação em 5 minutos
* Rate limiting: 100 req/min por usuário

## Contrato de API

```
GET /api/v1/leads/{lead_id}/interests

Response 200:
{
  "preferences": {
    "business_type": "locacao" | "venda" | "both" | null,
    "city": "string | null",
    "neighborhoods": ["string"] | null,
    "property_type": "apartamento" | "casa" | "studio" | "cobertura" | null,
    "rent_value": { "min": number | null, "max": number | null } | null,
    "total_value": { "min": number | null, "max": number | null } | null,
    "bedrooms": { "min": number } | null,
    "suites": { "min": number } | null,
    "bathrooms": { "min": number } | null,
    "parking": { "min": number } | null,
    "furnished": boolean | null,
    "pet_friendly": boolean | null
  },
  "observations": ["string"],
  "properties": [
    {
      "id": "string",
      "is_primary": boolean,
      "type": "venda" | "locacao",
      "property_type": "string",
      "price": number,
      "address": "string",
      "área_m2": number,
      "bedrooms": number,
      "bathrooms": number,
      "parking": number,
      "image_url": "string | null",
      "created_at": "ISO8601",
      "updated_at": "ISO8601",
      "viewed_by_lead_at": "ISO8601 | null"
    }
  ],
  "págination": {
    "total": number,
    "limit": number,
    "offset": number,
    "has_more": boolean
  }
}

Response 404:
{
  "error": "lead_not_found",
  "message": "Lead não encontrado"
}

Response 500:
{
  "error": "internal_error",
  "message": "Erro interno do servidor"
}
```

## Mudanças no modelo de dados

* Nenhuma mudança necessária - dados já coletados durante fluxo de qualificacao existente
* [TBD @Backend] Confirmar se tabela `lead_property_interests` já existe com campo `is_primary`
* [TBD @Backend] Confirmar se campo `viewed_by_lead_at` esta sendo populado

## Segurança & privacidade

* Autenticação obrigatória via token JWT
* Autorizacao: corretor só pode acessar leads atribuidos a ele ou da mesma imobiliária
* Não logar PII sensivel nos logs (endereco completo, valores específicos)
* Válidar `lead_id` como UUID válido antes de processar requisicao
* Sanitizar dados de observacoes para prevencao de XSS

---

# Critérios de aceite

* Seção "Detalhes de Interesse" exibe preferências em layout de duas colunas responsivo (coluna única em mobile)
* Campos exibidos: Tipo de negócio, Cidade, Bairro(s), Tipo de imóvel, Valor de locacao desejado, Valor total desejado, Quartos, Suites, Banheiros, Vagas, Mobiliado (Sim/Nao), Pet-friendly (Sim/Nao)
* Múltiplos bairros exibidos como lista separada por virgulas
* Preferências numericas exibem formato "+N" (ex: "+2" para "2 ou mais quartos")
* Preferências ausentes exibem "-" como placeholder
* Valores monetarios formatados como "R$ X.XXX,XX" (locacao) ou "R$ X.XXX.XXX" (venda)
* Seção "Observacoes Adicionais" exibe lista com bullet points das notas capturadas pela IA
* Observacoes longas (>200 caracteres) truncadas com botão "Ver mais"
* Card de imóvel exibe: thumbnail da imagem, badge "Principal" (quando aplicável), tipo de transacao, tipo de imóvel, preco formatado, endereco, specs (m2, quartos, banheiros, vagas)
* Card exibe datas: "Cadastrado em", "Atualizado em", "Visualizado pelo lead em"
* Botão "Ver detalhes" navega para página de detalhes do imóvel
* NFR (performance): Aba carrega em <1.5 segundos p95
* NFR (imagens): Lazy loading implementado para imagens de imóveis
* NFR (páginacao): Máximo 5 imóveis exibidos inicialmente; botão "Carregar mais" para ver mais
* Acessibilidade: Imagens possuem alt text descritivo; precos anunciados com contexto de moeda para screen readers
* Analytics: Evento `lead_interest_viewed` dispara ao visualizar aba com `{lead_id, broker_id, preferences_count, properties_count, timestamp}`
* Analytics: Evento `interest_property_clicked` dispara ao clicar em imóvel com `{lead_id, property_id, broker_id, is_primary}`

---

# Observabilidade & Analytics

## Eventos

* `lead_interest_viewed` props `{lead_id, broker_id, preferences_filled_count, properties_count, load_time_ms, timestamp}` trigger: quando corretor visualiza a aba Interesse
* `interest_property_clicked` props `{lead_id, property_id, broker_id, is_primary, position_in_list}` trigger: quando corretor clica em "Ver detalhes" de um imóvel
* `interest_observations_expanded` props `{lead_id, broker_id}` trigger: quando corretor expande observacoes truncadas
* `interest_load_more_clicked` props `{lead_id, broker_id, current_count, total_count}` trigger: quando corretor clica em "Carregar mais" imóveis
* `lead_interest_error` props `{lead_id, broker_id, error_type, error_message, timestamp}` trigger: quando ocorre erro ao carregar dados

## Dashboard (DataDog/Observabilidade)

* Taxa de visualizacao da aba Interesse por dia/semana
* Tempo médio de carregamento da aba (p50, p95, p99)
* Taxa de cliques em imóveis de interesse
* % de leads com preferências preenchidas vs vazias
* Taxa de erro por tipo de erro

## Alertas

* Tempo de carregamento >3s em >5% das requisicoes por 10 minutos (warning)
* Taxa de erro >2% em 5 minutos (page on-call)
* Zero visualizacoes da aba por >2 horas durante horário comercial (investigar)

## Auditoria

* Logar acesso a aba Interesse com: broker_id, lead_id, timestamp, load_time_ms, resultado (sucesso/erro)

---

# Plano de Rollout & Riscos

## Rollout

Feature flag `lead_interesse_tab_enabled` no frontend para habilitar/desabilitar aba

* **Fase 1:** Testar com contas internas em staging por 3 dias
* **Fase 2:** Habilitar para 2-3 imobiliárias piloto em producao (parceiros early adopters)
* **Fase 3:** Monitorar por 1 semana; se taxa de erro <1% e tempo de carga <1.5s p95, habilitar para 20% dos usuários
* **Fase 4:** Monitorar por mais 1 semana; se métricas saudaveis, rollout 100%

## Rollback

1. Desabilitar feature flag `lead_interesse_tab_enabled` via dashboard de configuração
2. Aba "Interesse" deixa de aparecer na navegação; usuários redirecionados para aba "Detalhes"
3. Dados permanecem intactos no backend; nenhuma perda de informacao
4. Investigar causa raiz e corrigir antes de reabilitar

---

# Riscos

1. **Dados de preferências incompletos:** Leads qualificados antes da implementação podem ter dados parciais → mitigar exibindo campos disponiveis com "-" para ausentes e mensagem informativa
2. **Imagens de imóveis lentas para carregar:** CDN pode ter latencia em imagens de alta resolução → mitigar com lazy loading, placeholder images, e compressao de imagens no CDN
3. **Alto volume de imóveis de interesse:** Leads com 10+ imóveis podem impactar performance → mitigar com páginacao (5 iniciais) e botão "Carregar mais"
4. **Integracao com catalogo de imóveis:** Dependencia de API de catalogo pode causar falhas → mitigar com fallback gracioso mostrando dados disponiveis e mensagem de erro parcial

---

# Questões em aberto

* \[PM\] "Ver detalhes" deve abrir na mesma aba ou em nova aba? (ate 10/01/2026)
* \[PM\] Qual limite de imóveis exibir antes de páginar? (sugestao: 5) (ate 10/01/2026)
* \[Engineering\] Dados de imóveis sao buscados separadamente ou embutidos na resposta do lead? (ate 10/01/2026)
* \[Engineering\] Campo `is_primary` já esta sendo populado durante fluxo de qualificacao? (ate 10/01/2026)
* \[Design\] Observacoes longas devem truncar após quantos caracteres? (sugestao: 200) (ate 10/01/2026)

---

# Premissas

* Imagens de imóveis sao servidas via CDN com URLs pre-assinadas
* Imóvel principal e marcado durante o fluxo de qualificacao pela IA
* Dados de preferências já estão sendo coletados pelo assistente de IA durante qualificacao
* Story 1 (Header & Tab Navigation) estara concluida antes do inicio desta implementação
* API de catalogo de imóveis está disponível e documentada
* Observacoes adicionais sao strings simples capturadas durante conversa com lead
