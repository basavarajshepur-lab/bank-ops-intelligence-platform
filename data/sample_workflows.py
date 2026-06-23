"""
Synthetic bank operations workflow data.
Reflects realistic processing times, error rates, and SLA compliance
for common UK retail and commercial banking processes.
"""

from core.models import WorkflowType

SAMPLE_WORKFLOWS: dict[WorkflowType, dict] = {

    WorkflowType.MORTGAGE_ORIGINATION: {
        "name": "Residential Mortgage Origination",
        "sla_target_days": 15,
        "estimated_annual_cost_gbp": 4_200_000,
        "stages": [
            ("Application Submission",  2,   3, 0.08, 0.95, 500),
            ("Credit Assessment",       24,  5, 0.15, 0.72, 500),
            ("Property Valuation",      72,  2, 0.12, 0.55, 470),
            ("Legal Review",            120, 8, 0.22, 0.38, 450),
            ("Offer Generation",        8,   4, 0.05, 0.88, 430),
            ("Completion",              48,  6, 0.10, 0.71, 420),
        ],
    },

    WorkflowType.KYC_ONBOARDING: {
        "name": "Corporate KYC / New Client Onboarding",
        "sla_target_days": 7,
        "estimated_annual_cost_gbp": 2_800_000,
        "stages": [
            ("Document Collection",    4,  3, 0.25, 0.82, 300),
            ("Identity Verification",  2,  2, 0.10, 0.91, 280),
            ("AML Screening",          8,  4, 0.18, 0.76, 270),
            ("Risk Assessment",        24, 6, 0.20, 0.62, 265),
            ("Compliance Review",      48, 5, 0.15, 0.55, 250),
            ("Account Activation",     1,  1, 0.03, 0.98, 240),
        ],
    },

    WorkflowType.LOAN_ORIGINATION: {
        "name": "SME Loan Origination",
        "sla_target_days": 10,
        "estimated_annual_cost_gbp": 3_500_000,
        "stages": [
            ("Application",       1,   2, 0.05, 0.97, 800),
            ("Bureau Check",      0.5, 1, 0.03, 0.99, 795),
            ("Underwriting",      48,  8, 0.28, 0.45, 780),
            ("Credit Decision",   4,   3, 0.12, 0.80, 720),
            ("Offer & Acceptance",24,  4, 0.08, 0.75, 700),
            ("Disbursement",      4,   2, 0.04, 0.92, 685),
        ],
    },

    WorkflowType.SAVINGS_ACCOUNT: {
        "name": "Retail Savings Account Opening",
        "sla_target_days": 3,
        "estimated_annual_cost_gbp": 1_100_000,
        "stages": [
            ("Online Application", 0.5, 0, 0.12, 0.99, 1200),
            ("ID Verification",    2,   2, 0.20, 0.88, 1100),
            ("AML Screening",      4,   3, 0.08, 0.85, 1050),
            ("Account Setup",      1,   4, 0.05, 0.92, 1020),
            ("Welcome Pack",       24,  2, 0.03, 0.79, 1010),
            ("Activation",         0.5, 1, 0.02, 0.97, 1000),
        ],
    },
}
