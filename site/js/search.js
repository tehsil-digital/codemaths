(function () {
  "use strict";

  var input = document.getElementById("lesson-search");
  var cards = Array.prototype.slice.call(document.querySelectorAll(".lesson-card"));
  var resultsCount = document.getElementById("results-count");
  var noResults = document.getElementById("no-results");

  if (!input || cards.length === 0) return;

  var indexed = cards.map(function (card) {
    return { card: card, text: card.textContent.toLowerCase() };
  });

  function render() {
    var query = input.value.trim().toLowerCase();
    var visible = 0;

    indexed.forEach(function (item) {
      var match = query === "" || item.text.indexOf(query) !== -1;
      item.card.classList.toggle("hidden", !match);
      if (match) visible += 1;
    });

    resultsCount.textContent = visible + (visible === 1 ? " lesson" : " lessons");
    noResults.classList.toggle("hidden", visible !== 0);
  }

  input.addEventListener("input", render);
  render();
})();
