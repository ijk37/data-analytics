document.documentElement.classList.add("da-js-ready");
(function () {
  var links = [
    { label: "Home", href: "https://ijk37.com/", className: "resource-sidebar-hub__home" },
    { label: "Data Science & AI", href: "https://ijk37.com/data-science-ai/", className: "resource-sidebar-hub__dsai" },
    { label: "Cyber Security", href: "https://ijk37.com/cyber-security/", className: "resource-sidebar-hub__cyber" }
  ];

  function addResourceHubNav() {
    document.querySelectorAll(".resource-sidebar-hub").forEach(function (node) {
      node.remove();
    });

    var sidebar = document.querySelector(".md-sidebar--secondary .md-sidebar__inner");
    if (!sidebar) return;

    var nav = document.createElement("nav");
    nav.className = "resource-sidebar-hub";
    nav.setAttribute("aria-label", "Learning resource hubs");

    var title = document.createElement("div");
    title.className = "resource-sidebar-hub__title";
    title.textContent = "Resource hubs";
    nav.appendChild(title);

    links.forEach(function (item) {
      var link = document.createElement("a");
      link.className = "resource-sidebar-hub__button " + item.className;
      link.href = item.href;
      link.textContent = item.label;
      nav.appendChild(link);
    });

    sidebar.appendChild(nav);
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(addResourceHubNav);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", addResourceHubNav);
  } else {
    addResourceHubNav();
  }
}());
