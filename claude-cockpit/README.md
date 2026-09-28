# Claude Cockpit – Verkaufsseite

Statische Website, läuft auf jedem Webspace (einfach den Ordner hochladen, ohne `_src/` und `page.html`).

| Datei | Inhalt |
|---|---|
| `index.html` | Verkaufsseite |
| `danke.html` | Danke-/Download-Seite nach dem Kauf (noindex) |
| `impressum.html`, `datenschutz.html`, `agb.html`, `widerruf.html` | Rechtstexte |
| `consent.js` | Cookie-Hinweis, lädt Meta Pixel / Google Analytics erst nach Einwilligung |
| `styles.css`, `fonts/`, `assets/` | Design, lokal gehostete Schriften, Bilder |

## Noch einzutragen
- Alle pink markierten `[Platzhalter]` in den Rechtstexten und auf der Danke-Seite
- Checkout-Link: `#CHECKOUT-LINK` in `page.html`
- Download-Links: `#DOWNLOAD-ZIP`, `#DOWNLOAD-WORD-1/2`, Video-Links `#VIDEO-1/2/3` in `_src/pages/danke.html`
- Optional: Meta-Pixel-ID in `consent.js` (erst dann erscheint der Cookie-Hinweis)

Die ZIP-Datei liegt bewusst **nicht** in diesem öffentlichen Repository.

## Ändern und neu bauen
Texte in `page.html` bzw. `_src/pages/*.html` bearbeiten, dann:

```
python3 claude-cockpit/_src/build.py
```
