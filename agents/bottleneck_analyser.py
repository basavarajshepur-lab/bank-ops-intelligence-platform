"""
bottleneck_analyser.py - Pure Python bottleneck detection. No LLM calls.

Scores each workflow stage on three dimensions:
  - Processing time relative to the longest stage (40%)
  - Error/rework rate relative to the highest in the workflow (30%)
  - SLA non-compliance rate (30%)

Top 2 scoring stages are flagged as bottlenecks.
"""

from core.models import WorkflowType, WorkflowStage, WorkflowMetrics


def run(
    workflow_name: str,
    workflow_type: WorkflowType,
    sla_target_days: float,
    estimated_annual_cost_gbp: int,
    raw_stages: list[tuple[str, float, int, float, float, int]],
) -> WorkflowMetrics:
    """
    raw_stages: list of (name, avg_hours, manual_touchpoints,
                         error_rate, sla_compliance, volume_monthly)
    """
    stages = [
        WorkflowStage(
            stage_name=name,
            avg_processing_hours=hours,
            manual_touchpoints=touchpoints,
            error_rate=error_rate,
            sla_compliance=sla,
            volume_monthly=volume,
        )
        for name, hours, touchpoints, error_rate, sla, volume in raw_stages
    ]

    max_hours = max(s.avg_processing_hours for s in stages) or 1
    max_error = max(s.error_rate for s in stages) or 1

    for stage in stages:
        stage.bottleneck_score = (
            (stage.avg_processing_hours / max_hours) * 0.40
            + (stage.error_rate / max_error) * 0.30
            + (1 - stage.sla_compliance) * 0.30
        )

    sorted_by_score = sorted(stages, key=lambda s: s.bottleneck_score, reverse=True)
    sorted_by_score[0].is_bottleneck = True
    if len(sorted_by_score) > 1:
        sorted_by_score[1].is_bottleneck = True

    total_avg_hours = sum(s.avg_processing_hours for s in stages)
    total_avg_days = total_avg_hours / 8  # assume 8-hour working day

    overall_sla = sum(s.sla_compliance for s in stages) / len(stages)

    return WorkflowMetrics(
        workflow_type=workflow_type,
        workflow_name=workflow_name,
        stages=stages,
        total_avg_days=round(total_avg_days, 1),
        sla_target_days=sla_target_days,
        overall_sla_compliance=round(overall_sla, 3),
        primary_bottleneck=sorted_by_score[0].stage_name,
        secondary_bottleneck=sorted_by_score[1].stage_name if len(sorted_by_score) > 1 else "",
        estimated_annual_cost_gbp=estimated_annual_cost_gbp,
    )
