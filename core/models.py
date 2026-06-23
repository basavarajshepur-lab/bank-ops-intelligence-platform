"""
Pydantic v2 data contracts for the Bank Ops Intelligence Platform.
Every agent input and output is typed here.
"""

from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field


class WorkflowType(str, Enum):
    MORTGAGE_ORIGINATION   = "Mortgage Origination"
    KYC_ONBOARDING         = "KYC / New Client Onboarding"
    LOAN_ORIGINATION       = "Loan Origination"
    SAVINGS_ACCOUNT        = "Savings Account Opening"


class RootCauseCategory(str, Enum):
    PROCESS    = "Process"
    TECHNOLOGY = "Technology"
    DATA       = "Data Quality"
    REGULATORY = "Regulatory"
    PEOPLE     = "People / Capacity"


class OpportunityType(str, Enum):
    AUTOMATION        = "Automation"
    AI_ML             = "AI / ML"
    PROCESS_REDESIGN  = "Process Redesign"
    INTEGRATION       = "System Integration"
    COMPLIANCE        = "Compliance Simplification"


class WorkflowStage(BaseModel):
    stage_name:            str
    avg_processing_hours:  float
    manual_touchpoints:    int
    error_rate:            float   # 0.0 - 1.0
    sla_compliance:        float   # 0.0 - 1.0
    volume_monthly:        int
    is_bottleneck:         bool  = False
    bottleneck_score:      float = 0.0


class WorkflowMetrics(BaseModel):
    workflow_type:              WorkflowType
    workflow_name:              str
    stages:                     list[WorkflowStage]
    total_avg_days:             float
    sla_target_days:            float
    overall_sla_compliance:     float
    primary_bottleneck:         str
    secondary_bottleneck:       str
    estimated_annual_cost_gbp:  int


class RootCause(BaseModel):
    stage_name: str
    cause:      str
    impact:     str        # High / Medium / Low
    category:   RootCauseCategory


class Recommendation(BaseModel):
    stage_name:                  str
    recommendation:              str
    opportunity_type:            OpportunityType
    estimated_time_saving_pct:   int
    implementation_complexity:   str   # Low / Medium / High
    priority:                    int


class WorkflowReport(BaseModel):
    workflow_metrics:  WorkflowMetrics
    root_causes:       list[RootCause]
    recommendations:   list[Recommendation]
    executive_summary: str
    top_recommendation: str
    generated_at:      datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
