---
inclusion: always
---

# Preferências do usuário — Prospector de Sites (MDG Digital / Kairós TecnologIA)

Regras gerais do projeto, válidas em todas as sessões. Regras técnicas de redesign de
sites ficam em `redesign-regras.md`.

## Idioma e estilo

- Responder sempre em português do Brasil (pt-BR).
- Respostas concisas e diretas, sem verbosidade desnecessária.

## Grafia da marca (SEMPRE)

O nome da empresa é escrito exatamente como **"Kairós TecnologIA"** — acento no "ó" e
"IA" final em MAIÚSCULO (trocadilho de Inteligência Artificial). Nunca "Kairós
Tecnologia", "Kairos Tecnologia" nem "kairós tecnologia". Vale para e-mail, mensagens de
WhatsApp, página-capa, assinatura, contrato e qualquer texto voltado ao cliente.

## Apresentação de arquivos

Ao mostrar/apresentar arquivos, SEMPRE escrever no texto, logo acima dos cartões, a
**pasta + o nome do arquivo** — porque o cartão corta o caminho e esconde o nome, que é
a informação mais importante.
- Formato: `.../pasta/do/arquivo/` → **nome-do-arquivo.ext**
- Exemplo: `.../sites/bh/oficinas/car-fix-lanternagem-e-pintura/` → **car-fix-lanternagem-e-pintura.html**

## Publicação é MANUAL (regra crítica, reforçada 02/09/2026)

O usuário publica os sites manualmente, no tempo dele, na hospedagem Locaweb. Ao
terminar um redesenho/ajuste que precise ir ao ar:
- Deixar o arquivo final correto, atualizar `fila-publicacao.txt` com a(s) linha(s)
  `local|remoto`, e só AVISAR que está pronto para publicar.
- NUNCA aguardar ou checar `fila-publicada-*.txt`, NUNCA verificar se há publicador
  automático rodando, NUNCA tentar publicar sozinho (FTP direto etc.), e NUNCA pedir
  para o usuário rodar `publicar-agora.bat` — ele já sabe e faz isso por conta própria.

## Prospecção — regras do usuário

- **gmnCid / gmnUrl (fallback obrigatório):** NUNCA gravar lead com `gmnCid` vazio nem
  com `gmnUrl` de busca (`/maps/search/...`). Quando a URL do Maps não virar
  `/maps/place/`, obter o CID pelo caminho alternativo (forçar a ficha com o prefixo
  `/maps/place/<Nome + rua + número + bairro + cidade>` e reler a URL; se não vier, ler
  `location.href` via JS ou extrair `0x<hex>:0x<hex>` e usar o 2º hex → decimal).
- **Validar WhatsApp de números fixos:** telefone FIXO (ou não confirmado como WhatsApp)
  deve ser VALIDADO antes de gravar — abrir `https://wa.me/55DDDNUMERO` e ler a página;
  se mostrar o perfil/empresa, é WhatsApp. Só leitura, NUNCA enviar mensagem.
- **Descobrir o Instagram:** sempre tentar achar o Instagram quando não vier no GMN nem
  no site antigo. Buscar no Google `<nome> <nicho> <cidade> instagram`, abrir até 4
  perfis do topo, conferir se os dados batem. (Detalhes na skill `prospeccao-maps`.)

## Mensagens de WhatsApp — frase PROIBIDA

NUNCA incluir a frase "Usei a logo de vocês na nova versão." (nem variações afirmando
que usamos/aplicamos a logo do cliente) no texto das mensagens de WhatsApp.
(definido em 20/08/2026)

## Dashboard — template fonte da verdade é o LOCAL

`dashboard-template-3colunas.html` (raiz da pasta `Clientes`) é o template ATIVO do
painel — NÃO o `references/dashboard-template.html` empacotado na skill `dashboard-leads`
(versão v2 desatualizada, sem os campos extras nem o modal em 3 colunas). O
`dashboard-template-3colunas.html` é o molde; `dashboard.html` é o resultado gerado
(molde + dados reais). NUNCA apagar o template. Toda regeneração do dashboard parte do
`dashboard-template-3colunas.html` local.
