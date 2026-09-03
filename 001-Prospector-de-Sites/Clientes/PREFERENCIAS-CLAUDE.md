# Preferências do usuário — ler no início de cada trabalho

_Arquivo mantido pelo usuário (MDG Digital / Kairós TecnologIA). Claude deve consultar no começo das sessões deste projeto._

## Apresentação de arquivos (present_files)
- Ao mostrar arquivos, SEMPRE escrever no texto, logo acima dos cartões, a **pasta + o nome do arquivo** — porque o cartão corta o caminho e esconde o nome, que é a informação mais importante.
- Formato: `.../pasta/do/arquivo/` → **nome-do-arquivo.ext**
- Exemplo: `.../sites/bh/oficinas/car-fix-lanternagem-e-pintura/` → **car-fix-lanternagem-e-pintura.html**

## Estilo geral
- Respostas concisas e diretas, sem verbosidade desnecessária (pt-BR).

## Prospecção — gmnCid / gmnUrl (fallback obrigatório)
- Ao prospectar (/prospectar), NUNCA gravar lead com `gmnCid` vazio nem com `gmnUrl` de busca (`/maps/search/...`).
- Quando a URL do Maps não virar `/maps/place/` (ficar em `/search/`), obter o CID pelo caminho alternativo: forçar a ficha com o prefixo `/maps/place/<Nome + rua + número + bairro + cidade>` e reler a URL da aba; se não vier, rodar `javascript_tool` lendo `location.href` (o tab context traz o `/place/` resolvido) ou extrair do conteúdo o padrão `0x<hex>:0x<hex>` e usar o 2º hex → decimal.
- Regra completa mora em `prospector-config.json` → `regrasProspeccao.comoObterGmnEgeoendereco` (fonte da verdade lida pelo fluxo).

## Prospecção — validar WhatsApp de números fixos
- Sempre que o telefone for FIXO (ou não estiver explícito que é WhatsApp), VALIDAR antes de gravar: abrir `https://wa.me/55DDDNUMERO` no Chrome (redireciona p/ `api.whatsapp.com/send?phone=...`) e LER a página — se mostrar o NOME do perfil/empresa + "Continuar para o WhatsApp Web", o número é WhatsApp e vai para o campo `whatsapp` (55+DDD+numero); se não mostrar perfil, não é.
- É só leitura, NUNCA enviar mensagem. Um lead pode ter mais de um número — testar todos. Requer WhatsApp Web logado.
- Regra completa em `prospector-config.json` → `regrasProspeccao.validacaoWhatsapp`.

## Prospecção — descobrir o Instagram
- Sempre tentar achar o Instagram do lead quando não vier no GMN nem no site antigo. Busca no Google: `<nome do cliente> oficina belo horizonte instagram`.
- Abrir ATÉ 4 perfis do topo da lista, ler a bio e conferir se batem os dados (nome, bairro/endereço, telefone, serviços). Se bater, gravar no campo `instagram` e aproveitar logo/dados/paleta. Se nenhum bater, registrar que não há Instagram localizável.
- Regra completa em `prospector-config.json` → `regrasProspeccao.buscaInstagram`.

## Mensagens de WhatsApp — frase proibida
- NUNCA incluir a frase "Usei a logo de vocês na nova versão." (nem variações afirmando que usamos/aplicamos a logo do cliente) no texto das mensagens de WhatsApp. (definido em 20/08/2026)
- Regra também registrada em `prospector-config.json` → `mensagemWhatsapp.fraseProibida` (fonte da verdade lida pelo fluxo).

## Redesign — padding lateral do hero (e qualquer seção com .wrap)
- Bug real encontrado no site Car Fix (24/08/2026): classe própria de seção (ex. `.hero-grid`) usando `padding: Xpx 0 Ypx` em shorthand zera o padding lateral herdado de `.wrap`, colando o conteúdo na borda da tela.
- Em TODO site novo/redesenhado, nunca usar esse shorthand com 0 na lateral em classes combinadas com `.wrap` — usar `padding-top`/`padding-bottom` isolados. Verificar todas as `class="wrap ..."` do HTML antes de entregar/publicar.
- Regra completa em `prospector-config.json` → `regrasRedesign.paddingLateralWrap` (fonte da verdade lida pelo fluxo).

## Redesign — overlay decorativo bloqueando cliques (links "não funcionam")
- Bug real encontrado no site ATOS Centro Automotivo (27/08/2026) e reincidente em mais 16 sites do mesmo template-base (corrigidos em 31/08/2026, incluindo auto-mecanica-tosatti): `.hero::before`/`.hero-bg` decorativo (`position:absolute;inset:0`, textura/gradiente) sem `pointer-events:none` ficava por cima do conteúdo do hero e capturava todos os cliques — os botões pareciam "não funcionar"/"errados" mesmo com o `href` certo.
- CHECAGEM OBRIGATÓRIA E AUTOMÁTICA (não só reativa) em TODO site novo/redesenhado e em QUALQUER edição de site existente, antes de publicar: todo elemento/pseudo-elemento decorativo com `position:absolute`/`fixed` cobrindo área com links/botões DEVE ter `pointer-events:none` — mesmo quando o container do conteúdo já parece protegido por `z-index`. Faz parte do checklist final, junto com o padding lateral. Se o usuário disser que um link "não funciona"/"está errado" apesar do href correto, checar isso ANTES de suspeitar do href/JS.
- Regra completa em `prospector-config.json` → `regrasRedesign.overlayDecorativoBloqueandoCliques` (fonte da verdade lida pelo fluxo, com a lista de sites já corrigidos e os confirmados seguros).

## Redesign — crédito "Criação: Kairós TecnologIA" no rodapé (definida em 27/08/2026; texto ajustado em 28/08/2026)
- Em TODO rodapé de TODO site novo/redesenhado, incluir do lado DIREITO (separado do bloco de dados do cliente à esquerda) a linha "Criação: Kairós TecnologIA" — atenção: "TecnologIA" com "IA" maiúsculo, não "Tecnologia" — com o nome da empresa linkando para `https://kairostecnologia.com.br` (`target="_blank" rel="noopener"`). Estilo discreto (fonte pequena, cor mais clara que o resto do rodapé) — não pode competir com os dados do cliente. Mobile: empilha, crédito por último.
- Regra completa em `prospector-config.json` → `regrasRedesign.creditoRodape` (fonte da verdade lida pelo fluxo).

## Publicação — é MANUAL, não checar/cobrar publicador automático (definida em 28/08/2026)
- O usuário publica os sites manualmente, no tempo dele. Ao terminar um redesenho/ajuste que precise ir ao ar: deixar o arquivo final correto, atualizar `fila-publicacao.txt` com a(s) linha(s) local|remoto, e só AVISAR que está pronto para publicar.
- NUNCA aguardar ou checar `fila-publicada-*.txt`, NUNCA verificar se o publicador automático do Windows está rodando, NUNCA tentar publicar sozinho (FTP direto do sandbox etc.), e NUNCA pedir para o usuário rodar `publicar-agora.bat` — ele já sabe e faz isso por conta própria. (Reforçada em 02/09/2026 após reincidência.)
- Regra completa em `prospector-config.json` → `regrasPublicacao.publicacaoManual` (fonte da verdade lida pelo fluxo).

## Redesign — aviso de demonstração (topo/rodapé) + botão voltar ao topo (definida em 02/09/2026)
- Em TODO site novo/redesenhado, incluir o aviso de demonstração (fundo branco, texto preto 12px) logo após `<body>` (antes do menu) e logo após `</footer>` (fim da página), com o texto: "Demonstração de site criada pela Kairós TecnologIA, construída com os dados públicos da empresa achados na internet e com acesso liberado só à ela. É uma proposta e não representa o site oficial da empresa."
- Incluir também um botão "voltar ao topo" pequeno, redondo, fixo e centralizado embaixo da tela, na cor da paleta do próprio site (cadeia de fallback de CSS var), que só aparece depois de rolar a página. Aplicar tanto no `<slug>.html` quanto no `<slug>-editor.html`.
- Aplicado retroativamente nos 54 sites do projeto em 02/09/2026. Regra completa em `prospector-config.json` → `regrasRedesign.avisoDemonstracaoEBotaoTopo` (fonte da verdade lida pelo fluxo).

## Dashboard — template fonte da verdade é o local, não o da skill (definida em 02/09/2026)
- `dashboard-template-3colunas.html` (raiz da pasta conectada) é o template ATIVO do painel — NÃO o `references/dashboard-template.html` empacotado na skill dashboard-leads (versão v2 desatualizada, sem os campos extras nem o modal em 3 colunas).
- Os dois arquivos não são redundantes: `dashboard-template-3colunas.html` é o molde (marcador de dados vazio), `dashboard.html` é o resultado gerado (molde + dados reais dos leads). Confirmado por comparação byte a byte em 02/09/2026. NUNCA apagar o template — sem ele, a próxima regeneração cai de volta no v2 desatualizado do plugin.
- Toda regeneração do dashboard deve partir do `dashboard-template-3colunas.html` local. Regra completa em `prospector-config.json` → `regrasDashboard.templateFonteDaVerdade` (fonte da verdade lida pelo fluxo).
