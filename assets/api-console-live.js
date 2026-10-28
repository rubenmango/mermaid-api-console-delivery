(function () {
  var frame = document.getElementById("live-frame");
  var label = document.getElementById("live-label");
  var seeds = document.querySelectorAll("[data-live]");
  if (!frame || !seeds.length) return;

  function setActive(btn) {
    frame.src = btn.getAttribute("data-src");
    if (label) label.textContent = btn.textContent;
    seeds.forEach(function (b) {
      b.classList.toggle("active", b === btn);
    });
  }

  seeds.forEach(function (btn) {
    btn.addEventListener("click", function () {
      setActive(btn);
    });
  });
})();
