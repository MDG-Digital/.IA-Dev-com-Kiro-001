# Coleta detalhada por lead (prospeccao-maps)

Regras minuciosas de captura de cada campo. O `SKILL.md` referencia este arquivo.

## WhatsApp — capture SEMPRE, separado do telefone

Fontes, na ordem: botão/link de WhatsApp no site do lead (procure `wa.me/`,
`api.whatsapp.com` ou ícone de WhatsApp — extraia o número do link); telefone celular
do perfil do Maps (números com 9º dígito são celular no Brasil — assuma WhatsApp).
Registre no formato internacional `55 + DDD + número` (ex.: `5511999990000`), pronto
pra `wa.me`. O WhatsApp alimenta os botões do dashboard e o plano B de abordagem
quando o e-mail não responde.

### Validar WhatsApp de números fixos (preferência do usuário)

Sempre que o telefone for FIXO (ou não estiver explícito que é WhatsApp), VALIDAR
antes de gravar: abrir `https://wa.me/55DDDNUMERO` no navegador (redireciona p/
`api.whatsapp.com/send?phone=...`) e LER a página — se mostrar o NOME do perfil/empresa
+ "Continuar para o WhatsApp Web", o número é WhatsApp e vai para o campo `whatsapp`
(55+DDD+numero); se não mostrar perfil, não é. É só leitura, NUNCA enviar mensagem.
Um lead pode ter mais de um número — testar todos. Requer WhatsApp Web logado.

## Contato — pelo menos UM canal é obrigatório (e-mail preferido)

O e-mail é o canal ideal (a proposta padrão vai por e-mail), mas NÃO é mais
eliminatório sozinho — um lead só com WhatsApp ou Instagram também fecha o ciclo
(proposta por WhatsApp/DM, ver skill `proposta-email`). Procure o e-mail nesta ordem:
site (rodapé e página de contato), links `mailto:`, busca no Google por
"[nome] + email/contato". Sem e-mail mas com WhatsApp ou Instagram → mantenha o lead
e marque o canal de abordagem. Só descarte por contato quando NÃO houver e-mail, nem
WhatsApp, nem Instagram. "Site" que aponta para diretório de terceiros (localtreino,
acheioprofissional etc.) não conta como site próprio — trate como SEM site.

## Instagram — SEMPRE, para TODO lead (com ou sem site)

Capture o @ ou a URL do perfil MESMO quando o lead já tem site — o Instagram é fonte
rica de fotos, serviços, horários e novidades que alimentam a criação/redesign. Procure
nesta ordem: site do lead (ícone/link no cabeçalho ou rodapé — pegue o `instagram.com/...`),
perfil do Google Maps, e busca `[nome] [cidade] instagram`. Ao abrir o perfil, anote
sinais úteis (nº de seguidores, se está ativo, principais serviços/fotos). Grave o @ ou
a URL em `instagram`. Se não achar com segurança, deixe em branco (revisão no dashboard).

### Descobrir o Instagram (preferência do usuário)

Sempre tentar achar o Instagram quando não vier no GMN nem no site antigo. Busca no
Google: `<nome do cliente> <nicho> <cidade> instagram`. Abrir ATÉ 4 perfis do topo,
ler a bio e conferir se batem os dados (nome, bairro/endereço, telefone, serviços).
Se bater, gravar em `instagram` e aproveitar logo/dados/paleta. Se nenhum bater,
registrar que não há Instagram localizável.

**Instagram como "site" no Maps (resolver na hora):** se o campo "site" do lead no Maps
for um `instagram.com/...`, ABRA o link — o perfil aparece e o @ aparece na URL/topo.
Resolva o @ na hora; NÃO mande pra revisão manual.

## Logo (campo `logo`)

Com o perfil do Instagram aberto, capture a foto de perfil (o avatar circular ao lado
do nome/bio — normalmente é a logomarca). Recorte a região do avatar, reduza para
~160px, salve como JPEG e grave no campo `logo` como data-URI base64 (~4KB, cabe no
banco). Se o perfil exigir login ou o avatar não for recortável, deixe `logo` vazio
(o editor de site permite subir a logo depois).

## Google Meu Negócio — link + CID (fallback obrigatório)

O objetivo é um link que abre o perfil COMPLETO do negócio em 1 clique, mais uma chave
estável pra não prospectar o mesmo lugar 2x. Com o perfil ABERTO no Google Maps:

1. **Leia a URL da barra de endereço** — formato
   `.../maps/place/Nome/@lat,lng,zoom/data=!...!1s0x<HEX_A>:0x<HEX_B>!...`.
2. **Extraia o CID:** valor depois dos dois-pontos, `0x<HEX_B>`. Converta esse
   hexadecimal para DECIMAL — o número decimal é o CID. Grave o número puro em `gmnCid`.
3. **Monte o `gmnUrl` preferido:** `https://www.google.com/maps?cid=<CID>` (limpo,
   estável, abre o painel completo). Antes de gravar, ABRA esse link numa aba nova e
   confirme que caiu no negócio certo.
4. **Fallbacks quando não der pra extrair o CID:** grave em `gmnUrl` a própria URL longa
   `/maps/place/...` da barra, OU o link do botão Compartilhar → Copiar link
   (`maps.app.goo.gl/...`), e deixe `gmnCid` vazio.
5. Se nada abrir com segurança o perfil, deixe os dois campos vazios (revisão manual).

**NUNCA gravar lead com `gmnCid` vazio nem com `gmnUrl` de busca (`/maps/search/...`).**
Quando a URL não virar `/maps/place/`, force a ficha com o prefixo
`/maps/place/<Nome + rua + número + bairro + cidade>` e releia a URL; se não vier, leia
`location.href` via JS (o contexto da aba traz o `/place/` resolvido) ou extraia do
conteúdo o padrão `0x<hex>:0x<hex>` e use o 2º hex → decimal.

> Observação técnica: o `0x<HEX_A>` antes dos dois-pontos é o Feature ID (auxiliar); o
> Place ID oficial (`ChIJ...`) NÃO aparece na URL — só via API Places, por isso não é
> usado aqui.

## Domínio sugerido (campo `dominio`)

- **Com site próprio:** guarde só a parte do domínio do site atual — sem `http(s)://`,
  sem `www.`, sem caminho. Ex.: `https://flavianamagalhaes.adv/sobre` →
  `flavianamagalhaes.adv`.
- **Sem site próprio:** CRIE um domínio sugerido a partir do NOME (minúsculas, sem
  acento/ç, só `a-z 0-9`, sem espaços), compactando/concatenando as palavras, com final
  `.com.br`. Ex.: `Auto Power Tech` → `autopowertech.com.br`.

O campo guarda o domínio COMPLETO (com `.com.br` ou o TLD do site). A mensagem de
WhatsApp usa esse valor direto em `www.<dominio>` e `atendimento@<dominio>` — não
acrescente `.com.br`, já está no campo.
