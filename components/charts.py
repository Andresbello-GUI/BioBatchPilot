"""
BatchPilot — charts.py
All Plotly chart rendering. Uses rgba() for all transparent colors — no 8-digit hex.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots

CHART_BG   = "#0d1117"
GRID_COLOR = "#21262d"
TEXT_COLOR = "#7d8590"
ACCENT     = "#00ff9f"

AXIS_STYLE = dict(
    gridcolor=GRID_COLOR,
    color=TEXT_COLOR,
    linecolor="#30363d",
    tickfont=dict(size=10, color=TEXT_COLOR, family="IBM Plex Mono"),
    title_font=dict(size=10, color=TEXT_COLOR),
)


def _base_layout(height=460):
    return dict(
        height=height,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(family="IBM Plex Mono", color=TEXT_COLOR),
        showlegend=True,
        legend=dict(
            bgcolor="#161b22", bordercolor="#30363d", borderwidth=1,
            font=dict(size=9, color="#8b949e"), orientation="h",
            yanchor="bottom", y=-0.22, xanchor="center", x=0.5,
        ),
        margin=dict(l=10, r=10, t=40, b=60),
    )


def make_upstream_cho_chart(data: dict) -> go.Figure:
    """Chart for Scenario 01 — Lactate Accumulation (standard CHO fed-batch)."""
    days = data["Day"]

    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=["VCD & Viability", "Glucose & Lactate",
                        "pH", "DO (%)", "Titer", "Osmolality"],
        vertical_spacing=0.18,
        horizontal_spacing=0.10,
    )

    # 1 — VCD + Viability
    fig.add_trace(go.Scatter(
        x=days, y=data["VCD (e6/mL)"],
        name="VCD", line=dict(color=ACCENT, width=2),
        mode="lines+markers", marker=dict(size=5),
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=days, y=data["Viability (%)"],
        name="Viability %", line=dict(color="#f0883e", width=2, dash="dot"),
        mode="lines+markers", marker=dict(size=5),
    ), row=1, col=1)

    # 2 — Glucose + Lactate
    fig.add_trace(go.Scatter(
        x=days, y=data["Glucose (g/L)"],
        name="Glucose", line=dict(color="#58a6ff", width=2),
        mode="lines+markers", marker=dict(size=5),
    ), row=1, col=2)
    fig.add_trace(go.Scatter(
        x=days, y=data["Lactate (g/L)"],
        name="Lactate", line=dict(color="#f85149", width=2.5),
        mode="lines+markers", marker=dict(size=6, symbol="diamond"),
    ), row=1, col=2)
    fig.add_hline(
        y=3.0, line_dash="dash",
        line_color="rgba(248,81,73,0.4)",
        annotation_text="Threshold 3.0",
        annotation_font_color="#f85149",
        annotation_font_size=9, row=1, col=2,
    )

    # 3 — pH
    fig.add_trace(go.Scatter(
        x=days, y=data["pH"],
        name="pH", line=dict(color="#d2a8ff", width=2),
        mode="lines+markers", marker=dict(size=5),
    ), row=1, col=3)
    fig.add_hline(
        y=7.00, line_dash="dash",
        line_color="rgba(210,168,255,0.27)",
        annotation_text="pH 7.00",
        annotation_font_color="#d2a8ff",
        annotation_font_size=9, row=1, col=3,
    )

    # 4 — DO
    fig.add_trace(go.Scatter(
        x=days, y=data["DO (%)"],
        name="DO %", line=dict(color="#79c0ff", width=2),
        mode="lines+markers", marker=dict(size=5),
        fill="tozeroy", fillcolor="rgba(121,192,255,0.07)",
    ), row=2, col=1)
    fig.add_hline(
        y=25, line_dash="dash",
        line_color="rgba(240,136,62,0.4)",
        annotation_text="Min setpoint",
        annotation_font_color="#f0883e",
        annotation_font_size=9, row=2, col=1,
    )

    # 5 — Titer
    fig.add_trace(go.Scatter(
        x=days, y=data["Titer (mg/L)"],
        name="Titer", line=dict(color=ACCENT, width=2),
        mode="lines+markers", marker=dict(size=5),
        fill="tozeroy", fillcolor="rgba(0,255,159,0.05)",
    ), row=2, col=2)

    # 6 — Osmolality
    fig.add_trace(go.Scatter(
        x=days, y=data["Osmolality (mOsm/kg)"],
        name="Osmolality", line=dict(color="#ffa657", width=2),
        mode="lines+markers", marker=dict(size=5),
    ), row=2, col=3)
    fig.add_hline(
        y=370, line_dash="dash",
        line_color="rgba(248,81,73,0.4)",
        annotation_text="Upper limit",
        annotation_font_color="#f85149",
        annotation_font_size=9, row=2, col=3,
    )

    fig.update_layout(**_base_layout())
    for ann in fig.layout.annotations:
        ann.font.color = "#7d8590"
        ann.font.size = 11
    fig.update_xaxes(**AXIS_STYLE, title_text="Day")
    fig.update_yaxes(**AXIS_STYLE)
    return fig


def make_upstream_do_chart(data: dict) -> go.Figure:
    """Chart for Scenario 02 — DO Instability."""
    x = data["Day"]

    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=["DO (%) — Oscillation", "VCD & Viability",
                        "Glucose & Lactate", "pH", "Titer", "Agitation proxy"],
        vertical_spacing=0.18,
        horizontal_spacing=0.10,
    )

    # 1 — DO (main focus)
    fig.add_trace(go.Scatter(
        x=x, y=data["DO (%)"],
        name="DO %", line=dict(color="#f85149", width=2.5),
        mode="lines+markers", marker=dict(size=6, symbol="diamond"),
    ), row=1, col=1)
    fig.add_hline(
        y=30, line_dash="dash",
        line_color="rgba(0,255,159,0.4)",
        annotation_text="Setpoint 30%",
        annotation_font_color=ACCENT,
        annotation_font_size=9, row=1, col=1,
    )
    fig.add_hline(
        y=25, line_dash="dash",
        line_color="rgba(248,81,73,0.4)",
        annotation_text="Min 25%",
        annotation_font_color="#f85149",
        annotation_font_size=9, row=1, col=1,
    )

    # 2 — VCD + Viability
    fig.add_trace(go.Scatter(
        x=x, y=data["VCD (e6/mL)"],
        name="VCD", line=dict(color=ACCENT, width=2),
        mode="lines+markers", marker=dict(size=5),
    ), row=1, col=2)
    fig.add_trace(go.Scatter(
        x=x, y=data["Viability (%)"],
        name="Viability %", line=dict(color="#f0883e", width=2, dash="dot"),
        mode="lines+markers", marker=dict(size=5),
    ), row=1, col=2)

    # 3 — Glucose + Lactate
    fig.add_trace(go.Scatter(
        x=x, y=data["Glucose (g/L)"],
        name="Glucose", line=dict(color="#58a6ff", width=2),
        mode="lines+markers", marker=dict(size=5),
    ), row=1, col=3)
    fig.add_trace(go.Scatter(
        x=x, y=data["Lactate (g/L)"],
        name="Lactate", line=dict(color="#d2a8ff", width=2),
        mode="lines+markers", marker=dict(size=5),
    ), row=1, col=3)

    # 4 — pH
    fig.add_trace(go.Scatter(
        x=x, y=data["pH"],
        name="pH", line=dict(color="#d2a8ff", width=2),
        mode="lines+markers", marker=dict(size=5),
    ), row=2, col=1)

    # 5 — Titer
    fig.add_trace(go.Scatter(
        x=x, y=data["Titer (mg/L)"],
        name="Titer", line=dict(color=ACCENT, width=2),
        fill="tozeroy", fillcolor="rgba(0,255,159,0.05)",
        mode="lines+markers", marker=dict(size=5),
    ), row=2, col=2)

    fig.update_layout(**_base_layout())
    for ann in fig.layout.annotations:
        ann.font.color = "#7d8590"
        ann.font.size = 11
    fig.update_xaxes(**AXIS_STYLE, title_text="Day")
    fig.update_yaxes(**AXIS_STYLE)
    return fig


def make_downstream_chrom_chart(data: dict) -> go.Figure:
    """Chart for Scenario 03 — Protein A Chromatography."""
    x = data["Load Volume (CV)"]

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=["UV A280 — Breakthrough Curve", "System Pressure",
                        "Conductivity", "Flow Rate"],
        vertical_spacing=0.20,
        horizontal_spacing=0.12,
    )

    # 1 — UV breakthrough (key chart)
    fig.add_trace(go.Scatter(
        x=x, y=data["UV A280 (mAU)"],
        name="UV A280", line=dict(color="#f85149", width=2.5),
        mode="lines+markers", marker=dict(size=6, symbol="diamond"),
        fill="tozeroy", fillcolor="rgba(248,81,73,0.07)",
    ), row=1, col=1)
    fig.add_hline(
        y=50, line_dash="dash",
        line_color="rgba(248,81,73,0.4)",
        annotation_text="Breakthrough threshold",
        annotation_font_color="#f85149",
        annotation_font_size=9, row=1, col=1,
    )

    # 2 — Pressure
    fig.add_trace(go.Scatter(
        x=x, y=data["Pressure (bar)"],
        name="Pressure", line=dict(color="#f0883e", width=2),
        mode="lines+markers", marker=dict(size=5),
    ), row=1, col=2)
    fig.add_hline(
        y=1.5, line_dash="dash",
        line_color="rgba(248,81,73,0.4)",
        annotation_text="Pressure limit",
        annotation_font_color="#f85149",
        annotation_font_size=9, row=1, col=2,
    )

    # 3 — Conductivity
    fig.add_trace(go.Scatter(
        x=x, y=data["Conductivity (mS/cm)"],
        name="Conductivity", line=dict(color="#58a6ff", width=2),
        mode="lines+markers", marker=dict(size=5),
    ), row=2, col=1)

    # 4 — Flow rate
    fig.add_trace(go.Scatter(
        x=x, y=data["Flow Rate (cm/h)"],
        name="Flow Rate", line=dict(color=ACCENT, width=2),
        mode="lines+markers", marker=dict(size=5),
    ), row=2, col=2)

    fig.update_layout(**_base_layout())
    for ann in fig.layout.annotations:
        ann.font.color = "#7d8590"
        ann.font.size = 11
    fig.update_xaxes(**AXIS_STYLE, title_text="Column Volumes (CV)")
    fig.update_yaxes(**AXIS_STYLE)
    return fig


def get_chart(chart_type: str, data: dict) -> go.Figure:
    """Router — returns the right chart for each scenario."""
    if chart_type == "upstream_cho":
        return make_upstream_cho_chart(data)
    elif chart_type == "upstream_do":
        return make_upstream_do_chart(data)
    elif chart_type == "downstream_chrom":
        return make_downstream_chrom_chart(data)
    else:
        raise ValueError(f"Unknown chart_type: {chart_type}")

