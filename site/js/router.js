(function () {
  "use strict";

  var routeViewIds = {
    "/": ["top", "lessons"],
    "/about": ["about"],
  };

  var routeMeta = {
    "/": {
      title: "Lean 4 Lessons for Undergraduates | CodeMaths",
      description: "Free, searchable Lean 4 video lessons for undergraduate students learning formal theorem proving — each with a linked tutorial video and companion code repo.",
    },
    "/about": {
      title: "About | CodeMaths",
      description: "What CodeMaths is and how the free Lean 4 lesson catalog works.",
    },
  };

  var allViewIds = Object.keys(routeViewIds).reduce(function (acc, key) {
    return acc.concat(routeViewIds[key]);
  }, []);

  var descriptionMeta = document.querySelector('meta[name="description"]');
  var canonicalLink = document.querySelector('link[rel="canonical"]');
  var ogTitleMeta = document.querySelector('meta[property="og:title"]');
  var ogDescriptionMeta = document.querySelector('meta[property="og:description"]');
  var ogUrlMeta = document.querySelector('meta[property="og:url"]');

  function normalize(path) {
    return routeViewIds[path] ? path : "/";
  }

  function render(path) {
    path = normalize(path);
    var activeIds = routeViewIds[path];

    allViewIds.forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.classList.toggle("hidden", activeIds.indexOf(id) === -1);
    });

    var info = routeMeta[path];
    if (info) {
      document.title = info.title;
      if (descriptionMeta) descriptionMeta.setAttribute("content", info.description);
      if (ogTitleMeta) ogTitleMeta.setAttribute("content", info.title);
      if (ogDescriptionMeta) ogDescriptionMeta.setAttribute("content", info.description);
    }
    var absoluteUrl = window.location.origin + path;
    if (canonicalLink) canonicalLink.setAttribute("href", absoluteUrl);
    if (ogUrlMeta) ogUrlMeta.setAttribute("content", absoluteUrl);

    document.querySelectorAll("[data-route-link]").forEach(function (link) {
      var isActive = normalize(link.getAttribute("href")) === path;
      link.classList.toggle("text-white", isActive);
    });
  }

  function navigate(path) {
    path = normalize(path);
    if (window.location.pathname !== path) {
      history.pushState(null, "", path);
    }
    render(path);
    window.scrollTo(0, 0);
  }

  document.addEventListener("click", function (event) {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
      return;
    }
    var link = event.target.closest("[data-route-link]");
    if (!link) return;
    event.preventDefault();
    navigate(link.getAttribute("href"));
  });

  window.addEventListener("popstate", function () {
    render(window.location.pathname);
  });

  render(window.location.pathname);
})();
