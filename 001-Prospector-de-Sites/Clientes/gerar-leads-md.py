# -*- coding: utf-8 -*-
"""
Gera o leads.md a partir do prospector.db (fonte da verdade).

O leads.md e um artefato DERIVADO: nunca deve ser editado a mao. Este script
o reconstroi inteiro a partir do banco.

Uso:
    python gerar-leads-md.py            # regenera so se o .db for mais novo que o .md
    python gerar-leads-md.py --force    # regenera sempre
    python gerar-leads-md.py --quiet    # sem mensagens (usado pelo hook de SessionStart)

Sai com codigo 0 sempre que nao ha erro (inclusive quando pula por estar atualizado).
"""
import sqlite3
import os
import sys
from collections import Counter, OrderedDict
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "prospector.db")
MD = os.path.join(BASE, "leads.md")

# ordem de status para o ranking dentro de cada nicho (funil -> descartado por ultimo)
STATUS_ORDEM = {
    "novo": 0, "redesenhado": 1, "publicado": 2, "proposta": 3,
    "respondeu": 4, "fechado": 5, "descartado": 9,
}
# ordem dos totais no rodape
ORDEM_TOTAIS = ["novo", "redesenhado", "publicado", "proposta", "respondeu", "fechado", "descartado"]

# rotulos amigaveis por nicho
LABELS = {
    "advogados": "Advogados",
    "oficinas": "Oficinas",
    "oficinas-pintura": "Oficinas — Lanternagem e Pintura",
    "oficinas-troca-de-oleo": "Oficinas — Troca de Óleo",
    "oficinas-auto-eletrica": "Oficinas — Auto Elétrica",
    "clinicas medicas": "Clínicas Médicas",
}
# ordem de exibicao das secoes (nichos fora desta lista entram no fim, na ordem do banco)
ORDEM_SECOES = [
    "advogados", "oficinas", "oficinas-pintura",
    "oficinas-troca-de-oleo", "oficinas-auto-eletrica", "clinicas medicas",
]


def esc(s):
    return (s or "").replace("|", "\\|")


def wpp(r):
    w = (r.get("whatsapp") or "").strip()
    if w:
        return w
    return (r.get("telefone") or "—").strip() or "—"


def url(r):
    return (r.get("urlNova") or "—").strip() or "—"


def gerar():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    rows = [dict(r) for r in c.execute(
        "SELECT nome,nicho,cidade,nota,avaliacoes,telefone,whatsapp,"
        "email,instagram,urlNova,motivo,status FROM leads"
    )]
    c.close()

    nichos = OrderedDict()
    for r in rows:
        n = (r.get("nicho") or "sem-nicho").strip()
        nichos.setdefault(n, []).append(r)

    out = []
    out.append("# Leads — Prospector de Sites")
    out.append("")
    out.append("**Região:** BH · **Critérios:** nota>3.8 · ≥20 aval · WhatsApp aceito  ")
    out.append(f"**Atualização:** {date.today().isoformat()} · "
               "**Fonte:** `prospector.db` (gerado automaticamente — NÃO editar à mão)")
    out.append("")
    out.append("> Fluxo: novo → redesenhado → publicado → proposta → respondeu → fechado.")
    out.append("")

    secoes = list(ORDEM_SECOES) + [n for n in nichos if n not in ORDEM_SECOES]
    for n in secoes:
        if n not in nichos:
            continue
        grupo = nichos[n]
        grupo.sort(key=lambda r: (
            STATUS_ORDEM.get((r.get("status") or "").strip(), 8),
            -(r.get("nota") or 0),
            -(r.get("avaliacoes") or 0),
        ))
        out.append(f"## {LABELS.get(n, n)}")
        out.append("")
        out.append("| Nome | Nota | Aval. | WhatsApp | Status | URL nova |")
        out.append("|------|------|-------|----------|--------|----------|")
        for r in grupo:
            out.append("| {nome} | {nota} | {aval} | {wpp} | {status} | {url} |".format(
                nome=esc(r.get("nome")),
                nota=r.get("nota") if r.get("nota") is not None else "—",
                aval=r.get("avaliacoes") if r.get("avaliacoes") is not None else "—",
                wpp=esc(wpp(r)),
                status=(r.get("status") or "—").strip() or "—",
                url=esc(url(r)),
            ))
        out.append("")

    tot = Counter((r.get("status") or "").strip() for r in rows)
    partes = [f"{k}: {tot[k]}" for k in ORDEM_TOTAIS if tot.get(k)]
    for k in tot:
        if k not in ORDEM_TOTAIS:
            partes.append(f"{k or 'sem-status'}: {tot[k]}")
    out.append("## Totais: " + " · ".join(partes) + f" (total {len(rows)})")
    out.append("")

    with open(MD, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return len(rows), dict(tot)


def main():
    args = set(sys.argv[1:])
    force = "--force" in args
    quiet = "--quiet" in args

    if not os.path.exists(DB):
        if not quiet:
            print(f"[gerar-leads-md] banco nao encontrado: {DB}", file=sys.stderr)
        return 0  # nao e erro fatal: sem banco, nada a fazer

    # regenera so se o banco for mais novo que o md (a menos que --force)
    if not force and os.path.exists(MD):
        if os.path.getmtime(DB) <= os.path.getmtime(MD):
            if not quiet:
                print("[gerar-leads-md] leads.md ja esta atualizado (banco nao mudou).")
            return 0

    n, tot = gerar()
    if not quiet:
        print(f"[gerar-leads-md] leads.md regenerado: {n} leads | {tot}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
