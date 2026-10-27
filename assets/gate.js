/**
 * Delivery package password gate (client-side only — obscurity, not real auth).
 * Config via window.DELIVERY_GATE before this script:
 *   { hash: sha256-hex of password, storageKey?: string, title?: string }
 */
(function () {
  var cfg = window.DELIVERY_GATE || {};
  var HASH = (cfg.hash || "").toLowerCase();
  var KEY = cfg.storageKey || "mc-delivery-gate-v1";
  var TITLE = cfg.title || "Mermaid · Delivery";

  function unlocked() {
    try {
      return localStorage.getItem(KEY) === "ok";
    } catch (e) {
      return false;
    }
  }

  function unlock() {
    try {
      localStorage.setItem(KEY, "ok");
    } catch (e) {}
    document.documentElement.classList.remove("dg-locked");
    var el = document.getElementById("delivery-gate");
    if (el) el.remove();
  }

  async function sha256Hex(text) {
    var data = new TextEncoder().encode(text);
    var buf = await crypto.subtle.digest("SHA-256", data);
    return Array.from(new Uint8Array(buf))
      .map(function (b) {
        return b.toString(16).padStart(2, "0");
      })
      .join("");
  }

  if (!HASH) return;
  if (unlocked()) {
    document.documentElement.classList.remove("dg-locked");
    return;
  }

  document.documentElement.classList.add("dg-locked");

  function mount() {
    if (document.getElementById("delivery-gate")) return;

    var style = document.createElement("style");
    style.textContent =
      "html.dg-locked body>*:not(#delivery-gate){display:none!important}" +
      "#delivery-gate{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;" +
      "background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;color:#37352F}" +
      "#delivery-gate .dg-card{width:min(360px,92vw);padding:28px 24px;border:1px solid #E9E9E7;border-radius:8px;background:#F7F6F3}" +
      "#delivery-gate .dg-kicker{font-size:12px;color:#9B9A97;font-weight:500;letter-spacing:.02em;margin:0 0 10px}" +
      "#delivery-gate h1{font-size:20px;margin:0 0 8px;letter-spacing:-.01em}" +
      "#delivery-gate p{margin:0 0 16px;font-size:14px;color:#787774;line-height:1.5}" +
      "#delivery-gate form{display:flex;flex-direction:column;gap:10px}" +
      "#delivery-gate input{height:36px;padding:0 12px;border:1px solid #E9E9E7;border-radius:6px;font:inherit;font-size:14px;background:#fff}" +
      "#delivery-gate input:focus{outline:2px solid rgba(91,79,196,.35);outline-offset:1px}" +
      "#delivery-gate button{height:36px;border:none;border-radius:6px;background:#37352F;color:#fff;font:inherit;font-size:13px;font-weight:500;cursor:pointer}" +
      "#delivery-gate button:hover{background:#000}" +
      "#delivery-gate .dg-err{font-size:13px;color:#C4554D;min-height:1.2em;margin:0}";

    var root = document.createElement("div");
    root.id = "delivery-gate";
    root.setAttribute("role", "dialog");
    root.setAttribute("aria-modal", "true");
    root.setAttribute("aria-label", "Password required");
    root.innerHTML =
      '<div class="dg-card">' +
      '<p class="dg-kicker">' +
      TITLE.replace(/</g, "&lt;") +
      "</p>" +
      "<h1>Password required</h1>" +
      "<p>This delivery package is shared privately. Enter the password to continue.</p>" +
      "<form>" +
      '<input type="password" name="password" autocomplete="current-password" placeholder="Password" required />' +
      '<button type="submit">Unlock</button>' +
      '<p class="dg-err" aria-live="polite"></p>' +
      "</form>" +
      "</div>";

    document.head.appendChild(style);
    document.body.appendChild(root);

    var form = root.querySelector("form");
    var input = root.querySelector('input[name="password"]');
    var err = root.querySelector(".dg-err");
    input.focus();

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      err.textContent = "";
      var value = input.value || "";
      sha256Hex(value)
        .then(function (hex) {
          if (hex === HASH) {
            unlock();
          } else {
            err.textContent = "Incorrect password.";
            input.select();
          }
        })
        .catch(function () {
          err.textContent = "Could not verify password in this browser.";
        });
    });
  }

  if (document.body) mount();
  else document.addEventListener("DOMContentLoaded", mount);
})();
