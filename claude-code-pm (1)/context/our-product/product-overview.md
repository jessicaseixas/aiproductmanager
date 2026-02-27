# Visão geral do produto

## O que é?

Loft Qualifica Leads é uma ferramenta conversacional com IA projetada para automatizar a qualificação de leads para imobiliárias, operando via WhatsApp para permitir engajamento 24 horas com potenciais clientes. O sistema utiliza inteligência artificial para interagir com leads automaticamente, realizando qualificação e triagem automática em até 15 segundos, coletando informações abrangentes e avaliando seu potencial de conversão. As principais funcionalidades incluem disponibilidade 24/7 no WhatsApp respondendo a consultas continuamente sem intervenção humana, processamento rápido de leads em 15 segundos, identificação automática de prospects com maior potencial de conversão, enriquecimento de dados através de coleta de perfil durante as conversas, integração transparente com CRM onde leads qualificados fluem diretamente para os fluxos do Loft/ CRM, e simulação de conversação natural com IA. O produto elimina atrasos na resposta a leads e períodos de esfriamento, reduz o trabalho manual de qualificação para equipes de vendas, permite que a equipe foque em atividades de alto valor, melhora a qualidade dos dados para follow-ups personalizados, e suporta reengajamento de leads não convertidos anteriormente, posicionando-se como infraestrutura de inteligência essencial para vantagem competitiva na conversão de leads.

## Arquitetura do produto

O produto é composto por três componentes principais que trabalham juntos para entregar a solução completa de qualificação de leads:

```
                    ┌─────────────────────────────┐
                    │    LOFT QUALIFICA LEADS     │
                    │  Qualificação inteligente   │
                    │       de leads imob.        │
                    └─────────────┬───────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
          ▼                       ▼                       ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│   ASSISTENTE IA     │ │     BACK-OFFICE     │ │    INTEGRAÇÕES      │
│     WhatsApp        │ │                     │ │                     │
├─────────────────────┤ ├─────────────────────┤ ├─────────────────────┤
│                     │ │                     │ │                     │
│ • Atendimento 24/7  │ │ • Gestão de leads   │ │ • Portais imob.     │
│ • Qualificação      │ │ • Dashboard         │ │   (OLX, Zap, etc.)  │
│   automática        │ │ • Configurações     │ │ • CRMs              │
│ • Agendamento       │ │ • Usuários          │ │   (Vista, Hubspot)  │
│ • Handoff humano    │ │                     │ │ • Catálogo imóveis  │
│                     │ │                     │ │                     │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

### Assistente IA (WhatsApp)

O Assistente de IA é o componente voltado para o cliente que interage diretamente com leads via WhatsApp. Ele é responsável por:

- **Disponibilidade 24/7**: Responde a leads a qualquer momento, incluindo noites, finais de semana e feriados, garantindo que nenhum lead fique sem resposta
- **Qualificação automática**: Conduz conversas estruturadas para coletar informações do lead e avaliar intenção e prontidão de compra/aluguel
- **Sugestão de imóveis**: Entende as preferências do lead e pode sugerir imóveis relevantes do portfólio da imobiliária
- **Agendamento de visitas**: Agenda visitas a imóveis diretamente na conversa, integrando com calendários dos corretores
- **Handoff humano**: Transfere conversas para atendentes humanos quando necessário (perguntas complexas, leads de alto valor ou solicitações explícitas)

### Back-office

O back-office é a aplicação web usada por imobiliárias para gerenciar e monitorar o produto. Ele oferece:

- **Gestão de leads**: Visualizar todos os leads, seu status de qualificação, histórico de conversas e dados coletados
- **Dashboard e analytics**: Monitorar métricas-chave como tempo de resposta, taxa de qualificação, funil de conversão e performance da IA
- **Configuração**: Personalizar comportamento da IA, critérios de qualificação, horário comercial e respostas automatizadas
- **Gestão de usuários**: Controlar acesso da equipe, atribuir leads a corretores e gerenciar permissões

### Integrações

A camada de integrações conecta o Loft Qualifica Leads a sistemas externos, permitindo fluxo automatizado de leads:

- **Portais imobiliários**: Receber leads automaticamente dos principais portais brasileiros como OLX, ZAP Imóveis, Viva Real e Imovelweb
- **Sistemas de CRM**: Enviar leads qualificados e dados de conversas para CRMs como Loft/ CRM (Vista), Hubspot, RD Station e outros
- **Catálogo de imóveis**: Sincronizar inventário de imóveis da imobiliária para que a IA possa discutir e sugerir listagens disponíveis

## Problemas que resolve

A dinâmica de busca imobiliária online apresenta desafios significativos tanto para leads quanto para imobiliárias, criando ineficiências que impactam taxas de conversão e performance do negócio.

### Da perspectiva do lead:
- **Velocidade é crítica**: Leads atendidos em até 5 minutos apresentam taxas de conversão 2,6x maiores para visitas a imóveis e 3x maiores para vendas comparados aos que esperam mais de 1 hora
- **Respostas atrasadas são a norma**: O tempo médio de resposta das imobiliárias brasileiras a leads online é de aproximadamente 6 horas, muito além da janela ideal de 5 minutos
- **Muitos leads são completamente ignorados**: Cerca de 41% dos leads que chegam online nunca recebem qualquer atenção das imobiliárias, representando enormes oportunidades perdidas

### Da perspectiva da imobiliária:
- **Alto volume cria gargalos operacionais**: O volume de leads online é substancial, e corretores precisam equilibrar qualificação de leads com diversas outras tarefas essenciais como cadastrar imóveis, realizar visitas e fechar negócios
- **Leads frios desperdiçam tempo valioso**: Muitos leads que chegam online não respondem imediatamente ou respondem indicando que não estão ativamente procurando imóveis, apenas navegando por curiosidade, fazendo imobiliárias perderem tempo com prospects não qualificados
- **Sem visibilidade de priorização**: Corretores não conseguem identificar antecipadamente quais leads têm maior potencial de conversão antes da qualificação, frequentemente resultando em tempo perdido com leads frios ao invés de focar em prospects quentes, perdendo negócios para concorrentes que respondem mais rápido

## Visão do produto

Ser o melhor produto de qualificação automatizada de leads no setor imobiliário brasileiro, oferecendo uma excelente experiência aos leads, tornando as imobiliárias mais eficientes e aumentando a taxa de fechamento de negócios.

## Público-alvo

Imobiliárias (especialmente pequenas e médias) e corretores autônomos.

### Corretores autônomos e imobiliárias pequenas/médias

Este segmento é sensível a preço e busca soluções simples e fáceis de usar. Sua principal necessidade é aumentar as taxas de conversão de leads. Ao posicionar o produto para este público, deve-se enfatizar melhoria de conversão, preço acessível e uso de Inteligência Artificial.

### Grandes imobiliárias e redes de imobiliárias

Este segmento busca soluções que integrem com seus sistemas existentes e possam ser customizadas para seus fluxos de trabalho. Precisam aumentar taxas de conversão de leads enquanto reduzem tempo desperdiçado com leads frios, e requerem soluções economicamente viáveis em alta escala. Ao posicionar o produto para este público, o foco deve ser em melhoria de conversão, redução de tempo gasto com leads frios e uso de Inteligência Artificial.

## Vantagens competitivas

- Portfólio de produtos e serviços imobiliários da Loft
- Loft/ CRM é o terceiro em market share no setor imobiliário brasileiro e, como somos donos de ambos os produtos, podemos criar uma integração muito fluida com ele, enquanto limitamos nossos concorrentes de fazer o mesmo
- Base atual de usuários dos produtos Loft, que pode ser usada para aquisição de clientes com CAC 0

## Distribuição

### Add-on do Loft/ CRM

Disponível desde out/2025 como add-on para todos os clientes existentes e novos do Loft/ CRM.

### Versão standalone

Disponível a partir de abr/2026 para qualquer pessoa, independente de serem clientes do Loft/ CRM ou não.

## Monetização

### Modelo de precificação

O produto usa um modelo de precificação baseado em uso, pós-pago, onde clientes pagam por conversa entre um lead e o assistente de IA. Isso garante que clientes paguem apenas pelo que realmente consomem, sem requisitos de volume mínimo.

### Definição de conversa

Uma conversa é definida como uma qualificação em andamento sendo conduzida pelo assistente de IA com um lead específico. Critérios principais:
- Considerada "em andamento" enquanto o lead não estiver inativo por 60 minutos
- O timer de 60 minutos de inatividade só conta durante horário comercial (6h - 20h BRT)
- Uma nova conversa pode ser iniciada para um lead (pela IA ou pelo lead) quando não há uma conversa em andamento para ele
- Toda conversa é cobrada, independente de ser o mesmo lead

### Exceções de cobrança

Os seguintes tipos de conversa **não são cobrados**:
- Conversas onde o lead nunca respondeu
- Conversas onde não foi possível contatar o lead (ex.: número de telefone errado ou Meta decidiu não entregar a mensagem)

### Precificação por volume

O preço por conversa diminui progressivamente baseado no volume mensal de conversas do cliente. O preço inicial é R$4,00 por conversa, podendo diminuir até R$1,80 para clientes de alto volume.

#### Fórmula de precificação

```python
import math

logarithmic_trend = -0.805
vertical_shift = 7.7072
minimum_price = 1.8
maximum_price = 4.0

raw_price = logarithmic_trend * math.log(quantity) + vertical_shift
return max(minimum_price, min(maximum_price, raw_price))
```

A fórmula usa uma curva logarítmica para calcular o preço por conversa baseado no volume mensal (`quantity`), limitado entre R$1,80 e R$4,00.

### Controle de custos

Clientes têm controle total sobre seus gastos através de dois mecanismos. Primeiro, podem definir um limite de volume de conversas para limitar custos mensais. Segundo, podem pausar o produto a qualquer momento e retomá-lo quando quiserem, proporcionando flexibilidade para gerenciar seu orçamento conforme suas necessidades.

### Promoção de lançamento

Clientes que contratarem o produto entre outubro de 2025 e fevereiro de 2026 receberão uso gratuito sem limites de volume até o final de março de 2026.
