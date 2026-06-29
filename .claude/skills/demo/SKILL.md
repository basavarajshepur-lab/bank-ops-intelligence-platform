---
description: Launch the Bank Ops Intelligence Platform for a customer or bank demo. Starts the Streamlit app, opens it in the browser, and takes a screenshot showing the live dashboard.
---

# Demo — Bank Ops Intelligence Platform

Use this skill whenever you want to demo the platform to a customer, bank, or stakeholder. It starts the Streamlit server, waits for it to be ready, and screenshots the running app.

---

## Prerequisites

- Python 3.11+ installed and on PATH
- Dependencies installed: `pip install -r requirements.txt`
- Working directory: `C:\Users\basav\OneDrive\Documents\Portfolio\bank-ops-intelligence-platform`
- `.env` file present with `ANTHROPIC_API_KEY` set (optional — metrics load without it; AI analysis requires it)

---

## Step 1 — Kill any existing Streamlit instance

Before launching, clear any previous session on port 8501:

```powershell
$proc = Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($proc) { Stop-Process -Id $proc -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 1 }
```

---

## Step 2 — Start Streamlit in the background

```powershell
$env:PYTHONPATH = "C:\Users\basav\OneDrive\Documents\Portfolio\bank-ops-intelligence-platform"
Start-Process -FilePath "python" `
  -ArgumentList "-m streamlit run app.py --server.port 8501 --server.headless true" `
  -WorkingDirectory "C:\Users\basav\OneDrive\Documents\Portfolio\bank-ops-intelligence-platform" `
  -WindowStyle Hidden
```

Then poll until the server responds (up to 30 seconds):

```powershell
$ready = $false
for ($i = 0; $i -lt 30; $i++) {
    try {
        $r = Invoke-WebRequest -Uri "http://localhost:8501" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($r.StatusCode -eq 200) { $ready = $true; break }
    } catch {}
    Start-Sleep -Seconds 1
}
if (-not $ready) { Write-Error "Streamlit did not start within 30 seconds" }
```

---

## Step 3 — Screenshot the running app

Use `chromium-cli` to capture what a visitor sees:

```bash
chromium-cli --session bank-ops-demo <<'EOF'
nav http://localhost:8501
wait-for text=Bank Ops Intelligence Platform
screenshot
EOF
```

Screenshot saves to: `chromium_cli/sessions/bank-ops-demo/screenshots/screenshot.png`

Read the screenshot file and display it to the user with the Read tool so they can see the live dashboard.

---

## Step 4 — Walk through the demo flow

After confirming the app is up, guide the demo through these steps using `chromium-cli`:

```bash
chromium-cli --session bank-ops-demo <<'EOF'
nav http://localhost:8501
wait-for text=Bank Ops Intelligence Platform
screenshot
wait-for text=Stage Performance
screenshot
EOF
```

**Key screens to show stakeholders:**
1. **Workflow selector** — pick any of the four workflows from the dropdown
2. **KPI metrics row** — End-to-End Time vs SLA target, SLA Compliance %, Annual Ops Cost, Primary Bottleneck
3. **Stage Performance table** — bottleneck stages marked with ⚠
4. **Processing Time chart** — red bars = bottleneck stages
5. **SLA Compliance chart** — shows which stages are below the 85% target line
6. **Run AI Analysis** — click this (requires API key) to trigger Claude root cause analysis and recommendations
7. **Executive Summary** — the COO-ready 3-sentence output
8. **Recommendations tab** — 4 prioritised actions with time savings and complexity ratings

---

## Stop the server after the demo

```powershell
$proc = Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($proc) { Stop-Process -Id $proc -Force }
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Port 8501 already in use | Run the kill step (Step 1) again |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` in the project directory |
| AI Analysis button greyed out | Add `ANTHROPIC_API_KEY` to `.env` and restart |
| Page loads but charts are blank | Refresh the browser — Streamlit sometimes needs one reload on first boot |
| `chromium-cli` not found | Take screenshot manually by opening `http://localhost:8501` in a browser |

---

## Demo talking points

- **No consultants, no audit, no 3-week wait** — the bottleneck analysis runs in under 5ms; the full AI pipeline takes ~3 seconds
- **Four real banking workflows** — mortgage origination, KYC onboarding, SME loan, savings account opening; all with realistic SLA targets and cost figures
- **Three output layers** — raw metrics, AI root cause diagnosis, prioritised recommendations — not just a dashboard
- **Explainable AI** — every recommendation shows which stage, which metric, which root cause category, and implementation complexity; no black boxes
- **Powered by Claude** — the same AI used by leading financial institutions
