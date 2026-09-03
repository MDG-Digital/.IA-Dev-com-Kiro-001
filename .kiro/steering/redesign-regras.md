---
inclusion: fileMatch
fileMatchPattern: "**/sites/**/*.html"
---

# Regras técnicas de redesign de sites (checklist obrigatório)

Bugs reais encontrados no projeto e transformados em regras. Aplicar em TODO site novo/
redesenhado e em QUALQUER edição de site existente, ANTES de entregar/publicar. Complementa
a skill `redesign-premium`.

## Padding lateral do hero (e qualquer seção com .wrap)

Bug real (Car Fix, 24/08/2026): classe própria de seção (ex.: `.hero-grid`) usando
`padding: Xpx 0 Ypx` em shorthand ZERA o padding lateral herdado de `.wrap`, colando o
conteúdo na borda da tela.
- Nunca usar esse shorthand com `0` na lateral em classes combinadas com `.wrap`.
- Usar `padding-top`/`padding-bottom` isolados.
- Verificar TODAS as `class="wrap ..."` do HTML antes de entregar.

## Overlay decorativo bloqueando cliques (links "não funcionam")

Bug real (ATOS Centro Automotivo, 27/08/2026; reincidente em +16 sites do mesmo
template-base): `.hero::before`/`.hero-bg` decorativo (`position:absolute;inset:0`, textura/
gradiente) sem `pointer-events:none` ficava por cima do conteúdo e capturava todos os
cliques — botões pareciam "não funcionar" mesmo com o `href` certo.
- CHECAGEM OBRIGATÓRIA E AUTOMÁTICA (não só reativa): todo elemento/pseudo-elemento
  decorativo com `position:absolute`/`fixed` cobrindo área com links/botões DEVE ter
  `pointer-events:none` — mesmo quando o container do conteúdo já parece protegido por
  `z-index`.
- Se o usuário disser que um link "não funciona"/"está errado" apesar do href correto,
  checar ISSO antes de suspeitar do href/JS.

## Crédito "Criação: Kairós TecnologIA" no rodapé

(definida em 27/08/2026; texto ajustado em 28/08/2026) Em TODO rodapé de TODO site novo/
redesenhado, incluir do lado DIREITO (separado do bloco de dados do cliente à esquerda) a
linha **"Criação: Kairós TecnologIA"** — atenção: "TecnologIA" com "IA" MAIÚSCULO — com o
nome da empresa linkando para `https://kairostecnologia.com.br`
(`target="_blank" rel="noopener"`). Estilo discreto (fonte pequena, cor mais clara) — não
pode competir com os dados do cliente. Mobile: empilha, crédito por último.

## Aviso de demonstração + botão voltar ao topo

(definida em 02/09/2026) Em TODO site novo/redesenhado:
- Incluir o **aviso de demonstração** (fundo branco, texto preto 12px) logo após `<body>`
  (antes do menu) e logo após `</footer>` (fim da página), com o texto exato:
  > Demonstração de site criada pela Kairós TecnologIA, construída com os dados públicos da empresa achados na internet e com acesso liberado só à ela. É uma proposta e não representa o site oficial da empresa.
- Incluir um **botão "voltar ao topo"** pequeno, redondo, fixo e centralizado embaixo da
  tela, na cor da paleta do próprio site (cadeia de fallback de CSS var), que só aparece
  depois de rolar a página.
- Aplicar tanto no `<slug>.html` quanto no `<slug>-editor.html`.

## Responsividade (inegociável)

Perfeita em 360, 375, 768, 1024, 1280 e 1440px — sem rolagem horizontal, sem texto
vazando, sem imagem esticada, sem seção quebrada em nenhum desses pontos.
