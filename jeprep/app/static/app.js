// Small progressive enhancements. Everything works without JavaScript; the server enforces all rules.
(function () {
  // Demo login: preselect the role that matches the chosen fake user.
  var user = document.getElementById("demo-user");
  var role = document.getElementById("demo-role");
  if (user && role) {
    var sync = function () {
      var opt = user.options[user.selectedIndex];
      if (opt && opt.dataset.role) { role.value = opt.dataset.role; }
    };
    user.addEventListener("change", sync);
    sync();
  }

  // Mapping editor: dim the posting columns for rows whose role is not "amount".
  var applyRole = function (select) {
    var row = select.closest("tr");
    if (row) { row.classList.toggle("is-nonamount", select.value !== "amount"); }
  };
  document.querySelectorAll("select.js-role").forEach(function (select) {
    applyRole(select);
    select.addEventListener("change", function () { applyRole(select); });
  });

  // "Tick all reviewed": a convenience, still a deliberate human click.
  var all = document.getElementById("check-all-reviewed");
  if (all) {
    all.addEventListener("click", function () {
      document.querySelectorAll("input.js-reviewed").forEach(function (box) { box.checked = true; });
    });
  }
})();
