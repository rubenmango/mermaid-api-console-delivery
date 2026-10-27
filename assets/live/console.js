(function () {
  const account = document.getElementById("account");
  const menu = document.getElementById("account-menu");
  if (account && menu) {
    account.addEventListener("click", (e) => {
      e.stopPropagation();
      const open = menu.classList.toggle("open");
      account.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("click", () => {
      menu.classList.remove("open");
      account.setAttribute("aria-expanded", "false");
    });
    menu.addEventListener("click", (e) => e.stopPropagation());
  }
  document.querySelectorAll("[data-kebab]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const m = document.getElementById(btn.getAttribute("data-kebab"));
      document.querySelectorAll(".kebab-menu.open").forEach((x) => {
        if (x !== m) x.classList.remove("open");
      });
      m.classList.toggle("open");
    });
  });
  document.addEventListener("click", () =>
    document.querySelectorAll(".kebab-menu.open").forEach((x) => x.classList.remove("open"))
  );
  document.querySelectorAll("tr.key-row[data-href]").forEach((row) => {
    row.addEventListener("click", (e) => {
      if (e.target.closest("[data-no-row-nav], a, button")) return;
      location.href = row.getAttribute("data-href");
    });
  });
  document.querySelectorAll("[data-copy]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(btn.getAttribute("data-copy"));
        const label = btn.dataset.copiedLabel;
        if (!label) return;
        const prev = btn.innerHTML;
        btn.textContent = label;
        setTimeout(() => {
          btn.innerHTML = prev;
        }, 1600);
      } catch (_) {}
    });
  });
  document.querySelectorAll(".switch").forEach((btn) => {
    btn.addEventListener("click", () => {
      const on = btn.getAttribute("aria-pressed") !== "true";
      btn.setAttribute("aria-pressed", String(on));
      const body = btn.closest(".card")?.querySelector("[data-toggle-body]");
      if (body) body.hidden = !on;
    });
  });
})();
