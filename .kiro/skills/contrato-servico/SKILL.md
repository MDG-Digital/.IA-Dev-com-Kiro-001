---
name: contrato-servico
description: Use ao gerar contratos de prestação de serviço para clientes fechados — criação/redesign de site, publicação e manutenção. Acione quando o usuário disser "contrato", "gerar contrato", "formalizar", "cliente fechou", "enviar contrato".
---

# Contrato de prestação de serviço

Gerar a minuta do contrato do serviço fechado (redesign + publicação de página, com
manutenção opcional), pronta pra virar PDF/DOCX e ir por e-mail.

> ⚠️ **SLUG:** o `[slug]` é o valor gravado no `prospector.db` para o lead (case pelo `nome`)
> — nunca re-derive do nome. Regra única: skill `dashboard-leads`.

## Como acionar (antes: comando /contrato)

1. Identifique o cliente pelo que o usuário indicar, ou liste os leads com status
   `fechado`/`respondeu` do banco e pergunte qual.
2. Reúna o que o banco JÁ tem: nome, cidade, valor fechado, URL publicada, escopo (página
   redesenhada + publicação), dados do prestador (do `prospector-config.json`).
3. LEIA as fontes antes de perguntar: prestador em `prospector-config.json` → `contratante`;
   dados do cliente em `docCliente`/`endCliente` do banco. Pergunte APENAS o que faltar — e se
   o usuário colar a mensagem do cliente com CPF/endereço, extraia e salve no banco. Confirme
   também: forma de pagamento, prazo de entrega e manutenção mensal (valor).

## Fonte dos dados (nesta ordem)

1. **Banco (`prospector.db`):** nome, cidade, valor fechado, URL publicada. Quando preenchidos
   à mão no dashboard, use `razaoSocial` e `responsavel` para qualificar o CONTRATANTE, e
   `diaVencimento` + `valorTrimestral` para a cláusula de Suporte e Hospedagem (cobrança
   trimestral, vencimento no dia informado). Vazios → colete ou deixe "(preencher)".
2. **Config (`prospector-config.json`):** dados do PRESTADOR (`contratante`; se não existir,
   colete uma vez e salve).
3. **Usuário:** CPF/CNPJ e endereço do CONTRATANTE, forma de pagamento, prazo, manutenção.

## Geração

Gere as DUAS versões:

- **HTML** (folha ao vivo do dashboard): de `references/contrato-template.html` — substitua
  TODOS os `{{PLACEHOLDERS}}` (confira que nenhum sobrou: busca por `{{`). Salve em
  `sites/bh/oficinas/[slug]/contrato-[slug].html`. PDF: abrir no navegador → Ctrl+P → Salvar
  como PDF (informe ao usuário). Cláusulas parametrizáveis: manutenção mensal (só se
  contratada) e parcelamento (texto muda conforme a forma de pagamento).
- **DOCX travado** (o que vai pro cliente): monte um `dados.json` com as mesmas chaves +
  `MANUTENCAO: true/false` e `VALOR_MANUTENCAO`, e rode
  `python references/gerar-docx.py dados.json sites/bh/oficinas/[slug]/contrato-[slug].docx`
  (instale `python-docx` com `pip install python-docx` se preciso). O documento sai SOMENTE
  LEITURA com regiões editáveis destacadas em amarelo (CPF/endereço se faltarem, data e
  assinatura). Avise 1 vez: a proteção do Word é dissuasória, não impede quem quiser
  desativá-la; para validade forte, assinatura eletrônica (gov.br, Autentique).

## E-mail de envio (rascunho no Gmail via MCP)

Assunto: `Contrato de prestação de serviço — nova página [Nome do negócio]`. Corpo (na voz
do usuário): agradecer a confiança, resumir em 2 linhas o combinado (escopo + valor + prazo),
pedir que leia a minuta e responda com um "de acordo" (ou assine digitalmente), fechar com a
assinatura do config. Instrua o usuário a ANEXAR o PDF/DOCX antes de enviar. Se o MCP de Gmail
não estiver ativo, entregue o texto pronto e o caminho do arquivo para o usuário enviar.

## Atualização de status

Atualize o banco/dashboard (skill `dashboard-leads`): `contratoStatus='enviado'`,
`contratoEm=[hoje]`, `manutencao=[valor mensal, se houver]`. Quando o cliente assinar →
`contratoStatus='assinado'`; quando o pagamento entrar → `pago=1`. Ao receber o contrato
assinado, salve em `sites/bh/oficinas/[slug]/contrato-[slug]-assinado.docx` (ou .pdf).

## Limites

- SEMPRE manter o aviso do rodapé: minuta base, recomenda-se revisão por advogado.
- Não prometer validade jurídica nem substituir assinatura formal.
- Nunca inventar cláusula financeira: tudo vem do banco/usuário.
