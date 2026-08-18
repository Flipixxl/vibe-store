(function () {
  "use strict";

  var root = document.documentElement;

  /* ---------- Theme toggle ---------- */
  var themeToggle = document.getElementById("themeToggle");

  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      var isDark = root.classList.toggle("theme-dark");
      localStorage.setItem("vibe-theme", isDark ? "dark" : "light");
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
})();