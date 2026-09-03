# -*- coding: utf-8 -*-
# Prospector de Sites — publica os 2 sites em REDESENHADO e move para PROPOSTA.
# Roda na maquina do usuario (disco real): sobe via FTP (curl.exe) e grava no prospector.db.
import os, re, json, sqlite3, subprocess, datetime, sys

PASTA = os.path.dirname(os.path.abspath(__file__))
DB    = os.path.join(PASTA, "prospector.db")
CFG   = os.path.join(PASTA, "prospector-config.json")
PASTA_BASE = "sites/bh/oficinas"
HOJE  = datetime.date.today().isoformat()               # YYYY-MM-DD
AGORA = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

# leads a publicar/propor (os dois em redesenhado)
SLUGS = ["atos-centro-automotivo", "bosch-santa-amelia", "ft-auto-reparo", "lubrikar-service", "sancar", "teccar-multimarcas", "top-car-pampulha"]

def carrega_cfg():
    with open(CFG, encoding="utf-8-sig") as f:
        return json.load(f)

def sobe_ftp(cfg, slug):
    hg = cfg["hostgator"]
    local  = os.path.join(PASTA, "sites", "bh", "oficinas", slug, slug + ".html")
    if not os.path.exists(local):
        print(f"  [{slug}] PULOU — nao achei {local}")
        return False
    remoto = f"ftp://{hg['servidor']}/public_html/{PASTA_BASE}/{slug}/index.html"
    print(f"  [{slug}] subindo {slug}.html -> public_html/{PASTA_BASE}/{slug}/index.html ...")
    r = subprocess.run(
        ["curl.exe", "-sS", "--connect-timeout", "20", "-T", local, remoto,
         "--user", f"{hg['usuario']}:{hg['senha']}", "--ftp-create-dirs"],
        capture_output=True, text=True)
    if r.returncode == 0:
        print("      OK")
        return True
    print(f"      FALHOU (curl {r.returncode}) {r.stderr.strip()[:120]}")
    return False

def limpa_journal():
    for ext in ("-journal", "-wal", "-shm"):
        p = DB + ext
        try:
            if os.path.exists(p):
                os.remove(p)
        except Exception:
            pass

def atualiza_db(publicados):
    limpa_journal()
    c = sqlite3.connect(DB, timeout=20)
    c.execute("PRAGMA busy_timeout=20000")
    for slug in publicados:
        url = f"https://kairostecnologia.com/{PASTA_BASE}/{slug}/"
        c.execute(
            "UPDATE leads SET status='proposta', dataProposta=?, urlNova=?, atualizado=? "
            "WHERE slug=? AND status IN ('redesenhado','publicado','novo')",
            (HOJE, url, AGORA, slug))
        print(f"  [{slug}] status -> proposta | urlNova = {url}")
    c.commit()
    # regenera snapshot do dashboard.html (fallback offline)
    cols = [d[1] for d in c.execute("PRAGMA table_info(leads)")]
    leads = [dict(zip(cols, row)) for row in c.execute("SELECT * FROM leads")]
    c.close()
    dash = os.path.join(PASTA, "dashboard.html")
    if os.path.exists(dash):
        html = open(dash, encoding="utf-8").read()
        snap = json.dumps({"atualizado": AGORA, "leads": leads}, ensure_ascii=False)
        novo, n = re.subn(
            r'(<script[^>]*id="dados"[^>]*>).*?(</script>)',
            lambda m: m.group(1) + snap + m.group(2),
            html, count=1, flags=re.S)
        if n:
            open(dash, "w", encoding="utf-8").write(novo)
            print("  dashboard.html: snapshot atualizado")

def main():
    if not os.path.exists(CFG):
        print("ERRO: prospector-config.json nao encontrado."); return
    cfg = carrega_cfg()
    hg = cfg.get("hostgator", {})
    if not (hg.get("usuario") and hg.get("senha") and hg.get("servidor")):
        print("ERRO: conexao HostGator incompleta no config."); return

    print("== 1) Publicando os 2 sites na HostGator ==")
    publicados = [s for s in SLUGS if sobe_ftp(cfg, s)]

    if not publicados:
        print("\nNenhum site subiu — banco NAO alterado. Confira a conexao e tente de novo.")
        return

    print("\n== 2) Atualizando banco (status=proposta) e dashboard ==")
    atualiza_db(publicados)

    print("\nPRONTO.")
    print("Publicados:", ", ".join(publicados))
    print("URLs:")
    for s in publicados:
        print(f"  https://kairostecnologia.com/{PASTA_BASE}/{s}/")
    print("\nAgora e so enviar as mensagens do mensagens-whatsapp.md pelos WhatsApp dos leads.")
    print("Abra o iniciar-dashboard.bat para ver os cards em PROPOSTA.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERRO:", e)
    input("\nPressione ENTER para fechar...")
