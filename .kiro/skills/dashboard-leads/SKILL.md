---
name: dashboard-leads
description: Use para criar e ATUALIZAR o dashboard de leads — o painel de controle local (SQLite + página web) onde o usuário administra prospecções, sites, publicações e propostas. Acione sempre que qualquer etapa mudar dados de leads (prospectar, redesenhar, publicar, proposta), ou quando o usuário disser "dashboard", "painel", "meus leads", "controle de clientes", "banco de dados de leads".
---

# Dashboard de leads (SQLite + página local)

Arquitetura na RAIZ da pasta do projeto (a pasta `Clientes`):

- **`prospector.db`** — banco SQLite, a FONTE DA VERDADE dos leads.
- **`dashboard-server.py` + `iniciar-dashboard.bat` (Windows) / `iniciar-dashboard.command` (Mac)** — mini-servidor local (Python padrão, sem dependências). Duplo clique no `.bat` → abre `http://localhost:8765` com o painel completo: editar, excluir e arrastar cards salvam direto no banco.
- **`dashboard.html`** — a página do painel (gerada do template). Servida pelo servidor (modo banco) ou aberta por duplo clique (modo arquivo: só leitura + edições presas ao navegador). O badge no topo indica o modo.

> ⚠️ **Template fonte da verdade é o LOCAL:** `dashboard-template-3colunas.html` (raiz
> da pasta `Clientes`) é o template ATIVO — NÃO o `references/dashboard-template.html`
> empacotado nesta skill (versão v2 desatualizada). Toda regeneração do dashboard deve
> partir do `dashboard-template-3colunas.html` local. Nunca apague esse template.

## Setup (uma vez, na skill setup-prospector ou no primeiro uso)

1. Copie `references/dashboard-server.py` e `references/iniciar-dashboard.bat` desta
   skill para a raiz da pasta do projeto.
2. Crie o `prospector.db` com o schema abaixo (via python/sqlite3).
3. Gere o `dashboard.html` a partir do `dashboard-template-3colunas.html` local
   substituindo o marcador de dados pelo snapshot JSON.
4. Diga ao usuário: "duplo clique em `iniciar-dashboard.bat` abre o painel com o banco
   conectado" (requer Python instalado no Windows — sem ele, o dashboard.html funciona
   no modo arquivo).

## Schema do banco

```sql
CREATE TABLE IF NOT EXISTS leads(
  slug TEXT PRIMARY KEY, nome TEXT, nicho TEXT, cidade TEXT, nota REAL, avaliacoes INTEGER,
  email TEXT, telefone TEXT, whatsapp TEXT, siteAntigo TEXT, motivo TEXT,
  status TEXT DEFAULT 'novo', urlNova TEXT, dataProposta TEXT, valor REAL, obs TEXT,
  contratoStatus TEXT DEFAULT 'pendente', contratoEm TEXT, manutencao REAL, pago INTEGER DEFAULT 0,
  docCliente TEXT, endCliente TEXT,
  instagram TEXT, gmnUrl TEXT, gmnCid TEXT, dominio TEXT, razaoSocial TEXT, responsavel TEXT, diaVencimento INTEGER, valorTrimestral REAL, logo TEXT,
  atualizado TEXT DEFAULT (datetime('now','localtime')));
```

Status: `novo | redesenhado | publicado | proposta | respondeu | fechado | descartado`. `slug` é a chave.

**Campos extras:** `instagram`, `gmnUrl` e `gmnCid` são preenchidos automaticamente na
prospecção e passam por REVISÃO MANUAL no dashboard. `gmnUrl` é o link que abre o perfil
COMPLETO do negócio em 1 clique — padrão preferido `https://www.google.com/maps?cid=<CID>`,
com fallback para a URL longa `/maps/place/...`. `gmnCid` guarda só o CID (número), chave
estável do negócio: deduplica (não prospectar o mesmo lugar 2x) e reconstrói o link se
quebrar. `dominio`: quem TEM site → domínio do site atual; quem NÃO tem → um `.com.br`
sugerido do nome. `logo` guarda a logomarca (foto de perfil do Instagram) como base64
(~4KB). `razaoSocial`, `responsavel`, `diaVencimento` (1–31) e `valorTrimestral` são
preenchidos À MÃO pelo usuário, só para clientes que vão fechar contrato — podem ficar vazios.

## Convenção de slug (REGRA ÚNICA — fonte da verdade)

O `slug` é a **identidade** do lead: mesmo nome para a pasta (`sites/bh/oficinas/<slug>/`),
os arquivos (`<slug>.html`, `<slug>-editor.html`, `proposta.html`, `contrato-<slug>...`) e a
URL pública (`.../<pastaBase>/<slug>/`). Se o slug do banco divergir da pasta/arquivo, os
botões do dashboard quebram. Por isso:

1. **Como gerar (só na prospecção, quando o lead nasce):** derive do NOME DO NEGÓCIO —
   minúsculas, sem acento e sem `ç` (á→a, ç→c), remova tudo que não for `a-z 0-9`, troque
   espaços/`_`/`&`/`|`/`/` por `-`, colapse hífens repetidos e apare as pontas. **Sem
   prefixo de nicho.** Ex.: "Centro Automotivo Juninho" → `centro-automotivo-juninho`. Se
   colidir com um slug existente, acrescente `-2`, `-3`…
   ```python
   import re, unicodedata
   def slugify(nome):
       s = unicodedata.normalize('NFKD', nome).encode('ascii','ignore').decode()
       s = re.sub(r'[^a-zA-Z0-9]+','-', s).strip('-').lower()
       return re.sub(r'-{2,}','-', s)
   ```
2. **Slug é IMUTÁVEL.** Depois de gravado, NUNCA re-derive nem renomeie. Todo passo
   posterior (redesenhar, publicar, proposta, editor, contrato) LÊ o slug já gravado no
   `prospector.db` (casando pelo `nome`) e usa esse valor EXATO em pastas, arquivos e URLs.
3. **Checagem antes de criar/publicar arquivos:** confirme que `sites/bh/oficinas/<slug>/`
   usa o mesmo `slug` do banco. Divergiu → pare e alinhe pelo slug do banco antes de continuar.

## Como as etapas atualizam (SEMPRE os 2 passos)

1. **Upsert no banco** via python (exemplo):
```python
import sqlite3
c = sqlite3.connect('CAMINHO/prospector.db')
c.execute("INSERT INTO leads (slug,nome,status) VALUES (?,?,?) ON CONFLICT(slug) DO UPDATE SET status=excluded.status, atualizado=datetime('now','localtime')", ('slug','Nome','novo'))
c.commit()
```
   - **Prospectar** → insere leads (`novo`) e descartados (`descartado`, motivo em `obs`),
     preenchendo `instagram` e `gmnUrl`/`gmnCid`. NUNCA sobrescreva lead cujo status já avançou.
   - **Redesenhar** → `status='redesenhado'` · **Publicar** → `status='publicado'`, `urlNova`
     · **Proposta** → `status='proposta'`, `dataProposta`.
   - Usuário conta que respondeu/fechou → `status='respondeu'|'fechado'`, `valor`
     (+ `manutencao` se houver mensalidade).
   - **Contrato** → `contratoStatus='enviado'` + `contratoEm`. Assinou → `contratoStatus='assinado'`.
     Pagamento recebido → `pago=1`.
2. **Regenerar o snapshot:** leia todos os leads do banco e regrave `dashboard.html` do
   template local com o JSON embutido atualizado (`{"atualizado": "...", "leads": [...]}`).

Se o banco não existir ainda, crie-o e importe os leads do snapshot embutido no
`dashboard.html` atual antes do upsert. Respeite edições do usuário: antes de regravar um
lead, leia o registro atual do banco.

## O que o painel faz sozinho (não reimplementar)

Kanban drag & drop, edição em modal, exclusão, busca, paginação automática, funil,
follow-ups (proposta 4+ dias), receita fechada/potencial, vista Contratos (status +
link do documento + pago) e vista Financeiro (recebido, a receber, MRR de manutenções,
projeção 12 meses) — tudo no template. A aplicação só mantém o BANCO correto e o
snapshot em dia.
