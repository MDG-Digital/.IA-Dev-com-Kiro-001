---
name: deploy-locaweb
description: Use ao publicar páginas na hospedagem Locaweb — upload via script local, FTP ou painel, criação de pastas por cliente, verificação da URL pública e HTTPS. Acione quando o usuário disser "publicar", "subir o site", "colocar no ar", "deploy", "locaweb".
---

# Deploy na Locaweb

Publicar páginas em `public_html/[pastaBase]/[slug]/` e garantir a URL pública
`https://[dominio]/[pastaBase]/[slug]/` funcionando.

> ⚠️ **SLUG:** a pasta remota e a URL usam o `slug` já gravado no `prospector.db` para o
> lead (o mesmo da pasta local `sites/bh/oficinas/<slug>/`). Leia o slug do banco — nunca
> re-derive do nome. Regra única de slug: skill `dashboard-leads`.

## Credenciais

Tudo vem de `prospector-config.json` (bloco `locaweb`): `usuario`, `dominio`, `servidor`,
`senha`, `pastaBase` (padrão `clientes`). **A senha vive SÓ nesse arquivo, no computador do
usuário — nunca é digitada no chat, nunca é exibida em nenhuma saída, log ou comando
mostrado ao usuário.** Se a senha estiver vazia, oriente: dashboard → aba Configurações →
Conexão Locaweb → colar a senha e salvar (ou editar o arquivo na mão). Nunca pelo chat.

## Publicação é MANUAL (regra fixa — preferência do usuário, reforçada 02/09/2026)

O usuário publica os sites manualmente, no tempo dele. Ao terminar um redesenho/ajuste que
precise ir ao ar:

1. Deixe o(s) arquivo(s) final(is) correto(s) na pasta do cliente.
2. **Gere a página-capa** de cada cliente: preencha `capa-proposta-template.html` (skill
   `proposta-email`) com os dados do lead + assinatura do config e salve como
   `sites/bh/oficinas/[slug]/proposta.html` — é ela que vai no e-mail de proposta.
3. **Monte a fila** `fila-publicacao.txt` na raiz da pasta do projeto, uma linha por arquivo:
   `caminho/local/arquivo.html|public_html/[pastaBase]/[slug]/index.html`. Inclua página
   (`index.html`) e capa (`proposta.html`) de cada cliente.
4. **Apenas AVISE que está pronto para publicar.** NÃO peça para o usuário rodar o
   `publicar-agora.bat`, NÃO aguarde nem cheque `fila-publicada-*.txt`, NÃO verifique se há
   publicador automático rodando, NÃO tente subir sozinho (FTP direto etc.). Ele já sabe e
   publica por conta própria.

Os scripts do publicador (`publicar-agora.bat`/`.ps1`, `instalar-publicador.bat`) ficam em
`references/` e são copiados para a pasta do projeto no setup; o usuário os roda quando quiser.
Eles leem as credenciais do bloco `locaweb` do config.

## Método alternativo — FTP direto (só sob pedido explícito)

Só se o usuário pedir explicitamente para tentar subir daqui:
`curl -sS --connect-timeout 15 -T [arquivo] "ftp://[servidor]/public_html/[pastaBase]/[slug]/index.html" --user "[usuario]:[senha do config]" --ftp-create-dirs`
(senha lida do arquivo via script — jamais mostrada). Se a rede bloquear, não insista —
volte ao fluxo manual.

## Verificação (quando o usuário confirmar que publicou)

Só depois de o usuário dizer que publicou:
1. Abra `https://[dominio]/[pastaBase]/[slug]/` e a capa `.../proposta.html` — confirme que
   carregam com o conteúdo certo.
2. **HTTPS obrigatório:** precisa carregar com cadeado válido. Se der erro de certificado, a
   Locaweb oferece SSL — guie o usuário pelo painel da Locaweb (Hospedagem → SSL/Certificados,
   ativar o certificado gratuito Let's Encrypt para o domínio; pode levar alguns minutos).
   Enquanto o HTTPS não valida, a publicação NÃO está concluída — link `http://` NUNCA vai
   para cliente.
3. Atualize `leads.md` + dashboard (skill `dashboard-leads`) com status `publicado` e a URL.

## Saída

Liste, por cliente: URL da página nova e URL da capa (`.../proposta.html`). Após o usuário
publicar e a verificação passar, sugira o próximo passo: enviar as propostas (skill
`proposta-email`).
