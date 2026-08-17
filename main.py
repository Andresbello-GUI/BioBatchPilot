"""
BatchPilot — main.py
Bioprocess Training Simulator · MVP

Run with:
    streamlit run main.py

Install dependencies (once):
    pip install streamlit plotly pandas numpy
"""

import streamlit as st
import pandas as pd

# ── Scenario imports ──────────────────────────────────────────────────────────
from scenarios.upstream.scenario_01_lactate      import SCENARIO as S01
from scenarios.upstream.scenario_02_do_instability import SCENARIO as S02
from scenarios.downstream.scenario_03_protein_a  import SCENARIO as S03

# ── Chart engine ──────────────────────────────────────────────────────────────
from components.charts import get_chart

# ─────────────────────────────────────────────────────────────────────────────
# SCENARIO REGISTRY — add new scenarios here, nothing else changes
# ─────────────────────────────────────────────────────────────────────────────
ALL_SCENARIOS = {
    "01": S01,
    "02": S02,
    "03": S03,
}

SECTION_ORDER = ["Upstream", "Downstream"]

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BatchPilot",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
.stApp { background-color: #0d1117; color: #e6edf3; }

.bp-header { background: linear-gradient(135deg,#0d1117 0%,#161b22 100%);
    border-bottom: 1px solid rgba(0,255,159,0.2); padding: 16px 24px; margin-bottom: 24px; }
.bp-logo { font-family:'IBM Plex Mono',monospace; font-size:1.6rem; font-weight:600;
    color:#00ff9f; letter-spacing:-0.5px; }
.bp-tagline { font-size:0.75rem; color:#7d8590; letter-spacing:2px;
    text-transform:uppercase; margin-top:2px; }

.scenario-card { background:#161b22; border:1px solid #30363d;
    border-left:3px solid var(--sc); border-radius:8px; padding:20px 24px; margin-bottom:20px; }
.scenario-title { font-family:'IBM Plex Mono',monospace; font-size:0.7rem;
    color:var(--sc); text-transform:uppercase; letter-spacing:2px; margin-bottom:6px; }
.scenario-name { font-size:1.3rem; font-weight:700; color:#e6edf3; margin-bottom:10px; }
.meta-tag { background:#21262d; border:1px solid #30363d; border-radius:4px;
    padding:4px 10px; font-size:0.75rem; color:#8b949e;
    font-family:'IBM Plex Mono',monospace; display:inline-block; margin:2px; }

.alert-box { background:#1f1507; border:1px solid rgba(240,136,62,0.27);
    border-left:3px solid #f0883e; border-radius:6px;
    padding:14px 18px; margin:14px 0; font-size:0.88rem; color:#e6c88a; }
.alert-title { font-family:'IBM Plex Mono',monospace; font-weight:600;
    font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;
    color:#f0883e; margin-bottom:4px; }

.section-header { font-family:'IBM Plex Mono',monospace; font-size:0.68rem;
    color:#7d8590; text-transform:uppercase; letter-spacing:2px;
    border-bottom:1px solid #21262d; padding-bottom:8px; margin-bottom:14px; }

.stButton > button { background:#161b22 !important; border:1px solid #30363d !important;
    color:#e6edf3 !important; border-radius:6px !important;
    font-family:'IBM Plex Sans',sans-serif !important; font-size:0.85rem !important;
    text-align:left !important; padding:12px 16px !important;
    width:100% !important; white-space:normal !important; height:auto !important; }
.stButton > button:hover { background:#21262d !important;
    border-color:rgba(0,255,159,0.53) !important; color:#00ff9f !important; }

.feedback-correct { background:#0d2218; border:1px solid rgba(0,255,159,0.27);
    border-left:3px solid #00ff9f; border-radius:8px; padding:20px 24px; margin-top:20px; }
.feedback-risky { background:#1f1507; border:1px solid rgba(240,136,62,0.27);
    border-left:3px solid #f0883e; border-radius:8px; padding:20px 24px; margin-top:20px; }
.feedback-wrong { background:#1c0e0e; border:1px solid rgba(248,81,73,0.27);
    border-left:3px solid #f85149; border-radius:8px; padding:20px 24px; margin-top:20px; }
.feedback-label { font-family:'IBM Plex Mono',monospace; font-size:0.68rem;
    text-transform:uppercase; letter-spacing:2px; margin-bottom:8px; }
.feedback-text { font-size:0.9rem; line-height:1.7; color:#c9d1d9; }

.expert-note { background:#161b22; border:1px solid #30363d; border-radius:6px;
    padding:12px 16px; margin-top:14px; font-size:0.82rem;
    color:#8b949e; font-style:italic; }
.expert-note strong { color:#58a6ff; font-style:normal;
    font-family:'IBM Plex Mono',monospace; font-size:0.72rem;
    text-transform:uppercase; letter-spacing:1px; }

.score-box { background:#161b22; border:1px solid #30363d;
    border-radius:8px; padding:16px; text-align:center; }
.score-number { font-family:'IBM Plex Mono',monospace; font-size:2.2rem;
    font-weight:600; color:#00ff9f; }
.score-label { font-size:0.72rem; color:#7d8590;
    text-transform:uppercase; letter-spacing:1px; }

.kpi-chip { background:#161b22; border:1px solid #30363d;
    border-radius:6px; padding:10px 14px; display:inline-block;
    min-width:110px; margin:4px; }
.kpi-name { font-family:'IBM Plex Mono',monospace; font-size:0.65rem;
    color:#7d8590; text-transform:uppercase; letter-spacing:1px; }
.kpi-value { font-family:'IBM Plex Mono',monospace; font-size:1.0rem;
    font-weight:600; margin-top:2px; }
.kpi-normal   { color:#00ff9f; }
.kpi-warning  { color:#f0883e; }
.kpi-critical { color:#f85149; }

.progress-bar-container { background:#21262d; border-radius:4px;
    height:4px; margin-bottom:20px; }
.progress-bar-fill { background:linear-gradient(90deg,#00ff9f,#58a6ff);
    height:4px; border-radius:4px; }

/* Scenario selector cards */
.scenario-pick { background:#161b22; border:1px solid #30363d;
    border-radius:8px; padding:16px; margin-bottom:10px; cursor:pointer; }
.scenario-pick:hover { border-color:rgba(0,255,159,0.4); }

#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "page":           "home",   # home | scenario
        "active_id":      None,
        "step":           "brief",  # brief | data | decision | feedback | complete
        "score":          0,
        "chosen_action":  None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


def reset_scenario():
    st.session_state.step          = "brief"
    st.session_state.score         = 0
    st.session_state.chosen_action = None


def go_home():
    st.session_state.page      = "home"
    st.session_state.active_id = None
    reset_scenario()


def launch_scenario(sid: str):
    st.session_state.page      = "scenario"
    st.session_state.active_id = sid
    reset_scenario()


# ─────────────────────────────────────────────────────────────────────────────
# SHARED HEADER
# ─────────────────────────────────────────────────────────────────────────────
def render_header():
    st.markdown("""
    <div class="bp-header">
        <div class="bp-logo">⬡ BatchPilot</div>
        <div class="bp-tagline">Bioprocess Decision Simulator · MVP Alpha</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────────────────────────────────────────
def render_home():
    render_header()

    st.markdown("""
    <div style="max-width:680px; margin-bottom:32px">
        <div style="font-size:1.5rem; font-weight:700; color:#e6edf3; margin-bottom:10px">
            Practice biomanufacturing decisions<br>before you make them in a real GMP environment.
        </div>
        <div style="font-size:0.92rem; color:#8b949e; line-height:1.8">
            Each scenario places you inside a real bioprocess situation. You interpret data,
            choose actions, and see consequences — with expert feedback explaining what an
            experienced scientist would do next.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Group by section
    by_section = {}
    for sid, sc in ALL_SCENARIOS.items():
        sec = sc["section"]
        by_section.setdefault(sec, []).append((sid, sc))

    for section in SECTION_ORDER:
        if section not in by_section:
            continue

        color = by_section[section][0][1]["section_color"]
        st.markdown(
            f'<div class="section-header" style="color:{color}">'
            f'{section.upper()}</div>',
            unsafe_allow_html=True,
        )

        for sid, sc in by_section[section]:
            col_info, col_btn = st.columns([4, 1], gap="small")
            with col_info:
                st.markdown(f"""
                <div style="padding:4px 0">
                    <span style="font-family:'IBM Plex Mono',monospace; font-size:0.65rem;
                        color:{color}; text-transform:uppercase; letter-spacing:1px">
                        Scenario {sid}
                    </span>
                    <div style="font-size:1rem; font-weight:600; color:#e6edf3; margin:2px 0">
                        {sc['title']}
                    </div>
                    <div style="font-size:0.8rem; color:#8b949e">
                        {sc['process']} · {sc['context_day']} · {sc['difficulty']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                if st.button("Start →", key=f"start_{sid}"):
                    launch_scenario(sid)
                    st.rerun()

            st.markdown(
                "<hr style='border:none; border-top:1px solid #21262d; margin:8px 0'>",
                unsafe_allow_html=True,
            )

    # Stats bar
    total = len(ALL_SCENARIOS)
    upstream_count   = sum(1 for s in ALL_SCENARIOS.values() if s["section"] == "Upstream")
    downstream_count = sum(1 for s in ALL_SCENARIOS.values() if s["section"] == "Downstream")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    for col, val, label in [
        (c1, total,            "Total Scenarios"),
        (c2, upstream_count,   "Upstream"),
        (c3, downstream_count, "Downstream"),
        (c4, "—",              "GMP · Coming soon"),
    ]:
        with col:
            st.markdown(f"""
            <div class="score-box">
                <div class="score-number" style="font-size:1.6rem">{val}</div>
                <div class="score-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SCENARIO ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def render_scenario(sc: dict):
    render_header()

    # Progress bar
    progress_map = {"brief": 15, "data": 40, "decision": 65, "feedback": 88, "complete": 100}
    prog = progress_map.get(st.session_state.step, 15)
    st.markdown(f"""
    <div class="progress-bar-container">
        <div class="progress-bar-fill" style="width:{prog}%"></div>
    </div>
    """, unsafe_allow_html=True)

    col_main, col_side = st.columns([3, 1], gap="large")

    # ── SIDEBAR ──
    with col_side:
        st.markdown('<div class="section-header">Session</div>', unsafe_allow_html=True)
        score = st.session_state.score
        sc_color = "#00ff9f" if score >= 25 else "#f0883e" if score >= 10 else "#f85149"
        st.markdown(f"""
        <div class="score-box">
            <div class="score-number" style="color:{sc_color}">{score}</div>
            <div class="score-label">Score</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Scenario</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:0.78rem; color:#8b949e; line-height:1.9">
            <b style="color:#e6edf3">Section:</b> {sc['section']}<br>
            <b style="color:#e6edf3">Process:</b> {sc['process']}<br>
            <b style="color:#e6edf3">Stage:</b> {sc['context_day']}<br>
            <b style="color:#e6edf3">Objective:</b> {sc['objective']}<br>
            <b style="color:#e6edf3">Role:</b> {sc['role']}
        </div>
        """, unsafe_allow_html=True)

        if sc.get("flags"):
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">Flags</div>', unsafe_allow_html=True)
            flags_html = "<div style='font-size:0.8rem; line-height:2.1'>"
            for icon, text in sc["flags"]:
                flags_html += f"{icon} {text}<br>"
            flags_html += "</div>"
            st.markdown(flags_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← All Scenarios"):
            go_home()
            st.rerun()
        if st.session_state.step != "brief":
            if st.button("↩ Restart"):
                reset_scenario()
                st.rerun()

    # ── MAIN CONTENT ──
    with col_main:
        color = sc["section_color"]

        # ── BRIEF ──
        if st.session_state.step == "brief":
            st.markdown(f"""
            <div class="scenario-card" style="--sc:{color}">
                <div class="scenario-title">Scenario {sc['id']} · {sc['section']}</div>
                <div class="scenario-name">{sc['title']}</div>
                <span class="meta-tag">{sc['process']}</span>
                <span class="meta-tag">{sc['context_day']}</span>
                <span class="meta-tag">{sc['difficulty']}</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(sc["brief"])

            st.markdown(f"""
            <div class="alert-box">
                <div class="alert-title">⚠ Process Alert</div>
                {sc['alert']}
            </div>
            """, unsafe_allow_html=True)

            if st.button("→ Review Process Data", use_container_width=True):
                st.session_state.step = "data"
                st.rerun()

        # ── DATA ──
        elif st.session_state.step == "data":
            st.markdown('<div class="section-header">Process Data</div>', unsafe_allow_html=True)

            # KPI chips
            kpis_html = "<div>"
            for name, info in sc["kpis"].items():
                kpis_html += f"""
                <div class="kpi-chip">
                    <div class="kpi-name">{name}</div>
                    <div class="kpi-value kpi-{info['status']}">{info['value']}</div>
                </div>"""
            kpis_html += "</div><br>"
            st.markdown(kpis_html, unsafe_allow_html=True)

            # Chart
            fig = get_chart(sc["chart_type"], sc["process_data"])
            st.plotly_chart(fig, use_container_width=True,
                            config={"displayModeBar": False})

            # Raw data toggle
            with st.expander("View raw data table"):
                df = pd.DataFrame(sc["process_data"])
                x_col = df.columns[0]
                st.dataframe(df.set_index(x_col), use_container_width=True)

            # Batch notes
            if sc.get("batch_notes"):
                st.markdown(f"""
                <div class="alert-box">
                    <div class="alert-title">📋 Batch Notes</div>
                    {sc['batch_notes']}
                </div>
                """, unsafe_allow_html=True)

            if st.button("→ Make Decision", use_container_width=True):
                st.session_state.step = "decision"
                st.rerun()

        # ── DECISION ──
        elif st.session_state.step == "decision":
            st.markdown('<div class="section-header">Decision Panel</div>',
                        unsafe_allow_html=True)
            st.markdown(
                "Based on the process data, **what is your immediate action?** "
                "Choose carefully — each decision has consequences on the process outcome."
            )
            st.markdown("<br>", unsafe_allow_html=True)

            for d in sc["decisions"]:
                if st.button(d["label"], key=f"dec_{d['id']}", use_container_width=True):
                    st.session_state.chosen_action = d["id"]
                    st.session_state.score += d["score"]
                    st.session_state.step = "feedback"
                    st.rerun()

        # ── FEEDBACK ──
        elif st.session_state.step == "feedback":
            chosen = next(
                d for d in sc["decisions"]
                if d["id"] == st.session_state.chosen_action
            )
            quality_map = {
                "correct": ("correct", "✓ Correct Action",          "#00ff9f"),
                "risky":   ("risky",   "⚠ Risky — Partially Correct","#f0883e"),
                "wrong":   ("wrong",   "✗ Incorrect Action",         "#f85149"),
            }
            css, label_text, label_color = quality_map[chosen["quality"]]

            st.markdown(f"""
            <div class="feedback-{css}">
                <div class="feedback-label" style="color:{label_color}">{label_text}</div>
                <div style="font-weight:600; color:#e6edf3; margin-bottom:10px">
                    {chosen['label']}
                </div>
                <div class="feedback-text">{chosen['feedback']}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="expert-note">
                <strong>What an experienced scientist would check next</strong><br><br>
                {chosen['expert']}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">Consequence</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:#161b22; border:1px solid #30363d; border-radius:6px;
                        padding:14px 18px; font-size:0.87rem; color:#8b949e; line-height:1.7">
                {chosen['consequence']}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("↩ Try another decision", use_container_width=True):
                    st.session_state.step = "decision"
                    st.session_state.chosen_action = None
                    st.rerun()
            with c2:
                if st.button("→ Complete Scenario", use_container_width=True):
                    st.session_state.step = "complete"
                    st.rerun()

        # ── COMPLETE ──
        elif st.session_state.step == "complete":
            score = st.session_state.score
            if score >= 25:
                grade, gc, gm = "Excellent",    "#00ff9f", "Strong process reasoning. You identified the root cause and acted appropriately."
            elif score >= 12:
                grade, gc, gm = "Acceptable",   "#f0883e", "You recognised the problem but your action introduced unnecessary risk."
            else:
                grade, gc, gm = "Needs Review", "#f85149", "The chosen action did not address the root cause. Review the key concepts below."

            st.markdown(f"""
            <div style="background:#161b22; border:1px solid #30363d; border-radius:10px;
                        padding:30px; text-align:center; margin-bottom:24px">
                <div style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem;
                    color:#7d8590; letter-spacing:2px; text-transform:uppercase; margin-bottom:10px">
                    Scenario Complete · {sc['title']}
                </div>
                <div style="font-size:3rem; font-weight:700;
                    font-family:'IBM Plex Mono',monospace; color:{gc}">{score}</div>
                <div style="color:{gc}; font-weight:600; margin:8px 0">{grade}</div>
                <div style="color:#8b949e; font-size:0.87rem; max-width:420px;
                    margin:0 auto; line-height:1.7">{gm}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-header">Key Concepts</div>', unsafe_allow_html=True)
            for concept in sc.get("key_concepts", []):
                st.markdown(f"- {concept}")

            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("↩ Restart This Scenario", use_container_width=True):
                    reset_scenario()
                    st.rerun()
            with c2:
                if st.button("← All Scenarios", use_container_width=True):
                    go_home()
                    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "scenario":
    sid = st.session_state.active_id
    sc  = ALL_SCENARIOS.get(sid)
    if sc:
        render_scenario(sc)
    else:
        go_home()
        st.rerun()

#streamlit run main.py