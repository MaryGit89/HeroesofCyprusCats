/*
  Cookie-Hinweis für Claude Cockpit
  ---------------------------------
  Solange unten keine ID eingetragen ist, lädt die Seite KEINE Tracking-Tools,
  setzt keine Cookies und zeigt auch keinen Banner (Schriften und Bilder liegen lokal).

  Sobald du z. B. für deine Meta-Anzeigen das Meta Pixel nutzen willst:
  1. ID unten eintragen
  2. Datenschutzerklärung: Abschnitt "Meta Pixel" freischalten (siehe datenschutz.html)
  Dann erscheint der Banner automatisch, und das Pixel lädt erst nach einem "Ja".
*/
(function () {
  var CONFIG = {
    metaPixelId: '',        // z. B. '123456789012345'
    googleAnalyticsId: ''   // z. B. 'G-XXXXXXXXXX'
  };

  var KEY = 'cockpit-consent-v1';
  var hasMarketing = !!CONFIG.metaPixelId;
  var hasStats = !!CONFIG.googleAnalyticsId;
  var openers = document.querySelectorAll('[data-consent-open]');

  if (!hasMarketing && !hasStats) {
    // Nichts einwilligungspflichtiges im Einsatz: Link "Cookie-Einstellungen" ausblenden.
    openers.forEach(function (el) { el.hidden = true; });
    return;
  }

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY)); } catch (e) { return null; }
  }
  function save(choice) {
    choice.date = new Date().toISOString();
    try { localStorage.setItem(KEY, JSON.stringify(choice)); } catch (e) {}
  }

  function loadMetaPixel() {
    if (!hasMarketing || window.fbq) return;
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = [];
      t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', CONFIG.metaPixelId);
    window.fbq('track', 'PageView');
    // Auf der Danke-Seite steht <body data-track="purchase">: Kauf an Meta melden.
    if (document.body.dataset.track === 'purchase') {
      window.fbq('track', 'Purchase', { value: 99.00, currency: 'EUR' });
    }
  }

  function loadAnalytics() {
    if (!hasStats || window.gtag) return;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(CONFIG.googleAnalyticsId);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', CONFIG.googleAnalyticsId, { anonymize_ip: true });
  }

  function apply(choice) {
    if (choice.marketing) loadMetaPixel();
    if (choice.stats) loadAnalytics();
  }

  function banner(current) {
    if (document.querySelector('.consent')) return;
    var box = document.createElement('div');
    box.className = 'consent';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-label', 'Cookie-Einstellungen');
    var opts = '';
    if (hasStats) {
      opts += '<label><input type="checkbox" id="consent-stats"' + (current && current.stats ? ' checked' : '') + '>' +
        '<span>Statistik<small>Google Analytics: hilft mir zu sehen, wie die Seite genutzt wird.</small></span></label>';
    }
    if (hasMarketing) {
      opts += '<label><input type="checkbox" id="consent-marketing"' + (current && current.marketing ? ' checked' : '') + '>' +
        '<span>Marketing<small>Meta Pixel: misst, ob meine Anzeigen auf Facebook und Instagram funktionieren.</small></span></label>';
    }
    box.innerHTML =
      '<h2>Kurz zu Cookies 🍪</h2>' +
      '<p>Notwendiges läuft immer. Alles andere nur, wenn du Ja sagst. Du kannst deine Wahl jederzeit unten auf der Seite unter „Cookie-Einstellungen“ ändern. Mehr dazu in der <a href="datenschutz.html">Datenschutzerklärung</a>.</p>' +
      '<div class="consent-opts">' +
        '<label><input type="checkbox" checked disabled><span>Notwendig<small>Speichert nur deine Auswahl hier.</small></span></label>' +
        opts +
      '</div>' +
      '<div class="consent-actions">' +
        '<button type="button" class="btn btn-ghost" data-c="necessary">Nur notwendige</button>' +
        '<button type="button" class="btn btn-ghost" data-c="save">Auswahl speichern</button>' +
        '<button type="button" class="btn" data-c="all">Alle akzeptieren</button>' +
      '</div>';
    document.body.appendChild(box);

    box.addEventListener('click', function (ev) {
      var action = ev.target.getAttribute('data-c');
      if (!action) return;
      var choice = { stats: false, marketing: false };
      if (action === 'all') choice = { stats: hasStats, marketing: hasMarketing };
      if (action === 'save') {
        var s = box.querySelector('#consent-stats');
        var m = box.querySelector('#consent-marketing');
        choice = { stats: !!(s && s.checked), marketing: !!(m && m.checked) };
      }
      var before = read();
      save(choice);
      box.remove();
      // Einwilligung zurückgezogen: neu laden, damit schon geladene Tools verschwinden.
      if (before && ((before.stats && !choice.stats) || (before.marketing && !choice.marketing))) {
        location.reload();
        return;
      }
      apply(choice);
    });
  }

  openers.forEach(function (el) {
    el.addEventListener('click', function () { banner(read()); });
  });

  var stored = read();
  if (stored) apply(stored); else banner(null);
})();
