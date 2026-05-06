(function () {
  "use strict";

  const listEl = document.getElementById("symptom-list");
  const runBtn = document.getElementById("run");
  const out = document.getElementById("results");

  function apiErrorMessage(data, statusText) {
    const d = data && data.detail;
    if (Array.isArray(d)) {
      return d
        .map(function (x) {
          return x.msg || JSON.stringify(x);
        })
        .join(" ");
    }
    if (typeof d === "string") return d;
    return statusText || "Request failed";
  }

  function escapeHtml(t) {
    const div = document.createElement("div");
    div.textContent = t;
    return div.innerHTML;
  }

  async function loadSymptoms() {
    const r = await fetch("/api/symptoms");
    if (!r.ok) {
      listEl.innerHTML =
        '<p class="alert alert--warn">Could not load symptoms. Check that the API is running.</p>';
      return;
    }
    const data = await r.json();
    listEl.innerHTML = "";
    listEl.className = "symptom-grid";
    data.symptoms.forEach(function (s) {
      const id = "sym-" + s.index;
      const lab = document.createElement("label");
      lab.className = "symptom-chip";
      lab.setAttribute("for", id);
      lab.innerHTML =
        '<input type="checkbox" data-idx="' +
        s.index +
        '" id="' +
        id +
        '"/>' +
        '<span><span class="symptom-chip__num">' +
        s.index +
        '</span>' +
        '<span class="symptom-chip__label">' +
        escapeHtml(s.label) +
        "</span></span>";
      listEl.appendChild(lab);
    });
    runBtn.disabled = false;
  }

  function selectedIndices() {
    return Array.prototype.slice
      .call(document.querySelectorAll("#symptom-list input[type=checkbox]:checked"))
      .map(function (cb) {
        return parseInt(cb.dataset.idx, 10);
      })
      .sort(function (a, b) {
        return a - b;
      });
  }

  runBtn.addEventListener("click", async function () {
    const indices = selectedIndices();
    if (!indices.length) {
      out.classList.add("is-visible");
      out.innerHTML =
        '<div class="alert alert--warn">Select at least one symptom to continue.</div>';
      return;
    }
    runBtn.disabled = true;
    out.classList.add("is-visible");
    out.innerHTML = '<div class="loading-text">Running inference</div>';
    try {
      const r = await fetch("/api/diagnose", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ indices: indices }),
      });
      let data = {};
      try {
        data = await r.json();
      } catch (e) {
        data = {};
      }
      if (!r.ok) throw new Error(apiErrorMessage(data, r.statusText));

      let html = "";
      if (data.no_match) {
        html +=
          '<div class="alert alert--warn"><strong>No strong match</strong> for this combination in the current knowledge base. Try more symptoms or different combinations.</div>';
      } else {
        if (data.exact_rule_match) {
          html +=
            '<div class="alert alert--success">A full rule match was found for your symptom set.</div>';
        } else {
          html +=
            '<div class="alert alert--warn">No single rule matched every required symptom; results are ranked by overlap with disease profiles.</div>';
        }
        html += '<h3 class="result-heading">Selected symptoms</h3><div class="pill-list">';
        data.symptoms_display.forEach(function (s) {
          html += '<span class="pill">' + escapeHtml(s) + "</span>";
        });
        html += "</div>";
        html +=
          '<h3 class="result-heading">Possible diagnoses (' + data.diagnoses.length + ")</h3>";
        data.diagnoses.forEach(function (d, i) {
          html +=
            '<article class="diagnosis-card">' +
            '<div class="diagnosis-card__top">' +
            '<span class="diagnosis-card__badge">' +
            (i + 1) +
            "</span>" +
            '<span class="diagnosis-card__title">' +
            escapeHtml(d.disease_display) +
            "</span>" +
            "</div>" +
            '<p class="diagnosis-card__treatment">' +
            escapeHtml(d.treatment) +
            "</p>" +
            "</article>";
        });
      }
      out.innerHTML = html;
    } catch (e) {
      out.innerHTML =
        '<div class="alert alert--warn">' +
        escapeHtml(e.message || String(e)) +
        "</div>";
    }
    runBtn.disabled = false;
  });

  loadSymptoms();
})();
