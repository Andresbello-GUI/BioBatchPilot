"""
BatchPilot — Scenario 02
Upstream · Fed-batch CHO · Dissolved Oxygen Instability
"""

SCENARIO = {
    "id": "02",
    "section": "Upstream",
    "section_color": "#00ff9f",
    "title": "Dissolved Oxygen Instability",
    "process": "Fed-batch CHO · mAb production",
    "difficulty": "Intermediate",
    "context_day": "Day 5 of 14",
    "objective": "Identify root cause of DO oscillation and stabilise the culture",
    "role": "Upstream Scientist",

    "brief": (
        "You are monitoring a fed-batch CHO bioreactor on Day 5. The culture has been "
        "growing well — VCD is at 7.2 ×10⁶/mL with 94% viability. Titer is on track.\n\n"
        "However, over the last 6 hours you have observed **irregular oscillations in dissolved "
        "oxygen (DO)** that are not following the expected control response. DO is swinging "
        "between 18% and 48% every 2–3 hours despite the cascade control being active "
        "(agitation → airflow → O₂ enrichment).\n\n"
        "Lactate is normal at 1.2 g/L. Glucose is adequate at 3.9 g/L. pH is stable at 7.15. "
        "No alarms have fired yet, but the oscillation pattern is abnormal and needs investigation."
    ),

    "alert": (
        "DO oscillating 18–48% over 6 hours · Control cascade active but ineffective · "
        "Pattern inconsistent with normal cell demand response"
    ),

    "batch_notes": (
        "DO control cascade: agitation 180–280 rpm, airflow 0.5–1.2 vvm, O₂ overlay enabled. "
        "Last calibration of DO probe: Day 0 (5 days ago). "
        "Agitation increased automatically to maximum yesterday evening. "
        "No feed bolus in the last 12 hours. "
        "Temperature stable at 37.0°C."
    ),

    "process_data": {
        "Day":            [1,   2,   3,   4,   5.0, 5.25, 5.5, 5.75, 6.0],
        "VCD (e6/mL)":    [0.4, 1.0, 2.3, 4.5, 7.2, 7.3,  7.3, 7.4,  7.5],
        "Viability (%)":  [98,  97,  97,  95,  94,  94,   93,  94,   93],
        "Glucose (g/L)":  [6.0, 5.5, 4.8, 4.2, 3.9, 3.8,  3.8, 3.7,  3.7],
        "Lactate (g/L)":  [0.2, 0.4, 0.7, 1.0, 1.2, 1.2,  1.3, 1.2,  1.3],
        "pH":             [7.20,7.19,7.18,7.17,7.15,7.15, 7.15,7.15, 7.14],
        "DO (%)":         [40,  40,  38,  35,  42,  18,   46,  20,   48],
        "Titer (mg/L)":   [0,   8,   30,  85,  155, 158,  161, 164,  167],
    },

    "kpis": {
        "VCD":       {"value": "7.4 ×10⁶/mL", "status": "normal"},
        "Viability": {"value": "93%",          "status": "normal"},
        "DO":        {"value": "18–48% oscillating", "status": "critical"},
        "Glucose":   {"value": "3.7 g/L",      "status": "normal"},
        "Lactate":   {"value": "1.3 g/L",      "status": "normal"},
        "pH":        {"value": "7.14",         "status": "normal"},
        "Titer":     {"value": "167 mg/L",     "status": "normal"},
        "Agitation": {"value": "Max (280 rpm)","status": "warning"},
    },

    "flags": [
        ("🔴", "DO oscillating — pattern abnormal"),
        ("🟡", "Agitation at maximum"),
        ("🟡", "DO probe not recalibrated since Day 0"),
        ("🟢", "Lactate normal"),
        ("🟢", "Viability stable"),
    ],

    "chart_type": "upstream_do",

    "decisions": [
        {
            "id": "A",
            "label": "A — Check and recalibrate the DO probe — suspect sensor drift",
            "quality": "correct",
            "score": 30,
            "feedback": (
                "Good first step. The oscillation pattern — regular, with swings that don't match "
                "cell demand changes — is more consistent with a sensor artefact than a biological "
                "event. After 5 days in culture, polarographic DO probes can drift significantly. "
                "The control cascade responds to the sensor signal, so if the sensor is drifting, "
                "the cascade will overcorrect and create artificial oscillations."
            ),
            "expert": (
                "An experienced scientist would first verify the probe reading against a second "
                "measurement method (e.g. optical probe if available, or a quick off-line check). "
                "If drift is confirmed, recalibrate in-situ if the system allows, or switch to a "
                "backup probe. Do not assume the biology is the cause until the instrument is ruled out."
            ),
            "consequence": (
                "Probe recalibrated. DO reading stabilises at ~35%. "
                "Control cascade returns to normal operation. Culture unaffected."
            ),
        },
        {
            "id": "B",
            "label": "B — Increase O₂ overlay to maximum to stabilise DO",
            "quality": "risky",
            "score": 10,
            "feedback": (
                "This addresses the symptom, not the cause. If the oscillation is sensor-driven, "
                "flooding the reactor with O₂ will not resolve the issue and may cause hyperoxia — "
                "DO > 60% can inhibit CHO cell growth and increase ROS production. If the root "
                "cause is genuine oxygen demand, this buys time but does not solve the problem."
            ),
            "expert": (
                "Increasing O₂ overlay is sometimes necessary as a bridging measure, but it "
                "should never be the first response without understanding the root cause. "
                "At Day 5 with normal metabolic parameters, hyperoxia is a real risk."
            ),
            "consequence": (
                "DO temporarily stabilises but oscillations resume within 4 hours. "
                "O₂ enrichment at maximum may suppress cell growth rate slightly."
            ),
        },
        {
            "id": "C",
            "label": "C — Reduce agitation — suspect shear stress from over-correction",
            "quality": "risky",
            "score": 8,
            "feedback": (
                "Reducing agitation when the culture is already struggling to meet oxygen demand "
                "is counterproductive. Agitation is the first line of the DO control cascade — "
                "reducing it will likely cause DO to drop further. The hypothesis of "
                "shear-driven oscillation does not fit: shear stress would show in viability "
                "decline, which is not occurring here."
            ),
            "expert": (
                "Shear stress from agitation typically presents as progressive viability decline "
                "and cell aggregation — not DO oscillation. Rule out the simpler explanations "
                "(sensor, control loop tuning) before touching the agitation strategy."
            ),
            "consequence": (
                "DO drops to 12% within 2 hours. Agitation reduced further. "
                "Culture shows mild stress response — viability drops to 89%."
            ),
        },
        {
            "id": "D",
            "label": "D — Pause the control cascade and switch to manual DO control",
            "quality": "wrong",
            "score": 0,
            "feedback": (
                "Manual DO control in a fed-batch CHO bioreactor is not a standard response and "
                "introduces significant human error risk. In a GMP environment this would require "
                "immediate supervisor approval and extensive documentation. The oscillation pattern "
                "does not justify bypassing automated control — it justifies investigating the "
                "sensor and control loop first."
            ),
            "expert": (
                "Switching to manual control is a last resort when the automated system has "
                "demonstrably failed. Here, the automated system is working — it is responding to "
                "what it believes the DO is. The problem is likely in the input (sensor), "
                "not in the control logic."
            ),
            "consequence": (
                "Manual control introduces lag and inconsistency. DO drops to 8% before "
                "correction is applied. Viability drops to 85%. Deviation report required for "
                "bypassing automated control without documented justification."
            ),
        },
    ],

    "key_concepts": [
        "**DO control cascade** — typical sequence: agitation → airflow → O₂ enrichment → "
        "CO₂ reduction; each step activates when the previous is maxed",
        "**Sensor drift** — polarographic probes drift over time and require periodic "
        "recalibration; optical probes are more stable but also require verification",
        "**Root cause vs symptom** — always distinguish between the signal (DO oscillation) "
        "and its origin (sensor, cell demand, control tuning, equipment)",
        "**Hyperoxia risk** — DO consistently above 60% can inhibit CHO growth and increase "
        "reactive oxygen species; more O₂ is not always better",
        "**Control loop hunting** — if a PID controller is poorly tuned, it can create "
        "oscillations independent of the biology",
    ],
}

