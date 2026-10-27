# Decisions — Mermaid API console (Non-admin · v3)

Figma: [Platform · `141:3891`](https://www.figma.com/design/SkEVtrAYLajpQjBeXLD5QU/Platform?node-id=141-3891)  
Handoff: `mermaid-api-console-handoff.md` (customer UI first; admin phase 2)

## Locked for v3

1. **Keys shown once.** Full secret only in the create-key modal. Get started never displays a key. Key detail / table show masked IDs only (no eye icon).
2. **Agent setup is a prompt card.** One-line “Set up with your coding agent” + **Copy prompt**. Prompt text is not shown on the page; clipboard payload includes env + render/validate/balance guidance.
3. **Entry from Chart.** API console opens from Mermaid Chart profile → Developer mode → API keys (same account). Login is Chart SSO, not a separate signup.
4. **Shell.** Grouped sidebar (Access / Spend / Resources), breadcrumb + search top bar, credits pill. No “Flow” in the top chrome.
5. **Credits model.** Plan allowance first, then purchased packs. Packs: 5k / 10k / 15k / custom (×1,000). Auto top-up, spend limit, low-balance email on Billing.
6. **Returning overview layout B** (`141:4937`): API card full width; left stack Credits → Top keys → Endpoints; tall Recent calls on the right.
7. **Alerts, not toasts** for balance / expiry / payment complete (inline alert banners).
8. **Admin · v3 deferred.** Customer screens ship first; admin remains on the prior v2 prototype until rebuilt.

## Roads not taken

| Idea | Why not |
|---|---|
| Dual-column Get started with visible prompt + “Create key and fill” | Meeting pick: single agent row + Copy prompt; key created elsewhere |
| Eye / reveal on key rows | Secrets are one-shot only |
| Separate API product home | Entry must feel in-product from Chart dashboard |
| Toast for payment success | Spec uses persistent alert on Billing |
| Shipping Admin · v3 in this package | Explicit phase 2 in the handoff |
