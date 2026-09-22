(function () {
  "use strict";

  var searchInput = document.getElementById("lesson-search");
  var sortSelect = document.getElementById("sort-order");
  var pageSizeSelect = document.getElementById("page-size");
  var grid = document.getElementById("lesson-grid");
  var resultsCount = document.getElementById("results-count");
  var noResults = document.getElementById("no-results");
  var pagination = document.getElementById("pagination");

  if (!grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll(".lesson-card"));
  if (cards.length === 0) return;

  var items = cards.map(function (card) {
    var heading = card.querySelector("h2");
    return {
      card: card,
      text: card.textContent.toLowerCase(),
      title: heading ? heading.textContent.trim().toLowerCase() : "",
    };
  });

  var state = { page: 1 };

  function visibleItems() {
    var query = searchInput ? searchInput.value.trim().toLowerCase() : "";
    var sortDir = sortSelect ? sortSelect.value : "asc";

    var filtered = items.filter(function (item) {
      return query === "" || item.text.indexOf(query) !== -1;
    });

    filtered.sort(function (a, b) {
      if (a.title === b.title) return 0;
      var result = a.title < b.title ? -1 : 1;
      return sortDir === "desc" ? -result : result;
    });

    return filtered;
  }

  function render() {
    var pageSize = pageSizeSelect ? parseInt(pageSizeSelect.value, 10) : items.length;
    var filtered = visibleItems();
    var totalPages = Math.max(1, Math.ceil(filtered.length / pageSize));

    state.page = Math.min(Math.max(state.page, 1), totalPages);

    var start = (state.page - 1) * pageSize;
    var pageItems = filtered.slice(start, start + pageSize);
    var pageCardSet = pageItems.reduce(function (set, item) {
      set.add(item.card);
      return set;
    }, new Set());

    filtered.forEach(function (item) {
      grid.appendChild(item.card);
    });

    items.forEach(function (item) {
      item.card.classList.toggle("hidden", !pageCardSet.has(item.card));
    });

    var countLabel = filtered.length + (filtered.length === 1 ? " lesson" : " lessons");
    if (totalPages > 1) countLabel += " · page " + state.page + " of " + totalPages;
    resultsCount.textContent = countLabel;
    noResults.classList.toggle("hidden", filtered.length !== 0);

    renderPagination(totalPages);
  }

  function renderPagination(totalPages) {
    if (!pagination) return;
    pagination.innerHTML = "";
    if (totalPages <= 1) return;

    function pageButton(label, page, options) {
      options = options || {};
      var btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = label;
      btn.className = "min-w-9 rounded-lg border px-3 py-1.5 text-sm font-medium transition " + (
        options.active
          ? "border-indigo-500 bg-indigo-500 text-white"
          : "border-slate-700 text-slate-300 hover:border-slate-600 hover:text-white"
      );
      if (options.disabled) {
        btn.disabled = true;
        btn.className += " cursor-not-allowed opacity-40";
      } else {
        btn.addEventListener("click", function () {
          state.page = page;
          render();
        });
      }
      return btn;
    }

    pagination.appendChild(pageButton("Prev", state.page - 1, { disabled: state.page <= 1 }));
    for (var page = 1; page <= totalPages; page++) {
      pagination.appendChild(pageButton(String(page), page, { active: page === state.page }));
    }
    pagination.appendChild(pageButton("Next", state.page + 1, { disabled: state.page >= totalPages }));
  }

  function onControlChange() {
    state.page = 1;
    render();
  }

  if (searchInput) searchInput.addEventListener("input", onControlChange);
  if (sortSelect) sortSelect.addEventListener("change", onControlChange);
  if (pageSizeSelect) pageSizeSelect.addEventListener("change", onControlChange);

  render();
})();
