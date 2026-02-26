"""
Hand-coding app for 100 CFPB narratives.
Run: python handcode_app.py
Open: http://localhost:5000
"""

from flask import Flask, render_template_string, request, jsonify
import pandas as pd
import json
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
BLIND_CSV = os.path.join(APP_DIR, "output", "cfpb_handcode_100_blind.csv")
SAVE_FILE = os.path.join(APP_DIR, "output", "cfpb_handcode_100_responses.json")

app = Flask(__name__)

# Load narratives once at startup
df = pd.read_csv(BLIND_CSV, dtype={"complaint_id": "int64"})
narratives = df.to_dict("records")

# Load existing responses
def load_responses():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE) as f:
            return json.load(f)
    return {}

def save_responses(responses):
    with open(SAVE_FILE, "w") as f:
        json.dump(responses, f, indent=2)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CFPB Hand-Coding</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Georgia, serif; background: #f5f5f0; color: #222; }

  .top-bar {
    position: sticky; top: 0; z-index: 10;
    background: #fff; border-bottom: 1px solid #ddd;
    padding: 10px 24px; display: flex; align-items: center;
    justify-content: space-between; gap: 16px;
  }
  .progress-text { font-size: 14px; color: #666; }
  .progress-bar-bg {
    flex: 1; max-width: 400px; height: 8px;
    background: #e0e0e0; border-radius: 4px; overflow: hidden;
  }
  .progress-bar-fill {
    height: 100%; background: #2a7; border-radius: 4px;
    transition: width 0.3s;
  }
  .nav-btn {
    padding: 6px 18px; font-size: 14px; cursor: pointer;
    border: 1px solid #999; border-radius: 4px; background: #fff;
  }
  .nav-btn:hover { background: #eee; }
  .nav-btn:disabled { opacity: 0.4; cursor: default; }
  .nav-jump { width: 56px; text-align: center; font-size: 14px;
    border: 1px solid #999; border-radius: 4px; padding: 4px; }

  .container { max-width: 900px; margin: 0 auto; padding: 24px; }

  .meta {
    display: flex; gap: 24px; flex-wrap: wrap;
    padding: 12px 0; border-bottom: 1px solid #ddd;
    font-size: 14px; color: #555; margin-bottom: 16px;
  }
  .meta span { white-space: nowrap; }
  .meta .label { font-weight: bold; color: #333; }

  .narrative {
    background: #fff; border: 1px solid #ddd; border-radius: 6px;
    padding: 24px 28px; line-height: 1.7; font-size: 16px;
    white-space: pre-wrap; word-wrap: break-word;
    max-height: 50vh; overflow-y: auto; margin-bottom: 24px;
  }

  .coding-panel {
    background: #fff; border: 1px solid #ddd; border-radius: 6px;
    padding: 20px 24px;
  }
  .field { margin-bottom: 18px; }
  .field-label { font-weight: bold; font-size: 14px; margin-bottom: 6px; }

  .radio-group { display: flex; gap: 4px; flex-wrap: wrap; }
  .radio-group label {
    padding: 6px 16px; border: 1px solid #ccc; border-radius: 4px;
    font-size: 14px; cursor: pointer; transition: all 0.15s;
    user-select: none;
  }
  .radio-group input { display: none; }
  .radio-group input:checked + span {
    background: #2a7; color: #fff; border-color: #2a7;
  }
  .radio-group label:has(input:checked) {
    background: #2a7; color: #fff; border-color: #2a7;
  }
  .radio-group label:hover { background: #f0f0f0; }
  .radio-group label:has(input:checked):hover { background: #259; }

  .slider-row { display: flex; align-items: center; gap: 12px; }
  .slider-row input[type=range] { flex: 1; max-width: 300px; }
  .slider-val {
    min-width: 32px; text-align: center; font-weight: bold;
    font-size: 15px;
  }

  .justification-box {
    width: 100%; min-height: 60px; padding: 8px 12px;
    font-family: Georgia, serif; font-size: 14px; line-height: 1.5;
    border: 1px solid #ccc; border-radius: 4px; resize: vertical;
  }

  .save-status {
    text-align: center; padding: 8px; font-size: 13px; color: #888;
    min-height: 30px;
  }
  .save-status.saved { color: #2a7; }

  .coded-indicator {
    display: inline-block; width: 10px; height: 10px;
    border-radius: 50%; margin-right: 6px;
  }
  .coded-indicator.yes { background: #2a7; }
  .coded-indicator.no { background: #ddd; }
</style>
</head>
<body>

<div class="top-bar">
  <button class="nav-btn" id="prevBtn" onclick="go(-1)">Back</button>
  <div style="display:flex;align-items:center;gap:8px;">
    <span class="coded-indicator" id="codedDot"></span>
    <input class="nav-jump" id="jumpInput" type="number" min="1" max="100"
      onchange="jumpTo(this.value)" title="Jump to narrative #">
    <span style="font-size:14px;color:#666;">/ 100</span>
  </div>
  <div class="progress-bar-bg">
    <div class="progress-bar-fill" id="progressFill"></div>
  </div>
  <span class="progress-text" id="progressText"></span>
  <button class="nav-btn" id="nextBtn" onclick="go(1)">Next</button>
</div>

<div class="container">
  <div class="meta" id="metaBar"></div>
  <div class="narrative" id="narrativeText"></div>
  <div class="coding-panel">

    <div class="field">
      <div class="field-label">Classification</div>
      <div class="radio-group" id="classRadios">
        <label><input type="radio" name="classification" value="EVALUATIVE"><span>EVALUATIVE</span></label>
        <label><input type="radio" name="classification" value="DELEGATIVE"><span>DELEGATIVE</span></label>
        <label><input type="radio" name="classification" value="UNCLASSIFIABLE"><span>UNCLASSIFIABLE</span></label>
      </div>
    </div>

    <div class="field">
      <div class="field-label">Delegative Score</div>
      <div class="slider-row">
        <input type="range" id="delegSlider" min="0" max="10" step="1" value="0"
          oninput="document.getElementById('delegVal').textContent=(this.value/10).toFixed(1); autoSave();">
        <span class="slider-val" id="delegVal">0.0</span>
      </div>
    </div>

    <div class="field">
      <div class="field-label">Evaluative Score</div>
      <div class="slider-row">
        <input type="range" id="evalSlider" min="0" max="10" step="1" value="0"
          oninput="document.getElementById('evalVal').textContent=(this.value/10).toFixed(1); autoSave();">
        <span class="slider-val" id="evalVal">0.0</span>
      </div>
    </div>

    <div class="field">
      <div class="field-label">Confidence</div>
      <div class="radio-group" id="confRadios">
        <label><input type="radio" name="confidence" value="HIGH"><span>HIGH</span></label>
        <label><input type="radio" name="confidence" value="MEDIUM"><span>MEDIUM</span></label>
        <label><input type="radio" name="confidence" value="LOW"><span>LOW</span></label>
      </div>
    </div>

    <div class="field">
      <div class="field-label">Justification</div>
      <textarea class="justification-box" id="justification"
        placeholder="One sentence explaining your classification..."
        oninput="autoSave();"></textarea>
    </div>

  </div>
  <div class="save-status" id="saveStatus"></div>
</div>

<script>
const narratives = NARRATIVES_JSON;
let responses = RESPONSES_JSON;
let current = 0;
let saveTimer = null;

function render() {
  const n = narratives[current];
  const num = n.narrative_number;

  document.getElementById("jumpInput").value = num;
  document.getElementById("metaBar").innerHTML =
    `<span><span class="label">Product:</span> ${n.product_type}</span>` +
    `<span><span class="label">Company:</span> ${n.company}</span>` +
    `<span><span class="label">Date:</span> ${n.date}</span>` +
    `<span><span class="label">ID:</span> ${n.complaint_id}</span>`;
  document.getElementById("narrativeText").textContent = n.narrative_text;
  document.getElementById("narrativeText").scrollTop = 0;

  // Load saved response
  const key = String(num);
  const r = responses[key] || {};

  // Classification radios
  document.querySelectorAll('input[name="classification"]').forEach(el => {
    el.checked = (el.value === (r.classification || ""));
  });

  // Sliders
  const ds = r.delegative_score != null ? Math.round(r.delegative_score * 10) : 0;
  const es = r.evaluative_score != null ? Math.round(r.evaluative_score * 10) : 0;
  document.getElementById("delegSlider").value = ds;
  document.getElementById("delegVal").textContent = (ds/10).toFixed(1);
  document.getElementById("evalSlider").value = es;
  document.getElementById("evalVal").textContent = (es/10).toFixed(1);

  // Confidence radios
  document.querySelectorAll('input[name="confidence"]').forEach(el => {
    el.checked = (el.value === (r.confidence || ""));
  });

  // Justification
  document.getElementById("justification").value = r.justification || "";

  // Nav buttons
  document.getElementById("prevBtn").disabled = (current === 0);
  document.getElementById("nextBtn").disabled = (current === narratives.length - 1);

  // Coded indicator
  const dot = document.getElementById("codedDot");
  dot.className = "coded-indicator " + (r.classification ? "yes" : "no");

  updateProgress();
}

function updateProgress() {
  const coded = Object.values(responses).filter(r => r.classification).length;
  document.getElementById("progressText").textContent = coded + " / 100 coded";
  document.getElementById("progressFill").style.width = coded + "%";
}

function go(delta) {
  saveNow();
  current = Math.max(0, Math.min(narratives.length - 1, current + delta));
  render();
  window.scrollTo(0, 0);
}

function jumpTo(val) {
  const idx = narratives.findIndex(n => n.narrative_number === parseInt(val));
  if (idx >= 0) {
    saveNow();
    current = idx;
    render();
    window.scrollTo(0, 0);
  }
}

function collectResponse() {
  const num = narratives[current].narrative_number;
  const cls = document.querySelector('input[name="classification"]:checked');
  const conf = document.querySelector('input[name="confidence"]:checked');
  return {
    narrative_number: num,
    complaint_id: narratives[current].complaint_id,
    classification: cls ? cls.value : "",
    delegative_score: parseInt(document.getElementById("delegSlider").value) / 10,
    evaluative_score: parseInt(document.getElementById("evalSlider").value) / 10,
    confidence: conf ? conf.value : "",
    justification: document.getElementById("justification").value.trim()
  };
}

function autoSave() {
  if (saveTimer) clearTimeout(saveTimer);
  saveTimer = setTimeout(saveNow, 500);
}

function saveNow() {
  const r = collectResponse();
  const key = String(r.narrative_number);
  responses[key] = r;
  updateProgress();

  // Update coded dot
  const dot = document.getElementById("codedDot");
  dot.className = "coded-indicator " + (r.classification ? "yes" : "no");

  fetch("/save", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(responses)
  }).then(res => {
    if (res.ok) {
      document.getElementById("saveStatus").textContent = "Saved";
      document.getElementById("saveStatus").className = "save-status saved";
    }
  }).catch(() => {
    document.getElementById("saveStatus").textContent = "Save failed";
    document.getElementById("saveStatus").className = "save-status";
  });
}

// Auto-save on radio clicks
document.querySelectorAll('input[type="radio"]').forEach(el => {
  el.addEventListener("change", autoSave);
});

// Keyboard shortcuts
document.addEventListener("keydown", e => {
  if (e.target.tagName === "TEXTAREA") return;
  if (e.key === "ArrowLeft" || e.key === "ArrowUp") { e.preventDefault(); go(-1); }
  if (e.key === "ArrowRight" || e.key === "ArrowDown") { e.preventDefault(); go(1); }
});

render();
</script>
</body>
</html>"""


@app.route("/")
def index():
    responses = load_responses()
    # Inject data into template
    html = HTML.replace("NARRATIVES_JSON", json.dumps(narratives))
    html = html.replace("RESPONSES_JSON", json.dumps(responses))
    return html


@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()
    save_responses(data)
    return jsonify({"status": "ok"})


@app.route("/export")
def export():
    """Export responses as CSV download."""
    responses = load_responses()
    if not responses:
        return "No responses yet", 404
    rows = sorted(responses.values(), key=lambda r: r.get("narrative_number", 0))
    csv_df = pd.DataFrame(rows)
    csv_text = csv_df.to_csv(index=False)
    return csv_text, 200, {
        "Content-Type": "text/csv",
        "Content-Disposition": "attachment; filename=handcode_responses.csv"
    }


if __name__ == "__main__":
    print(f"Loaded {len(narratives)} narratives from {BLIND_CSV}")
    if os.path.exists(SAVE_FILE):
        r = load_responses()
        coded = sum(1 for v in r.values() if v.get("classification"))
        print(f"Existing responses: {coded}/100 coded")
    print(f"Responses auto-save to: {SAVE_FILE}")
    print(f"Export CSV at: http://localhost:5000/export")
    print(f"\nOpen: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
