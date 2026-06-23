"""
recommendation_agent.py - Claude agent: generates actionable recommendations.

Takes root causes and workflow metrics, returns prioritised Recommendation objects
with estimated impact and implementation complexity.
"""

import json
import os
from anthropic import Anthropic
from core.models import WorkflowMetrics, RootCause, Recommendation, OpportunityType

MODEL = os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001")


def run(
    metrics: WorkflowMetrics,
    root_causes: list[RootCause],
) -> list[Recommendation]:
    client = Anthropic()

    causes_summary = "\n".join(
        f"- [{rc.stage_name}] {rc.cause} (Impact: {rc.impact}, Category: {rc.category.value})"
        for rc in root_causes
    )

    bottleneck_stages = "\n".join(
        f"- {s.stage_name}: {s.avg_processing_hours:.0f}h avg, {s.error_rate:.0%} error rate, "
        f"{s.sla_compliance:.0%} SLA compliance, {s.manual_touchpoints} manual touchpoints"
        for s in metrics.stages if s.is_bottleneck
    )

    prompt = f"""You are a product manager at a B2B SaaS company that builds workflow automation software for banks and financial institutions.

A client bank has shared their {metrics.workflow_name} workflow performance data. Generate 4 specific, actionable product recommendations to improve their operations.

WORKFLOW CONTEXT:
Total average end-to-end time: {metrics.total_avg_days:.1f} days (SLA target: {metrics.sla_target_days} days)
Overall SLA compliance: {metrics.overall_sla_compliance:.0%}
Estimated annual operations cost: GBP {metrics.estimated_annual_cost_gbp:,}

BOTTLENECK STAGES:
{bottleneck_stages}

ROOT CAUSES IDENTIFIED:
{causes_summary}

Return a JSON array of exactly 4 recommendation objects, prioritised 1-4 (1 = highest priority), each with:
- "stage_name": which stage this addresses (use exact stage name from above, or "All Stages" for cross-cutting)
- "recommendation": one specific, concrete recommendation (2-3 sentences max)
- "opportunity_type": one of "Automation", "AI / ML", "Process Redesign", "System Integration", "Compliance Simplification"
- "estimated_time_saving_pct": integer 5-60, realistic estimate of processing time reduction
- "implementation_complexity": "Low", "Medium", or "High"
- "priority": 1, 2, 3, or 4

Focus on recommendations a SaaS product team could build and deliver to the bank — not internal bank change management.
Return only the JSON array, no other text."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    recommendations = []

    try:
        start = text.find("[")
        end = text.rfind("]") + 1
        recs_raw = json.loads(text[start:end])
        for r in recs_raw:
            try:
                opp_type = OpportunityType(r.get("opportunity_type", "Automation"))
            except ValueError:
                opp_type = OpportunityType.AUTOMATION
            recommendations.append(Recommendation(
                stage_name=r.get("stage_name", "All Stages"),
                recommendation=r.get("recommendation", ""),
                opportunity_type=opp_type,
                estimated_time_saving_pct=int(r.get("estimated_time_saving_pct", 15)),
                implementation_complexity=r.get("implementation_complexity", "Medium"),
                priority=int(r.get("priority", len(recommendations) + 1)),
            ))
    except Exception:
        recommendations.append(Recommendation(
            stage_name=metrics.primary_bottleneck,
            recommendation="Automate manual data validation at the primary bottleneck stage to reduce error rates and rework cycles.",
            opportunity_type=OpportunityType.AUTOMATION,
            estimated_time_saving_pct=30,
            implementation_complexity="Medium",
            priority=1,
        ))

    return sorted(recommendations, key=lambda r: r.priority)
