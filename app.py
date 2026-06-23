"""
Bank Ops Intelligence Platform
AI-powered workflow analysis for financial institution operations teams.

Run: python -m streamlit run app.py
"""

from dotenv import load_dotenv
load_dotenv()

import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core.models import WorkflowType
from core.pipeline import run_pipeline
from data.sample_workflows import SAMPLE_WORKFLOWS

st.set_page_config(
    page_title="Bank Ops Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state ───────────────────────────────────────────────────────────────

if "report" not in st.session_state:
    st.session_state.report = None
if "metrics" not in st.session_state:
    st.session_state.metrics = None
if "selected_type" not in st.session_state:
    st.session_state.selected_type = None

# ── Helpers ─────────────────────────────────────────────────────────────────────

def sla_color(compliance: float) -> str:
    if compliance >= 0.85:
        return "#22c55e"
    if compliance >= 0.65:
        return "#f59e0b"
    return "#ef4444"

def complexity_badge(level: str) -> str:
    colors = {"Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"}
    return f'<span style="background:{colors.get(level,"#94a3b8")};color:white;padding:2px 8px;border-radius:4px;font-size:0.8em">{level}</span>'

def impact_badge(level: str) -> str:
    colors = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#22c55e"}
    return f'<span style="background:{colors.get(level,"#94a3b8")};color:white;padding:2px 8px;border-radius:4px;font-size:0.8em">{level}</span>'

def build_stage_chart(metrics):
    stages = metrics.stages
    colors = ["#ef4444" if s.is_bottleneck else "#3b82f6" for s in stages]
    labels = [f"{'⚠ ' if s.is_bottleneck else ''}{s.stage_name}" for s in stages]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels,
        x=[s.avg_processing_hours for s in stages],
        orientation="h",
        marker_color=colors,
        text=[f"{s.avg_processing_hours:.0f}h" for s in stages],
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Avg processing: %{x:.0f} hours<br>"
            "Error rate: %{customdata[0]:.0%}<br>"
            "SLA compliance: %{customdata[1]:.0%}<extra></extra>"
        ),
        customdata=[(s.error_rate, s.sla_compliance) for s in stages],
    ))
    fig.update_layout(
        height=320,
        margin=dict(t=10, l=0, r=60, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Average Processing Hours", showgrid=True, gridcolor="#e2e8f0"),
        yaxis=dict(autorange="reversed"),
        font=dict(family="Inter, sans-serif", size=12),
    )
    return fig

def build_sla_chart(metrics):
    stages = metrics.stages
    colors = [sla_color(s.sla_compliance) for s in stages]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=[s.stage_name for s in stages],
        x=[s.sla_compliance * 100 for s in stages],
        orientation="h",
        marker_color=colors,
        text=[f"{s.sla_compliance:.0%}" for s in stages],
        textposition="outside",
    ))
    fig.add_vline(x=85, line_dash="dash", line_color="#94a3b8",
                  annotation_text="85% target", annotation_position="top right")
    fig.update_layout(
        height=320,
        margin=dict(t=10, l=0, r=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="SLA Compliance (%)", range=[0, 115], showgrid=True, gridcolor="#e2e8f0"),
        yaxis=dict(autorange="reversed"),
        font=dict(family="Inter, sans-serif", size=12),
    )
    return fig

# ── Header ──────────────────────────────────────────────────────────────────────

st.markdown("""
<div style="background:linear-gradient(135deg,#1A1A2E 0%,#16213E 100%);
            padding:28px 32px;border-radius:12px;margin-bottom:24px">
    <h1 style="color:white;margin:0;font-size:1.8rem">🏦 Bank Ops Intelligence Platform</h1>
    <p style="color:#94a3b8;margin:6px 0 0 0;font-size:0.95rem">
        AI-powered workflow analysis for financial institution operations teams
    </p>
</div>
""", unsafe_allow_html=True)

# ── API key check ───────────────────────────────────────────────────────────────

if not os.getenv("ANTHROPIC_API_KEY"):
    st.warning(
        "**ANTHROPIC_API_KEY not set.** Workflow data and metrics are still available below. "
        "Add your key to `.env` to enable AI root cause analysis and recommendations.",
        icon="⚠️",
    )

# ── Workflow selector ───────────────────────────────────────────────────────────

col_sel, col_run = st.columns([3, 1])

with col_sel:
    workflow_options = {wt.value: wt for wt in WorkflowType}
    selected_label = st.selectbox(
        "Select workflow to analyse",
        options=list(workflow_options.keys()),
        key="workflow_selector",
    )
    selected_type = workflow_options[selected_label]

workflow_data = SAMPLE_WORKFLOWS[selected_type]

with col_run:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    run_analysis = st.button(
        "Run AI Analysis",
        type="primary",
        use_container_width=True,
        disabled=not os.getenv("ANTHROPIC_API_KEY"),
    )

if selected_type != st.session_state.selected_type:
    st.session_state.report = None
    st.session_state.selected_type = selected_type

# ── Always-visible: Workflow metrics ───────────────────────────────────────────

from agents.bottleneck_analyser import run as compute_metrics

metrics = compute_metrics(
    workflow_name=workflow_data["name"],
    workflow_type=selected_type,
    sla_target_days=workflow_data["sla_target_days"],
    estimated_annual_cost_gbp=workflow_data["estimated_annual_cost_gbp"],
    raw_stages=workflow_data["stages"],
)
st.session_state.metrics = metrics

st.markdown("---")
st.markdown(f"### {workflow_data['name']}")

m1, m2, m3, m4 = st.columns(4)
m1.metric("End-to-End Time", f"{metrics.total_avg_days:.1f} days", f"SLA target: {metrics.sla_target_days} days",
          delta_color="inverse")
m2.metric("SLA Compliance", f"{metrics.overall_sla_compliance:.0%}",
          delta="Below 85% target" if metrics.overall_sla_compliance < 0.85 else "On target",
          delta_color="inverse" if metrics.overall_sla_compliance < 0.85 else "normal")
m3.metric("Annual Ops Cost", f"£{metrics.estimated_annual_cost_gbp:,}")
m4.metric("Primary Bottleneck", metrics.primary_bottleneck)

# Stage detail table
st.markdown("#### Stage Performance")

stage_df = pd.DataFrame([{
    "Stage": ("⚠ " if s.is_bottleneck else "") + s.stage_name,
    "Avg Hours": f"{s.avg_processing_hours:.0f}h",
    "Manual Touchpoints": s.manual_touchpoints,
    "Error Rate": f"{s.error_rate:.0%}",
    "SLA Compliance": f"{s.sla_compliance:.0%}",
    "Monthly Volume": f"{s.volume_monthly:,}",
    "Bottleneck Score": f"{s.bottleneck_score:.2f}",
} for s in metrics.stages])

st.dataframe(stage_df, hide_index=True, use_container_width=True)

# Charts side by side
ch1, ch2 = st.columns(2)
with ch1:
    st.markdown("##### Processing Time by Stage")
    st.caption("⚠ Red = bottleneck stage")
    st.plotly_chart(build_stage_chart(metrics), use_container_width=True)

with ch2:
    st.markdown("##### SLA Compliance by Stage")
    st.plotly_chart(build_sla_chart(metrics), use_container_width=True)

# ── AI Analysis ─────────────────────────────────────────────────────────────────

if run_analysis:
    with st.spinner("Running AI analysis..."):
        progress_bar = st.progress(0)
        progress_text = st.empty()

        def update_progress(step, total, label):
            progress_bar.progress(step / total)
            progress_text.text(label)

        report = run_pipeline(
            workflow_name=workflow_data["name"],
            workflow_type=selected_type,
            sla_target_days=workflow_data["sla_target_days"],
            estimated_annual_cost_gbp=workflow_data["estimated_annual_cost_gbp"],
            raw_stages=workflow_data["stages"],
            progress_callback=update_progress,
        )
        st.session_state.report = report
        progress_bar.empty()
        progress_text.empty()

report = st.session_state.report

if report:
    st.markdown("---")
    st.markdown("## AI Analysis")

    # Executive summary
    st.markdown(
        f"""<div style="background:#f0fdf4;border-left:4px solid #22c55e;
                      padding:16px 20px;border-radius:0 8px 8px 0;margin-bottom:20px">
            <strong>Executive Summary</strong><br><br>
            {report.executive_summary}<br><br>
            <strong>Top Recommendation:</strong> {report.top_recommendation}
        </div>""",
        unsafe_allow_html=True,
    )

    rc_tab, rec_tab = st.tabs(["Root Cause Analysis", "Recommendations"])

    with rc_tab:
        st.markdown("#### Bottleneck Root Causes")
        for rc in report.root_causes:
            with st.expander(f"**{rc.stage_name}** — {rc.category.value}", expanded=True):
                col_a, col_b = st.columns([6, 1])
                with col_a:
                    st.write(rc.cause)
                with col_b:
                    st.markdown(impact_badge(rc.impact), unsafe_allow_html=True)

    with rec_tab:
        st.markdown("#### Prioritised Recommendations")
        for i, rec in enumerate(report.recommendations, 1):
            with st.expander(f"**#{i} — {rec.stage_name}** · {rec.opportunity_type.value}", expanded=(i == 1)):
                r1, r2, r3 = st.columns([2, 1, 1])
                with r1:
                    st.write(rec.recommendation)
                with r2:
                    st.metric("Time Saving", f"~{rec.estimated_time_saving_pct}%")
                with r3:
                    st.markdown(f"**Complexity**<br>{complexity_badge(rec.implementation_complexity)}",
                                unsafe_allow_html=True)

elif os.getenv("ANTHROPIC_API_KEY"):
    st.info("Select a workflow and click **Run AI Analysis** to identify root causes and get AI-powered recommendations.")

# ── Footer ──────────────────────────────────────────────────────────────────────

st.markdown("---")
st.caption(
    "Bank Ops Intelligence Platform · Powered by Claude AI · "
    "Workflow data is synthetic and used for demonstration purposes only."
)
