(function () {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  const ICON = {
    success: '<svg viewBox="0 0 20 20" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.6" d="M10 17a7 7 0 1 0 0-14 7 7 0 0 0 0 14Zm-3-7 2 2 4-4"/></svg>',
    info: '<svg viewBox="0 0 20 20" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.6" d="M10 17a7 7 0 1 0 0-14 7 7 0 0 0 0 14Zm0-4V9.5m0-3h.01"/></svg>',
    warning: '<svg viewBox="0 0 20 20" aria-hidden="true"><path fill="currentColor" d="M10 2.5 18.5 17h-17L10 2.5Zm-.8 5.5v4.5h1.6V8H9.2Zm0 6v1.6h1.6V14H9.2Z"/></svg>',
    error: '<svg viewBox="0 0 20 20" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.6" d="M10 17a7 7 0 1 0 0-14 7 7 0 0 0 0 14Zm0-10.5V11m0 2.5h.01"/></svg>',
    check: '<svg width="16" height="16" viewBox="0 0 20 20" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" d="m5 10.5 3.2 3.2L15 7"/></svg>',
  };

  /* ---------- toast ---------- */
  let host;
  function toast(type, title) {
    if (!host) {
      host = document.createElement("div");
      host.className = "toasts";
      host.setAttribute("role", "status");
      host.setAttribute("aria-live", "polite");
      document.body.appendChild(host);
    }
    const t = document.createElement("div");
    t.className = "toast " + type;
    t.innerHTML = (ICON[type] || "") + "<span>" + title + "</span>";
    host.appendChild(t);
    setTimeout(() => {
      t.classList.add("leaving");
      t.addEventListener("animationend", () => t.remove(), { once: true });
    }, 2600);
  }
  window.toast = toast;

  /* ---------- popovers (account, kebab) ---------- */
  const closeAll = (except) =>
    $$(".popover.open").forEach((p) => {
      if (p === except) return;
      p.classList.remove("open");
      const trig = $(`[aria-controls="${p.id}"]`);
      if (trig) trig.setAttribute("aria-expanded", "false");
    });
  const account = $("#account");
  const menu = $("#account-menu");
  if (account && menu) {
    account.setAttribute("aria-controls", "account-menu");
    account.addEventListener("click", (e) => {
      e.stopPropagation();
      closeAll(menu);
      const open = menu.classList.toggle("open");
      account.setAttribute("aria-expanded", String(open));
    });
  }
  $$("[data-kebab]").forEach((btn) => {
    const m = document.getElementById(btn.dataset.kebab);
    btn.setAttribute("aria-controls", m.id);
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      closeAll(m);
      btn.setAttribute("aria-expanded", String(m.classList.toggle("open")));
    });
  });
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".popover")) closeAll();
  });
  $$(".popover").forEach((p) =>
    p.addEventListener("click", (e) => {
      const b = e.target.closest("button[data-toast]");
      if (b) closeAll();
    })
  );

  /* ---------- modals ---------- */
  function openModal(id) {
    const m = document.getElementById(id);
    if (!m) return;
    m.classList.remove("closing");
    m.hidden = false;
    const f = m.querySelector("[autofocus], input, .btn.primary, .btn.light, .btn.danger");
    if (f) setTimeout(() => f.focus(), 30);
  }
  function closeModal(m) {
    if (!m || m.hidden) return;
    if (reduced) { m.hidden = true; m.dispatchEvent(new Event("closed")); return; }
    m.classList.add("closing");
    m.addEventListener(
      "animationend",
      () => {
        m.hidden = true;
        m.classList.remove("closing");
        m.dispatchEvent(new Event("closed"));
      },
      { once: true }
    );
  }
  window.openModal = openModal;
  window.closeModal = closeModal;
  $$("[data-open]").forEach((b) =>
    b.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      closeAll();
      openModal(b.dataset.open);
    })
  );
  $$(".overlay").forEach((o) => {
    o.addEventListener("click", (e) => {
      if (e.target === o || e.target.closest("[data-close]")) closeModal(o);
    });
  });
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    const o = $$(".overlay").find((x) => !x.hidden);
    if (o) closeModal(o);
    else closeAll();
  });

  /* ---------- feedback buttons ---------- */
  function busy(btn, ms, done) {
    btn.classList.add("busy");
    btn.disabled = true;
    setTimeout(() => {
      btn.classList.remove("busy");
      btn.disabled = false;
      done && done();
    }, ms);
  }
  window.busy = busy;
  $$("[data-toast]").forEach((b) =>
    b.addEventListener("click", (e) => {
      if (b.closest(".popover")) {
        const [type, msg] = b.dataset.toast.split("|");
        toast(type, msg);
        return;
      }
      e.preventDefault();
      const [type, msg] = b.dataset.toast.split("|");
      busy(b, 520, () => {
        toast(type, msg);
        $$(".cell-input.dirty").forEach((i) => i.classList.remove("dirty"));
        const m = b.closest(".overlay");
        if (m) closeModal(m);
      });
    })
  );
  $$("a[data-busy]").forEach((a) =>
    a.addEventListener("click", (e) => {
      e.preventDefault();
      busy(a, 700, () => (location.href = a.href));
    })
  );
  $$(".cell-input, .field-row input").forEach((i) => {
    const init = i.value;
    i.addEventListener("input", () => i.classList.toggle("dirty", i.value !== init));
  });

  /* ---------- copy ---------- */
  $$("[data-copy]").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.stopPropagation();
      try { await navigator.clipboard.writeText(btn.dataset.copy); } catch (_) {}
      const prev = btn.innerHTML;
      if (btn.dataset.copiedLabel) {
        btn.innerHTML = ICON.check + " " + btn.dataset.copiedLabel;
      } else {
        btn.innerHTML = ICON.check;
      }
      btn.classList.add("done");
      if (btn.dataset.copyToast) toast("success", btn.dataset.copyToast);
      clearTimeout(btn._t);
      btn._t = setTimeout(() => {
        btn.innerHTML = prev;
        btn.classList.remove("done");
      }, 1800);
    });
  });

  /* ---------- rows ---------- */
  $$("tr.key-row[data-href]").forEach((row) =>
    row.addEventListener("click", (e) => {
      if (e.target.closest("[data-no-row-nav], a, button, input, select")) return;
      location.href = row.dataset.href;
    })
  );

  $$("[data-row-revoke]").forEach((b) =>
    b.addEventListener("click", () => {
      closeAll();
      const tr = b.closest("tr");
      const st = tr.querySelector("[data-state]");
      if (st) st.innerHTML = '<span class="pill revoked">Revoked</span>';
      tr.classList.add("dimmed", "flash");
      b.disabled = true;
      toast("success", "Key revoked — calls are refused and cost 0");
    })
  );
  $$("[data-row-rename]").forEach((b) =>
    b.addEventListener("click", () => {
      closeAll();
      const cell = b.closest("tr").querySelector("[data-name]");
      const prev = cell.textContent;
      cell.innerHTML = "";
      const inp = document.createElement("input");
      inp.className = "cell-input wide";
      inp.value = prev;
      cell.appendChild(inp);
      inp.focus();
      inp.select();
      const commit = (save) => {
        const v = save ? inp.value.trim() || prev : prev;
        cell.textContent = v;
        if (save && v !== prev) { cell.closest("tr").classList.add("flash"); toast("success", "Renamed to “" + v + "”"); }
      };
      inp.addEventListener("click", (e) => e.stopPropagation());
      inp.addEventListener("keydown", (e) => {
        if (e.key === "Enter") commit(true);
        if (e.key === "Escape") { e.stopPropagation(); commit(false); }
      });
      inp.addEventListener("blur", () => cell.contains(inp) && commit(true));
    })
  );
  $$("[data-row-remove]").forEach((b) =>
    b.addEventListener("click", () => {
      const tr = b.closest("tr");
      tr.classList.add("leaving");
      tr.addEventListener("animationend", () => tr.remove(), { once: true });
      toast("success", "Override removed");
    })
  );

  /* ---------- switches + reveal ---------- */
  $$(".reveal").forEach((r) => (r.inert = !r.classList.contains("open")));
  $$(".switch").forEach((sw) =>
    sw.addEventListener("click", () => {
      const on = sw.getAttribute("aria-pressed") !== "true";
      sw.setAttribute("aria-pressed", String(on));
      const card = sw.closest(".card");
      const reveal = card && card.querySelector(":scope > .reveal");
      if (reveal) {
        reveal.classList.toggle("open", on);
        reveal.inert = !on;
      }
      if (sw.dataset.toggleToast) toast(on ? "success" : "info", sw.dataset.toggleToast.split("|")[on ? 0 : 1]);
      if (card && card.dataset.autotopup !== undefined && !on) showTopup(card, "form");
    })
  );

  function showTopup(card, which) {
    const form = card.querySelector("[data-topup-form]");
    const active = card.querySelector("[data-topup-active]");
    if (!form || !active) return;
    form.hidden = which !== "form";
    active.hidden = which !== "active";
    (which === "form" ? form : active).classList.remove("swap-in");
    void (which === "form" ? form : active).offsetWidth;
    (which === "form" ? form : active).classList.add("swap-in");
  }
  $$("[data-autotopup]").forEach((card) => {
    const on = card.querySelector("[data-topup-on]");
    const edit = card.querySelector("[data-topup-edit]");
    const sel = () => card.querySelector(".pack[aria-pressed=true]");
    on && on.addEventListener("click", () =>
      busy(on, 600, () => {
        const p = sel();
        const th = card.querySelector("[data-topup-threshold]").value || "500";
        const sum = card.querySelector("[data-topup-summary]");
        if (p && sum) sum.textContent = `Buys ${p.dataset.amt} credits (${p.dataset.price}) on your saved card when the balance falls under ${th}.`;
        showTopup(card, "active");
        toast("success", "Auto top-up is on");
      })
    );
    edit && edit.addEventListener("click", () => showTopup(card, "form"));
  });

  /* ---------- packs ---------- */
  const fmt = (n) => n.toLocaleString("en-US");
  $$(".packs").forEach((packs) => {
    const buy = packs.dataset.buy ? document.getElementById(packs.dataset.buy) : null;
    const ext = buy ? buy.querySelector("svg")?.outerHTML || "" : "";
    const update = () => {
      const p = packs.querySelector(".pack[aria-pressed=true]");
      if (!p) return;
      if (p.dataset.pack === "custom") {
        const inp = p.querySelector("input");
        const n = Number((inp.value || "0").replace(/[^\d]/g, "")) || 0;
        p.dataset.amt = fmt(n);
        p.dataset.price = "$" + (n / 1000).toFixed(2);
        const ok = n >= 1000 && n % 1000 === 0;
        p.querySelector(".stepper").classList.toggle("invalid", !ok);
        if (buy) {
          buy.disabled = !ok;
          buy.innerHTML = ok ? `Buy ${fmt(n)} credits for $${(n / 1000).toFixed(2)} ${ext}` : "Choose a multiple of 1,000 credits";
        }
      } else if (buy) {
        p.querySelector(".stepper")?.classList.remove("invalid");
        buy.disabled = false;
        buy.innerHTML = `Buy ${p.dataset.amt} credits for ${p.dataset.price} ${ext}`;
      }
      if (buy) {
        const a = $("#stripe-amt"), pr = $("#stripe-price");
        if (a) a.textContent = p.dataset.amt;
        if (pr) pr.textContent = p.dataset.price;
      }
    };
    packs.addEventListener("click", (e) => {
      const p = e.target.closest(".pack");
      if (!p) return;
      packs.querySelectorAll(".pack").forEach((x) => x.setAttribute("aria-pressed", String(x === p)));
      if (p.dataset.pack === "custom" && !e.target.closest("input, .arrows")) p.querySelector("input").focus();
      update();
    });
    packs.addEventListener("input", (e) => {
      const p = e.target.closest(".pack");
      if (!p) return;
      packs.querySelectorAll(".pack").forEach((x) => x.setAttribute("aria-pressed", String(x === p)));
      update();
    });
    packs.querySelectorAll(".arrows button").forEach((b) =>
      b.addEventListener("click", (e) => {
        e.stopPropagation();
        const inp = b.closest(".stepper").querySelector("input");
        const n = Number(inp.value.replace(/[^\d]/g, "")) || 0;
        inp.value = fmt(Math.max(1000, n + (b.dataset.step === "up" ? 1000 : -1000)));
        inp.dispatchEvent(new Event("input", { bubbles: true }));
      })
    );
    update();
  });

  /* ---------- filters ---------- */
  $$("[data-filter-table]").forEach((sel) => {
    const table = document.getElementById(sel.dataset.filterTable);
    const key = sel.dataset.filterKey;
    const run = () => {
      const v = sel.value;
      let shown = 0;
      table.querySelectorAll("tbody tr[data-" + key + "]").forEach((tr) => {
        const match = v === "all" || tr.dataset[key] === v;
        tr.hidden = !match;
        if (match) shown++;
      });
      const empty = table.querySelector("tr.empty-row");
      if (empty) {
        empty.hidden = shown > 0;
        const label = sel.options[sel.selectedIndex].dataset.word || v;
        empty.querySelector("td").textContent = `No ${label} calls in the last 30 days.`;
      }
      table.querySelectorAll("tbody tr:not([hidden])").forEach((tr, i) => {
        tr.style.animation = "none";
        void tr.offsetWidth;
        tr.style.animation = `fade-up 0.3s var(--ease-out) ${i * 25}ms both`;
      });
    };
    sel.addEventListener("change", run);
    run();
  });

  /* ---------- chart range chips ---------- */
  $$("[data-range]").forEach((group) => {
    const bars = document.getElementById(group.dataset.range);
    const all = JSON.parse(bars.dataset.series);
    group.addEventListener("click", (e) => {
      const c = e.target.closest(".chip");
      if (!c) return;
      group.querySelectorAll(".chip").forEach((x) => x.setAttribute("aria-pressed", String(x === c)));
      const n = Number(c.dataset.n);
      const data = all.slice(-n);
      const max = Math.max(...data);
      bars.innerHTML = data.map((h) => `<i style="height:${Math.round((h / max) * 100)}%" title="${h} credits"></i>`).join("");
    });
  });

  /* ---------- count up ---------- */
  if (!reduced) {
    $$("[data-count]").forEach((el) => {
      const target = Number(el.dataset.count);
      if (!target) return;
      const text = el.firstChild;
      const t0 = performance.now();
      const dur = 700;
      const step = (t) => {
        const k = Math.min(1, (t - t0) / dur);
        const e = 1 - Math.pow(1 - k, 3);
        text.nodeValue = fmt(Math.round(target * e)) + " ";
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    });
  }

  /* ---------- dismissible alerts ---------- */
  $$(".alert .x").forEach((x) =>
    x.addEventListener("click", () => {
      const a = x.closest(".alert");
      a.classList.add("leaving");
      a.addEventListener("animationend", () => a.remove(), { once: true });
    })
  );

  /* ---------- search ---------- */
  const PAGES = document.body.dataset.mode === "admin"
    ? [
        ["Dashboard", "admin-overview.html", "Admin"],
        ["All keys", "admin-keys.html", "Keys"],
        ["Overrides", "admin-overrides.html", "Keys"],
        ["Consumption", "admin-consumption.html", "Spend"],
        ["Billing", "admin-billing.html", "Spend"],
        ["Credit pool", "admin-pool.html", "Spend"],
        ["Burst limits", "admin-burst.html", "Spend"],
        ["Member view", "usage-org.html", "Switch"],
        ["Personal", "overview.html", "Switch"],
      ]
    : [
        ["Dashboard", "overview.html", "Overview"],
        ["Get started", "get-started.html", "Dashboard"],
        ["API keys", "keys.html", "Access"],
        ["Create key", "keys.html?new=1", "Access"],
        ["CI render bot", "key-detail.html", "Key"],
        ["Usage", "usage.html", "Spend"],
        ["Billing", "billing.html", "Spend"],
        ["Buy credits", "billing.html", "Billing"],
        ["Auto top-up", "billing-autotopup-on.html", "Billing"],
        ["Purchases", "billing-purchases.html", "Billing"],
        ["Email notifications", "settings.html", "Settings"],
        ["Acme Inc · Admin view", "admin-overview.html", "Switch"],
      ];
  const input = $(".search input");
  if (input) {
    const wrap = input.closest(".search-wrap");
    const box = document.createElement("div");
    box.className = "popover search-results";
    box.id = "search-results";
    wrap.appendChild(box);
    let hl = 0;
    const render = () => {
      const q = input.value.trim().toLowerCase();
      const res = PAGES.filter(([t, , g]) => !q || t.toLowerCase().includes(q) || g.toLowerCase().includes(q)).slice(0, 8);
      hl = Math.min(hl, Math.max(0, res.length - 1));
      box.innerHTML = res.length
        ? res.map(([t, h, g], i) => `<a href="${h}"${i === hl ? ' class="hl"' : ""}>${t}<span>${g}</span></a>`).join("")
        : '<div class="none">No results</div>';
    };
    input.addEventListener("focus", () => { render(); closeAll(box); box.classList.add("open"); });
    input.addEventListener("input", () => { hl = 0; render(); });
    input.addEventListener("keydown", (e) => {
      const links = $$("a", box);
      if (e.key === "ArrowDown") { hl = Math.min(links.length - 1, hl + 1); render(); e.preventDefault(); }
      if (e.key === "ArrowUp") { hl = Math.max(0, hl - 1); render(); e.preventDefault(); }
      if (e.key === "Enter" && links[hl]) location.href = links[hl].href;
      if (e.key === "Escape") { box.classList.remove("open"); input.blur(); }
    });
    input.addEventListener("blur", () => setTimeout(() => box.classList.remove("open"), 120));
    document.addEventListener("keydown", (e) => {
      if ((e.key === "k" && (e.metaKey || e.ctrlKey)) || (e.key === "/" && !/input|textarea|select/i.test(document.activeElement.tagName))) {
        e.preventDefault();
        input.focus();
      }
    });
  }
})();
