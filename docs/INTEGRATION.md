# Integration — Mermaid API console (v3)

## Product source (private)

Implementing HTML / assets for eng live under:

**https://github.com/Mermaid-Chart/app-team/tree/main/handoffs/mermaid-api-console/src**

Public Pages package keeps only a stub at `src/README.md`.

## What this is

Static HTML prototype of the **customer** API console (Coral / Storm dark shell), matching Figma Non-admin · v3. Not wired to real Mermaid Chart auth or billing APIs yet.

## Suggested host wiring

| Concern | Prototype today | Product target |
|---|---|---|
| Entry | Chart MasterBar → Developer mode → login URL | Same entry; deep-link to console route |
| Auth | Fake “Log in with Mermaid Chart” → Get started | Chart session / SSO |
| Keys | Local HTML + once-shown modal | Create key API; show secret once; never re-fetch |
| Agent prompt | Clipboard string in `console.js` / page | Server or client template with no key embedded until create |
| Usage / billing | Static numbers + Stripe modal stub | Real balance, packs, Stripe Checkout return URL |
| Credits pill | Hard-coded per screen | Shared balance endpoint |
| Admin | Not in v3 package | Separate admin surface (phase 2) |

## Screen map

| Screen | Live file | Figma node |
|---|---|---|
| Login | `login.html` | `141:3927` |
| Get started | `get-started.html` | `141:3955` |
| Keys + new key modal | `keys.html` / `?new=1` | `141:4102` / `141:4076` |
| Key detail | `key-detail.html` | `141:4165` |
| Overview (returning) | `overview.html` | `141:4937` |
| Usage · free | `usage.html` | `141:4367` |
| Usage · org | `usage-org.html` | `141:4417` |
| Billing | `billing.html` | `141:4459` |
| Payment complete | `billing-success.html` | `141:4703` |
| Purchases | `billing-purchases.html` | purchases tab |
| Settings | `settings.html` | `146:7494` |

## Local preview (design repo)

From Unified-editor-Onboarding:

```bash
cd prototypes && python3 -m http.server 8765 --bind 127.0.0.1
open http://127.0.0.1:8765/mermaid-api-v3/
```

Chart app MasterBar points at `http://127.0.0.1:8765/mermaid-api-v3/login.html` while prototyping.
