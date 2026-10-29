"""Build the delivery pages: index.html (slide), styles.html, decisions.html.

Run from the package root:  python3 tools/build.py
Screenshots live in assets/screenshots/, the clickable console in assets/live/.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIGMA = "https://www.figma.com/design/SkEVtrAYLajpQjBeXLD5QU/Platform"
FIGMA_CUSTOMER = f"{FIGMA}?node-id=141-3891"
FIGMA_ADMIN = f"{FIGMA}?node-id=206-12847"
APP_TEAM = "https://github.com/Mermaid-Chart/app-team/tree/main/handoffs/mermaid-api-console"
GATE_HASH = "756027fb4eb79a876aa00ee052d2876f8c10eb834930cf93e6810af1cb8d3432"

# (file stem, title, caption)
SHOTS = [
    ("00a-chart-developer-mode", "Chart · account menu", "Developer mode"),
    ("00b-chart-dev-banner", "Chart · developer banner", "Create API keys and manage usage and credits"),
    ("00c-chart-search", "Chart · global search", "API keys, docs, usage results"),
    ("01-login", "Login", "Log in with Mermaid Chart"),
    ("02-login-loading", "Signing in", "Reef + jellyfish, what you can do here"),
    ("03-get-started", "Get started", "Agent prompt + manual steps"),
    ("04-new-key", "Your new key", "Secret shown once"),
    ("05-keys-row-menu", "Keys · row menu", "Rename, copy ID, revoke"),
    ("06-key-detail", "Key detail", "Chart, endpoints, recent calls"),
    ("07-key-detail-revoked", "Key detail · revoked", "Restore"),
    ("08-overview", "Overview · returning", "Expiry alert, API card, credits"),
    ("09-usage", "Usage · free plan", "Allowance + plan table"),
    ("10-usage-org", "Usage · org member", "Share of the pool"),
    ("11-billing", "Billing", "Balance, packs, limits"),
    ("12-billing-custom", "Billing · custom amount", "Multiples of 1,000"),
    ("13-billing-checkout", "Billing · Stripe Checkout", "Confirm dialog"),
    ("14-billing-success", "Billing · payment complete", "Success alert"),
    ("15-billing-autotopup", "Billing · auto top-up active", "Summary + Edit"),
    ("16-billing-purchases", "Billing · purchases", "API credit invoices"),
    ("17-settings", "Settings", "Email notifications"),
    ("18-admin-overview", "Admin · overview", "Org pool, members near limits"),
    ("19-admin-switcher", "Admin · workspace switcher", "Personal · Admin · Member"),
    ("20-admin-keys", "Admin · all keys", "Across the org"),
    ("21-admin-revoke", "Admin · revoke member keys", "Confirm dialog"),
    ("22-admin-consumption", "Admin · consumption", "By member and endpoint"),
    ("23-admin-pool", "Admin · credit pool", "Split by member, live totals"),
    ("24-admin-burst", "Admin · burst limits", "Org default + overrides"),
]
SHOT = {s: (i, t, c) for i, (s, t, c) in enumerate(SHOTS, 1)}


def src(stem):
    return f"./assets/screenshots/{stem}.png"


def anchor(stem):
    return f"#shot-{SHOT[stem][0]:02d}"


def head(title):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<!-- Docs chrome: Notion-plain (docs/notion-plain-docs.mdc) · judgement: docs/ruben-taste-layer.mdc · product UI: Figma Platform (system wins) -->
<script>
(function(){{try{{if(localStorage.getItem('mc-delivery-gate-v1')==='ok')return;}}catch(e){{}}document.documentElement.classList.add('dg-locked');}})();
</script>
<style>html.dg-locked body > *:not(#delivery-gate){{visibility:hidden}}</style>
<link rel="stylesheet" href="./assets/delivery.css" />
</head>
<body>
<script>
window.DELIVERY_GATE = {{
  hash: "{GATE_HASH}",
  storageKey: "mc-delivery-gate-v1",
  title: "MERMAID · API CONSOLE · DELIVERY"
}};
</script>
<script src="./assets/gate.js"></script>
<div class="wrap">"""


def topbar(active):
    def link(href, label, key):
        cur = ' aria-current="page" class="on"' if key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'

    return f"""
  <header class="topbar">
    <div class="topbar-left"><span class="logo" aria-hidden="true"></span> MERMAID · PLATFORM · DELIVERY</div>
    <div class="topbar-links">
      {link("./index.html", "Slide", "index")}
      {link("./styles.html", "Styles", "styles")}
      {link("./decisions.html", "Decisions &amp; rules", "decisions")}
      <a href="./docs/INTEGRATION.md">Integration</a>
      <a class="btn-primary" href="{FIGMA_CUSTOMER}" target="_blank" rel="noopener">Open Figma</a>
    </div>
  </header>"""


def foot(extra=""):
    return f"""
  <footer class="foot">
    Sources: Figma Platform customer <code>141:3891</code> and admin <code>206:12847</code> · handoff v3 · meeting Oct 27, 2026 (Knut, Ashish) · Ruben's design reviews. {extra}
  </footer>
</div>"""


def sec(num, sid, title, sub, body):
    return f"""
  <section id="{sid}">
    <div class="sec-head"><span class="sec-num">{num}</span><h2>{title}</h2></div>
    <p class="sec-sub">{sub}</p>
    {body}
  </section>"""


def dir_card(stem, kind, title, body, tag, tag_kind="holds"):
    return f"""<div class="dir-card {kind}">
        <a href="{anchor(stem)}"><img class="dir-shot" src="{src(stem)}" alt="" loading="lazy" /></a>
        <div class="dir-body"><h3>{title}</h3><p>{body}</p><span class="tag {tag_kind}">{tag}</span></div>
      </div>"""


def storyboard(stems, six=True):
    steps = "".join(
        f'<figure class="sb-step"><a href="{anchor(s)}"><img src="{src(s)}" alt="" loading="lazy" />'
        f'<figcaption><b><span class="sb-n">{n:02d}</span> {SHOT[s][1]}</b>{SHOT[s][2]}</figcaption></a></figure>'
        for n, s in enumerate(stems, 1)
    )
    return f'<div class="storyboard{" six" if six else ""}">{steps}</div>'


def film(stems):
    return '<div class="film">' + "".join(
        f'<a href="{anchor(s)}"><img src="{src(s)}" alt="" loading="lazy" /><span>{SHOT[s][1]}</span></a>' for s in stems
    ) + "</div>"


def cards(items, cols=""):
    """items: (title, [bullets]) — rule cards."""
    out = []
    for title, bullets in items:
        lis = "".join(f"<li>{b}</li>" for b in bullets)
        out.append(f'<div class="rule-card"><h3>{title}</h3><ul>{lis}</ul></div>')
    return f'<div class="rule-grid {cols}">{"".join(out)}</div>'


# ====================================================================== INDEX
LIVE_SEEDS = [
    ("login", "login.html", "Login"),
    ("get-started", "get-started.html", "Get started"),
    ("new-key", "keys.html?new=1", "New key"),
    ("overview", "overview.html", "Overview"),
    ("billing", "billing.html", "Billing"),
    ("usage", "usage.html", "Usage"),
    ("settings", "settings.html", "Settings"),
    ("admin", "admin-overview.html", "Admin"),
    ("admin-pool", "admin-pool.html", "Credit pool"),
    ("styleguide", "styleguide.html", "Style guide"),
]
seeds = "".join(
    f'<button type="button" data-live="{k}" data-src="./assets/live/{f}"{" class=\"active\"" if i == 0 else ""}>{label}</button>'
    for i, (k, f, label) in enumerate(LIVE_SEEDS)
)
gallery = "".join(
    f'<figure id="shot-{i:02d}"><h3>{i:02d} · {t}</h3><a href="{src(s)}" target="_blank" rel="noopener"><img class="shot" src="{src(s)}" alt="{t}" loading="lazy" /></a></figure>'
    for i, (s, t, c) in enumerate(SHOTS, 1)
)

index = head("Mermaid API console — Developer delivery") + topbar("index") + f"""
  <div class="pill-row">
    <span class="tag feature">API console</span>
    <span class="tag holds">Customer · v3</span>
    <span class="tag holds">Admin · v3</span>
    <span class="tag tweak">Motion + feedback</span>
  </div>
  <h1>Mermaid API console</h1>
  <p class="sub">Keys, usage and billing for the Mermaid API, inside the Mermaid Chart account. Entry from Developer mode in the Chart account menu, and from search. Customer and org-admin views share one dark Coral shell, switched from the top bar.</p>
  <div class="meta">
    <div><b>Figma</b>Platform · <code>141:3891</code> · <code>206:12847</code></div>
    <div><b>Status</b>Clickable HTML prototype</div>
    <div><b>Screens</b>42 live pages</div>
    <div><b>Product src</b><a href="{APP_TEAM}">app-team / handoffs</a></div>
  </div>

  <nav class="toc" aria-label="On this page">
    <a href="#stages">Stages</a><a href="#entry">Entry</a><a href="#roles">Roles</a><a href="#live">Live</a>
    <a href="#flows">Flows</a><a href="#motion">Motion</a><a href="#shots">Screenshots</a><a href="#spec">Spec</a>
    <a href="./styles.html">Styles →</a><a href="./decisions.html">Decisions &amp; rules →</a>
  </nav>

  <div class="callout">
    <strong>Chrome vs product.</strong> These pages use Notion-plain docs chrome. Everything inside Live and the screenshots follows the Figma Coral system: storm surfaces, one pink primary, deep-purple data.
  </div>
""" + sec("01", "stages", "Where this sits", "Both roles are prototyped. Wiring to real auth, balance and Stripe is next.", """
    <div class="stage-rail">
      <div class="stage-card"><span class="n">01</span><h3>Chart entry</h3><p class="where">Developer mode · banner · search</p></div>
      <div class="stage-card"><span class="n">02</span><h3>Login</h3><p class="where">Chart SSO · loading</p></div>
      <div class="stage-card you"><span class="n">03 · THIS PAGE</span><h3>Customer + admin console</h3><p class="where">Keys · usage · billing · org</p></div>
      <div class="stage-card"><span class="n">04</span><h3>Wire APIs</h3><p class="where">Keys · balance · Stripe</p></div>
      <div class="stage-card"><span class="n">05</span><h3>Super admin</h3><p class="where">Not designed · out of scope</p></div>
    </div>
    <div class="metric-grid">
      <div class="metric"><div class="num">42</div><div class="label">Live pages, customer and admin</div></div>
      <div class="metric"><div class="num">2</div><div class="label">Entry points from Mermaid Chart: Developer mode, search</div></div>
      <div class="metric"><div class="num">1×</div><div class="label">Key secret shown: the create dialog only</div></div>
    </div>""") + sec("02", "entry", "Entry from Mermaid Chart", "Figma Entry 0 → 0.1 → 0.2: Developer mode in the account menu turns on a banner on the dashboard; Create opens the console.", f"""
    <div class="dir-grid three">
      {dir_card("00a-chart-developer-mode", "pull", "1 · Developer mode", "Account menu, between Settings and Sign out. Toggles developer mode; remembered per user.", "Entry")}
      {dir_card("00b-chart-dev-banner", "push", "2 · Banner", "“Create API keys and manage usage and credits.” with Create, on top of the dashboard while developer mode is on. Slides in.", "Pick")}
      {dir_card("00c-chart-search", "pull", "3 · Global search", "Typing “API” shows API keys, docs, and usage and credits. Works with or without developer mode.", "Also")}
    </div>
    <figure class="motion-clip"><video src="./assets/motion/entry.webm" autoplay muted loop playsinline preload="metadata"></video><figcaption><b>Entry in motion</b> Account menu → Developer mode → banner slides in → ⌘K “API”.</figcaption></figure>""") + sec("03", "roles", "Two roles, one shell", "The User / Admin toggle in the top bar switches roles on every page. The account menu on Acme pages switches workspace.", f"""
    <div class="dir-grid">
      {dir_card("08-overview", "pull", "User", "Own keys, allowance, purchased credits, recent calls. Billing holds packs, auto top-up and limits.", "Customer · v3")}
      {dir_card("18-admin-overview", "push", "Org admin", "Org pool, members near their limits, all keys, overrides, consumption, credit pool split, burst limits.", "Admin · v3")}
    </div>""") + sec("04", "live", "Live console", "Share the live hub for the clickable prototype. Same password as this slide; every page is gated.", f"""
    <div class="live-meta"><span>Showing <b id="live-label">Login</b></span><span>Open full hub → <a href="./assets/live/index.html" target="_blank" rel="noopener">assets/live/</a></span></div>
    <div class="seeds" role="toolbar" aria-label="Screen seeds">{seeds}</div>
    <div class="live-frame-wrap"><iframe id="live-frame" title="Mermaid API console live" src="./assets/live/login.html"></iframe></div>""") + sec("05", "flows", "Storyboards", "Three journeys. Thumbs jump to full frames below.", f"""
    <h3 class="flow-h">First key</h3>
    {storyboard(["01-login", "02-login-loading", "03-get-started", "04-new-key", "05-keys-row-menu", "06-key-detail"])}
    <h3 class="flow-h">Spend</h3>
    {storyboard(["08-overview", "09-usage", "11-billing", "12-billing-custom", "13-billing-checkout", "14-billing-success"])}
    <h3 class="flow-h">Org admin</h3>
    {storyboard(["18-admin-overview", "19-admin-switcher", "20-admin-keys", "21-admin-revoke", "23-admin-pool", "24-admin-burst"])}
    {film(["07-key-detail-revoked", "10-usage-org", "15-billing-autotopup", "16-billing-purchases", "17-settings", "22-admin-consumption"])}""") + sec("06", "motion", "Motion and feedback", "Every action answers. Full tokens and live specimens are on the Styles page.", """
    <div class="metric-grid four">
      <div class="metric"><div class="num">280<small>ms</small></div><div class="label">Page cross-fade; sidebar and top bar stay put, nav pill and tabs slide</div></div>
      <div class="metric"><div class="num">520<small>ms</small></div><div class="label">Busy spinner before a toast or navigation</div></div>
      <div class="metric"><div class="num">30<small>ms</small></div><div class="label">Stagger on bars, sparks and page blocks</div></div>
      <div class="metric"><div class="num">16<small>s</small></div><div class="label">Login background zoom, 1 → 1.05</div></div>
    </div>
    <div class="motion-grid">
      <figure class="motion-clip"><video src="./assets/motion/login-flow.webm" autoplay muted loop playsinline preload="metadata"></video><figcaption><b>Login → Signing in → Get started</b> Copy softens, the screen dims, the card morphs, the reef brightens back and the jellyfish rise.</figcaption></figure>
      <figure class="motion-clip"><video src="./assets/motion/components.webm" autoplay muted loop playsinline preload="metadata"></video><figcaption><b>Components</b> Busy spinner → toast, pack picker, switches, row menu (spring), dialog in and out.</figcaption></figure>
    </div>
    <div class="callout">Feedback patterns: toasts for actions (copy, save, revoke, rename), inline alerts for balance and payment state, inline rename, row flash, empty filter rows, disabled Buy with a reason. <a href="./styles.html#motion">Motion tokens →</a></div>""") + sec("07", "shots", "Screenshots", "1440 × 900 frames from the live package. Click to open full size.", f"""
    <div class="grid two">{gallery}</div>""") + sec("08", "spec", "Spec · code", "Short bullets. The full list is on Decisions &amp; rules.", f"""
    <ul class="compact">
      <li><strong>Keys once</strong>: full secret only in the create dialog; masked everywhere else; no reveal.</li>
      <li><strong>Agent card</strong>: Copy prompt only; the prompt reads <code>MERMAID_API_KEY</code>.</li>
      <li><strong>Credits</strong>: allowance first, then one purchased pool; packs 5k / 10k / 15k / custom ×1,000.</li>
      <li><strong>Roles</strong>: members see their share, no admin actions; admins see names and last 4, never secrets.</li>
      <li><strong>Integrate</strong>: <a href="./docs/INTEGRATION.md">INTEGRATION.md</a> · product tree in <code>Mermaid-Chart/app-team/handoffs/mermaid-api-console/</code></li>
    </ul>""") + foot() + """
<script src="./assets/api-console-live.js"></script>
</body>
</html>
"""

# ====================================================================== STYLES
COLORS = [
    ("Surfaces", [("storm-975", "#18171C", "App, sidebar, top bar"), ("storm-950", "#1F1E24", "Cards"),
                  ("storm-900", "#242329", "Inputs, code blocks"), ("storm-850", "#2E2D34", "Hover tint, raised")]),
    ("Lines + text", [("storm-800", "#3A3944", "Hairlines, borders, bar track"), ("storm-700", "#504D60", "Selected nav pill, tab"),
                      ("storm-400", "#8585A4", "Descriptions, labels"), ("storm-200", "#C4C4D4", "Breadcrumb, muted"),
                      ("storm-50", "#F2F3F7", "Primary text")]),
    ("Brand + data", [("pink", "#E0095F", "Primary button, one per screen"), ("deep-300", "#7B72E9", "Plan allowance series"),
                      ("deep-200", "#B7B2F5", "Purchased series, focus ring")]),
    ("Status", [("green", "#4ADE80", "OK, Live, Active"), ("amber", "#F5A524", "Low, warning"),
                ("red", "#F05264", "Refused, danger"), ("blue", "#4EA1F5", "Info"), ("teal", "#A8DCD6", "Switch on")]),
    ("Alert surfaces", [("alert-warn-bg", "#461A01", "Warning fill · border #5F371E"), ("alert-ok-bg", "#1F3423", "Success fill · border #2A3A2F"),
                        ("alert-info-bg", "#1A3048", "Info fill · border #253A4D")]),
]
swatches = "".join(
    f'<div class="sw-group"><h3>{g}</h3>' + "".join(
        f'<div class="sw"><i style="background:{h}"></i><div><code>--{n}</code><span>{h} · {u}</span></div></div>' for n, h, u in items
    ) + "</div>"
    for g, items in COLORS
)
TYPE = [
    ("Page title", "24 / 600", "Billing"), ("Section number", "20 / 600", "250 credits available"),
    ("Body", "18 / 400", "Allowance first, then purchased credits."), ("Label, nav, table", "14 / 500", "Buy 5,000 credits for $5.00"),
    ("Note, card subtitle", "12 / 400", "Refused or failed calls cost 0 credits."), ("Code, keys", "JetBrains Mono 14", "mmd_0889••••••b574"),
]
type_rows = "".join(f'<tr><td>{a}</td><td><code>{b}</code></td><td class="ex">{c}</td></tr>' for a, b, c in TYPE)
MOTION = [
    ("--dur-1", "120 ms", "Hover, colour, button press (scale 0.97)"),
    ("--dur-2", "200 ms", "Popovers, nav icons, toasts"),
    ("--dur-3", "320 ms", "Modals in/out, reveal panels (grid rows 0fr → 1fr)"),
    ("--ease-out", "cubic-bezier(.22, 1, .36, 1)", "Default for everything that settles"),
    ("--ease-spring", "cubic-bezier(.34, 1.4, .64, 1)", "Menus, switch thumb, pack radio dot"),
    ("View transition", "280 ms", "Cross-document; sidebar + top bar fixed; nav pill, tab, mode toggle slide"),
    ("Content stagger", "fade-up 6 px, 40 ms steps", "Each block of .content on load"),
    ("Data", "grow x / grow y, 30 ms stagger", "Meters, share bars, chart bars, sparklines"),
    ("Count-up", "~600 ms", "Big numbers with data-count"),
    ("Login background", "16 s ease-out", "Zoom 1 → 1.05 behind the card; carries over into Signing in (no restart)"),
    ("Log in → Signing in", "0.9 s + 0.7 s", "Copy softens away, screen dims to 60%, card tints, card morphs (view transition), reef brightens back over 1.6 s"),
    ("Jellyfish", "pulse 5–7 s · glide 28–44 s", "Bell breathes (scale 1.045 / .955); one steady upward glide, never bobs back; far ones move less"),
    ("Reduced motion", "1 ms", "All of the above collapse to their end state"),
]
motion_rows = "".join(f"<tr><td><code>{a}</code></td><td><code>{b}</code></td><td>{c}</td></tr>" for a, b, c in MOTION)
COMPONENTS = [
    ("Sidebar", "184:11527 · admin 205:15830", "<AppSidebar role selected>"),
    ("Top bar", "18:3680", "<TopBar breadcrumb credits mode>"),
    ("Nav item", "182:13500", "<NavItem icon label href active>"),
    ("Account row + menu", "183:13724 · 108:36016", "<AccountSwitcher> → <AccountMenu>"),
    ("Button / Secondary", "175:11102", "<Button variant surface size>"),
    ("Switch", "175:11107", "<Switch checked> + reveal body"),
    ("Input / Stepper", "180:16052", "<NumberInput suffix> · <Stepper>"),
    ("Tabs (segmented)", "Coral Navigation / Tabs", "<SegmentedTabs>"),
    ("Alert / Note", "Coral library", "<Alert tone>"),
    ("Dialog", "Coral Dialog", "<Dialog> new key, Stripe, upgrade, revoke"),
    ("Row menu", "108:36016", "<DropdownMenu> per context"),
    ("Status badge", "Coral library", "<StatusBadge status>"),
    ("Pack card", "hand-built", "<PackPicker> with custom ×1,000"),
    ("Balance bar + legend", "hand-built", "<BalanceMeter plan purchased>"),
    ("Toast stack", "prototype only", "<Toaster> (see decision D3)"),
]
comp_cards = "".join(
    f'<div class="comp"><h3>{a}</h3><span class="node">{b}</span><code>{c}</code></div>' for a, b, c in COMPONENTS
)

styles = head("Mermaid API console — Styles") + topbar("styles") + f"""
  <div class="pill-row"><span class="tag feature">Styles</span><span class="tag holds">Coral · dark only</span><span class="tag tweak">Motion tokens</span></div>
  <h1>Styles</h1>
  <p class="sub">Tokens, type, components and motion for the API console. The specimen below renders from the same <code>console.css</code> and <code>console.js</code> as every screen, so what you click here is what ships.</p>
  <nav class="toc" aria-label="On this page">
    <a href="#specimen">Live specimen</a><a href="#colour">Colour</a><a href="#type">Type</a><a href="#space">Spacing + radius</a>
    <a href="#motion">Motion</a><a href="#components">Components</a><a href="#frame">Full frame</a>
  </nav>
  <div class="callout"><strong>Source of truth.</strong> Figma Coral Foundations for values; <code>assets/live/console.css</code> for how they're applied. When the two disagree, Figma wins and the CSS is the bug.</div>
""" + sec("01", "specimen", "Live specimen", "Click buttons for the busy spinner and toast, flip switches, open the dialog and the row menu.", """
    <div class="live-frame-wrap tall"><iframe title="Style guide specimen" src="./assets/live/styleguide.html" loading="lazy"></iframe></div>""") + sec("02", "colour", "Colour", "Dark mode only. Use tokens, never raw hex, in product code.", f"""
    <div class="sw-grid">{swatches}</div>""") + sec("03", "type", "Type", "Inter for UI, JetBrains Mono for keys and code. Title to description gap 8 px.", f"""
    <table class="spec"><thead><tr><th>Role</th><th>Size / weight</th><th>Example</th></tr></thead><tbody>{type_rows}</tbody></table>""") + sec("04", "space", "Spacing + radius", "4 px grid. These numbers come straight from the Figma shell spec.", """
    <div class="metric-grid four">
      <div class="metric"><div class="num">240</div><div class="label">Sidebar width</div></div>
      <div class="metric"><div class="num">60</div><div class="label">Top bar height</div></div>
      <div class="metric"><div class="num">24 / 16</div><div class="label">Content padding / gap between blocks</div></div>
      <div class="metric"><div class="num">8 / 6</div><div class="label">Card radius / inner radius</div></div>
      <div class="metric"><div class="num">36</div><div class="label">Nav item, button and input height</div></div>
      <div class="metric"><div class="num">48</div><div class="label">Inline card header height</div></div>
      <div class="metric"><div class="num">16</div><div class="label">Card body padding, title → subtitle gap</div></div>
      <div class="metric"><div class="num">1px</div><div class="label">storm-800 hairline everywhere</div></div>
    </div>""") + sec("05", "motion", "Motion", "Small, quick, and always answering a user action or a page change.", f"""
    <div class="motion-grid">
      <figure class="motion-clip"><video src="./assets/motion/components.webm" autoplay muted loop playsinline preload="metadata"></video><figcaption><b>Components</b> Busy spinner → toast, pack picker, switches, row menu, dialog.</figcaption></figure>
      <figure class="motion-clip"><video src="./assets/motion/login-flow.webm" autoplay muted loop playsinline preload="metadata"></video><figcaption><b>Login</b> Log in → Signing in (reef, jellyfish) → Get started.</figcaption></figure>
    </div>
    <table class="spec"><thead><tr><th>Token</th><th>Value</th><th>Use</th></tr></thead><tbody>{motion_rows}</tbody></table>""") + sec("06", "components", "Components", "Figma component → suggested code component.", f"""
    <div class="comp-grid">{comp_cards}</div>""") + sec("07", "frame", "Full frame", "The specimen as one image, for review without clicking.", f"""
    <a href="{src('25-styleguide')}" target="_blank" rel="noopener"><img class="shot" src="{src('25-styleguide')}" alt="Style guide" loading="lazy" /></a>""") + foot() + """
</body>
</html>
"""

# ====================================================================== DECISIONS
MEETING = [
    ("Entry is “API keys”", "In the main app and global search, not only buried in settings. Now delivered as Developer mode → banner (D10).", "00b-chart-dev-banner"),
    ("Keys shown once", "At creation only. No eye icon, no reveal later.", "04-new-key"),
    ("Agent prompt uses the env var", "<code>MERMAID_API_KEY</code>, never the raw key.", "03-get-started"),
    ("Flow removed from the header", "Top bar: breadcrumb, search, credits, Documentation.", "11-billing"),
    ("Reuse the Chart upgrade popup", "And the existing Stripe redirect.", "13-billing-checkout"),
    ("One purchased-credit pool", "Each purchase resets the pool expiry to 12 months (see open question 1).", "14-billing-success"),
]
meeting_cards = "".join(
    f'<div class="dec-card"><a href="./index.html{anchor(s)}"><img src="{src(s)}" alt="" loading="lazy" /></a>'
    f'<div class="dec-body"><span class="n">M{i}</span><h3>{t}</h3><p>{b}</p></div></div>'
    for i, (t, b, s) in enumerate(MEETING, 1)
)
REVIEW = [
    ("Low balance + auto top-up live on Billing only", "The dashboard Credits card shows the combined balance and Buy credits."),
    ("Get started never shows a key", "One-line agent card with Copy prompt; prompt text isn't displayed."),
    ("Settings through the account menu", "Opened from the avatar row at the bottom of the sidebar."),
    ("Breadcrumbs once, in the top bar", "No second breadcrumb in the page."),
    ("Data colours", "Plan series deep-300, purchased deep-200, track storm-800."),
    ("Account row full-bleed and square", "No side insets, radius 0, flush with the bottom."),
]
PROTO = [
    ("D1", "Admin · v3 built", "All admin frames are clickable: overview, all keys, overrides, revoke, consumption, credit pool, burst limits, plus a composed Billing.", "holds", "Shipped"),
    ("D2", "User / Admin toggle in the top bar", "Every page can switch role. The Acme account menu also switches workspace (Personal, Admin view, Member view).", "tweak", "Confirm with design"),
    ("D3", "Toasts for action feedback", "Copy, save, rename and revoke answer with a toast. Balance, expiry and payment states stay as inline alerts. The handoff says “Never Toasts”, so this needs a yes or no.", "blocked", "Needs decision"),
    ("D4", "Motion system", "View transitions between pages, staggered content, growing data, spring menus, reduced-motion safe.", "holds", "Shipped"),
    ("D5", "Header button uses a key icon", "Superseded by D10: the header button is gone.", "tweak", "Superseded"),
    ("D6", "Signing in is a scene", "Figma 233:96981: reef + rising jellyfish, three “what you can do here” bullets, about 3.6 s before Get started. Log in → Signing in is one continuous transition.", "holds", "Shipped"),
    ("D7", "Get started greets by first name", "“{first name}, let’s get started”, from the same source as the account menu.", "holds", "Shipped"),
    ("D8", "Admin Org pool is one line", "“10,640 credits available” with a pool / purchased bar, per Figma. The pack-expiry warning moved off the overview (still on admin Billing).", "tweak", "Confirm expiry hint"),
    ("D9", "Quieter alert surfaces", "Darker fills, low-contrast borders for warning, success and info, sampled from Figma.", "holds", "Shipped"),
    ("D10", "Entry is Developer mode → banner", "Figma Entry 0 / 0.1 / 0.2: account menu Developer mode turns on a dashboard banner with Create; search keeps API results. Replaces the header API keys button.", "holds", "Shipped"),
]
proto_cards = "".join(
    f'<div class="stage-card"><span class="n">{n}</span><h3>{t}</h3><p class="where">{b}</p><span class="tag {k}">{tag}</span></div>'
    for n, t, b, k, tag in PROTO
)
PRODUCT_RULES = [
    ("Keys", ["Full key once, right after creation; then masked <code>mmd_0889••••••b574</code>.", "Key emails never include the secret.",
              "Row menu: Rename, Copy key ID, Revoke key. Revoked keys show Restore.", "Revoked: calls are refused and cost 0 credits."]),
    ("Greeting", ["Get started heading uses the signed-in user’s first name: “{first name}, let’s get started” (e.g. “Ruben, let’s get started”).",
                  "Same name source as the account menu; never a hardcoded name."]),
    ("Agent prompt", ["Card: “Set up with your coding agent” · “Reads your key from MERMAID_API_KEY.”", "Button Copy prompt → Copied.",
                      "Manual setup: export the key, then one <code>curl</code> to <code>/v1/render</code>."]),
    ("Credits", ["Every plan has a monthly allowance; resets the 1st, 00:00 UTC; no rollover.", "Allowance first, then purchased credits.",
                 "Allowances shown: Free 25 · Basic 250 · Plus 1,000 · Premium 5,000 · Enterprise custom (to confirm)."]),
    ("Packs", ["5,000 / $5 · 10,000 / $10 · 15,000 / $15 · custom in multiples of 1,000.", "CTA follows the pack: “Buy 5,000 credits for $5.00”.",
               "Stripe Checkout: confirm → Stripe → back to Billing → Payment complete alert."]),
    ("Auto top-up", ["Off by default. On: buy when the balance falls under 500.", "Active: summary line + Edit.", "No saved card: Stripe saves one first."]),
    ("Limits", ["Spend limit caps purchased credits per month.", "Low-balance email default 25 credits (a tenth of the allowance).",
                "Off collapses the card to its header."]),
    ("Members vs admins", ["Members: own keys, their share, org usage; no admin actions.", "Admins: all keys, overrides, revoke, consumption, pool split, burst.",
                           "Admins see names and last 4 characters, never the secret."]),
    ("Recent calls", ["Filters: Status, Endpoint, Key (dashboard only).", "Empty filter: “No refused calls in the last 30 days.”",
                      "Refused or failed calls cost 0 credits."]),
    ("Purchases", ["Only API credit purchases. Columns: Date, Credits, Amount, Taken back, Buyer, Invoice.", "Empty: “No API credit purchases yet.”"]),
]
DESIGN_RULES = [
    ("Foundation", ["Coral Foundations + Iconography; tokens over raw values.", "Dark mode only.", "One pink primary per screen; everything else Secondary, Ghost or Link.",
                    "No explanatory notes inside screens. Short copy, one-line subtitles."]),
    ("Surfaces", ["App, sidebar, top bar storm-975. Cards storm-950 + 1px storm-800, radius 8.", "Hover storm-800 · selected pill storm-700."]),
    ("Card header", ["Inline by default, ~48 tall. With actions: subtitle 16 px after the title.", "Alone: subtitle pinned right.",
                     "Stacked only when the subtitle can't fit at 1024 wide.", "Bottom divider only when the card has a body."]),
    ("Shell", ["Sidebar 240: Dashboard · Access · Spend · Resources.", "Top bar 60: breadcrumb · search 360 × 32 · mode toggle · credits · Documentation.",
               "No avatar in the top bar; account row lives in the sidebar."]),
    ("Tables", ["Fixed column widths that match headers; numbers right-aligned.", "Equal row heights, 1px dividers.", "Actions and badges in fixed right columns."]),
    ("Controls", ["Buttons 36 and 32. Labels short; the main CTA keeps its amount.", "Billing tabs: outlined segmented pill, not underline.",
                  "Switch centred on the header row, 16 px from the right edge."]),
    ("Motion", ["Only for a user action or a page change. Nothing loops except the sign-in jellyfish (ambient, slow, always rising; still under reduced motion).", "Log in → Signing in is one scene: the copy softens away, the screen dims, the card morphs, then the reef brightens back (about 0.9s + 0.7s).", "120 / 200 / 320 ms; ease-out to settle, spring for menus.",
                "Respect prefers-reduced-motion everywhere."]),
    ("Feedback", ["Every action answers within 520 ms: spinner, then result.", "Destructive actions confirm in a dialog; the row then changes state and flashes.",
                  "Disabled buttons say why (“Choose a multiple of 1,000 credits”)."]),
]
ROADS = [
    ("Dual-column Get started with visible prompt", "Meeting pick: single agent row + Copy prompt."),
    ("Eye / reveal on key rows", "Secrets are one-shot only."),
    ("Separate API product home", "Entry must feel in-product from the Chart dashboard."),
    ("Toast for payment success", "Spec keeps a persistent alert on Billing."),
    ("Admin switch only in the account menu", "Hard to find on personal pages; added the top-bar toggle (D2)."),
    ("Plus icon on the header button", "Key icon reads as “API keys” at a glance (D5)."),
    ("Header API keys button", "Figma Entry moved the way in to Developer mode + dashboard banner (D10)."),
]
roads_cards = "".join(f'<div class="road"><h3>{a}</h3><p>{b}</p></div>' for a, b in ROADS)
OPEN = [
    ("Expiry model", "Single pool reset to 12 months vs per-pack expiry in some copy and emails. Knut."),
    ("Tier allowances", "Confirm Free 25 → Enterprise custom with Ashish and Knut."),
    ("Real upgrade popup", "Reuse the Chart popup + Stripe redirect; confirm the return to Billing."),
    ("Emails", "Nine templates to coordinate with Dom: sender, footer, which ship first."),
    ("Admin values", "/v1/generate and /v1/repair cost, burst values, split rule for new members, Billing admin-only?"),
    ("Coin icon", "Coral has none; pack cards borrow the database icon."),
    ("Auto top-up pack", "Can the user pick which pack auto top-up buys?"),
    ("Toasts (D3)", "Keep toasts for action feedback, or alerts only?"),
    ("Expiry hint on admin overview (D8)", "Figma drops the “4,000 shared credits expire Dec 2” warning. Keep a hint anywhere on the overview?"),
]
open_cards = "".join(f'<div class="q"><span class="n">Q{i}</span><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(OPEN, 1))

decisions = head("Mermaid API console — Decisions & rules") + topbar("decisions") + f"""
  <div class="pill-row"><span class="tag feature">Decisions</span><span class="tag holds">Rules</span><span class="tag blocked">{len(OPEN)} open questions</span></div>
  <h1>Decisions &amp; rules</h1>
  <p class="sub">What was decided, by whom, and the rules the screens follow. Meeting decisions are quoted from the Oct 27 review; prototype decisions are this delivery's calls and are marked when they need sign-off.</p>
  <nav class="toc" aria-label="On this page">
    <a href="#meeting">Meeting</a><a href="#reviews">Design reviews</a><a href="#prototype">Prototype calls</a>
    <a href="#product-rules">Product rules</a><a href="#design-rules">Design rules</a><a href="#roads">Roads not taken</a><a href="#open">Open questions</a>
  </nav>
""" + sec("01", "meeting", "Meeting decisions", "Oct 27, 2026 with Knut and Ashish. Click a frame to see it in the slide.", f"""
    <div class="dec-grid">{meeting_cards}</div>""") + sec("02", "reviews", "Design review decisions", "Ruben, same day.", cards([(t, [b]) for t, b in REVIEW], "three")) + sec("03", "prototype", "Prototype calls", "Made while building this delivery. D3 contradicts the handoff and needs an answer.", f"""
    <div class="stage-rail three">{proto_cards}</div>""") + sec("04", "product-rules", "Product rules", "How the console behaves. Strings are literal; copy deck lives in the handoff.", cards(PRODUCT_RULES, "three")) + sec("05", "design-rules", "Design rules", "How the screens are built. Values on the Styles page.", cards(DESIGN_RULES, "two") + '<p class="more"><a href="./styles.html">Tokens and specimens → Styles</a></p>') + sec("06", "roads", "Roads not taken", "And why.", f"""
    <div class="road-grid">{roads_cards}</div>""") + sec("07", "open", "Open questions", "Blocking final copy or engineering. Owner in each card.", f"""
    <div class="q-grid">{open_cards}</div>""") + foot() + """
</body>
</html>
"""

(ROOT / "index.html").write_text(index)
(ROOT / "styles.html").write_text(styles)
(ROOT / "decisions.html").write_text(decisions)
print("wrote index.html, styles.html, decisions.html ·", len(SHOTS), "shots")
