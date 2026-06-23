# Bank Ops Intelligence Platform

**AI-powered workflow analysis for financial institution operations teams**

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Production--Ready%20Demo-brightgreen) ![Claude](https://img.shields.io/badge/Powered%20by-Claude%20AI-orange)

---

## The Problem

Banks run critical operations — mortgage origination, KYC onboarding, loan processing, savings account opening — on workflows that haven't fundamentally changed in 15 years. The technology has changed (core banking platforms, CRM systems, document management), but the **process intelligence** hasn't kept up.

A typical UK bank:
- Takes 18–25 days to process a residential mortgage when the SLA target is 15 days
- Has a KYC compliance review stage with 55% SLA compliance and a 15% rework rate
- Employs compliance analysts who spend most of their time manually validating data that automation could handle in seconds
- Cannot answer "which stage is causing the most delay, and why?" without a 3-week internal audit

The problem isn't lack of data. Banks have enormous amounts of process data. The problem is that **no tool synthesises it into clear bottleneck identification + root cause analysis + actionable recommendations** in a form that a Head of Operations can act on the same day.

---

## What This Platform Does

A three-agent AI pipeline that analyses bank operations workflow data and delivers:

```
Workflow Data  →  Bottleneck Analyser  →  Root Cause Agent  →  Recommendation Agent  →  Executive Summary
               (pure Python, <5ms)      (Claude, per stage)    (Claude, single call)     (Claude, ~3s)
```

**Agent 1 — Bottleneck Analyser (pure Python)**
Scores every workflow stage on three dimensions:
- Processing time relative to the longest stage (40% weight)
- Error/rework rate relative to the highest in the workflow (30% weight)
- SLA non-compliance rate (30% weight)

Flags the top 2 bottleneck stages for AI analysis.

**Agent 2 — Root Cause Agent (Claude)**
For each flagged bottleneck: analyses processing time, manual touchpoints, error rate, and volume to identify the 2 most likely root causes — categorised as Process, Technology, Data Quality, Regulatory, or People/Capacity.

**Agent 3 — Recommendation Agent (Claude)**
Generates 4 prioritised product recommendations for the operations team. Each recommendation includes: which stage it addresses, opportunity type (Automation / AI/ML / Process Redesign / System Integration / Compliance Simplification), estimated time saving, and implementation complexity.

**Executive Summary (Claude)**
A 3-sentence COO-ready summary with the single most important action to take first.

---

## Why I Built This

I have 14 years of experience as a product manager *inside* financial institutions — at Deutsche Bank, LSEG/Refinitiv, JPMorgan, and Barclays. I have sat in the rooms where operations heads present their SLA miss reports. I have been the PM who had to choose which process bottleneck to fix first with limited engineering capacity.

The frustration I kept seeing: **operations teams know they have a problem, but they don't know where to start.** The diagnosis is expensive (internal audit), slow (weeks), and often politically difficult (nobody wants to flag their own process as the bottleneck).

A B2B SaaS product that solves this problem — one that a vendor like SBS, Finastra, Temenos, or Thought Machine could offer as part of their platform — would need to:

1. **Connect to workflow data** the bank already has (core banking system exports, BPM tools, manual spreadsheets)
2. **Identify bottlenecks algorithmically** before involving any human analyst
3. **Generate root cause hypotheses** that give operations managers a starting point for investigation
4. **Recommend specific product capabilities** the vendor can build or already has — not generic change management advice

This platform demonstrates that full pipeline. The workflow data is synthetic, but the analysis pattern is directly drawn from real operations problems I've worked on.

---

## Workflows Covered

| Workflow | SLA Target | Typical Annual Cost | Primary Pain Point |
|----------|-----------|---------------------|-------------------|
| Residential Mortgage Origination | 15 days | £4.2M+ | Legal Review (120h avg, 22% rework, 38% SLA) |
| Corporate KYC / New Client Onboarding | 7 days | £2.8M+ | Compliance Review (48h avg, 62% SLA compliance) |
| SME Loan Origination | 10 days | £3.5M+ | Underwriting (48h avg, 28% rework, 45% SLA) |
| Retail Savings Account Opening | 3 days | £1.1M+ | ID Verification (20% error rate, manual) |

---

## Product Strategy Notes

This demo represents **Phase 1** of a broader product: the diagnostic layer.

**Phase 2 — Workflow Optimisation Engine**
Move from analysis to recommendations with embedded change management: workflow redesign templates, process playbooks, and ROI calculators banks can use in internal business cases.

**Phase 3 — Real-Time Operations Intelligence**
Integration with core banking APIs (Thought Machine Vault, Temenos Transact, Finastra Fusion) to replace synthetic data with live workflow telemetry. Dashboard moves from post-hoc analysis to real-time SLA monitoring with proactive alerting.

**Phase 4 — Benchmarking Network**
Anonymised benchmarking: "Your KYC onboarding takes 6.4 days. Our top-quartile clients achieve 3.1 days. Here are the 3 changes they made." This is the network effect that makes the platform defensible — no individual bank has this data.

**Target Personas**
- **Head of Operations / COO** — owns the SLA problem; needs a board-ready diagnosis
- **Chief Data Officer / Data Product Lead** — wants AI-generated insights from operational data; this is their use case
- **Digital Transformation PM** — needs to prioritise which process to automate first; the bottleneck score gives them an objective ranking

---

## Tech Stack

- **Python 3.11+** — core language
- **Streamlit** — interactive UI
- **Anthropic Claude (Haiku)** — root cause + recommendation agents
- **Plotly** — workflow visualisation
- **Pydantic v2** — typed data contracts between agents

---

## Getting Started

### 1. Clone and install

```bash
git clone https://github.com/basavarajshepur-lab/bank-ops-intelligence-platform
cd bank-ops-intelligence-platform
pip install -r requirements.txt
```

### 2. Set your API key

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

Get an API key at [console.anthropic.com](https://console.anthropic.com).

### 3. Run

```bash
python -m streamlit run app.py
```

The workflow metrics and charts load immediately without an API key. Click **Run AI Analysis** (requires API key) to trigger the Claude agents.

---

## Project Structure

```
bank-ops-intelligence-platform/
├── app.py                        # Streamlit UI
├── requirements.txt
├── .env.example
├── agents/
│   ├── bottleneck_analyser.py    # Pure Python: stage scoring
│   ├── root_cause_agent.py       # Claude: root cause identification
│   └── recommendation_agent.py  # Claude: prioritised recommendations
├── core/
│   ├── models.py                 # Pydantic data contracts
│   └── pipeline.py               # Agent orchestration
└── data/
    └── sample_workflows.py       # Synthetic bank ops data
```

---

## Related Work

This project is part of a series demonstrating AI applications in financial services:

- [AML Copilot](https://github.com/basavarajshepur-lab/aml-copilot) — Multi-agent AML alert triage
- [Model Risk Copilot](https://github.com/basavarajshepur-lab/model-risk-copilot) — AI model validation and risk scoring
- [KYC-AML Intelligence Agent](https://github.com/basavarajshepur-lab/kyc-aml-intelligence-agent) — End-to-end KYC/AML workflow automation
- [Responsible AI in FinServ](https://github.com/basavarajshepur-lab/responsible-ai-finserv) — AI governance framework for regulated environments
- [Data Intelligence Platform](https://github.com/basavarajshepur-lab/Data-Intelligence-Platform-multiagent) — Multi-agent data quality and enrichment

---

## License

MIT
