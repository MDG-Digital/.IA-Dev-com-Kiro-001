# Configuração de MCP — Prospector de Sites no Kiro

As skills do Prospector de Sites usam servidores MCP para as integrações que, no antigo
plugin do Claude, eram feitas por "Claude in Chrome" e pelos conectores do Google.

O Kiro protege o arquivo `.kiro/settings/mcp.json` contra escrita automática, então você
precisa criá-lo/editá-lo você mesmo — pela interface do Kiro (painel de MCP / paleta de
comandos → "MCP") ou colando o conteúdo abaixo.

Node.js já está instalado nesta máquina (v24), então os servidores rodam via `npx`.

> **Onde fica cada config:** o `playwright` e o `google-sheets` podem ficar no arquivo do
> projeto (`.kiro/settings/mcp.json`). O `gmail` é pessoal (usa a sua conta), então está no
> arquivo GLOBAL do usuário (`C:\Users\User\.kiro\settings\mcp.json`) para valer em qualquer
> workspace e não ir para o GitHub. O `mcp.json` está no `.gitignore`.

## Conteúdo do `mcp.json`

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "disabled": false,
      "autoApprove": []
    },
    "gmail": {
      "command": "npx",
      "args": ["-y", "@gongrzhe/server-gmail-autoauth-mcp"],
      "disabled": false,
      "autoApprove": []
    },
    "google-sheets": {
      "command": "npx",
      "args": ["mcp-google-sheets@latest"],
      "env": {
        "SERVICE_ACCOUNT_PATH": ""
      },
      "disabled": true,
      "autoApprove": []
    }
  }
}
```

## O que cada servidor faz e o que exige

### 1. `playwright` — navegador (ESSENCIAL, habilitado)
Substitui o "Claude in Chrome". Usado por `prospeccao-maps` (abrir Google Maps, ler perfis,
executar JavaScript para coletar imagens) e por `redesign-premium` (extrair conteúdo/fotos do
site original). Não precisa de credenciais. No primeiro uso, o Playwright baixa o navegador
sozinho.

### 2. `gmail` — e-mail (CONECTADO E VALIDADO)
Substitui o conector do Gmail. Usado por `proposta-email` e `contrato-servico` para criar
rascunhos, enviar e ler respostas.

**Servidor usado: `@gongrzhe/server-gmail-autoauth-mcp`.**
Escolhido porque usa **stdio puro (não abre porta HTTP)** — evita o erro `EADDRINUSE`
(conflito de porta) que o servidor `@shinzolabs/gmail-mcp` causava, deixando instâncias
zumbis e resultando em "Connection Failed" no Kiro.

Autenticação (feita uma vez, já concluída nesta máquina):
1. As credenciais OAuth (Desktop app) ficam em `C:\Users\User\.gmail-mcp\gcp-oauth.keys.json`.
2. Rodar `npx @gongrzhe/server-gmail-autoauth-mcp auth` abre o navegador para aprovar; o token
   é salvo em `C:\Users\User\.gmail-mcp\credentials.json`.
3. O servidor acha esses arquivos sozinho em `~/.gmail-mcp/` — por isso o bloco NÃO precisa de
   `env` com caminhos nem de porta.

Se algum dia precisar reautenticar (token expirado/revogado): rode o comando `auth` acima de
novo e reconecte o servidor no Kiro.

### 3. `google-sheets` — planilha (OPCIONAL, desabilitado)
Espelha os leads numa planilha do Google. NÃO é obrigatório: o fluxo já mantém `leads.md`,
`prospector.db` e `dashboard.html` localmente. Habilite só se quiser a planilha na nuvem.
Requer uma conta de serviço do Google (Service Account) com acesso ao Sheets; aponte
`SERVICE_ACCOUNT_PATH` para o JSON da conta e compartilhe a planilha com o e-mail da conta.

## Se o Gmail voltar a dar "Connection Failed"

Com o `@gongrzhe/...` (stdio, sem porta) isso não deve mais acontecer. Se acontecer, o mais
provável é token expirado — rode `npx @gongrzhe/server-gmail-autoauth-mcp auth` novamente e
reconecte. (O problema antigo de instâncias presas em porta era exclusivo do servidor
`@shinzolabs/gmail-mcp`, que foi abandonado.)

## Enquanto o Gmail/Sheets não estiverem ativos

As skills funcionam em modo degradado: os e-mails/mensagens são escritos e entregues como
texto (ou salvos em arquivo) para você enviar, e as respostas você cola no chat para o Kiro
classificar. Nada trava por falta desses MCPs — só o navegador (Playwright) é essencial para
a etapa de prospecção.
```
