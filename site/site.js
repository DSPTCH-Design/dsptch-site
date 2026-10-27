(function () {
  // Mobile menu
  document.querySelectorAll(".menu-btn").forEach(function (b) {
    b.addEventListener("click", function () {
      var nav = b.closest(".nav");
      var open = nav.classList.toggle("open");
      b.setAttribute("aria-expanded", open ? "true" : "false");
      b.textContent = open ? "Close" : "Menu";
    });
  });

  // Work filters
  var grid = document.querySelector("[data-grid]");
  var fbtns = [].slice.call(document.querySelectorAll("[data-filter]"));
  function filter(f) {
    fbtns.forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.filter === f ? "true" : "false"); });
    if (!grid) return;
    var n = 0;
    [].forEach.call(grid.children, function (c) { c.hidden = !(f === "all" || c.dataset.type === f); if (!c.hidden) n++; });
    var cnt = document.querySelector("[data-count]");
    if (cnt) cnt.textContent = n + (n === 1 ? " project" : " projects");
  }
  var toHash = { website: "websites", creative: "creative", all: "all" };
  var fromHash = { websites: "website", creative: "creative", all: "all" };
  fbtns.forEach(function (b) {
    b.addEventListener("click", function () {
      filter(b.dataset.filter);
      try { history.replaceState(null, "", "#" + toHash[b.dataset.filter]); } catch (e) {}
    });
  });
  if (grid) filter(fromHash[(location.hash || "").slice(1)] || "website");

  // Query params (package / intent / ad source)
  var q = {};
  try { new URLSearchParams(location.search).forEach(function (v, k) { q[k] = v; }); } catch (e) {}
  var src = document.getElementById("source");
  if (src) src.value = [q.utm_source, q.utm_medium, q.utm_campaign].filter(Boolean).join(" / ") || document.referrer || "direct";
  var pkg = document.getElementById("package");
  if (pkg && q.package) pkg.value = q.package;

  // Start form: show the right questions for the chosen intent
  var form = document.querySelector("[data-intent-form]");
  if (form) {
    var sets = [].slice.call(form.querySelectorAll("[data-for]"));
    function show(intent) {
      sets.forEach(function (s) { s.hidden = s.dataset.for.split(" ").indexOf(intent) < 0; });
    }
    form.querySelectorAll('input[name="intent"]').forEach(function (r) {
      r.addEventListener("change", function () { show(r.value); });
    });
    if (q.intent) {
      var r = form.querySelector('input[name="intent"][value="' + q.intent + '"]');
      if (r) r.checked = true;
    }
    var cur = form.querySelector('input[name="intent"]:checked');
    show(cur ? cur.value : "website");
  }

  // Outside Netlify (local file or preview), forms go straight to the thank-you page
  var live = /netlify\.app$|dsptchdesign\.com$/.test(location.hostname);
  if (!live) {
    document.querySelectorAll("form[data-netlify]").forEach(function (f) {
      f.addEventListener("submit", function (ev) { ev.preventDefault(); location.href = "thanks.html"; });
    });
  }
})();
