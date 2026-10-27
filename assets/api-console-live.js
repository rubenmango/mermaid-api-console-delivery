(function () {
  var frame = document.getElementById("live-frame");
  var label = document.getElementById("live-label");
  var seeds = document.querySelectorAll("[data-live]");
  if (!frame || !seeds.length) return;

  var map = {
    "get-started": { src: "./assets/live/get-started.html", label: "Get started" },
    keys: { src: "./assets/live/keys.html", label: "Keys" },
    "new-key": { src: "./assets/live/keys.html?new=1", label: "Your new key" },
    overview: { src: "./assets/live/overview.html", label: "Overview · returning" },
    billing: { src: "./assets/live/billing.html", label: "Billing" },
    usage: { src: "./assets/live/usage.html", label: "Usage · free" },
    settings: { src: "./assets/live/settings.html", label: "Settings" },
    login: { src: "./assets/live/login.html", label: "Login" },
  };

  function setActive(key) {
    var item = map[key] || map["get-started"];
    frame.src = item.src;
    if (label) label.textContent = item.label;
    seeds.forEach(function (btn) {
      btn.classList.toggle("active", btn.getAttribute("data-live") === key);
    });
  }

  seeds.forEach(function (btn) {
    btn.addEventListener("click", function () {
      setActive(btn.getAttribute("data-live"));
    });
  });

  setActive("get-started");
})();
