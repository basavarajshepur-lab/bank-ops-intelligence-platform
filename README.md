# Bank Ops Intelligence Platform

**AI-powered workflow analysis for financial institution operations teams**

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Production--Ready%20Demo-brightgreen) ![Claude](https://img.shields.io/badge/Powered%20by-Claude%20AI-orange)

---

## Executive Summary

### The Problem

Every bank runs a set of critical processes: approving mortgages, onboarding new clients, processing loans, opening savings accounts. These are the engine that keeps a bank running — and most banks are running them badly without knowing exactly why.

Here is the uncomfortable reality most banks live with every day:

- A mortgage that should take 15 days takes 22 days — but nobody can tell you exactly which part of the process is to blame.
- A compliance team is drowning in manual document reviews, yet the system generating those documents hasn't changed in a decade.
- An operations manager *knows* something is wrong, but proving it requires commissioning a 3-week internal audit that costs more than the problem itself.
- When the audit finally arrives, it describes what happened last quarter — not what is happening right now.

The pain is not a lack of data. Banks have enormous amounts of process data. The pain is that **none of it is synthesised into a clear answer to the question every operations head needs answered: "What is our biggest bottleneck right now, why does it exist, and what should we do about it first?"**

That is exactly what the Bank Ops Intelligence Platform answers.

### What This Tool Does

Think of it as a very experienced operations consultant who works in seconds instead of weeks.

You select a banking workflow — mortgage origination, KYC client onboarding, loan processing, or savings account opening. The platform immediately shows you:

**1. Where the delays are** — A clear, visual breakdown of every stage in the process: how long each step takes on average, how often errors or rework occur, and what percentage of cases are completing within the required timeframe (SLA compliance). Bottleneck stages are flagged in red so there is no ambiguity.

**2. Why the delays are happening** — An AI agent (powered by Claude) analyses the flagged bottlenecks and generates a root cause diagnosis, categorised as: Process, Technology, Data Quality, Regulatory, or People / Capacity.

**3. What to do about it** — A second AI agent generates up to four specific, prioritised recommendations covering automation, AI/ML, process redesign, system integration, or compliance simplification — with estimated time savings and implementation complexity for each.

**4. An executive summary ready to share** — Three sentences written for a COO or Head of Operations, in the kind of clear, decisive language that belongs in a board meeting.

### Workflows Covered

| Workflow | SLA Target | Typical Annual Cost | Biggest Pain Point |
|---|---|---|---|
| Residential Mortgage Origination | 15 days | £4.2 million | Legal Review: 120h average, 22% error rate, only 38% of cases on time |
| Corporate KYC / New Client Onboarding | 7 days | £2.8 million | Compliance Review: 48h average, only 62% of cases on time |
| SME Loan Origination | 10 days | £3.5 million | Underwriting: 48h average, 28% rework rate, only 45% on time |
| Retail Savings Account Opening | 3 days | £1.1 million | ID Verification: 20% error rate, still largely manual |

### Business Value

**Faster diagnosis = faster action.** Without this tool, identifying the primary bottleneck in a mortgage process requires a 3–4 week internal audit. The platform produces the same diagnosis in under five seconds — changing what is politically possible. Problems surface and get fixed in days rather than quarters.

**Targeted investment, not guesswork.** Banks frequently spend £500,000 automating a stage running at 95% SLA compliance while the stage running at 38% compliance continues to drag down the entire process. The bottleneck scoring system points every recommended investment directly at the problem causing the most damage.

**SLA recovery = customer retention and regulatory safety.** Closing a 10-percentage-point SLA gap on a mortgage process handling 500 cases per month, at £4.2M annual cost, can represent hundreds of thousands of pounds in annual savings before accounting for improved customer experience.

**Compliance without chaos.** Not every delay labelled "compliance" is compliance's fault — often it is a process or technology problem masquerading as a regulatory constraint. The root cause categorisation helps operations teams distinguish between delays they must accept and delays they can eliminate.

### Who This Is For

**Head of Operations / COO** — You own the SLA problem. You need a clear, defensible answer to "where are we failing and what are we doing about it?" without waiting for an internal audit. This platform delivers that answer on demand, in language you can take directly to a board presentation.

**Chief Data Officer / Data Product Lead** — You have been told to extract value from operational data. This platform is a concrete demonstration of what that looks like: raw process data transformed into actionable intelligence using AI.

**Digital Transformation Programme Manager** — You have a finite transformation budget and a list of processes to potentially automate. The bottleneck score gives you an objective, data-driven ranking of which process to tackle first — removing the political difficulty of prioritisation.

**Banking Technology Vendors (Finastra, Temenos, Thought Machine, SBS)** — This capability could be embedded directly into your existing operations management or core banking product. Banks already using your platform are generating the workflow data this tool analyses. An AI intelligence layer on top of that data is a natural upsell.

### How It Works

1. **Pick a workflow** from the dropdown (Mortgage, KYC, Loan, or Savings Account Opening)
2. **The platform immediately shows you the data** — processing times, error rates, SLA compliance by stage, and which stages are flagged as bottlenecks. No API key required for this step.
3. **Click "Run AI Analysis"** — within a few seconds the platform delivers root cause diagnoses for the worst bottlenecks and a set of prioritised recommendations.
4. **You get an executive summary** — three sentences you can walk into a leadership meeting with.

No consultants. No audit. No three-week wait.

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

### 4. Run a customer or bank demo with one command

If you are using [Claude Code](https://claude.ai/code), a `/demo` skill is included in this repo. It starts the Streamlit server, waits for it to be ready, screenshots the live dashboard, and walks you through the full demo flow with built-in stakeholder talking points.

```
/demo
```

To use it, open this project in Claude Code and type `/demo` at the prompt. No manual server management needed — the skill handles launch, screenshot, and shutdown. See [`.claude/skills/demo/SKILL.md`](.claude/skills/demo/SKILL.md) for the full script and troubleshooting guide.

---

## Project Structure

```
bank-ops-intelligence-platform/
├── app.py                        # Streamlit UI
├── requirements.txt
├── .env.example
├── USER_GUIDE.md                 # Plain-language guide for non-technical readers
├── agents/
│   ├── bottleneck_analyser.py    # Pure Python: stage scoring
│   ├── root_cause_agent.py       # Claude: root cause identification
│   └── recommendation_agent.py  # Claude: prioritised recommendations
├── core/
│   ├── models.py                 # Pydantic data contracts
│   └── pipeline.py               # Agent orchestration
├── data/
│   └── sample_workflows.py       # Synthetic bank ops data
└── .claude/
    └── skills/
        └── demo/
            └── SKILL.md          # /demo skill: one-command customer demo launcher
```

---

## Competitive Advantages

### 1. Built by Someone Who Has Lived the Problem

The platform was designed by a product manager with 14 years of experience inside financial institutions — Deutsche Bank, JPMorgan, Barclays, and LSEG/Refinitiv. The pain points it addresses are not theoretical. The bottleneck patterns, the SLA thresholds, the way root causes are categorised — all of it reflects real operational problems encountered in real banks.

Generic process mining tools are built by engineers who understand processes in the abstract. This tool is built around the specific decisions an operations head needs to make on a Monday morning.

### 2. Three Layers of Intelligence, Not Just a Dashboard

Most operations dashboards stop at layer one: they show you the numbers. The Bank Ops Intelligence Platform adds two more layers that competitors rarely provide:

- **Layer 2: Root cause diagnosis** — not just "Legal Review is slow" but "Legal Review is slow because of document completeness failures upstream and insufficient parallelisation in the review queue"
- **Layer 3: Prioritised, specific recommendations** — not "consider automation" but "automate document completeness checking at the Application Submission stage; estimated 30% time saving; low implementation complexity"

### 3. No New Infrastructure Required

The platform connects to data the bank already has. It does not require a new data warehouse, a new integration project, or a six-month implementation programme. Operations data from core banking exports, BPM tools, or even manual spreadsheets feeds directly in.

### 4. Results in Under Five Seconds

The bottleneck analysis runs in pure Python in under five milliseconds. The AI root cause and recommendation analysis runs in approximately three seconds. The complete diagnostic cycle that previously took weeks now takes a single coffee break.

### 5. Explainable, Auditable Output

In a regulated industry, AI outputs that cannot be explained are not useful — and may be actively dangerous. Every recommendation produced by this platform includes the reasoning behind it: which stage, which metric triggered the flag, which root cause category was identified, and how implementation complexity was assessed. There are no black boxes.

### 6. A Diagnostic Layer That Grows Into a Platform

This tool is currently a diagnostic engine — it tells you what is wrong and why. But the same foundation supports a progression from diagnosis to active management: real-time SLA monitoring, automated alerts when a stage degrades, workflow redesign templates, and eventually industry benchmarking ("your KYC takes 6.4 days; the top quartile of banks achieves 3.1 days"). Competitors who stop at reporting cannot grow into that position. This platform is designed to.

---

## Future Growth Opportunities

The current version is Phase 1 of a broader product roadmap.

### Phase 2 — Workflow Optimisation Engine
Move from "here is the problem" to "here is exactly how to fix it." Embedded workflow redesign templates, change management playbooks, and ROI calculators that operations teams can use to build internal business cases for investment. Instead of telling a bank to "redesign the legal review process," the platform provides the redesigned process template.

### Phase 3 — Real-Time Operations Intelligence
Connect directly to live banking systems (Thought Machine Vault, Temenos Transact, Finastra Fusion) rather than relying on periodic exports. The dashboard becomes a live control room: SLA compliance tracked by the hour, automatic alerts when a stage degrades, and AI-generated recommendations that update in real time as conditions change. This is the difference between a weather forecast and a weather radar.

### Phase 4 — Industry Benchmarking Network
The most defensible version of this product aggregates anonymised data across multiple banks to provide industry benchmarking: "Your mortgage origination takes 22 days. Our top-quartile clients achieve 14 days. Here are the three specific changes they made." No individual bank can generate this insight on their own. The benchmarking network is a classic network-effect business — the more institutions that participate, the more valuable the data becomes for every participant. Once established, this is extremely difficult for a competitor to replicate.

### Phase 5 — Vendor Ecosystem Integration
Embed the platform as a native capability within the product suites of major banking technology vendors. Rather than selling to banks directly, partner with the platforms banks already use — making the intelligence layer a standard feature of operations management, similar to how analytics became a standard feature of CRM systems.

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
