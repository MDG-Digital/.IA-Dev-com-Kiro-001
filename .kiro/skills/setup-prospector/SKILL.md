---
name: setup-prospector
description: Use para configurar o Prospector de Sites pela primeira vez (ou reconfigurar) — assinatura, nichos, localização, modo de envio e conexão com a Locaweb, além de criar o banco e o dashboard. Acione quando o usuário disser "configurar prospector", "setup", "começar do zero", "primeira vez".
---

# Setup do Prospector de Sites

Configura o ambiente uma vez. Siga esta ordem.

## 1. Pasta de trabalho

O projeto vive na pasta `Clientes` (raiz de trabalho): config, leads, banco e sites ficam nela.

## 2. Verificar config existente

Procure `prospector-config.json` na pasta. Se existir, mostre um resumo (sem exibir a senha)
e pergunte o que atualizar. Se não existir, colete os dados abaixo.

## 3. Dados do usuário (perguntar em formulário)

- **Assinatura da proposta:** nome completo, apresentação (ex.: "Designer de páginas de alta
  conversão") e WhatsApp/telefone de contato.
- **Nichos padrão:** sugira nutricionistas, psicólogos, advogados, psiquiatras — mas deixe
  editar livremente.
- **Localização padrão — `pais`, `estado`, `cidade`** (e `regiao`, opcional). Fixos até o
  usuário mudar. Definem também o país onde o Google/Instagram é consultado — guarde
  `google_gl` e `google_hl` (Brasil → `gl=BR`, `hl=pt-BR`).
- **Leads qualificados por busca:** padrão 10.
- **Modo de envio da proposta:** padrão "criar rascunho no Gmail para revisão".

## 4. Conexão com a Locaweb

Pergunte se o usuário já contratou a hospedagem Locaweb.
- **Ainda não:** explique que precisa de um plano que aceite múltiplos sites, e que depois de
  ativar deve voltar e rodar o setup de novo. Salve o config parcial e encerre.
- **Já contratou:** NÃO colete dados da Locaweb pelo chat (nem usuário, nem servidor, JAMAIS a
  senha). Tudo vai na aba Configurações do dashboard:
  1. Abra o dashboard (`iniciar-dashboard.bat`) → aba **Configurações** → seção
     **Conexão Locaweb**.
  2. Preencha os campos + senha: usuário, domínio, servidor e a senha (do painel/FTP da
     Locaweb). "Salvar conexão" → vai do navegador direto pro `prospector-config.json` no
     computador, sem passar pelo chat.
  3. Peça pra avisar quando salvar — aí você LÊ o config (sem exibir a senha) e valida.
  Nunca exiba, imprima ou registre a senha. Editar o `prospector-config.json` na mão também vale.

## 5. Salvar e testar

Salve em `prospector-config.json` neste formato:

```json
{
  "assinatura": { "nome": "", "apresentacao": "", "whatsapp": "" },
  "localizacao": { "pais": "Brasil", "estado": "MG", "cidade": "Belo Horizonte", "regiao": "Venda Nova", "google_gl": "BR", "google_hl": "pt-BR" },
  "prospeccao": { "nichos": ["nutricionistas", "psicologos", "advogados", "psiquiatras"], "leadsPorBusca": 10 },
  "envio": { "modo": "rascunho" },
  "locaweb": { "usuario": "", "dominio": "", "servidor": "", "senha": "", "pastaBase": "clientes" },
  "marca": "Kairós TecnologIA"
}
```

Se os dados da Locaweb foram informados, o teste de conexão segue a skill `deploy-locaweb`
(fluxo manual: o usuário publica um `teste.html` e você verifica a URL). Publicação é manual —
não peça para rodar publicador nem espere poller (ver skill `deploy-locaweb`).

## 6. Dashboard inicial

Siga a seção "Setup" da skill `dashboard-leads`: copie `dashboard-server.py` e
`iniciar-dashboard.bat` para a raiz da pasta, crie `prospector.db` (schema da skill) e gere o
`dashboard.html` a partir do `dashboard-template-3colunas.html` local. Explique: duplo clique
em `iniciar-dashboard.bat` abre o painel em `http://localhost:8765` (requer Python; sem ele, o
dashboard.html abre em modo leitura).

## 7. MCPs (integrações)

Confirme com o usuário o estado das integrações em `.kiro/settings/mcp.json`:
- **Navegador (Playwright MCP):** necessário para prospectar e extrair sites. Requer Node.js.
- **Gmail MCP:** necessário para criar rascunhos e ler respostas. Requer autenticação Google.
- **Google Sheets MCP (opcional):** só se quiser espelhar os leads numa planilha do Google.
Oriente a habilitar cada um conforme a necessidade.

## 8. Encerrar

Confirme o que foi salvo e explique o ciclo (guiando sempre o próximo passo):
prospectar → redesenhar → publicar → proposta, com o editor visual opcional para ajustes e o
`dashboard.html` como painel de controle de tudo.
