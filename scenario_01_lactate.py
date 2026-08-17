"""
BatchPilot — Scenario 01
Upstream · Fed-batch CHO · Lactate Accumulation
"""

SCENARIO = {
    "id": "01",
    "section": "Upstream",
    "section_color": "#00ff9f",
    "title": "Lactate Accumulation",
    "process": "Fed-batch CHO · mAb production",
    "difficulty": "Intermediate",
    "context_day": "Day 7 of 14",
    "objective": "Maximise titer at harvest",
    "role": "Upstream Scientist",

    "brief": (
        "You are the upstream scientist responsible for a fed-batch CHO bioreactor run "
        "producing a monoclonal antibody. This is Day 7 of a planned 14-day culture.\n\n"
        "Your morning review reveals a concerning trend: **lactate has been rising steadily "
        "since Day 4** and has now exceeded 4.9 g/L — above your facility's intervention "
        "threshold of 3.0 g/L.\n\n"
        "Concurrently, **cell viability has dropped from 95% to 78%** over the last 3 days, "
        "pH has drifted below 7.00, and dissolved oxygen is approaching its minimum setpoint. "
        "Titer is at 340 mg/L — approximately 45% of the expected end-of-run target."
    ),

    "alert": (
        "Lactate at 4.9 g/L (threshold: 3.0 g/L) · Viability 78% and declining · "
        "pH 6.92 · DO 27% · Osmolality 382 mOsm/kg"
    ),

    "batch_notes": (
        "Lactate trend is steeper than expected for this feed strategy. "
        "pH control is approaching lower setpoint limit (6.90). "
        "Viability decline rate has accelerated vs previous days. "
        "No signs of contamination detected. "
        "Next feed scheduled for Day 7 afternoon."
    ),

    "process_data": {
        "Day":                  [1,   2,    3,    4,    5,    6,    7],
        "VCD (e6/mL)":          [0.5, 1.2,  2.8,  5.1,  8.3,  11.2, 12.4],
        "Viability (%)":        [98,  97,   96,   95,   91,   85,   78],
        "Glucose (g/L)":        [6.0, 5.2,  4.1,  3.8,  3.2,  2.8,  2.5],
        "Lactate (g/L)":        [0.3, 0.5,  0.8,  1.4,  2.6,  3.8,  4.9],
        "pH":                   [7.20,7.18, 7.16, 7.12, 7.05, 6.98, 6.92],
        "DO (%)":               [40,  42,   38,   35,   33,   30,   27],
        "Titer (mg/L)":         [0,   12,   45,   110,  198,  290,  340],
        "Osmolality (mOsm/kg)": [290, 295,  305,  318,  335,  358,  382],
    },

    "kpis": {
        "VCD":        {"value": "12.4 ×10⁶/mL", "status": "normal"},
        "Viability":  {"value": "78%",           "status": "critical"},
        "Glucose":    {"value": "2.5 g/L",       "status": "warning"},
        "Lactate":    {"value": "4.9 g/L",       "status": "critical"},
        "pH":         {"value": "6.92",          "status": "critical"},
        "DO":         {"value": "27%",           "status": "warning"},
        "Titer":      {"value": "340 mg/L",      "status": "normal"},
        "Osmolality": {"value": "382 mOsm/kg",   "status": "critical"},
    },

    "flags": [
        ("🔴", "Lactate > threshold"),
        ("🔴", "Viability declining"),
        ("🔴", "pH below 7.00"),
        ("🟡", "DO approaching minimum"),
        ("🟡", "Glucose low"),
    ],

    "chart_type": "upstream_cho",

    "decisions": [
        {
            "id": "A",
            "label": "A — Reduce glucose feed rate immediately",
            "quality": "correct",
            "score": 30,
            "feedback": (
                "Good instinct. Excess glucose drives aerobic glycolysis (Warburg effect) in CHO "
                "cells, producing lactate even when oxygen is available. Reducing the feed rate "
                "decreases the glucose surplus and gives cells time to consume lactate via the TCA "
                "cycle. This is typically the first intervention at this stage."
            ),
            "expert": (
                "An experienced upstream scientist would also check the feed composition — high "
                "glutamine can be a secondary driver of lactate accumulation independent of glucose. "
                "They would reduce feed by 20–30% and monitor lactate trend over the next 12–24 "
                "hours before further action."
            ),
            "consequence": (
                "Lactate accumulation slows. Viability partially stabilises over 24–48h. "
                "Titer growth continues but at a slightly reduced rate."
            ),
        },
        {
            "id": "B",
            "label": "B — Wait 24 hours and take a new sample",
            "quality": "risky",
            "score": 10,
            "feedback": (
                "Passive monitoring is risky at this point. Lactate at 4.9 g/L with pH 6.92 and "
                "viability at 78% — and still dropping — indicates the culture is under significant "
                "metabolic stress. Waiting another 24 hours without intervention may allow "
                "irreversible damage to the cell population."
            ),
            "expert": (
                "An experienced scientist would not wait passively here. At this lactate level, "
                "there is still a window to recover. The longer you wait, the narrower that window "
                "becomes. Passive monitoring is appropriate when trends are stable — not when they "
                "are deteriorating."
            ),
            "consequence": (
                "Lactate rises to ~5.8 g/L. Viability drops to ~68%. Titer plateaus. "
                "The batch may still be recoverable but the window is narrowing."
            ),
        },
        {
            "id": "C",
            "label": "C — Increase agitation to improve oxygen transfer",
            "quality": "wrong",
            "score": 0,
            "feedback": (
                "This does not address the root cause. Lactate accumulation here is driven by "
                "metabolic overflow — too much glucose driving aerobic glycolysis — not by oxygen "
                "limitation. DO at 27% is suboptimal but not the primary driver. Increasing "
                "agitation may cause shear stress to a population already at 78% viability."
            ),
            "expert": (
                "Confusing the DO drop with the cause of lactate accumulation is a common mistake. "
                "The drop in DO is a consequence of high cell density and metabolic activity — not "
                "the cause of the problem. Always trace the issue back to its metabolic origin first."
            ),
            "consequence": (
                "Lactate continues to rise. Shear stress from increased agitation accelerates "
                "viability decline to ~70% within 12 hours."
            ),
        },
        {
            "id": "D",
            "label": "D — Harvest the batch now to preserve titer",
            "quality": "risky",
            "score": 15,
            "feedback": (
                "Premature harvest at Day 7 would capture ~340 mg/L. Typical target for this "
                "process is 600–800 mg/L at Day 12–14. You would be recovering less than half "
                "the potential yield. This is only justified if the batch is truly unrecoverable."
            ),
            "expert": (
                "Harvesting prematurely is sometimes the right call — but only after intervention "
                "has failed and viability is below 60–65% with no recovery trend. At 78% viability "
                "there is still a realistic path to recovery. Escalate to your supervisor and "
                "discuss intervention options before making a harvest decision."
            ),
            "consequence": (
                "Batch harvested at 340 mg/L — approximately 45–55% of target yield. "
                "Significant product loss. Yield deviation triggers formal review."
            ),
        },
    ],

    "key_concepts": [
        "**Warburg effect / aerobic glycolysis** — CHO cells produce lactate even under aerobic "
        "conditions when glucose is in excess",
        "**Metabolic shift** — fed-batch cultures often shift from lactate production to lactate "
        "consumption if feed is controlled correctly",
        "**pH as a proxy** — pH drift in the absence of CO₂ issues typically indicates lactate "
        "accumulation",
        "**Intervention window** — at 78% viability the batch is still recoverable; "
        "at <65% options narrow significantly",
        "**Feed strategy** — glucose feed rate is the primary lever for lactate control in CHO "
        "fed-batch",
    ],
}

