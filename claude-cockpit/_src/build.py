#!/usr/bin/env python3
"""Baut index.html und die Unterseiten aus page.html + den Inhalten in _src/pages/.
Aufruf: python3 claude-cockpit/_src/build.py"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_src" / "pages"

HEAD = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
"""

HEADER = """<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Claude Cockpit, zur Startseite">
      <img src="assets/logo.png" alt="KI mit Marie" width="42" height="44">
      <span><strong>Claude Cockpit</strong>von KI mit Marie</span>
    </a>
    <a class="back" href="index.html">← Zur Startseite</a>
  </div>
</header>
"""

FOOTER = """<footer>
  <div class="wrap">
    <span>© 2026 KI mit Marie · Marie Christine Reiter</span>
    <nav aria-label="Rechtliches">
      <a href="impressum.html">Impressum</a>
      <a href="datenschutz.html">Datenschutz</a>
      <a href="agb.html">AGB</a>
      <a href="widerruf.html">Widerrufsbelehrung</a>
      <button type="button" class="linkish" data-consent-open>Cookie-Einstellungen</button>
    </nav>
  </div>
</footer>
<script src="consent.js" defer></script>
"""

def wrap_index():
    page = (ROOT / "page.html").read_text()
    head_end = page.index('<link rel="stylesheet" href="styles.css">') + len('<link rel="stylesheet" href="styles.css">\n')
    out = HEAD + page[:head_end] + "</head>\n<body>\n" + page[head_end:] + "</body>\n</html>\n"
    (ROOT / "index.html").write_text(out)

def build_page(src):
    text = src.read_text()
    meta, body = text.split("\n---\n", 1)
    fields = dict(line.split(": ", 1) for line in meta.strip().splitlines())
    extra = '<meta name="robots" content="noindex, nofollow">\n' if fields.get("noindex") == "yes" else ""
    body_attr = f' data-track="{fields["track"]}"' if fields.get("track") else ""
    html = (HEAD + f"<title>{fields['title']} · Claude Cockpit</title>\n" + extra +
            '<link rel="stylesheet" href="styles.css">\n</head>\n' +
            f"<body{body_attr}>\n" + HEADER +
            '<main class="doc">\n  <div class="wrap">\n' + body.strip() + "\n  </div>\n</main>\n" +
            FOOTER + "</body>\n</html>\n")
    (ROOT / (src.stem + ".html")).write_text(html)

wrap_index()
for p in sorted(SRC.glob("*.html")):
    build_page(p)
print("ok")
