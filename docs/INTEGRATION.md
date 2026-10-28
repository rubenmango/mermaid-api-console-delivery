# Integration — Mermaid API console (v3)

## Product source (private)

Implementing HTML / assets for eng live under:

**https://github.com/Mermaid-Chart/app-team/tree/main/handoffs/mermaid-api-console/src**

Public Pages package keeps only a stub at `src/README.md`.

## What this is

Static HTML prototype of the API console, customer and org admin (Coral / Storm dark shell), matching Figma customer `141:3891` and admin `206:12847`. Not wired to real Mermaid Chart auth or billing APIs yet. Every page is generated from one script and shares `console.css` + `console.js`.

## Suggested host wiring

| Concern | Prototype today | Product target |
|---|---|---|
| Entry | Chart header “API keys” button, account menu item, ⌘K results | Same three entries; deep-link to console routes |
| Auth | Fake “Log in with Mermaid Chart” → loading → Get started | Chart session / SSO |
| Role | User / Admin toggle in the top bar; workspace switcher in the Acme account menu | Role from the org membership; hide the toggle for non-admins |
| Keys | Once-shown dialog; row rename / revoke in the page | Create key API; show the secret once; never re-fetch |
| Agent prompt | Clipboard string in the page | Template with `MERMAID_API_KEY`, never the key |
| Usage / billing | Static numbers + Stripe dialog stub | Real balance, packs, Stripe Checkout return URL |
| Credits pill | Hard-coded per screen | Shared balance endpoint |
| Feedback | `window.toast(type, title)` + `data-toast`, `data-busy` | App toaster, if decision D3 is accepted |
| Motion | `@view-transition` + CSS keyframes; reduced-motion safe | Route transitions in the host framework |

## Screen map

| Screen | Live file | Figma node |
|---|---|---|
| Login · signing in | `login.html` · `login-loading.html` | `141:3927` · signing in `233:96981` |
| Get started · row menu | `get-started.html` · `get-started-menu.html` | `141:3955` |
| Keys + new key dialog | `keys.html` / `?new=1` | `141:4102` / `141:4076` |
| Key detail · filtered · empty · revoked | `key-detail*.html` | `141:4165` |
| Overview A / B | `overview-a.html` · `overview.html` | `141:4937` |
| Usage · free / org | `usage.html` · `usage-org.html` | `141:4367` · `141:4417` |
| Billing states | `billing*.html` (15 files) | `141:4459` → `141:4703` |
| Settings · menu | `settings.html` · `settings-menu.html` | `146:7494` |
| Admin overview · switcher | `admin-overview.html` · `admin-switcher.html` | `206:12847` |
| Admin keys · overrides · revoke | `admin-keys.html` · `admin-overrides.html` · `admin-revoke.html` | `206:12847` |
| Admin consumption · pool · burst · billing | `admin-consumption.html` · `admin-pool.html` · `admin-burst.html` · `admin-billing.html` | `206:12847` |
| Style guide | `styleguide.html` | Coral Foundations |

## Local preview (design repo)

From Unified-editor-Onboarding:

```bash
cd prototypes && python3 -m http.server 8765 --bind 127.0.0.1
open http://127.0.0.1:8765/mermaid-api-v3/
```

Chart app MasterBar points at `http://127.0.0.1:8765/mermaid-api-v3/login.html` while prototyping.
