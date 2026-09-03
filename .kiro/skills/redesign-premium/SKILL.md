---
name: redesign-premium
description: Use ao redesenhar o site de um cliente prospectado OU criar a primeira página de um cliente que ainda não tem site — versão premium e de alta conversão, mantendo conteúdo, logo e paleta quando existirem, e usando Instagram e Google como fonte quando não houver site. Acione quando o usuário disser "redesenhar site", "melhorar página", "refazer o site do cliente", "criar site do cliente", "editor visual".
---

# Redesign premium de páginas

Criar uma NOVA VERSÃO da página do cliente — não uma página nova. O cliente precisa
reconhecer o próprio negócio, só que elevado ao padrão que o faturamento dele merece.
**Quando o cliente ainda NÃO tem site**, criar a PRIMEIRA página a partir das informações
públicas reais (Google Meu Negócio, avaliações do Google e Instagram) — mesmas regras de
"nada inventado".

## Como acionar em lote (antes: comando /redesenhar)

1. Leia `prospector-config.json` e `leads.md`.
2. Se o usuário trouxer URLs/nomes, use-os. Senão, selecione os leads com status `novo`
   mais bem ranqueados — **mínimo de 5 por lote** (se houver menos de 5 novos, use todos
   e avise que prospectar de novo aumenta o lote).
3. Confirme a lista com o usuário antes de começar.

## Ferramentas no Kiro (adaptação do antigo "Claude in Chrome")

A extração do site original e das imagens depende de um navegador. Use o **Playwright MCP**
(configurado em `.kiro/settings/mcp.json`): abrir o site, executar JavaScript para coletar
`img.currentSrc` de todas as imagens (role a página inteira antes, para vencer lazy-load),
e tirar screenshot do original. Se o navegador MCP não estiver disponível, avise: sem ele
não dá para extrair fotos/conteúdo automaticamente.

## Regras invioláveis

1. **Nenhum FATO inventado — mas o texto deve ser APRIMORADO.** Todo serviço, credencial,
   número, endereço e contato vem do site original quando existir, ou — inclusive quando há
   site — do perfil do Google (Maps/GMN) e do Instagram. Sem dados fictícios, sem depoimentos
   criados, sem serviços que o cliente não oferece. Reescreva o texto com copy melhor
   (títulos mais fortes, frases claras, hierarquia) — sempre dizendo a mesma verdade.
2. **Fotos e logo originais são OBRIGATÓRIOS.** Toda foto utilizável (profissional,
   consultório, logo) deve constar na página nova, pelas URLs originais (colete via
   `img.currentSrc` rolando a página inteira). Sem site → fotos públicas do Instagram e do
   GMN + logo do perfil; sem logo utilizável, composição tipográfica — nunca invente logo.
3. **Identidade preservada.** Manter logo, paleta e fotos do cliente. Paleta fraca → refinar
   tons, nunca trocar a família de cores.
4. **Mais completo que o original.** CRIE as seções relevantes que faltam — só com
   informação real: prova social (nota + avaliações reais do Google), como funciona o
   atendimento, localização com mapa, horários (do Maps), FAQ com dúvidas respondíveis pelo
   conteúdo real. Seção que exigiria inventar fato = não criar.
5. **Arquivo único + slug do banco.** `sites/bh/oficinas/[slug]/[slug].html` autocontido:
   CSS inline no `<head>`, sem build, sem dependências além de Google Fonts. **O `[slug]`
   NÃO é derivado do nome aqui — leia o slug já gravado no `prospector.db` (case pelo `nome`)
   e use-o EXATAMENTE** na pasta e nos arquivos. Regra única de slug: skill `dashboard-leads`.
6. **Responsividade TOTAL (inegociável).** Perfeita em 360, 375, 768, 1024, 1280 e 1440px —
   sem rolagem horizontal, sem texto vazando, sem imagem esticada, sem seção quebrada. Grid/
   flex fluidos, `clamp()` para tipografia, breakpoints testados um a um.
7. **Editor sempre.** Todo redesign gera junto `sites/bh/oficinas/[slug]/[slug]-editor.html`
   (camada de edição de `references/editor-visual.md`) — nunca entregar sem a versão editável.
8. **Comparador sempre.** Todo lote termina com `comparar.html` na raiz da pasta do projeto,
   gerado de `references/comparador-template.html` (substituir `__CLIENTES__` pelo array JSON;
   mesclar com clientes já existentes).

## Logo, paleta e carrossel de imagens reais (quando houver Instagram/GMN)

1. **Logo no topo:** aplique a logomarca (campo `logo` do banco = foto de perfil do
   Instagram, base64) numa barra fixa no topo (header) e no rodapé. Sem logo utilizável,
   composição tipográfica.
2. **Paleta da marca:** derive das cores da logo/identidade (destaque = cor predominante da
   logo). Refine tons fracos, nunca troque a família.
3. **Carrossel no topo (lado direito do hero):** slider com as 3 imagens fixadas do Instagram
   + 1 do Street View/360° do GMN (quando houver). Capture por recorte de tela, reduza
   (~700px, JPEG) e embuta em base64. Fonte faltando → use as que houver, não invente.
4. **Nada inventado:** textos/serviços vêm do material real (bio/posts do Instagram,
   avaliações e dados do Google).

## Estrutura da página (adaptar à profissão)

1. **Hero:** nome + especialidade, promessa em 1 linha, CTA primário (WhatsApp) visível sem
   rolar, foto do profissional/clínica.
2. **Prova social:** nota do Google em destaque ("5.0 ★ · 121 avaliações no Google"), real e
   verificável. Citar 2-3 trechos de avaliações reais se coletados.
3. **Serviços/áreas:** cards clicáveis — cada um leva à âncora da seção ou ao WhatsApp com
   mensagem pré-preenchida (`https://wa.me/55DDDNUMERO?text=Olá! Vim pelo site e quero saber sobre [serviço]`).
4. **Sobre:** formação e credenciais reais (nunca cortar).
5. **Oferta estruturada** (quando fizer sentido): opções de engajamento SEM preços, só nomes
   e o que incluem, todas levando ao WhatsApp. Só planos que agrupem o serviço já oferecido.
6. **Localização e contato:** endereço, mapa (iframe do Google Maps), horários, telefone, redes.
7. **Rodapé:** dados do profissional (registro de classe se existir no original).

## Copywriting (aprimorar sem inventar — reescrever é obrigatório)

- **Headline do hero = benefício, não rótulo** (rótulo vira kicker/subtítulo pra SEO).
- **Estrutura PAS suave:** toque na dor real, mostre o caminho, apresente o serviço como
  solução — no tom do nicho, sem agressividade de lançamento.
- **Escaneabilidade:** blocos de 2-3 linhas, bullets com verbo, subtítulos que contam a
  história sozinhos.
- **1 CTA por dobra**, orientado à ação e ao benefício, todos pro WhatsApp com mensagem
  pré-preenchida contextual.
- **Prova social costurada**, não empilhada. **Microcopy** em botões e formulários.
- Proibido: clichês vazios sem fato que os sustente; superlativos inventados; promessas que
  o cliente não faz.

## Padrão estético

- Tipografia: uma serifada elegante para títulos (Playfair Display, Fraunces, Lora) + uma
  sans limpa para corpo (Inter, Sora, DM Sans), pesos 400/600. h1 ≥ 40px desktop / 30px mobile.
- Espaçamento generoso: seções com 80-120px de respiro vertical desktop.
- Paleta: 1 cor da marca + neutros quentes + 1 tom de destaque para CTA. Contraste AA mínimo.
- Botão de WhatsApp flutuante fixo no canto inferior direito.
- Micro-toques premium: bordas 12-16px, sombras suaves, transições de 0.2s. Sem carrosséis
  pesados, sem JS além do essencial. Página deve abrir instantânea.

## Checklist final (obrigatório antes de entregar)

- [ ] Zero texto placeholder / lorem ipsum
- [ ] Todos os links e CTAs apontam para contato REAL do cliente
- [ ] WhatsApp no formato wa.me correto (55 + DDD + número)
- [ ] Responsivo verificado em 360, 375, 768, 1024, 1280 e 1440px — zero rolagem horizontal
- [ ] Título e meta description com nome + especialidade + cidade
- [ ] Todo conteúdo importante do site antigo está presente
- [ ] Logo e fotos ORIGINAIS do cliente presentes
- [ ] `[slug]-editor.html` gerado e `comparar.html` atualizado
- [ ] **Padding lateral:** nenhuma classe combinada com `.wrap` usa `padding: X 0 Y` (zera a
      lateral). Ver steering `redesign-regras`.
- [ ] **Overlay decorativo:** todo elemento/pseudo `position:absolute/fixed` sobre links tem
      `pointer-events:none`. Ver steering `redesign-regras`.
- [ ] **Aviso de demonstração** (topo e rodapé) + **botão voltar ao topo** presentes. Ver
      steering `redesign-regras`.
- [ ] **Crédito "Criação: Kairós TecnologIA"** no rodapé. Ver steering `redesign-regras`.

## Editor visual (antes: comando /editor)

Para gerar `[slug]-editor.html`: crie/regenere uma cópia da página com a camada de edição
injetada antes de `</body>`. O script completo está em `references/editor-visual.md` — use-o
exatamente como está. Explique ao usuário em 3 linhas: abra no navegador e clique em qualquer
texto para editar; clique em qualquer imagem para trocá-la por um arquivo do computador
(fica embutida); botão "Exportar página" baixa o HTML final limpo (sem o editor). Se o usuário
enviar o arquivo exportado, substitua `[slug].html` pelo conteúdo exportado antes de publicar.

## Comparador (obrigatório)

`comparar.html` na raiz, de `references/comparador-template.html`: substitua `__CLIENTES__`
pelo array JSON dos clientes (formato no rodapé do template). Se já existir, LEIA o array
atual e acrescente os novos no topo — nunca perca os antigos.

## Saída (formato travado)

1. Apresente os arquivos no chat: `comparar.html` PRIMEIRO, depois página e editor de cada
   cliente. Acima dos cartões, escreva sempre a pasta + nome do arquivo (ver steering
   `preferencias-usuario`).
2. Resumo de 1 linha por cliente (o que melhorou).
3. Confirmação explícita: "Dashboard atualizado: [N] leads com status redesenhado" após
   atualizar o banco/dashboard (skill `dashboard-leads`).
4. Orientação curta: `comparar.html` = antes/depois · `[slug]-editor.html` = editar textos/
   imagens · próximo passo: publicar (skill `deploy-locaweb`).
