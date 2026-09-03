---
name: prospeccao-maps
description: Use ao prospectar clientes no Google Maps — buscar negócios bem avaliados (COM OU SEM site), qualificar leads, avaliar a oportunidade (site fraco ou ausência de site) e capturar Instagram e dados do Google Meu Negócio para a planilha de leads. Acione quando o usuário disser "prospectar", "buscar clientes", "achar leads", "clientes com site ruim", "clientes sem site".
---

# Prospecção no Google Maps

Encontrar o cliente ouro: negócio que JÁ fatura bem (nota alta, muitas avaliações)
mas perde clientes por ter um site fraco OU por não ter site nenhum. Não se cria
demanda — conserta-se (ou cria-se) a presença digital onde o dinheiro está escapando.

> ⚠️ **SLUG (identidade do lead — nasce aqui):** ao registrar cada lead no banco/
> dashboard, gere o `slug` pela REGRA ÚNICA da skill `dashboard-leads` (slugify do
> NOME do negócio: minúsculas, sem acento, sem prefixo de nicho — nada de `of-`/`cl-`).
> Esse slug é imutável e vira o nome da pasta (`sites/bh/oficinas/<slug>/`), dos
> arquivos e da URL pública. Todos os comandos seguintes o reutilizam exatamente.

## Ferramentas no Kiro (adaptação do antigo "Claude in Chrome")

Este fluxo depende de um navegador para abrir o Google Maps, ler perfis, executar
JavaScript (coletar `img.currentSrc`) e tirar screenshots. No Kiro isso é feito por
um **MCP de navegador** (Playwright MCP), configurado em `.kiro/settings/mcp.json`.
- Se o Playwright MCP estiver ativo, use suas ferramentas de navegação/leitura/JS.
- Para buscas simples de apoio (achar e-mail, Instagram), as ferramentas web nativas
  do Kiro também servem.
- Se nenhum navegador MCP estiver disponível, avise o usuário: a varredura do Maps
  precisa dele; sem isso, só dá para registrar leads que o usuário fornecer à mão.

## Preparação (antes: comando /prospectar)

1. Leia `prospector-config.json` na pasta do projeto. Se não existir, oriente a rodar
   a skill `setup-prospector` primeiro.
2. Determine nicho e cidade a partir do pedido do usuário. Se ele não informar,
   pergunte qual nicho padrão do config usar e confirme a cidade. O usuário SEMPRE
   pode trocar nicho/cidade — nunca trave nos padrões.
3. **Dedup (OBRIGATÓRIO):** carregue o cadastro da fonte da verdade — `prospector.db`
   (e `leads.md`, se existir). Todo negócio já cadastrado (inclusive `descartado`) é
   EXCLUÍDO da nova busca. Valide cada candidato com
   `references/checar-cadastro.py` (casa por gmnCid, telefone/WhatsApp ou slug do
   nome) — só segue quem voltar `NOVO`. Nunca reprospecte cliente/lead existente.

## Localização das buscas (país/estado/cidade — configurável)

Vem de `prospector-config.json` → bloco `localizacao`: `pais`, `estado`, `cidade`
(e `regiao` opcional). Valem para TODAS as buscas e ficam FIXOS até o usuário pedir
mudança. Monte as buscas do Maps com "[nicho] em [cidade]/[regiao], [estado], [pais]".

**Busca localizada — evitar o viés dos EUA:** para achar Instagram/negócio local,
faça a busca pelo navegador MCP no Google do país configurado:
`https://www.google.com/search?q=<consulta>&gl=<google_gl>&hl=<google_hl>&cr=country<google_gl>`
(Brasil → `gl=BR&hl=pt-BR&cr=countryBR`; Canadá → `gl=CA&hl=en-CA`). Como a requisição
sai da conexão do usuário (IP local), o Google responde como o país certo. Leia a
SERP por screenshot ou leitura da página.

## Fluxo (via navegador MCP)

1. Abrir `https://www.google.com/maps` e buscar `[nicho] em [cidade]`.
2. Percorrer os resultados um a um, em ordem. Para cada estabelecimento:
   - Abrir o perfil e ler nota, nº de avaliações e link do site.
   - **Filtro 1 — potencial financeiro:** nota ≥ 4.0 E avaliações ≥ 20. Reprovou → próximo.
   - **Filtro 2 — canal de contato:** ao menos UM canal — e-mail, WhatsApp ou
     Instagram. Sem nenhum contato público → descartar (registrar o motivo) e seguir.
   - **Filtro 3 — oportunidade de site:** sem site (ou fora do ar, ou "site" que é só
     diretório de terceiros/linktree) → qualifica (motivo = "não tem site próprio");
     com site → abrir em nova aba e avaliar pelos critérios abaixo — site fraco
     (2+ problemas) → qualifica (motivo = os problemas); site moderno e bom → descartar
     (baixa oportunidade), registrar o motivo.
3. Parar ao atingir a meta de leads qualificados (config, padrão 10) ou após avaliar
   25 estabelecimentos.
4. **Deduplicar (OBRIGATÓRIO):** antes de avaliar/qualificar cada estabelecimento,
   cheque-o contra o cadastro (`prospector.db`). Já existe (inclusive `descartado`) → PULE.

## Deduplicação (OBRIGATÓRIA)

`prospector.db` é a FONTE DA VERDADE. Antes de qualificar cada candidato, valide com
`references/checar-cadastro.py` (Python puro, sem dependências):

    python checar-cadastro.py --db prospector.db "Nome do Negócio" --tel "(31) 3264-1753" --wa 5531986921283 --cid <CID>
    # JA_CADASTRADO | <slug> | status=... | por=...   -> PULAR
    # NOVO                                            -> seguir

Casa por gmnCid, telefone/WhatsApp (só dígitos) ou slug do nome. Uma chave basta.
Em lote: `--lote arquivo.txt` (linhas `Nome;telefone;whatsapp;cid`). Grave SEMPRE o
`gmnCid` dos leads novos — é ele que torna a dedup à prova de erro nas próximas rodadas.

## Critérios de site ruim (guardar o motivo específico)

Aplica-se aos leads QUE TÊM site. Qualifica se o site ativo tiver 2+ destes problemas:
layout datado; sem CTA claro de agendamento/contato; domínio gratuito/plataforma alheia;
não responsivo; conteúdo desorganizado; sem prova social. O motivo deve ser objetivo e
verificável — será citado na proposta.

## Coleta por lead

Nome, nota, nº de avaliações, telefone, WhatsApp (formato `55DDDnúmero`), e-mail, URL
do site, motivo, Instagram (SEMPRE) e Google Meu Negócio (URL + CID). Regras detalhadas
de captura de WhatsApp, e-mail, Instagram, logo, CID e domínio sugerido estão em
`references/coleta-detalhada.md`.

## Saída — planilha + leads.md + dashboard

1. **Planilha de leads (CSV):** gere/atualize `leads-[nicho]-[cidade].csv` com as
   colunas: #, Nome, Nota, Avaliações, E-mail, Telefone, Site atual, Motivo, Situação
   (Qualificado/Descartado + motivo), Status, URL nova. Inclua TODOS os avaliados
   (qualificados E descartados), ranqueados por potencial (melhor nota + maior
   oportunidade: sem site, depois pior site).
   - No antigo plugin isso ia para uma planilha do Google Sheets via conector. No Kiro,
     geramos o CSV localmente. **Se o MCP do Google Sheets estiver configurado e ativo**,
     suba/atualize a planilha por ele e devolva o link ao usuário; senão, entregue o
     caminho do CSV.
2. **Cópia local `leads.md`:** mantenha como cópia de trabalho (mesmas colunas) para
   controle de status (`novo → redesenhado → publicado → proposta`). Em rodadas novas,
   some os leads novos aos antigos — nunca duplique cliente já avaliado.
3. **Dashboard:** crie/atualize `dashboard.html` na raiz da pasta do projeto seguindo a
   skill `dashboard-leads` — leads novos entram com `status: novo`, descartados com
   `status: descartado`. ⚠️ Ao gravar cada lead, gere o `slug` pela REGRA ÚNICA da skill
   `dashboard-leads`.

A entrega final DEVE incluir a confirmação explícita "Dashboard atualizado: [N] leads"
(criando o dashboard pela skill `dashboard-leads` se a pasta não tiver um — obrigatório,
nunca pule). Mostre a tabela ao usuário com o caminho do CSV e do `dashboard.html`, e
sugira o próximo passo: redesenhar os 5+ melhores leads (skill `redesign-premium`).

## Boas práticas

- Trabalhar por região dá vantagem: menos concorrência na oferta e conhecimento local.
- Enquanto o navegador trabalha, não interromper o fluxo com perguntas — só reportar a
  tabela final. Se o Google Maps pedir login/captcha, pausar e avisar o usuário.
