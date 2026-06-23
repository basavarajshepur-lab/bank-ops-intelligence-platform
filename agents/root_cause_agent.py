"""
root_cause_agent.py - Claude agent: identifies root causes for workflow bottlenecks.

Called once per bottleneck stage. Returns structured RootCause objects.
"""

import json
import os
from anthropic import Anthropic
from core.models import WorkflowMetrics, RootCause, RootCauseCategory

MODEL = os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001")


def run(metrics: WorkflowMetrics) -> list[RootCause]:
    client = Anthropic()
    bottleneck_stages = [s for s in metrics.stages if s.is_bottleneck]
    root_causes = []

    for stage in bottleneck_stages:
        prompt = f"""You are a specialist in bank operations process improvement.

Analyse this workflow stage and identify the 2 most likely root causes of its performance issues.

Workflow: {metrics.workflow_name}
Stage: {stage.stage_name}
Average processing time: {stage.avg_processing_hours:.1f} hours
Manual touchpoints: {stage.manual_touchpoints}
Error / rework rate: {stage.error_rate:.0%}
SLA compliance: {stage.sla_compliance:.0%}
Monthly volume: {stage.volume_monthly:,} cases

Return a JSON array of exactly 2 objects, each with:
- "cause": one sentence describing the root cause
- "impact": "High", "Medium", or "Low"
- "category": one of "Process", "Technology", "Data Quality", "Regulatory", "People / Capacity"

Return only the JSON array, no other text."""

        response = client.messages.create(
            model=MODEL,
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}],
        )

        text = response.content[0].text.strip()
        try:
            start = text.find("[")
            end = text.rfind("]") + 1
            causes_raw = json.loads(text[start:end])
            for c in causes_raw:
                try:
                    category = RootCauseCategory(c.get("category", "Process"))
                except ValueError:
                    category = RootCauseCategory.PROCESS
                root_causes.append(RootCause(
                    stage_name=stage.stage_name,
                    cause=c.get("cause", "Unknown cause"),
                    impact=c.get("impact", "Medium"),
                    category=category,
                ))
        except Exception:
            root_causes.append(RootCause(
                stage_name=stage.stage_name,
                cause=f"High error rate ({stage.error_rate:.0%}) and processing time suggest manual data entry and re-work loops.",
                impact="High",
                category=RootCauseCategory.PROCESS,
            ))

    return root_causes
