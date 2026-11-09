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
  if (pkg && (q.package || q.plan)) pkg.value = q.package || q.plan;

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


  // UTM fields (free homepage form)
  document.querySelectorAll("[data-utm]").forEach(function (i) { i.value = q[i.dataset.utm] || ""; });

  // Package buttons on the landing page remember the choice
  document.querySelectorAll("[data-pkg]").forEach(function (a) {
    a.addEventListener("click", function () { var i = document.getElementById("pkg-interest"); if (i) i.value = a.dataset.pkg; });
  });

  // Multi-step form with Meta events at each step
  var track = function (ev, custom) { try { if (window.fbq) window.fbq(custom ? "trackCustom" : "track", ev); } catch (e) {} };
  document.querySelectorAll("form[data-steps]").forEach(function (f) {
    var steps = [].slice.call(f.querySelectorAll("[data-step]"));
    var bars = [].slice.call(f.querySelectorAll(".progress i"));
    var back = f.querySelector("[data-back]"), next = f.querySelector("[data-next]"), send = f.querySelector("[data-send]");
    var err = f.querySelector(".step-err");
    var cur = 0, started = false;
    var nosite = f.querySelector("[data-nosite]"), url = f.querySelector("#fh-url");
    if (nosite && url) nosite.addEventListener("change", function () {
      url.disabled = nosite.checked; url.required = !nosite.checked; if (nosite.checked) url.value = "";
    });
    f.addEventListener("input", function () { if (!started) { started = true; track("FormStart", true); track("InitiateCheckout"); } }, true);
    function valid(i) {
      var ok = true;
      steps[i].querySelectorAll("input,select,textarea").forEach(function (el) {
        if (!el.checkValidity()) ok = false;
      });
      return ok;
    }
    function go(i) {
      cur = i;
      steps.forEach(function (s, k) { s.hidden = k !== i; });
      bars.forEach(function (b, k) { b.classList.toggle("on", k <= i); });
      back.hidden = i === 0; next.hidden = i === steps.length - 1; send.hidden = i !== steps.length - 1;
      err.hidden = true;
    }
    function check() {
      if (valid(cur)) return true;
      err.hidden = false;
      var bad = steps[cur].querySelector(":invalid"); if (bad) bad.focus();
      return false;
    }
    next.addEventListener("click", function () {
      if (!check()) return;
      if (cur === 1) track("FormStep2", true);
      go(cur + 1);
      var top = f.getBoundingClientRect().top + window.scrollY - 24;
      if (window.scrollY > top) window.scrollTo({ top: top, behavior: "smooth" });
    });
    back.addEventListener("click", function () { go(cur - 1); });
    f.addEventListener("submit", function (ev) {
      if (!check()) { ev.preventDefault(); return; }
      f.dataset.ok = "1";
    }, true);
    go(0);
  });

  // Outside Netlify (local file or preview), forms go straight to the thank-you page
  var live = /netlify\.app$|dsptchdesign\.com$/.test(location.hostname);
  if (!live) {
    document.querySelectorAll("form[data-netlify]").forEach(function (f) {
      f.addEventListener("submit", function (ev) { ev.preventDefault(); if (f.hasAttribute("data-steps") && !f.dataset.ok) return; location.href = f.getAttribute("action") || "thanks.html"; });
    });
  }
})();
