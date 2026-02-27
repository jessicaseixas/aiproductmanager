<!-- jira: none -->

# Busca de Outros Imoveis

> Quando o lead demonstra interesse em conhecer outras opcoes, o assistente apresenta imóveis do catalogo da imobiliária.

| | |
|---|---|
| **Status** | Produção |
| **Jira** | - |
| **Lançamento** | Out/2024 |

---

## Problema

Lead veio por um anuncio especifico, mas pode ter interesse em outros imóveis. Sem apresentar opcoes, perde-se oportunidade de venda.

## Solução

- Pergunta sobre características desejadas (localização, quartos, tamanho)
- Busca imóveis no catálogo da imobiliária com base nos filtros
- Envia resumo dos resultados e botão "Visualizar imóveis"
- Abre webview com lista de imóveis (foto, preço, endereço, detalhes)
- Lead marca "Gostei" nos imóveis de interesse
- Ao clicar "Voltar para o WhatsApp", campo de texto vem pré-preenchido com os códigos selecionados
- Registra quais imóveis o lead demonstrou interesse

> **Nota técnica (Dez/2024):** Apresentação via webview substituiu o carrossel de imagens, reduzindo custo de ~R$0,40 para ~R$0,04 por mensagem e garantindo 100% de entrega.

## Usuário

Leads abertos a conhecer outras opcoes; imobiliárias que querem maximizar conversão do catalogo.

## Valor

- Aumento de oportunidades de venda por lead
- Melhor aproveitamento do catalogo de imóveis
- Lead recebe opcoes personalizadas sem esforco do corretor

## Dependências

Catalogo de imóveis da imobiliária integrado ao sistema.
