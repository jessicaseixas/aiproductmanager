
# Backoffice - Listagem de Atendimentos

---

# Overview

* **Objetivo:** Implementar a tela de listagem de atendimentos no backoffice do Loft Qualifica Leads Standalone, permitindo que usuários das imobiliárias visualizem, pesquisem e filtrem todas as sessões de qualificação de leads realizadas pelo assistente de IA.
* **Quem é afetado:** Usuários do backoffice do Loft Qualifica Leads (administradores e corretores de imobiliárias) que precisam acompanhar e gerenciar os atendimentos realizados pelo assistente de IA.
* **Comportamento atual:** N/A - Nova funcionalidade para a versão standalone do produto (lançamento previsto para Abr/2026).
* **Comportamento desejado:** Usuários podem visualizar uma lista páginada de todos os atendimentos, pesquisar por nome/telefone do lead, filtrar por múltiplos critérios (status, tipo de negócio, interesse em visita, origem, datas) e navegar entre diferentes visualizações (Todos, Em andamento, Finalizados).
* **Por que fazer isso agora:** A versão standalone do Loft Qualifica Leads será lançada em Abr/2026 para clientes que não utilizam o Loft/ CRM. Esta tela é essencial para que as imobiliárias tenham visibilidade sobre os atendimentos realizados pelo assistente de IA, permitindo acompanhamento do processo de qualificação e identificação de leads que precisam de atenção humana.
* **Links úteis:**
    * [Figma - Lista principal](https://www.figma.com/design/3iXlzrSi8RJEt8Ae52z1Kq/Qualifica-Leads---Standalone?node-id=48-1848)
    * [Figma - Lista com dados](https://www.figma.com/design/3iXlzrSi8RJEt8Ae52z1Kq/Qualifica-Leads---Standalone?node-id=116-1173)
    * [Figma - Modal de filtros (status)](https://www.figma.com/design/3iXlzrSi8RJEt8Ae52z1Kq/Qualifica-Leads---Standalone?node-id=116-4853)
    * [Figma - Modal de filtros (tipo negócio)](https://www.figma.com/design/3iXlzrSi8RJEt8Ae52z1Kq/Qualifica-Leads---Standalone?node-id=116-5232)
    * [Figma - Modal de filtros (origem)](https://www.figma.com/design/3iXlzrSi8RJEt8Ae52z1Kq/Qualifica-Leads---Standalone?node-id=116-5425)
    * [Figma - Empty state](https://www.figma.com/design/3iXlzrSi8RJEt8Ae52z1Kq/Qualifica-Leads---Standalone?node-id=161-3514)

---

# Casos de Uso Principais

## 1. Priorizar leads quentes para follow-up
**Quem:** Corretor / Gestor
**Quando:** Início do dia ou após receber notificação de lead qualificado
**Ação:** Filtrar por `Status = Concluído` + `Interesse em visita = Sim`
**Por quê:** Leads qualificados pela IA que demonstraram interesse em visitar são os mais quentes. Priorizar o contato com eles aumenta a taxa de conversão — dados de mercado mostram 2.6x mais conversão quando o lead é atendido em menos de 5 minutos.

## 2. Atender leads que precisam de intervenção humana
**Quem:** Corretor / Gestor de plantão
**Quando:** Múltiplas vezes ao dia (monitoramento contínuo)
**Ação:** Filtrar por `Status = Ajuda solicitada` ou usar tab "Em andamento"
**Por quê:** A IA identificou que não consegue resolver sozinha (dúvida complexa, lead pediu para falar com humano, situação fora do roteiro). Esses leads estão "quentes" esperando resposta — deixar esfriar significa perder o negócio para a concorrência.

## 3. Revisar leads sem resposta para reengajamento
**Quem:** Gestor / Corretor no fim do dia
**Quando:** Final do expediente ou revisão semanal
**Ação:** Filtrar por `Status = Sem resposta` + `Data último contato` nos últimos 7 dias
**Por quê:** Apróximadamente 41% dos leads online nunca são atendidos no mercado imobiliário brasileiro. Leads que não responderam à IA podem ser reengajados manualmente pelo corretor — uma segunda tentativa pode recuperar oportunidades perdidas.

---

# Definição de Pronto

* Critérios de aceitação completamente satisfeitos
* Testes automatizados adicionados (unitários e integração)
* Integração testada em staging com dados reais
* Eventos de analytics verificados em staging com propriedades corretas
* Dashboard de observabilidade criado e verificado
* Performance validada com volume de dados realista (>1000 registros)
* Responsividade testada em diferentes resoluções (desktop)
* Acessibilidade básica validada (navegação por teclado, contraste)

---

# Escopo

## Dentro do escopo

* Tela de listagem de atendimentos com tabela páginada
* Campo de busca por nome ou telefone do lead
* Modal de filtros com múltiplos critérios:
  * Status do atendimento (multi-select)
  * Tipo de negócio (multi-select)
  * Interesse em visita (single-select)
  * Origem (single-select)
  * Data do primeiro contato (date picker)
  * Data do último contato (date picker)
* Tabs para filtrar por status: "Todos", "Em andamento", "Finalizados"
* Tags/chips para filtros aplicados com opção de remover
* Páginação com navegação e contador de resultados
* Empty state quando não há atendimentos
* Integração com sidebar de navegação existente

## Fora do escopo

* Tela de detalhes do atendimento (ticket separado)
* Exportação de dados para CSV/Excel
* Ações em massa (selecionar múltiplos atendimentos)
* Notificações em tempo real de novos atendimentos
* Filtros salvos/favoritos
* Ordenação customizada de colunas
* Versão mobile/tablet

---

# Especificação de UX + Comportamento

## Pontos de entrada

* Menu lateral > "Atendimentos" (item destacado quando ativo)
* URL direta: `/atendimentos`

## Fluxo

1. Usuário acessa a tela de Atendimentos via menu lateral
2. Sistema carrega lista de atendimentos páginada (10 itens por página)
3. Usuário pode digitar no campo de busca para filtrar por nome/telefone
4. Usuário pode clicar em "Filtrar" para abrir modal de filtros
5. No modal, usuário seleciona os filtros desejados (multi-select ou single-select conforme campo)
6. Filtros selecionados aparecem como chips/tags dentro do campo correspondente
7. Usuário clica em "Aplicar" para aplicar filtros ou "Cancelar" para descartar
8. Filtros aplicados aparecem como chips removíveis na interface principal
9. Usuário pode clicar no "X" de um chip para remover filtro individual
10. Usuário pode navegar entre tabs "Todos", "Em andamento", "Finalizados"
11. Usuário pode navegar entre páginas usando páginador

## Estados

* **Carregando:** Skeleton/loading state enquanto dados são carregados
* **Lista preenchida:** Tabela com dados dos atendimentos
* **Empty state:** Quando não há atendimentos cadastrados:
  * Mensagem: "Seus leads aparecerão aqui"
  * Submensagem: "Fique tranquilo! Todos os leads atendidos ou em atendimento aparecerão nesta tela. Assim que o Qualifica Leads atender seu primeiro lead, ele será exibido aqui."
  * Botão de filtro desabilitado
* **Sem resultados:** Quando filtros/busca não retornam dados:
  * Mensagem: "Nenhum atendimento encontrado"
  * Submensagem: "Tente ajustar os filtros ou termos de busca"
* **Erro:** Falha ao carregar dados → exibir mensagem de erro com botão "Tentar novamente"

## Componentes da tabela

| Coluna | Descrição | Formato |
|--------|-----------|---------|
| Status | Tag colorida com status do atendimento | Tag com cor |
| Nome | Nome do lead | Texto |
| Telefone | Telefone do lead | Texto formatado |
| Origem | Portal/canal de origem | Texto |
| Tipo de negócio | Compra, Venda, Locação | Texto |
| Interesse em visita | Sim, Não, ou "-" | Texto |
| Primeiro contato | Data e hora do início | DD/MM/YYYY HH:mm |
| Último contato | Data e hora da última interação | DD/MM/YYYY HH:mm |

## Status e cores

| Status | Cor (Hex) | Descrição |
|--------|-----------|-----------|
| Em atendimento | #697077 (cinza) | Atendimento em andamento pela IA |
| Ajuda solicitada | #FFA600 (laranja) | IA solicitou intervenção humana |
| Intervenção humana | #697077 (cinza) | Corretor assumiu o atendimento |
| Concluído | #20A483 (verde) | Atendimento finalizado com sucesso |
| Sem resposta | #697077 (cinza) | Lead não respondeu no tempo limite |
| Número inválido | #697077 (cinza) | Não foi possível contatar o lead |

---

# Especificações técnicas

## Serviços

[TBD @Eng]

## Modelo de dados (response)

[TBD @Eng]

## Segurança & privacidade

* Autenticação via token JWT obrigatória
* Autorização: usuário deve ter permissão de acesso à imobiliária (tenant)
* Telefones exibidos parcialmente mascarados na UI (ex: (11) 9****-1234) - [TBD @PM - confirmar requisito de máscaramento]
* Não logar telefones completos ou dados PII em logs de aplicação
* Rate limiting: 100 requests/minuto por usuário

---

# Critérios de aceite

## Funcionalidade principal
* Usuário autenticado consegue visualizar lista de atendimentos da sua imobiliária
* Lista exibe todas as 8 colunas conforme específicado (Status, Nome, Telefone, Origem, Tipo de negócio, Interesse em visita, Primeiro contato, Último contato)
* Status são exibidos como tags com cores corretas conforme mapeamento
* Datas são formatadas no padrão brasileiro (DD/MM/YYYY HH:mm)

## Busca
* Campo de busca filtra por nome do lead (case-insensitive, busca parcial)
* Campo de busca filtra por telefone do lead (ignora formatação)
* Busca é acionada após 300ms de debounce ou ao pressionar Enter
* Limpar campo de busca restaura lista completa

## Filtros
* Modal de filtros abre ao clicar no botão "Filtrar"
* Filtro de status permite seleção múltipla
* Filtro de tipo de negócio permite seleção múltipla
* Filtro de interesse em visita permite seleção única
* Filtro de origem permite seleção única
* Filtros de data utilizam date picker com formato brasileiro
* Chips de filtros selecionados aparecem dentro do campo no modal
* Botão "Aplicar" fecha modal e aplica filtros
* Botão "Cancelar" fecha modal sem aplicar alterações
* Filtros aplicados aparecem como chips removíveis abaixo da busca
* Clicar no "X" do chip remove o filtro correspondente

## Tabs
* Tab "Todos" exibe todos os atendimentos
* Tab "Em andamento" exibe apenas atendimentos com status: em_atendimento, ajuda_solicitada, intervencao_humana
* Tab "Finalizados" exibe apenas atendimentos com status: concluido, sem_resposta, número_inválido
* Contador de cada tab exibe quantidade de itens

## Páginação
* Páginação exibe 10 itens por página
* Contador exibe "Mostrando resultados de X-Y de Z"
* Navegação entre páginas funciona corretamente
* Mudar filtros reseta para página 1

## Empty states
* Empty state principal exibe mensagem correta quando não há atendimentos
* Empty state de busca/filtro exibe mensagem quando não há resultados
* Botão de filtro é desabilitado no empty state principal

## NFRs
* NFR (performance): Lista carrega em <2 segundos p95 para até 1000 registros
* NFR (performance): Busca e filtros respondem em <500ms p95
* NFR (confiabilidade): Erros de API são tratados com mensagem amigável e opção de retry
* Segurança: Usuário só visualiza atendimentos da própria imobiliária (tenant isolation)
* Segurança: Requisições sem token válido retornam 401

## Analytics
* Analytics: Evento `atendimentos_list_viewed` dispara ao carregar a página
* Analytics: Evento `atendimentos_search_performed` dispara ao realizar busca com `{search_term, results_count}`
* Analytics: Evento `atendimentos_filter_applied` dispara ao aplicar filtros com `{filters_used[], results_count}`
* Analytics: Evento `atendimentos_tab_changed` dispara ao mudar tab com `{tab_name, results_count}`
* Analytics: Evento `atendimentos_page_changed` dispara ao navegar páginas com `{page_number}`

---

# Métricas de Sucesso

> **Nota:** Métricas de ativação e retenção (D7, primeiro uso) devem ser medidas no nível do **produto Standalone**, não desta tela específica. As métricas abaixo focam em adoção, engajamento e qualidade da feature.

## Adoção

| Métrica | Descrição | Fórmula |
|---------|-----------|---------|
| Penetração da feature | % de usuários ativos do produto que acessam a tela de Atendimentos | `(Usuários com 'list_viewed' / Total usuários ativos do produto) × 100` |

## Engajamento

| Métrica | Descrição | Fórmula |
|---------|-----------|---------|
| Frequência de uso semanal | Média de dias/semana que usuários acessam a tela | `SUM(dias com acesso) / COUNT(usuários ativos) por semana` |
| Taxa de uso de filtros | % de sessões que utilizam filtros | `(Sessões com 'filter_applied' / Sessões com 'list_viewed') × 100` |
| Taxa de uso de busca | % de sessões que utilizam busca | `(Sessões com 'search_performed' / Sessões com 'list_viewed') × 100` |
| Distribuição de tabs | % de uso por tab (Todos/Em andamento/Finalizados) | `COUNT(tab_changed) GROUP BY tab_name` |

## Qualidade (Guardrails)

| Métrica | Descrição | Fórmula |
|---------|-----------|---------|
| Taxa de erros | % de requisições com erro na listagem | `(Eventos 'list_error' / Total requisições) × 100` |
| Latência p95 | Tempo de carregamento da lista (percentil 95) | `PERCENTILE(latency_ms, 0.95)` |

## Segmentação (L2)

| Métrica | Descrição | Fórmula |
|---------|-----------|---------|
| Adoção por porte | Penetração segmentada por tamanho do tenant | `Penetração GROUP BY tenant_size` |
| Engajamento por porte | Frequência semanal por tamanho do tenant | `Frequência semanal GROUP BY tenant_size` |

---

# Observabilidade & Analytics

## Eventos

* `atendimentos_list_viewed` props `{tenant_id, user_id, total_count, timestamp}` trigger: ao carregar a tela
* `atendimentos_search_performed` props `{tenant_id, user_id, search_term_length, results_count, latency_ms}` trigger: ao executar busca (não logar termo de busca por conter PII)
* `atendimentos_filter_applied` props `{tenant_id, user_id, filters_used[], results_count, latency_ms}` trigger: ao aplicar filtros
* `atendimentos_tab_changed` props `{tenant_id, user_id, tab_name, results_count}` trigger: ao mudar tab
* `atendimentos_page_changed` props `{tenant_id, user_id, page_number, total_pages}` trigger: ao navegar páginas
* `atendimentos_list_error` props `{tenant_id, user_id, error_code, error_message}` trigger: ao ocorrer erro na listagem

## Dashboard (DataDog/Observabilidade)

* Taxa de visualização da tela de atendimentos por tenant
* Latência de carregamento da lista (p50/p95/p99)
* Taxa de uso de busca vs. filtros
* Distribuição de uso das tabs
* Taxa de erros na listagem

## Alertas

* Latência de listagem >3s p95 por >5 minutos (warning)
* Taxa de erro >5% em 5 minutos (page on-call)
* Zero acessos à tela por >1 hora durante horário comercial (investigar)

## Auditoria

* Logar acessos à listagem com: tenant_id, user_id, timestamp, filtros aplicados (sem PII)

---

# Plano de Rollout & Riscos

## Rollout

Feature flag `standalone_atendimentos_list` para habilitar/desabilitar a funcionalidade

* **Fase 1:** Deploy em staging e testes internos com dados de teste
* **Fase 2:** Habilitar para 2-3 imobiliárias piloto do programa beta standalone
* **Fase 3:** Monitorar por 1 semana; se taxa de erro <1% e feedback positivo, expandir para 20% dos usuários beta
* **Fase 4:** Rollout 100% para todos os usuários do standalone

## Rollback

* Desabilitar feature flag `standalone_atendimentos_list`
* Usuários são redirecionados para tela inicial ou mensagem de "em breve"
* Dados permanecem intactos no backend
* Re-habilitar após correção se necessário

---

# Riscos

1. **Performance com alto volume:** Imobiliárias com muitos atendimentos podem experimentar lentidão → mitigar com páginação eficiente no backend, índices adequados no banco, e lazy loading
2. **Filtros complexos:** Combinação de múltiplos filtros pode gerar queries lentas → mitigar com otimização de queries, cache de filtros frequentes, timeout com feedback ao usuário
3. **Dados sensíveis expostos:** Telefones de leads são PII → mitigar com máscaramento parcial na UI e não logar dados completos

---

# Questões em aberto

* \[PM\] Confirmar se telefones devem ser mascarados na listagem (ex: (11) 9****-1234)?
* \[PM\] Qual o limite máximo de resultados por página que o usuário pode selecionar (10, 25, 50)?
* \[Design\] O clique em uma linha da tabela deve levar para detalhes do atendimento ou abrir um drawer?
* \[Eng\] Qual a estimativa de volume de dados por tenant para dimensionar a solução de páginação?

---

# Premissas

* API de listagem de atendimentos já existe ou será desenvolvida em paralelo
* Autenticação e autorização do standalone já estão implementadas
* Design system e componentes base (tabela, modal, inputs) já existem
* Dados de atendimentos já são persistidos com todos os campos necessários (status, origem, tipo_negócio, etc.)
* Sidebar de navegação já está implementada e este item será adicionado a ela
