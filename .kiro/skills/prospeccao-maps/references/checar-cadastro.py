#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prospector — validador de duplicidade (dedup).

Antes de qualificar um lead novo na prospecção, cheque se o negócio JÁ está no
cadastro (prospector.db, a fonte da verdade). Evita reprospectar cliente existente.

Casa por 3 chaves, em ordem de força:
  1) gmnCid  (chave estável do Google Meu Negócio — quando disponível)
  2) telefone/WhatsApp (só dígitos, ignora DDI/zeros à esquerda)
  3) slug do nome (slugify: minúsculas, sem acento, sem prefixo)

Uso:
  python3 checar-cadastro.py --db prospector.db "Nome do Negocio" \
      [--tel "(31) 3264-1753"] [--wa 5531986921283] [--cid 1784...]

Saída (stdout):
  "JA_CADASTRADO | <slug> | status=<status> | por=<chave>"   (código de saída 2)
  "NOVO"                                                       (código de saída 0)

Modo lote: --lote arquivo.txt  (um "Nome;telefone;whatsapp;cid" por linha)
imprime uma linha de resultado por entrada.
"""
import argparse, re, sqlite3, sys, unicodedata


def slugify(nome):
    s = unicodedata.normalize('NFKD', nome or '').encode('ascii', 'ignore').decode()
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()
    return re.sub(r'-{2,}', '-', s)


def so_digitos(v):
    d = re.sub(r'\D', '', v or '')
    return d.lstrip('0') if d else ''


def tel_chave(v):
    """Normaliza telefone/WhatsApp para comparar: últimos 8-9 dígitos (número local),
    removendo DDI 55 e DDD quando possível — casa (31) 3264-1753 com 553132641753."""
    d = so_digitos(v)
    if d.startswith('55') and len(d) > 10:
        d = d[2:]
    return d[-9:] if len(d) >= 9 else d[-8:] if len(d) >= 8 else d


def carregar(db):
    c = sqlite3.connect(db)
    c.row_factory = sqlite3.Row
    cols = {r[1] for r in c.execute('PRAGMA table_info(leads)').fetchall()}
    tem_cid = 'gmnCid' in cols
    linhas = []
    for r in c.execute('SELECT * FROM leads'):
        linhas.append({
            'slug': r['slug'],
            'nome': r['nome'],
            'status': r['status'],
            'slug_nome': slugify(r['nome']),
            'tel': tel_chave(r['telefone'] if 'telefone' in r.keys() else ''),
            'wa': tel_chave(r['whatsapp'] if 'whatsapp' in r.keys() else ''),
            'cid': (str(r['gmnCid']).strip() if tem_cid and r['gmnCid'] else ''),
        })
    c.close()
    return linhas


def checar(reg, nome, tel=None, wa=None, cid=None):
    s = slugify(nome)
    tks = {tel_chave(tel), tel_chave(wa)} - {''}
    cidn = (str(cid).strip() if cid else '')
    for L in reg:
        if cidn and L['cid'] and cidn == L['cid']:
            return L, 'gmnCid'
        chaves = {L['tel'], L['wa']} - {''}
        if tks and (tks & chaves):
            return L, 'telefone/whatsapp'
        if s and (s == L['slug'] or s == L['slug_nome']):
            return L, 'nome/slug'
    return None, None


def fmt(m, chave):
    if m:
        return 'JA_CADASTRADO | %s | status=%s | por=%s' % (m['slug'], m['status'], chave)
    return 'NOVO'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('nome', nargs='?')
    ap.add_argument('--db', default='prospector.db')
    ap.add_argument('--tel')
    ap.add_argument('--wa')
    ap.add_argument('--cid')
    ap.add_argument('--lote')
    a = ap.parse_args()
    reg = carregar(a.db)
    if a.lote:
        for ln in open(a.lote, encoding='utf-8'):
            ln = ln.strip()
            if not ln or ln.startswith('#'):
                continue
            p = (ln.split(';') + ['', '', ''])[:4]
            m, k = checar(reg, p[0], p[1], p[2], p[3])
            print('%s -> %s' % (p[0], fmt(m, k)))
        return
    if not a.nome:
        ap.error('informe o nome do negócio (ou use --lote)')
    m, k = checar(reg, a.nome, a.tel, a.wa, a.cid)
    print(fmt(m, k))
    sys.exit(2 if m else 0)


if __name__ == '__main__':
    main()
