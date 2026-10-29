# Decisions — Mermaid API console (v3)

The visual version is `decisions.html`. This file mirrors it for reading in GitHub.

Figma: [Platform · customer `141:3891`](https://www.figma.com/design/SkEVtrAYLajpQjBeXLD5QU/Platform?node-id=141-3891) · [admin `206:12847`](https://www.figma.com/design/SkEVtrAYLajpQjBeXLD5QU/Platform?node-id=206-12847)
Handoff: `mermaid-api-console-handoff.md` (v3)

## Meeting decisions (Oct 27, 2026 · Knut, Ashish)

1. **Entry is “API keys”**: in the Chart header and global search, not only the account menu.
2. **Keys are shown once**: at creation, no eye icon, no reveal later.
3. **The agent prompt uses `MERMAID_API_KEY`**, never the raw key.
4. **Flow is removed from the header.**
5. **Upgrading reuses the Chart upgrade popup** and the Stripe redirect.
6. **One purchased-credit pool**: each purchase resets the expiry to 12 months (see open question 1).

## Design review decisions (Ruben, same day)

- Low balance and auto top-up settings live on Billing only. The dashboard Credits card shows the combined balance and Buy credits.
- Get started never shows a key. The agent card is one line with Copy prompt, and the prompt text isn't displayed.
- Settings is reached through the account menu at the bottom of the sidebar.
- Breadcrumbs appear once, in the top bar.
- Data colours: plan deep-300, purchased deep-200, track storm-800.
- Account row is full-bleed and square.

## Prototype calls (this delivery)

| # | Call | Status |
|---|---|---|
| D1 | Admin · v3 built: overview, all keys, overrides, revoke, consumption, credit pool, burst limits, composed Billing | Shipped |
| D2 | User / Admin toggle in the top bar on every page; Acme account menu switches workspace | Confirm with design |
| D3 | Toasts for action feedback (copy, save, rename, revoke); balance and payment states stay inline alerts. The handoff says “Never Toasts”. | **Needs decision** |
| D4 | Motion system: view transitions, stagger, growing data, spring menus, reduced-motion safe | Shipped |
| D5 | Header button uses a key icon | Shipped |
| D6 | Signing in is a scene (Figma `233:96981`): reef + rising jellyfish, “what you can do here” for ~3.6 s; Log in → Signing in is one continuous transition | Shipped |
| D7 | Get started greets by first name: “{first name}, let’s get started” (same source as the account menu) | Shipped |
| D8 | Admin Org pool is one line (“10,640 credits available”, pool / purchased bar); pack-expiry warning moved off the overview, still on admin Billing | Confirm expiry hint |
| D9 | Quieter alert surfaces: darker fills, low-contrast borders (warning, success, info) from Figma | Shipped |

## Rules

Product and design rules are listed in `decisions.html` (sections 04 and 05) and come from sections 4 and 7 of the handoff. Tokens and motion values are in `styles.html`.

## Roads not taken

| Idea | Why not |
|---|---|
| Dual-column Get started with a visible prompt | Meeting pick: single agent row + Copy prompt |
| Eye / reveal on key rows | Secrets are one-shot only |
| Separate API product home | Entry must feel in-product from Chart |
| Toast for payment success | Spec keeps a persistent alert on Billing |
| Admin switch only in the account menu | Hard to find from personal pages (D2) |
| Plus icon on the header button | Key icon reads as “API keys” (D5) |

## Open questions

1. Expiry model: single pool reset vs per-pack expiry in some copy and emails (Knut).
2. Tier allowances: Free 25 → Enterprise custom (Ashish, Knut).
3. Real upgrade popup: how it returns to Billing.
4. Emails: nine templates with Dom.
5. Admin values: `/v1/generate` and `/v1/repair` cost, burst values, split rule, Billing admin-only?
6. Coin icon: Coral has none.
7. Auto top-up pack: can the user choose it?
8. Toasts (D3): keep for action feedback, or alerts only?
9. Expiry hint (D8): keep any pack-expiry hint on the admin overview?
