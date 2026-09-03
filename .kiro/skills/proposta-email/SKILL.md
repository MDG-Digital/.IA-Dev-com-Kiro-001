---
name: proposta-email
description: Use ao escrever e enviar a proposta comercial por e-mail (ou WhatsApp) para um lead prospectado, fazer follow-up de propostas paradas e verificar respostas no Gmail. Acione quando o usuário disser "enviar proposta", "e-mail para o cliente", "mandar o site para o cliente", "follow-up", "verificar respostas".
---

# Proposta por e-mail (e follow-up e respostas)

O e-mail NÃO vende — desperta curiosidade e prova trabalho feito. O fechamento (preço,
escopo, reunião) acontece na resposta. Um e-mail que parece de vendedor morre no spam; um
e-mail que parece de alguém que já trabalhou de graça pro destinatário é aberto e respondido.

> ⚠️ **SLUG:** o link da capa (`https://[dominio]/[pastaBase]/[slug]/proposta.html`) usa o
> `slug` gravado no `prospector.db` — leia-o do banco, nunca re-derive do nome. Regra única:
> skill `dashboard-leads`.

## Ferramentas no Kiro (adaptação do conector Gmail)

O envio/leitura de e-mail usa um **MCP de Gmail** (configurado em `.kiro/settings/mcp.json`;
requer autenticação Google — ver o resumo da migração). Enquanto o MCP de Gmail não estiver
ativo:
- **Rascunho:** escreva o e-mail pronto (assunto + corpo HTML) e entregue ao usuário para ele
  colar no Gmail, OU salve como arquivo `.html`/`.txt` na pasta do cliente.
- **Verificar respostas:** peça ao usuário para conferir o Gmail e colar as respostas, que
  você então classifica e registra no banco.
Com o MCP de Gmail ativo, use as ferramentas dele (criar rascunho, buscar threads).

## Enviar proposta (antes: comando /proposta)

1. Leia `prospector-config.json` (assinatura e modo de envio) e `leads.md`.
2. Destinatários: o que o usuário pedir, ou todos os leads `publicado` que ainda não
   receberam proposta. Só leads com e-mail confirmado — para os demais, a abordagem é manual
   via WhatsApp (ofereça o texto adaptado, ver seção WhatsApp).
3. Para cada cliente, escreva o e-mail seguindo os princípios/estrutura abaixo, com dados
   reais: elogio baseado nas avaliações do Google, o defeito específico apontado na
   prospecção e — como ÚNICO link — a página-capa publicada
   (`https://[dominio]/[pastaBase]/[slug]/proposta.html`). Se a capa não existe, gere e
   publique-a (template nesta skill, upload pela skill `deploy-locaweb`). NUNCA mencione preço.
4. **Checklist anti-spam (bloqueante):** valide contra a checklist abaixo. Reescreva até
   passar em todos os itens.
5. Envio conforme o modo do config (rascunho, padrão; ou enviar direto).
6. Atualize `leads.md` e o banco/dashboard: status `proposta` + data de envio.

## Princípios

1. **Rapport primeiro.** Elogio ESPECÍFICO e verificável (nota no Google, avaliação real
   citada, credencial do site). Nunca genérico.
2. **A dor sem ofensa.** 1-2 defeitos objetivos como oportunidade, nunca como crítica.
3. **A prova antes do pedido.** O trabalho JÁ está no ar. O link é a proposta.
4. **Zero preço.** Preço só na conversa que a resposta abre.
5. **Zero pressão.** Sem urgência falsa. Um único CTA: dar uma olhada e responder.
6. **Curto.** 120-180 palavras.
7. **Grafia da marca (SEMPRE):** exatamente **"Kairós TecnologIA"** — acento no "ó" e "IA"
   final MAIÚSCULO. Nunca "Kairós Tecnologia" nem "Kairos Tecnologia".

## Estrutura

- **Assunto:** pergunta pessoal e específica, ≤ 60 caracteres, sem cara de marketing.
- **Parágrafo 1:** quem encontrou + elogio específico (avaliações/credencial).
- **Parágrafo 2:** observação sobre o site atual (1-2 pontos objetivos).
- **Parágrafo 3:** "preparei uma nova versão, já no ar" + O ÚNICO LINK: a capa
  (`.../proposta.html`), antes/depois lado a lado. Sem capa, linkar a página nova direto.
- **Parágrafo 4:** CTA — abrir no celular, responder com a impressão.
- **Assinatura:** nome, apresentação e WhatsApp do config.

## Checklist anti-spam (BLOQUEANTE — rodar antes de criar o rascunho)

- [ ] **1 link só** (a capa). No máximo 2 se incluir o site antigo.
- [ ] **Sem encurtador de URL.** Link com o domínio real e `https://`.
- [ ] **Link como âncora HTML** com texto visível = a URL limpa montada do config:
      `<a href="https://[dominio]/[pastaBase]/[slug]/proposta.html">https://[dominio]/[pastaBase]/[slug]/proposta.html</a>`.
      Corpo em HTML para o link não aparecer embrulhado em redirect visível.
- [ ] **Domínio limpo e humano.** Se o domínio do config for subdomínio técnico cheio de
      números, PARE: oriente ativar o domínio próprio e atualizar o campo `dominio` no
      dashboard. Proposta só sai com domínio apresentável.
- [ ] **Sem palavras-gatilho:** grátis, promoção, imperdível, oferta, desconto, clique aqui,
      100%, garantido, urgente.
- [ ] **Sem CAIXA ALTA, sem "!!", sem emoji** no assunto.
- [ ] **Texto simples** — HTML minimalista (parágrafos + a âncora; zero cores, botões,
      imagens ou anexos).
- [ ] **Assunto ≤ 60 caracteres**, como pergunta ou frase pessoal com o nome do negócio.
- [ ] **Primeira linha 100% personalizada** (nome + fato real das avaliações).
- [ ] **Remetente = conta Gmail pessoal ativa do usuário.** Envios 1 a 1, poucos por dia.

## Mensagem por WhatsApp (leads sem e-mail) — arquivo mensagens-whatsapp.md

Mesma lógica (rapport → oportunidade → prova), em tom de mensagem. **Número:** WhatsApp ou,
na falta, o telefone (só dígitos, `55 + DDD + número`). Quando o número responder, atualize
`whatsapp` no banco.

Estrutura:
1. Saudação + quem é ("Aqui é o [nome], da Kairós TecnologIA") + elogio ESPECÍFICO (nota/
   avaliações reais).
2. Oportunidade: 1-2 pontos objetivos (ou "ainda não tem site próprio"), como oportunidade.
3. "Preparei uma nova versão, já no ar" + o link da página nova (ou a capa).
4. **Parágrafo fixo (penúltimo — sempre este texto):**
   > Estamos aqui no Bairro São João Batista, na Região Norte de BH, e na Kairós usamos modernas soluções de IA (Inteligência Artificial) para criar sites com qualidade, atrativos e com custo bem acessível! Esse site de demonstração foi criado por IA com suas informações públicas no Google, no Instagram e no site atual.
5. **Domínio e e-mail (só quando o lead tiver o campo `dominio`):**
   > Podemos também revisar o seu cadastro no Google Meu Negócio, criar o seu domínio na internet, como por exemplo: www.<dominio>, e até seu e-mail personalizado: atendimento@<dominio>.
   Substitua `<dominio>` pelo campo `dominio` do lead (já vem com o TLD — NÃO acrescente `.com.br`).
6. **Fechamento (última frase — sempre):**
   > Dá uma olhada com calma e me diz o que achou. Abraço!

**Regras fixas do `mensagens-whatsapp.md`:**
- Logo APÓS a URL do site novo, incluir SEMPRE: `Esse site ainda pode ser alterado com outras imagens e textos.`
- O campo `Link p/ abrir já preenchido` fica SEMPRE como `https://wa.me/<numero>?text=...`
  (apenas as reticências) — NÃO gerar a mensagem inteira codificada no link.
- **Append-only:** NUNCA alterar mensagens já criadas; apenas ACRESCENTAR blocos novos ao final.
- **Frase PROIBIDA:** nunca incluir "Usei a logo de vocês na nova versão." nem variações
  afirmando que usamos/aplicamos a logo do cliente.
- Enviou → assim que o usuário confirmar o envio, atualize `status='proposta'` + `dataProposta`
  no banco e regenere o dashboard. Nunca deixe em `publicado` um lead cuja proposta já foi
  enviada por WhatsApp.

## Página-capa (o que o cliente vê ao clicar)

O link do e-mail leva à capa gerada na publicação (`references/capa-proposta-template.html`):
nome do cliente no topo, antes/depois lado a lado e a assinatura. Servida em `https://`,
personalizada com dados reais, sem pedir dado pessoal nenhum.

## Verificar respostas (antes: comando /respostas)

1. Leia o banco: leads com status `proposta` (ou o cliente pedido).
2. Para cada um, busque no Gmail (MCP) por conversas com o e-mail do lead a partir da
   `dataProposta` — ex.: `from:[email] after:[dataProposta]` e a thread da proposta original.
3. Classifique: **Respondeu** (existe mensagem DO lead) → `status='respondeu'` + resumo curto
   em `obs`; **Sem resposta** → mantém `proposta`.
4. Atualize via skill `dashboard-leads` e regenere o dashboard.
5. Resuma: quem respondeu (com a essência), quem segue sem resposta e há quantos dias.
- NUNCA marque `fechado` sozinho — só o usuário confirma (aí registre `valor`). Não responda
  e-mails automaticamente; ofereça rascunho de resposta se o usuário quiser.

## Follow-up (antes: comando /followup)

1. Verifique respostas ANTES (seção acima) para não fazer follow-up de quem já respondeu.
2. Elegíveis: status `proposta`, enviado há **3+ dias**, e SEM follow-up registrado (procure
   "follow-up" em `obs`).
3. Follow-up de no máximo 4 linhas, gentil, nunca cobra: referência leve ao 1º e-mail,
   pergunta única ("conseguiu ver a página que preparei?") + o mesmo link da capa. Sem preço,
   sem urgência. Passa pela checklist anti-spam.
4. Crie os rascunhos (mesmo modo do config). **1 follow-up por lead, para sempre.**
5. Registre em `obs`: "Follow-up enviado em [data]".

## Automação (opcional)

Se o usuário quiser verificação diária de respostas + follow-up, isso pode virar um Agent
Hook do Kiro (trigger agendado/manual) — ofereça criar.
