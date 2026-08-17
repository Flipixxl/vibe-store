(function () {
  "use strict";

  var root = document.documentElement;

  /* ---------- Theme toggle ---------- */
  var themeToggle = document.getElementById("themeToggle");
  var themeIcon = themeToggle ? themeToggle.querySelector(".theme-icon") : null;

  function applyTheme(light) {
    root.classList.toggle("theme-light", light);
    if (themeIcon) themeIcon.textContent = light ? "☀️" : "🌙";
  }

  if (themeToggle) {
    applyTheme(root.classList.contains("theme-light"));
    themeToggle.addEventListener("click", function () {
      var isLight = root.classList.toggle("theme-light");
      localStorage.setItem("vibe-theme", isLight ? "light" : "dark");
      if (themeIcon) themeIcon.textContent = isLight ? "☀️" : "🌙";
    });
  }

  /* ---------- Reveal on scroll ---------- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- Animated counters ---------- */
  var counters = document.querySelectorAll("[data-count]");
  if (counters.length) {
    var countIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        countIO.unobserve(el);
        var target = parseInt(el.dataset.count, 10) || 0;
        var suffix = el.dataset.suffix || "";
        var duration = 1400;
        var start = null;
        function step(ts) {
          if (!start) start = ts;
          var p = Math.min((ts - start) / duration, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(target * eased) + suffix;
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.4 });
    counters.forEach(function (el) { countIO.observe(el); });
  }

  /* ---------- Header scroll state + progress + to-top ---------- */
  var header = document.querySelector(".site-header");
  var progress = document.getElementById("scrollProgress");
  var toTop = document.getElementById("toTop");
  if (header || progress || toTop) {
    var onScroll = function () {
      var y = window.scrollY;
      if (header) header.classList.toggle("scrolled", y > 20);
      if (progress) {
        var h = document.documentElement.scrollHeight - window.innerHeight;
        progress.style.width = (h > 0 ? (y / h) * 100 : 0) + "%";
      }
      if (toTop) toTop.classList.toggle("show", y > 500);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }
  if (toTop) {
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---------- Mobile nav toggle ---------- */
  var toggle = document.querySelector(".menu-toggle");
  var mobileNav = document.querySelector(".mobile-nav");
  if (toggle && mobileNav) {
    toggle.addEventListener("click", function () {
      mobileNav.classList.toggle("open");
      toggle.classList.toggle("open");
    });
  }

  /* ---------- Close alerts ---------- */
  document.querySelectorAll(".alert-close").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var alert = btn.closest(".alert");
      if (alert) alert.remove();
    });
  });

  /* ---------- Hero parallax ---------- */
  var hero = document.querySelector(".hero");
  if (hero && window.matchMedia("(prefers-reduced-motion: reduce)").matches === false) {
    var orbit = hero.querySelector(".hero-orbit");
    var icon = hero.querySelector(".orbit-icon");
    window.addEventListener("mousemove", function (e) {
      var x = (e.clientX / window.innerWidth - 0.5) * 2;
      var y = (e.clientY / window.innerHeight - 0.5) * 2;
      if (orbit) orbit.style.transform = "translate(" + (x * -14) + "px, " + (y * -14) + "px)";
      if (icon) icon.style.transform = "translate(" + (x * 22) + "px, " + (y * 22) + "px)";
    }, { passive: true });
  }

  /* ---------- Tilt effect on product cards ---------- */
  var tiltEls = document.querySelectorAll("[data-tilt]");
  if (tiltEls.length && window.matchMedia("(prefers-reduced-motion: reduce)").matches === false) {
    tiltEls.forEach(function (card) {
      card.addEventListener("mousemove", function (e) {
        var rect = card.getBoundingClientRect();
        var x = (e.clientX - rect.left) / rect.width - 0.5;
        var y = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = "perspective(900px) rotateY(" + (x * 7) + "deg) rotateX(" + (y * -7) + "deg) translateY(-6px)";
      });
      card.addEventListener("mouseleave", function () {
        card.style.transform = "";
      });
    });
  }
})();