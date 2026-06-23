"""
Bank Ops Intelligence Platform pipeline — three agents in sequence.

Flow:
  raw_stages → bottleneck_analyser  (pure Python, <5ms)
             → root_cause_agent     (Claude, per bottleneck stage, ~4s each)
             → recommendation_agent (Claude, single call, ~6s)
             → executive summary    (Claude, ~3s)
             → WorkflowReport
"""

import json
import os
import re
from datetime import datetime, timezone
from anthropic import Anthropic
from agents import bottleneck_analyser, root_cause_agent, recommendation_agent
from core.models import WorkflowType, WorkflowReport

MODEL = os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001")


def run_pipeline(
    workflow_name: str,
    workflow_type: WorkflowType,
    sla_target_days: float,
    estimated_annual_cost_gbp: int,
    raw_stages: list[tuple],
    progress_callback=None,
) -> WorkflowReport:
    def notify(step, total, label):
        if progress_callback:
            progress_callback(step, total, label)

    notify(1, 4, "Analysing workflow stages...")
    metrics = bottleneck_analyser.run(
        workflow_name, workflow_type, sla_target_days,
        estimated_annual_cost_gbp, raw_stages,
    )

    notify(2, 4, "Identifying root causes (Claude)...")
    root_causes = root_cause_agent.run(metrics)

    notify(3, 4, "Generating recommendations (Claude)...")
    recommendations = recommendation_agent.run(metrics, root_causes)

    notify(4, 4, "Writing executive summary (Claude)...")
    summary, top_rec = _generate_summary(metrics, root_causes, recommendations)

    return WorkflowReport(
        workflow_metrics=metrics,
        root_causes=root_causes,
        recommendations=recommendations,
        executive_summary=summary,
        top_recommendation=top_rec,
        generated_at=datetime.now(timezone.utc),
    )


def _generate_summary(metrics, root_causes, recommendations) -> tuple[str, str]:
    client = Anthropic()

    top_rec = recommendations[0] if recommendations else None
    bottleneck_names = [rc.stage_name for rc in root_causes]
    unique_bottlenecks = list(dict.fromkeys(bottleneck_names))

    prompt = f"""Write a 3-sentence executive summary of this bank operations analysis for a COO or Head of Operations.
Be specific — reference actual numbers. End with the single most impactful action.

Workflow: {metrics.workflow_name}
End-to-end time: {metrics.total_avg_days:.1f} days vs SLA target of {metrics.sla_target_days} days
Overall SLA compliance: {metrics.overall_sla_compliance:.0%}
Estimated annual operations cost: GBP {metrics.estimated_annual_cost_gbp:,}
Primary bottleneck: {metrics.primary_bottleneck}
Secondary bottleneck: {metrics.secondary_bottleneck}
Root cause categories: {', '.join(set(rc.category.value for rc in root_causes))}
Top recommendation: {top_rec.recommendation[:120] if top_rec else 'Review bottleneck stages'} \
(~{top_rec.estimated_time_saving_pct}% time saving, {top_rec.implementation_complexity} complexity)

Return JSON with two keys:
- "summary": 3-sentence executive summary
- "top_recommendation": one sentence — the single action to take first"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            return (
                data.get("summary", text[:400]),
                data.get("top_recommendation", top_rec.recommendation if top_rec else ""),
            )
        except Exception:
            pass

    fallback = top_rec.recommendation if top_rec else "Review primary bottleneck stage"
    return text[:400], fallback
