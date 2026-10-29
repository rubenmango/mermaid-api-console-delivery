"""Inject the shared delivery password gate into every live prototype page.

The slide pages already load assets/gate.js. Direct /assets/live/*.html URLs
would otherwise bypass it. Same hash and storageKey as the rest of the package.
Run after copying HTML into assets/live/:  python3 tools/protect_live.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE = ROOT / "assets" / "live"
HASH = "756027fb4eb79a876aa00ee052d2876f8c10eb834930cf93e6810af1cb8d3432"
MARK = "DELIVERY_GATE"

HEAD = """<script>
(function(){try{if(localStorage.getItem('mc-delivery-gate-v1')==='ok')return;}catch(e){}document.documentElement.classList.add('dg-locked');})();
</script>
<style>html.dg-locked body > *:not(#delivery-gate){visibility:hidden}</style>
"""

BODY = f"""
<script>
window.DELIVERY_GATE = {{
  hash: "{HASH}",
  storageKey: "mc-delivery-gate-v1",
  title: "MERMAID · API CONSOLE"
}};
</script>
<script src="../gate.js"></script>
"""


def protect(path: Path) -> bool:
    html = path.read_text()
    if MARK in html:
        return False
    if "<head>" not in html or "<body" not in html:
        return False
    html = html.replace("<head>", "<head>\n" + HEAD, 1)
    html, n = re.subn(r"(<body[^>]*>)", r"\1" + BODY, html, count=1)
    if n != 1:
        return False
    path.write_text(html)
    return True


def main():
    n = 0
    for path in sorted(LIVE.glob("*.html")):
        if protect(path):
            n += 1
            print("gated", path.name)
        else:
            print("skip", path.name)
    print(f"gated {n} pages")


if __name__ == "__main__":
    main()
