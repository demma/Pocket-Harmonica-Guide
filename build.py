"""Gera index.html (o app instalável) a partir de app.html. Uso: python3 build.py

- app.html é a fonte única: abre direto no navegador para testar e serve de prévia.
- O nome e a cor vêm de manifest.webmanifest; a versão, de APP_VERSION em app.html.
- O nome do cache offline em sw.js é atualizado com a versão: sem isso o celular
  pode continuar mostrando a versão antiga.
"""
import json
import re
from pathlib import Path

root = Path(__file__).parent
app = (root / "app.html").read_text(encoding="utf-8")
manifest = json.loads((root / "manifest.webmanifest").read_text(encoding="utf-8"))
m = re.search(r"var APP_VERSION\s*=\s*'([^']+)'", app)
if not m:
    raise SystemExit("app.html precisa de var APP_VERSION='x.y.z'")
version = m.group(1)
slug = re.sub(r"[^a-z0-9]+", "-", manifest.get("short_name", "app").lower()).strip("-")

head = f"""<!doctype html>
<html lang="{manifest.get('lang', 'pt-BR')}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="{manifest.get('theme_color', '#111111')}">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="{manifest.get('short_name', 'App')}">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icons/icon-180.png?v={version}">
</head>
<body>
"""
tail = """
<script>
// iOS, app na tela inicial com barra de status translúcida: a janela informada é mais curta
// que a tela (falta a barra de status). Estica o contêiner .app até a altura física.
(function () {
  var app = document.querySelector('.app');
  if (!app) return;
  function fit() {
    var standalone = navigator.standalone || (window.matchMedia && matchMedia('(display-mode: standalone)').matches);
    var portrait = !window.matchMedia || matchMedia('(orientation: portrait)').matches;
    var sh = portrait ? Math.max(screen.width, screen.height) : Math.min(screen.width, screen.height);
    if (standalone && sh > window.innerHeight + 1) { app.style.bottom = 'auto'; app.style.height = sh + 'px'; }
    else { app.style.bottom = ''; app.style.height = ''; }
  }
  fit();
  window.addEventListener('resize', fit);
  window.addEventListener('orientationchange', function () { setTimeout(fit, 300); });
})();
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function () { navigator.serviceWorker.register('sw.js').catch(function () {}); });
}
</script>
</body>
</html>
"""
(root / "index.html").write_text(head + app + tail, encoding="utf-8")
sw = (root / "sw.js").read_text(encoding="utf-8")
sw = re.sub(r"const CACHE = '[^']*';", f"const CACHE = '{slug}-{version}';", sw)
(root / "sw.js").write_text(sw, encoding="utf-8")
print(f"index.html gerado · versão {version} · cache {slug}-{version}")
