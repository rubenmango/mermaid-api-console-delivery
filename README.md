# Mermaid API console — delivery

Password-gated designer → developer package for the API console: customer and org admin, v3.

| | |
|---|---|
| Notion-plain | `docs/notion-plain-docs.mdc` |
| Taste layer | `docs/ruben-taste-layer.mdc` |
| Figma | [Platform · customer `141:3891`](https://www.figma.com/design/SkEVtrAYLajpQjBeXLD5QU/Platform?node-id=141-3891) · [admin `206:12847`](https://www.figma.com/design/SkEVtrAYLajpQjBeXLD5QU/Platform?node-id=206-12847) · `FIGMA.md` |
| HTML delivery | `index.html` (slide) · [Pages](https://rubenmango.github.io/mermaid-api-console-delivery/) |
| Styles | `styles.html` (tokens, type, motion, components, live specimen) |
| Decisions & rules | `decisions.html` · `docs/DECISIONS.md` |
| Live | [`assets/live/`](https://rubenmango.github.io/mermaid-api-console-delivery/assets/live/) (password-gated) · seeds in `assets/api-console-live.js` |
| Screenshots | `assets/screenshots/` (27 frames + style guide) |
| Integration | `docs/INTEGRATION.md` |
| Product source | [`Mermaid-Chart/app-team` · `handoffs/mermaid-api-console/`](https://github.com/Mermaid-Chart/app-team/tree/main/handoffs/mermaid-api-console) |

## Local

Open `index.html` with any static server. Unlock with the shared Mermaid delivery password (told out-of-band, not in this README).

## Rebuild

`python3 tools/build.py` regenerates `index.html`, `styles.html` and `decisions.html` from the shot list and decision data in that script.

After copying HTML into `assets/live/`, run `python3 tools/protect_live.py` so every console page asks for the same password.
