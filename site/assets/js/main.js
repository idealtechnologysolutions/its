/* Ideal Technology Solutions: preview site script.
   Handles the mobile menu button and the desktop Services and Industries
   dropdowns. Everything else on the site works without JavaScript. */

(function () {
  "use strict";

  var header = document.querySelector(".site-header");
  if (!header) return;

  var menuToggle = header.querySelector(".menu-toggle");
  var groupToggles = Array.prototype.slice.call(header.querySelectorAll(".site-nav__toggle"));

  /* ---------- Mobile and tablet menu ---------- */

  function setMenu(open) {
    if (!menuToggle) return;
    menuToggle.setAttribute("aria-expanded", String(open));
    menuToggle.querySelector(".menu-toggle__label").textContent = open ? "Close" : "Menu";
    if (open) {
      header.setAttribute("data-menu-open", "");
    } else {
      header.removeAttribute("data-menu-open");
    }
  }

  if (menuToggle) {
    menuToggle.addEventListener("click", function () {
      setMenu(menuToggle.getAttribute("aria-expanded") !== "true");
    });
  }

  /* ---------- Desktop dropdowns ---------- */

  function closeGroups(except) {
    groupToggles.forEach(function (button) {
      if (button !== except) button.setAttribute("aria-expanded", "false");
    });
  }

  groupToggles.forEach(function (button) {
    button.addEventListener("click", function () {
      var open = button.getAttribute("aria-expanded") !== "true";
      closeGroups(button);
      button.setAttribute("aria-expanded", String(open));
    });

    // Close a dropdown when keyboard focus moves somewhere else on the page.
    // relatedTarget is null when the window loses focus, or when a click lands
    // on something that does not take focus (Safari links); clicks outside are
    // handled by the document listener below.
    button.parentNode.addEventListener("focusout", function (event) {
      var next = event.relatedTarget;
      if (next && !button.parentNode.contains(next)) {
        button.setAttribute("aria-expanded", "false");
      }
    });
  });

  document.addEventListener("click", function (event) {
    if (!event.target.closest(".site-nav__item")) closeGroups(null);
  });

  /* ---------- Escape closes whatever is open ---------- */

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;

    var openGroup = groupToggles.filter(function (button) {
      return button.getAttribute("aria-expanded") === "true";
    })[0];

    if (openGroup) {
      openGroup.setAttribute("aria-expanded", "false");
      openGroup.focus();
    } else if (menuToggle && menuToggle.getAttribute("aria-expanded") === "true") {
      setMenu(false);
      menuToggle.focus();
    }
  });

  /* ---------- Reset when the layout changes ---------- */

  var desktop = window.matchMedia("(min-width: 1080px)");
  function onLayoutChange() {
    setMenu(false);
    closeGroups(null);
  }
  if (desktop.addEventListener) {
    desktop.addEventListener("change", onLayoutChange);
  } else if (desktop.addListener) {
    desktop.addListener(onLayoutChange);
  }
})();
