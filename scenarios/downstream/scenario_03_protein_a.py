"""
BatchPilot — Scenario 03
Downstream · Protein A Affinity Chromatography · Resin Overload
"""

SCENARIO = {
    "id": "03",
    "section": "Downstream",
    "section_color": "#58a6ff",
    "title": "Protein A Capture — Column Overload",
    "process": "Protein A affinity chromatography · Post-harvest clarification",
    "difficulty": "Intermediate",
    "context_day": "Purification Run 3 · Post-harvest",
    "objective": "Maximise mAb capture yield while protecting resin lifetime",
    "role": "Downstream Scientist",

    "brief": (
        "You are the downstream scientist overseeing Protein A capture after a fed-batch CHO "
        "harvest. The column is being loaded with clarified harvest fluid at 150 cm/h.\n\n"
        "Midway through loading, you observe **UV absorbance rising in the column effluent** — "
        "earlier than expected. Pressure is within specification. The harvest titer came back "
        "higher than anticipated from the upstream run: **680 mg/L vs the expected 400 mg/L**.\n\n"
        "Your Protein A column has a dynamic binding capacity of approximately 35 mg/mL resin. "
        "The column volume is 1.5 L. You planned to load 5 L of harvest — but based on the "
        "actual titer, the load mass significantly exceeds what you calculated."
    ),

    "alert": (
        "UV A280 breakthrough rising in effluent · Load mass exceeds planned DBC · "
        "Harvest titer 70% above forecast · Currently at 65% of planned load volume"
    ),

    "batch_notes": (
        "Column: MabSelect SuRe, 1.5 L CV, HEPA-protected. "
        "Planned load: 5 L × 400 mg/L = 2,000 mg total. "
        "Actual load: 5 L × 680 mg/L = 3,400 mg total. "
        "DBC at 10% breakthrough: ~35 mg/mL → 52,500 mg total capacity. "
        "Wait — column is 1.5 L, so DBC = 35 × 1500 = 52,500 mg. Load is 3,400 mg. "
        "Recalculate: flow-through UV is rising earlier than the DBC model predicts. "
        "Possible cause: DBC has degraded after repeated cycles (this is Run 3)."
    ),

    "process_data": {
        "Load Volume (CV)":     [0,   1,   2,   3,   4,   5,   6,   7,   8],
        "UV A280 (mAU)":        [0,   5,   8,   12,  18,  45,  120, 310, 580],
        "Pressure (bar)":       [0.8, 0.9, 0.9, 1.0, 1.0, 1.1, 1.1, 1.2, 1.2],
        "Conductivity (mS/cm)": [15,  15,  15,  15,  15,  15,  15,  15,  15],
        "Flow Rate (cm/h)":     [150, 150, 150, 150, 150, 150, 150, 150, 150],
    },

    "kpis": {
        "UV Breakthrough": {"value": "Rising ↑",    "status": "critical"},
        "Pressure":        {"value": "1.2 bar",     "status": "warning"},
        "Load Volume":     {"value": "7.2 CV",      "status": "warning"},
        "Resin Capacity":  {"value": "~35 mg/mL",   "status": "normal"},
        "Harvest Titer":   {"value": "680 mg/L",    "status": "normal"},
        "Conductivity":    {"value": "15 mS/cm",    "status": "normal"},
        "Flow Rate":       {"value": "150 cm/h",    "status": "normal"},
        "Run Number":      {"value": "Cycle 3",     "status": "warning"},
    },

    "flags": [
        ("🔴", "UV breakthrough in effluent"),
        ("🟡", "Pressure trending upward"),
        ("🟡", "Resin on cycle 3 — DBC may have degraded"),
        ("🟡", "Load mass 70% above design"),
        ("🟢", "Conductivity stable"),
    ],

    "chart_type": "downstream_chrom",

    "decisions": [
        {
            "id": "A",
            "label": "A — Stop loading immediately and proceed to wash/elution",
            "quality": "correct",
            "score": 30,
            "feedback": (
                "Correct. UV breakthrough indicates the resin is approaching or has exceeded its "
                "dynamic binding capacity. Continuing to load would result in significant product "
                "loss in the flowthrough. Stopping at this point preserves the captured product "
                "and protects the resin. The remaining load volume can be pooled and re-processed "
                "in a second loading cycle."
            ),
            "expert": (
                "An experienced DSP scientist would stop loading at first sign of UV rise above "
                "baseline + 5–10%, collect the remaining harvest as a separate fraction, and "
                "assay the flowthrough for product content. If DBC degradation is suspected on "
                "cycle 3, a resin performance test (DBC determination) should be scheduled "
                "before the next run."
            ),
            "consequence": (
                "Yield preserved at ~91% in this cycle. Remaining harvest pooled for second "
                "loading cycle. Resin protected. Flowthrough assayed — confirms 8% product loss "
                "in breakthrough fraction."
            ),
        },
        {
            "id": "B",
            "label": "B — Reduce flow rate to 80 cm/h to improve binding kinetics",
            "quality": "risky",
            "score": 12,
            "feedback": (
                "Reducing flow rate increases residence time and can improve binding efficiency, "
                "but it does not resolve the root cause here: the column is overloaded relative "
                "to its available dynamic binding capacity. At this point in the breakthrough "
                "curve, slowing the flow buys marginal additional capture but does not prevent "
                "continued product loss."
            ),
            "expert": (
                "Flow rate reduction is appropriate when breakthrough is caused by kinetic "
                "limitations — the product is not binding fast enough at high flow rates. "
                "Here the cause is capacity overload. The column simply cannot bind more product "
                "regardless of flow rate. Stop loading and split the run into two cycles."
            ),
            "consequence": (
                "Yield improves marginally from 72% to ~80% in this cycle but product continues "
                "to be lost. Run takes 40% longer. Scheduling impact on downstream steps."
            ),
        },
        {
            "id": "C",
            "label": "C — Continue loading — UV rise may be a UV baseline shift or bubble",
            "quality": "wrong",
            "score": 0,
            "feedback": (
                "This is a high-risk decision. The UV pattern — gradual rise starting at ~5 CV "
                "and accelerating — is the classic signature of product breakthrough, not a "
                "baseline artefact or bubble. A bubble would cause a transient spike, not a "
                "sustained upward trend. Continuing to load will result in significant product "
                "loss in the flowthrough and potentially irreversible resin overloading."
            ),
            "expert": (
                "Never attribute a sustained UV upward trend to an artefact without evidence. "
                "If genuinely uncertain, pause loading briefly and check the flowthrough fraction "
                "with a quick off-line A280 reading. The data here does not support a baseline "
                "artefact hypothesis."
            ),
            "consequence": (
                "Product loss >30% in flowthrough. Batch yield drops to ~65%. "
                "Deviation report required. Resin may require additional regeneration cycles."
            ),
        },
        {
            "id": "D",
            "label": "D — Stop loading and strip the column — suspect resin fouling",
            "quality": "risky",
            "score": 5,
            "feedback": (
                "Resin fouling typically presents with rising pressure and abnormal UV baseline "
                "during equilibration — not clean breakthrough during loading at normal pressure. "
                "The data shows pressure is trending upward but within spec, and the UV pattern "
                "is consistent with capacity overload, not fouling. Stripping the column "
                "prematurely would discard the captured product."
            ),
            "expert": (
                "Learn to distinguish the two failure modes: "
                "Overload = UV rises during loading, pressure normal. "
                "Fouling = pressure rises progressively, UV baseline abnormal, poor peak shape. "
                "They require completely different responses. Here the signature is classic "
                "capacity overload. Proceed to elution, not strip."
            ),
            "consequence": (
                "Captured product lost during unplanned strip. Run aborted. "
                "Significant yield loss. Additional resin regeneration cycle required. "
                "Batch on hold pending investigation."
            ),
        },
    ],

    "key_concepts": [
        "**Dynamic binding capacity (DBC)** — maximum mass a resin captures under flow; "
        "always lower than static capacity and degrades with resin cycles",
        "**UV breakthrough curve** — rising UV280 in column effluent is the primary signal "
        "of DBC being approached; 10% breakthrough is the standard intervention point",
        "**Load mass calculation** — always calculate total load mass (volume × concentration), "
        "not just volume; when harvest titer varies, recalculate before loading",
        "**Cycle splitting** — when harvest volume exceeds single-cycle capacity, split into "
        "two sequential loading cycles rather than overloading",
        "**Overload vs fouling** — different root causes, different UV/pressure signatures, "
        "completely different interventions",
        "**Resin lifetime** — DBC degrades progressively with cycles; verify DBC periodically "
        "and set a resin replacement threshold",
    ],
}

