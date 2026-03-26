# import gradio as gr
# import pandas as pd
# import re
# import base64
# import matplotlib
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt
# import matplotlib.figure
# import numpy as np
# from datetime import datetime
# from PIL import Image, ImageDraw, ImageFont
# import os
# from io import BytesIO
# from groq import Groq
# import threading

# # ══════════════════════════════════════════════════════════════════
# #  GROQ CONFIG
# # ══════════════════════════════════════════════════════════════════
# _api_key = os.environ.get("GROQ_API_KEY")
# groq_client = Groq(api_key=_api_key) if _api_key else None
# GROQ_MODEL  = "llama-3.3-70b-versatile"


# def llm_evaluate_answer(phase_name, focus, label, question_text, user_answer):
#     if not groq_client:
#         return "⚠️ Setup Required: GROQ_API_KEY is missing from environment secrets."
#     if not user_answer or not user_answer.strip():
#         return ""
#     prompt = f"""You are an expert startup mentor evaluating a founder's answer.

# Phase     : {phase_name}
# Focus Area: {focus}
# Question  : [{label}] {question_text}
# Founder's Answer: {user_answer}

# Respond in EXACTLY this format (no extra text):
# SCORE: X/10
# FEEDBACK: (2-3 sentences of constructive mentor feedback)
# STRENGTH: (one key strength in this answer)
# GAP: (one area to improve or think deeper about)

# Be encouraging but honest. Keep total response under 100 words."""
#     try:
#         response = groq_client.chat.completions.create(
#             model=GROQ_MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.3
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return f"⚠️ AI Mentor unavailable: {str(e)}"


# def parse_ai_score(ai_feedback_text):
#     if not ai_feedback_text:
#         return None
#     m = re.search(r'SCORE:\s*(\d+(?:\.\d+)?)\s*/\s*10', ai_feedback_text, re.IGNORECASE)
#     if m:
#         return round(min(float(m.group(1)), 10.0) / 10.0, 2)
#     return None


# def llm_phase_report(phase_name, focus, all_qa_pairs):
#     if not groq_client:
#         return "⚠️ Cannot generate report: GROQ_API_KEY is missing."
#     qa_text = "\n".join([
#         f"Q{i+1}: {q}\nA: {a if a.strip() else '[SKIPPED]'}"
#         for i, (q, a) in enumerate(all_qa_pairs)
#     ])
#     prompt = f"""You are a senior startup mentor writing a phase assessment report.

# Phase     : {phase_name}
# Focus Area: {focus}

# The founder answered these 18 questions:
# {qa_text}

# Write a structured report with EXACTLY these sections:

# ## {phase_name} — {focus} Assessment

# **Overall Score: X/10**

# **Executive Summary** (3-4 sentences)

# **Key Strengths**
# - strength 1
# - strength 2
# - strength 3

# **Critical Gaps**
# - gap 1
# - gap 2
# - gap 3

# **Elephants in the Room** (2-3 sentences about the EIR answers)

# **Mentor Recommendation** (2-3 sentences on what to focus on next)

# Keep total report under 300 words. Be direct and actionable."""
#     try:
#         response = groq_client.chat.completions.create(
#             model=GROQ_MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.4
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return f"⚠️ AI Mentor unavailable: {str(e)}"


# def llm_hitl_report(all_data, founder_name):
#     if not groq_client:
#         return "⚠️ Cannot generate final report: GROQ_API_KEY is missing."
#     phases_summary = []
#     for phase in clean_phases:
#         qs       = get_all_qs(phase)
#         pd_      = all_data.get(phase, {})
#         focus    = get_focus_for_phase(phase)
#         answered = sum(1 for q in qs if q in pd_ and pd_[q].get("response", "").strip())
#         skipped  = sum(1 for q in qs if q in pd_ and not pd_[q].get("response", "").strip())
#         phases_summary.append(f"- {phase} [{focus}]: {answered}/18 answered, {skipped} skipped")
#     summary_text = "\n".join(phases_summary)
#     prompt = f"""You are the Chief Mentor at i2u.ai writing a confidential founder assessment.

# Founder Name: {founder_name or "The Founder"}

# Phase Completion Summary:
# {summary_text}

# Write a comprehensive HITL (Human in the Loop) report with EXACTLY these sections:

# # Unicorn Foundational Assessment — HITL Report
# ## Founder: {founder_name or "The Founder"}

# ### 1. Executive Overview
# (4-5 sentences)

# ### 2. Unicorn Potential Score: X/100

# ### 3. Phase-by-Phase Analysis
# (2 sentences per phase)

# ### 4. Top 3 Founder Strengths
# - strength 1
# - strength 2
# - strength 3

# ### 5. Top 3 Critical Risks
# - risk 1
# - risk 2
# - risk 3

# ### 6. Recommended 90-Day Action Plan
# - action 1
# - action 2
# - action 3

# ### 7. Mentor's Verdict
# (3-4 sentences — honest overall assessment)

# Keep total report under 500 words. This is a confidential professional assessment."""
#     try:
#         response = groq_client.chat.completions.create(
#             model=GROQ_MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.5
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return f"⚠️ AI Mentor unavailable: {str(e)}"


# # ── Logo ──
# try:
#     with open('WhatsApp Image 2026-03-19 at 2.43.33 PM.jpeg', 'rb') as _f:
#         LOGO_B64 = base64.b64encode(_f.read()).decode()
# except FileNotFoundError:
#     LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

# LOGO_SRC = f"data:image/png;base64,{LOGO_B64}"

# FOCUS_LABELS = [
#     "Resilience", "Validation", "Feasibility", "Traction", "Growth",
#     "Profit",     "Innovation", "Legacy",      "Stewardship"
# ]
# phase_focus_map = {}
# score_data      = {}

# # ══════════════════════════════════════════════════════════════════
# #  CSS
# # ══════════════════════════════════════════════════════════════════
# CSS = """
# @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;900&family=Sora:wght@300;400;600&display=swap');

# :root {
#     --bg:     #07081a;
#     --card:   #0d1035;
#     --gold:   #f59e0b;
#     --violet: #6d28d9;
#     --text:   #e2e8f0;
#     --dim:    #64748b;
# }

# .gradio-container { max-width: 100% !important; }

# footer { display: none !important; }
# .footer { display: none !important; }
# gradio-app footer { display: none !important; }
# div[class*="footer"] { display: none !important; }
# .svelte-1ed2p3z { display: none !important; }
# #footer { display: none !important; }
# body, .gradio-container {
#     background: var(--bg) !important;
#     font-family: 'Sora', sans-serif !important;
#     color: var(--text) !important;
# }
# h1,h2,h3,h4 { font-family: 'Outfit', sans-serif !important; }
# .c, .c * { text-align: center !important; }

# input, textarea, select {
#     background: #0a0c25 !important;
#     border: 1px solid rgba(109,40,217,0.40) !important;
#     border-radius: 12px !important;
#     color: var(--text) !important;
#     font-family: 'Sora', sans-serif !important;
# }
# input:focus, textarea:focus {
#     border-color: var(--gold) !important;
#     box-shadow: 0 0 0 3px rgba(245,158,11,0.15) !important;
#     outline: none !important;
# }
# label span {
#     font-family: 'Outfit', sans-serif !important;
#     font-weight: 700 !important;
#     color: #c4b5fd !important;
# }

# .logo-header {
#     display: flex !important;
#     flex-direction: column !important;
#     align-items: center !important;
#     justify-content: center !important;
#     padding: 18px 20px 14px !important;
#     background: linear-gradient(180deg, rgba(13,16,53,0.98) 0%, rgba(7,8,26,0.85) 100%) !important;
#     border-bottom: 1px solid rgba(109,40,217,0.28) !important;
#     margin-bottom: 8px !important;
#     text-align: center !important;
#     width: 100% !important;
#     box-sizing: border-box !important;
#     overflow: hidden !important;
# }
# .logo-header img {
#     width: 72px !important; height: 72px !important;
#     border-radius: 18px !important; object-fit: cover !important;
#     box-shadow: 0 4px 16px rgba(109,40,217,0.60), 0 0 0 2px rgba(245,158,11,0.45) !important;
#     margin: 0 auto 10px auto !important; display: block !important;
# }
# .logo-header .brand-name {
#     font-family: 'Outfit', sans-serif !important;
#     font-size: 1.8em !important; font-weight: 900 !important;
#     background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 45%, #8b5cf6 100%) !important;
#     -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
#     background-clip: text !important; letter-spacing: 2px !important;
# }
# .logo-header .tagline {
#     font-family: 'Sora', sans-serif !important; font-size: 0.85em !important;
#     color: #94a3b8 !important; letter-spacing: 1.2px !important; margin-top: 3px !important;
# }
# .question-title {
#     text-align: center !important; font-family: 'Outfit', sans-serif !important;
#     font-weight: 900 !important; font-size: 1.45em !important; color: #f59e0b !important;
#     letter-spacing: 1.5px !important; margin-bottom: 6px !important; padding: 10px 0 4px 0 !important;
# }
# .question-display {
#     background: rgba(109,40,217,0.12) !important;
#     border: 1.5px solid rgba(109,40,217,0.35) !important;
#     border-radius: 14px !important; padding: 18px 20px !important; margin-bottom: 12px !important;
# }
# .question-display p, .question-display * {
#     font-size: 1.15em !important; font-weight: 700 !important;
#     font-family: 'Outfit', sans-serif !important; color: #f8fafc !important;
#     line-height: 1.75 !important; margin: 0 !important;
# }
# .response-box textarea {
#     min-height: 100px !important; max-height: 160px !important;
#     overflow-y: auto !important; font-size: 0.98em !important;
#     line-height: 1.7 !important; border-radius: 12px !important;
#     padding: 12px !important; resize: vertical !important;
# }
# .eir-warning {
#     background: rgba(239,68,68,0.12) !important; border: 2px solid #ef4444 !important;
#     border-radius: 12px !important; padding: 14px 18px !important; margin-bottom: 12px !important;
# }
# .eir-warning p, .eir-warning * { color: #fca5a5 !important; font-weight: 600 !important; margin: 0 !important; }
# .skip-warning {
#     background: rgba(245,158,11,0.10) !important; border: 2px solid #f59e0b !important;
#     border-radius: 12px !important; padding: 14px 18px !important; margin-bottom: 12px !important;
# }
# .skip-warning p, .skip-warning * { color: #fde68a !important; font-weight: 600 !important; margin: 0 !important; }
# .save-st p {
#     padding: 12px 18px !important; border-radius: 12px !important;
#     background: rgba(34,197,94,0.10) !important; border-left: 4px solid #22c55e !important;
#     font-size: 0.92em !important; color: #86efac !important;
# }

# /* AI feedback loading animation */
# .ai-loading {
#     display: flex; align-items: center; gap: 10px;
#     padding: 12px 18px; border-radius: 12px;
#     background: rgba(109,40,217,0.10); border-left: 4px solid #6d28d9;
#     font-family: 'Sora', sans-serif; font-size: 0.92em; color: #c4b5fd;
# }
# .ai-loading-dots span {
#     display: inline-block; width: 6px; height: 6px; border-radius: 50%;
#     background: #8b5cf6; margin: 0 2px;
#     animation: bounce 1.2s infinite;
# }
# .ai-loading-dots span:nth-child(2) { animation-delay: 0.2s; }
# .ai-loading-dots span:nth-child(3) { animation-delay: 0.4s; }
# @keyframes bounce { 0%,80%,100%{transform:translateY(0)} 40%{transform:translateY(-6px)} }

# .hitl-block {
#     border-left: 3px solid var(--gold) !important;
#     background: rgba(245,158,11,0.05) !important;
#     border-radius: 0 12px 12px 0 !important; padding: 12px 16px !important;
# }
# .footer-md, .footer-md * {
#     text-align: center !important; color: var(--dim) !important; font-size: 0.82em !important;
# }
# .upload-compact button {
#     background: rgba(109,40,217,0.18) !important;
#     border: 1px solid rgba(109,40,217,0.45) !important;
#     border-radius: 10px !important; color: #c4b5fd !important;
#     font-family: 'Outfit', sans-serif !important; font-weight: 700 !important;
#     padding: 12px 24px !important; width: 100% !important; cursor: pointer !important;
# }
# .upload-compact .dnd-zone,
# .upload-compact [data-testid="drop-text"],
# .upload-compact .or { display: none !important; }

# .phase-btn button {
#     min-height: 130px !important; width: 100% !important;
#     border-radius: 22px !important; border: 1.5px solid rgba(56,168,245,0.45) !important;
#     cursor: pointer !important; font-family: 'Outfit', sans-serif !important;
#     font-size: 0.95em !important; font-weight: 700 !important;
#     white-space: normal !important; text-align: center !important;
#     padding: 20px 16px !important; color: #ffffff !important;
#     text-shadow: 0 1px 6px rgba(0,0,0,0.55) !important;
#     background:
#         linear-gradient(180deg,rgba(255,255,255,0.32) 0%,rgba(255,255,255,0.10) 30%,transparent 55%,rgba(0,0,0,0.22) 100%),
#         linear-gradient(170deg,#1e3a8a 0%,#1e40af 30%,#1a3fa8 65%,#0f2472 100%) !important;
#     box-shadow: inset 0 4px 8px rgba(255,255,255,0.22), 0 8px 0 #0a1a55, 0 14px 28px rgba(0,0,0,0.70) !important;
#     transition: transform 0.16s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.16s ease !important;
#     display: flex !important; flex-direction: column !important;
#     align-items: center !important; justify-content: center !important;
# }
# .phase-btn button:hover {
#     transform: translateY(-8px) scale(1.03) !important;
#     border-color: rgba(56,168,245,0.90) !important;
#     background:
#         linear-gradient(180deg,rgba(255,255,255,0.42) 0%,rgba(255,255,255,0.14) 30%,transparent 55%,rgba(0,0,0,0.12) 100%),
#         linear-gradient(170deg,#60c8ff 0%,#38a8f5 25%,#1e7dd4 55%,#104ea0 100%) !important;
#     box-shadow: inset 0 4px 10px rgba(255,255,255,0.38), 0 8px 0 #082a60,
#         0 20px 40px rgba(0,0,0,0.80), 0 0 28px rgba(56,168,245,0.70) !important;
# }
# .phase-btn button:active {
#     transform: translateY(5px) scale(0.974) !important;
#     filter: brightness(0.78) !important;
# }
# .hidden-btn { display: none !important; }
# .custom-drag-drop {
#     border: 2px dashed rgba(109, 40, 217, 0.8) !important;
#     background: #14102c !important; border-radius: 12px !important;
#     min-height: 120px !important;
# }
# """

# # ══════════════════════════════════════════════════════════════════
# #  DATA LOADING
# # ══════════════════════════════════════════════════════════════════
# def prettify_name(text):
#     text = str(text).replace("_", " ").replace("-", " ")
#     return re.sub(r'\s+', ' ', text).strip().title()

# PHASE_META = {
#     "conception": {"emoji": "✨"}, "spark": {"emoji": "✨"},
#     "initiation":  {"emoji": "🎯"}, "hunt":  {"emoji": "🎯"},
#     "formulation": {"emoji": "🔨"}, "build": {"emoji": "🔨"},
#     "market entry":{"emoji": "🚀"}, "launch":{"emoji": "🚀"},
#     "scaling":     {"emoji": "📈"}, "rocket":{"emoji": "📈"},
#     "efficiency":  {"emoji": "⚙️"},  "optimization":{"emoji": "⚙️"},
#     "leadership":  {"emoji": "🏛️"}, "institution":  {"emoji": "🏛️"},
#     "unicorn":     {"emoji": "🦄"}, "dominance":    {"emoji": "🦄"},
#     "masters":     {"emoji": "⭐"}, "jedi":         {"emoji": "⭐"},
#     "return":      {"emoji": "⭐"},
# }

# def get_emoji(name):
#     lower = name.lower()
#     for k, v in PHASE_META.items():
#         if k in lower: return v["emoji"]
#     return "📂"

# try:
#     df = pd.read_excel("Refined_Startup_Assessment_Questions.xlsx")
#     df.columns = df.columns.str.strip()
#     phase_col    = next((c for c in df.columns if c.lower() in ['level','phase','stage','phases']), df.columns[0])
#     question_col = next((c for c in df.columns if c.lower() in ['question','questions','criteria','description']), df.columns[-1])
#     score_col    = next((c for c in df.columns if c.lower() in ['base_score','score','base score']), None)
#     df = df.dropna(subset=[phase_col, question_col])
#     df = df[df[phase_col].astype(str).str.lower() != 'level name']
#     raw_phases         = df[phase_col].astype(str).unique().tolist()
#     ui_to_raw_map      = {prettify_name(p): p for p in raw_phases}
#     pretty_phases_list = list(ui_to_raw_map.keys())
#     excel_data         = df.groupby(phase_col)[question_col].apply(lambda x: [str(q) for q in x]).to_dict()
#     if score_col:
#         score_data = df.groupby(phase_col)[score_col].apply(
#             lambda x: [float(v) for v in x]
#         ).to_dict()
# except Exception as e:
#     pretty_phases_list = ["Error"]
#     ui_to_raw_map      = {"Error": "Error"}
#     excel_data         = {"Error": [f"Could not load file: {str(e)}"]}

# clean_phases = [p for p in pretty_phases_list if p.lower() not in ["level name", "error"]]

# try:
#     _focus_col = next((c for c in df.columns if c.lower() == 'focus'), None)
#     if _focus_col:
#         _pf = df.groupby(phase_col)[_focus_col].first().to_dict()
#         for pretty, raw in ui_to_raw_map.items():
#             if raw in _pf:
#                 phase_focus_map[pretty] = str(_pf[raw]).strip()
# except Exception:
#     pass

# def get_focus_for_phase(phase_name):
#     return phase_focus_map.get(phase_name, "Resilience")

# def get_all_qs(phase):
#     raw = ui_to_raw_map.get(phase, "")
#     return excel_data.get(raw, [])[:18]

# def get_dim_qs(phase):  return get_all_qs(phase)[:9]
# def get_eir_qs(phase):  return get_all_qs(phase)[9:18]

# def q_label(idx, phase_focus="Resilience"):
#     if idx < 9: return f"D{idx+1}", phase_focus
#     else:        return f"EITR{idx-8}", phase_focus


# # ══════════════════════════════════════════════════════════════════
# #  RADAR CHART CACHE — Only redraw when data changes
# # ══════════════════════════════════════════════════════════════════
# _radar_cache = {}

# VIBGYOR = [
#     "#FF0000","#FF7F00","#FFFF00","#00C800","#0000FF",
#     "#4B0082","#8B00FF","#00FFFF","#FF00FF",
# ]

# def _ai_score_values(qs, pd_):
#     vals = []
#     for q in qs:
#         if q in pd_ and pd_[q].get("response", "").strip():
#             ai_s = pd_[q].get("ai_score")
#             vals.append(float(ai_s) if ai_s is not None else 0.5)
#         else:
#             vals.append(0.0)
#     while len(vals) < 9:
#         vals.append(0.0)
#     return vals

# def _cache_key(values, title):
#     return f"{title}::{tuple(round(v, 3) for v in values)}"

# def build_dim_radar(all_data, phase_name="", phase_num=1, current_q_idx=0):
#     dim_qs = get_dim_qs(phase_name) if phase_name else []
#     pd_    = all_data.get(phase_name, {}) if all_data and phase_name else {}
#     values = _ai_score_values(dim_qs, pd_)
#     cur_focus = get_focus_for_phase(phase_name) if phase_name else FOCUS_LABELS[0]
#     title = f"Phase{phase_num}: {phase_name}\nFocus: {cur_focus}"
#     key = _cache_key(values, title)
#     if key in _radar_cache:
#         return _radar_cache[key]

#     N = 9
#     start_angle = np.pi / 2 - (2 * np.pi / N)
#     angles = np.linspace(start_angle, start_angle + 2 * np.pi, N, endpoint=False)
#     fig, ax = plt.subplots(figsize=(5.5, 5.8))
#     fig.patch.set_facecolor("#07081a")
#     ax.set_facecolor("#07081a")
#     ax.set_aspect("equal"); ax.axis("off")
#     for r in [0.2, 0.4, 0.6, 0.8, 1.0]:
#         px = [r * np.cos(a) for a in angles] + [r * np.cos(angles[0])]
#         py = [r * np.sin(a) for a in angles] + [r * np.sin(angles[0])]
#         ax.plot(px, py, color="#3a4a6a", linewidth=0.8, zorder=1)
#     for a in angles:
#         ax.plot([0, np.cos(a)], [0, np.sin(a)], color="#3a4a6a", linewidth=0.8, zorder=1)
#     dx = [v * np.cos(a) for v, a in zip(values, angles)]
#     dy = [v * np.sin(a) for v, a in zip(values, angles)]
#     dx_c = dx + [dx[0]]; dy_c = dy + [dy[0]]
#     ax.fill(dx_c, dy_c, color="#f59e0b", alpha=0.25, zorder=2)
#     ax.plot(dx_c, dy_c, color="#f59e0b", linewidth=2.0, zorder=3)
#     for i in range(N):
#         ax.plot([0, dx[i]], [0, dy[i]], color=VIBGYOR[i], linewidth=2.0, zorder=4)
#         if values[i] > 0:
#             ax.plot(dx[i], dy[i], marker='D', markersize=6, color=VIBGYOR[i], zorder=5)
#     for i, a in enumerate(angles):
#         r_text = 1.15; tx = r_text * np.cos(a); ty = r_text * np.sin(a)
#         ha = "center"; va = "center"
#         if tx > 0.1: ha = "left"
#         elif tx < -0.1: ha = "right"
#         if ty > 0.1: va = "bottom"
#         elif ty < -0.1: va = "top"
#         ax.text(tx, ty, f"D{i+1}", ha=ha, va=va, fontsize=9, color=VIBGYOR[i], fontweight="bold")
#     ax.set_title(title, fontsize=8.5, color="#f1f5f9", fontweight="bold", pad=20)
#     ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.35, 1.35)
#     plt.tight_layout(pad=1.2)
#     _radar_cache[key] = fig
#     # Keep cache small
#     if len(_radar_cache) > 50:
#         oldest = next(iter(_radar_cache))
#         del _radar_cache[oldest]
#     return fig


# def build_eir_radar(all_data, phase_name="", phase_num=1, current_q_idx=0):
#     eir_qs = get_eir_qs(phase_name) if phase_name else []
#     pd_    = all_data.get(phase_name, {}) if all_data and phase_name else {}
#     values = _ai_score_values(eir_qs, pd_)
#     cur_focus = get_focus_for_phase(phase_name) if phase_name else FOCUS_LABELS[0]
#     title = f"Phase{phase_num}: {phase_name}\nFocus: {cur_focus}"
#     key = _cache_key(values, "EIR::" + title)
#     if key in _radar_cache:
#         return _radar_cache[key]

#     N = 9
#     start_angle = np.pi / 2 - (2 * np.pi / N)
#     angles = np.linspace(start_angle, start_angle + 2*np.pi, N, endpoint=False).tolist()
#     bar_w  = 2*np.pi / N * 0.78
#     fig, ax = plt.subplots(figsize=(5.5, 5.8), subplot_kw=dict(polar=True))
#     fig.patch.set_facecolor("#07081a"); ax.set_facecolor("#0d1035")
#     for i, (angle, val) in enumerate(zip(angles, values)):
#         color = VIBGYOR[i]
#         if val <= 0:
#             ax.bar(angle, 0.05, width=bar_w, bottom=0.04,
#                    color=color, alpha=0.12, edgecolor="#2a3a5a", linewidth=0.6, zorder=3)
#         else:
#             ax.bar(angle, val, width=bar_w, bottom=0.04,
#                    color=color, alpha=0.88, edgecolor=color, linewidth=1.2, zorder=4)
#     ax.set_ylim(0, 1.22); ax.set_yticks([]); ax.set_xticks([])
#     ax.spines["polar"].set_color("#ef4444")
#     ax.grid(color="#1e2a4a", linewidth=0.4, linestyle="-", alpha=0.3)
#     label_r = 1.28
#     for i, angle in enumerate(angles):
#         ha = "center"
#         if np.cos(angle) > 0.1:    ha = "left"
#         elif np.cos(angle) < -0.1: ha = "right"
#         ax.text(angle, label_r, f"EITR{i+1}", ha=ha, va="center",
#                 fontsize=7.5, color=VIBGYOR[i], fontweight="bold", transform=ax.transData)
#     ax.set_title(f"{title}", fontsize=8.5, color="#fca5a5", fontweight="bold", pad=28)
#     plt.tight_layout(pad=1.2)
#     _radar_cache[key] = fig
#     if len(_radar_cache) > 50:
#         oldest = next(iter(_radar_cache))
#         del _radar_cache[oldest]
#     return fig


# # ══════════════════════════════════════════════════════════════════
# #  SCORECARD — Only rebuild what changed
# # ══════════════════════════════════════════════════════════════════

# def build_current_phase_scorecard_html(all_data, phase_name):
#     """Fast: only renders the current phase, not all phases."""
#     if not phase_name: return ""
#     pd_    = all_data.get(phase_name, {})
#     focus  = get_focus_for_phase(phase_name)
#     raw    = ui_to_raw_map.get(phase_name, "")
#     dim_qs = get_dim_qs(phase_name)
#     eir_qs = get_eir_qs(phase_name)
#     all_scores  = score_data.get(raw, [])
#     dim_scores  = all_scores[:9]
#     eir_scores  = all_scores[9:18]
#     base_score_val = dim_scores[0] if dim_scores else 0.1

#     def build_rows(qs_list, scores_list, prefix):
#         rows_html = ""
#         for i, q in enumerate(qs_list):
#             label = f"{prefix}{i+1}"
#             if q in pd_:
#                 ans  = pd_[q].get("response", "").strip()
#                 ai_s = pd_[q].get("ai_score")
#                 bs   = scores_list[i] if i < len(scores_list) else base_score_val
#                 if ans:
#                     status    = "✅ Ans"
#                     grade_val = (ai_s * bs) if ai_s is not None else bs
#                     grade_str = f"{grade_val:.2f}"
#                     assess    = ("🟢 Strong" if ai_s and ai_s >= 0.8 else
#                                  "🟡 Fair"   if ai_s and ai_s >= 0.5 else
#                                  "🟠 Needs Work" if ai_s else "🟢 Recorded")
#                 else:
#                     status = "⏭️ Skip"; grade_str = "—"; assess = "—"
#             else:
#                 status = "❌ N/A"; grade_str = "—"; assess = "—"
#             bg = "#0a0d2e" if i % 2 == 0 else "rgba(109,40,217,0.07)"
#             rows_html += (f"<tr style='background:{bg};text-align:center;font-size:11px;"
#                           f"color:#e2e8f0;font-family:Sora,sans-serif;'>"
#                           f"<td style='padding:6px;border:1px solid rgba(109,40,217,0.14);"
#                           f"color:#c4b5fd;font-weight:700;'>{label}</td>"
#                           f"<td style='padding:6px;border:1px solid rgba(109,40,217,0.14);'>{status}</td>"
#                           f"<td style='padding:6px;border:1px solid rgba(109,40,217,0.14);"
#                           f"color:#f59e0b;font-weight:700;'>{grade_str}</td>"
#                           f"<td style='padding:6px;border:1px solid rgba(109,40,217,0.14);'>{assess}</td></tr>")
#         return rows_html

#     dim_rows = build_rows(dim_qs, dim_scores, "D")
#     eir_rows = build_rows(eir_qs, eir_scores, "EITR")
#     th = ("padding:8px;color:#fbbf24;font-family:Outfit,sans-serif;font-size:11px;"
#           "font-weight:800;text-transform:uppercase;border:1px solid rgba(109,40,217,0.35);"
#           "background:#2d1b69;letter-spacing:0.5px;")

#     def make_table(rows, headers):
#         cols = "".join(f"<th style='{th}'>{h}</th>" for h in headers)
#         return (f"<table style='width:100%;border-collapse:collapse;table-layout:fixed;'>"
#                 f"<thead><tr>{cols}</tr></thead><tbody>{rows}</tbody></table>")

#     return f"""
#     <div style='width:100%;margin-top:24px;margin-bottom:20px;padding:0 20px;box-sizing:border-box;'>
#       <div style='text-align:center;margin-bottom:12px;'>
#         <span style='font-family:Outfit,sans-serif;font-weight:900;font-size:1.4em;color:#f59e0b;'>
#           📊 Provisional Score Card
#         </span>
#         <div style='font-family:Sora,sans-serif;font-size:0.95em;color:#94a3b8;margin-top:4px;'>
#           Phase: <span style='color:#c4b5fd;font-weight:bold;'>{phase_name}</span> |
#           Focus: <span style='color:#fbbf24;font-weight:bold;'>{focus}</span>
#         </div>
#       </div>
#       <div style='display:grid;grid-template-columns:1fr 1fr;gap:20px;'>
#         <div style='background:rgba(13,16,53,0.95);border:1px solid rgba(109,40,217,0.35);border-radius:10px;overflow:hidden;'>
#           {make_table(dim_rows, ["Dim","Q&A Sts","Grading","Assessment"])}
#         </div>
#         <div style='background:rgba(13,16,53,0.95);border:1px solid rgba(109,40,217,0.35);border-radius:10px;overflow:hidden;'>
#           {make_table(eir_rows, ["EITR","Q&A Sts","Grading","Assessment"])}
#         </div>
#       </div>
#     </div>"""


# def build_overall_metrics_html(all_data):
#     """Aggregated metrics across all phases."""
#     total_dim = total_eir = 0
#     total_dim_score = total_eir_score = 0.0
#     for phase in clean_phases:
#         dim_qs = get_dim_qs(phase); eir_qs = get_eir_qs(phase)
#         pd_    = all_data.get(phase, {})
#         raw    = ui_to_raw_map.get(phase, "")
#         all_sc = score_data.get(raw, [])
#         dim_sc = all_sc[:9]; eir_sc = all_sc[9:18]
#         base   = dim_sc[0] if dim_sc else 0.1
#         for i, q in enumerate(dim_qs):
#             if q in pd_ and pd_[q].get("response","").strip():
#                 total_dim += 1
#                 ai_s = pd_[q].get("ai_score"); bs = dim_sc[i] if i < len(dim_sc) else base
#                 total_dim_score += (ai_s * bs) if ai_s is not None else bs
#         for i, q in enumerate(eir_qs):
#             if q in pd_ and pd_[q].get("response","").strip():
#                 total_eir += 1
#                 ai_s = pd_[q].get("ai_score"); bs = eir_sc[i] if i < len(eir_sc) else base
#                 total_eir_score += (ai_s * bs) if ai_s is not None else bs

#     total_answered = total_dim + total_eir
#     total_max      = len(clean_phases) * 18
#     total_score_raw = total_dim_score + total_eir_score
#     if total_score_raw == 0:      total_score = "0.00"
#     elif total_score_raw >= 1000: total_score = f"{total_score_raw:,.0f}"
#     elif total_score_raw >= 1:    total_score = f"{total_score_raw:.2f}"
#     else:                         total_score = f"{total_score_raw:.4f}"
#     overall_grade = round((total_answered / total_max) * 10, 1) if total_max and total_answered > 0 else 0.0

#     def metric(label, value, color="#f59e0b"):
#         return (f"<div style='text-align:center;'>"
#                 f"<div style='font-family:Outfit,sans-serif;color:#94a3b8;font-size:0.9em;"
#                 f"text-transform:uppercase;letter-spacing:1px;margin-bottom:5px;'>{label}</div>"
#                 f"<div style='font-family:Sora,sans-serif;color:{color};font-size:2em;font-weight:700;'>{value}</div>"
#                 f"</div>")

#     sep = "<div style='width:1px;height:50px;background:rgba(109,40,217,0.3);'></div>"
#     return (f"<div style='display:flex;justify-content:space-around;align-items:center;"
#             f"background:rgba(13,16,53,0.95);border:1px solid rgba(109,40,217,0.45);"
#             f"border-radius:12px;padding:20px;margin-top:10px;'>"
#             f"{metric('Overall Grade', f'{overall_grade}/10')}{sep}"
#             f"{metric('Overall Score', total_score)}{sep}"
#             f"{metric('Total DIM', f'{total_dim} / {len(clean_phases)*9}', '#86efac')}{sep}"
#             f"{metric('Total EIR', f'{total_eir} / {len(clean_phases)*9}', '#fca5a5')}"
#             f"</div>")


# def build_scorecard(all_data, target_phase=None):
#     """Full scorecard for all phases or a single phase."""
#     phases_to_render = [target_phase] if target_phase else clean_phases
#     phase_rows = []
#     total_dim_all = total_eir_all = 0
#     total_dim_score_all = total_eir_score_all = 0.0

#     for phase in phases_to_render:
#         dim_qs = get_dim_qs(phase); eir_qs = get_eir_qs(phase)
#         pd_    = all_data.get(phase, {})
#         focus  = get_focus_for_phase(phase)
#         raw    = ui_to_raw_map.get(phase, "")
#         pnum   = clean_phases.index(phase) + 1 if phase in clean_phases else 1
#         all_sc = score_data.get(raw, [])
#         dim_sc = all_sc[:9]; eir_sc = all_sc[9:18]
#         base   = dim_sc[0] if dim_sc else 0.1

#         dim_ans = dim_skipped = dim_visited = 0; dim_score = 0.0
#         for i, q in enumerate(dim_qs):
#             if q in pd_:
#                 dim_visited += 1
#                 if pd_[q].get("response","").strip():
#                     dim_ans += 1
#                     ai_s = pd_[q].get("ai_score"); bs = dim_sc[i] if i < len(dim_sc) else base
#                     dim_score += (ai_s * bs) if ai_s is not None else bs
#                 else: dim_skipped += 1

#         eir_ans = eir_skipped = eir_visited = 0; eir_score = 0.0
#         for i, q in enumerate(eir_qs):
#             if q in pd_:
#                 eir_visited += 1
#                 if pd_[q].get("response","").strip():
#                     eir_ans += 1
#                     ai_s = pd_[q].get("ai_score"); bs = eir_sc[i] if i < len(eir_sc) else base
#                     eir_score += (ai_s * bs) if ai_s is not None else bs
#                 else: eir_skipped += 1

#         total_dim_all += dim_ans; total_eir_all += eir_ans
#         total_dim_score_all += dim_score; total_eir_score_all += eir_score

#         def fmt(s):
#             if s == 0: return "—"
#             if s >= 1000: return f"{s:,.0f}"
#             if s >= 1:    return f"{s:.2f}"
#             return f"{s:.4f}"

#         pct = int(((dim_ans + eir_ans) / 18) * 100) if (dim_visited + eir_visited) > 0 else 0
#         assess = ("🔴 Not Started" if (dim_visited + eir_visited) == 0 else
#                   "🟡 In Progress" if pct < 50 else
#                   "🟠 Partial"     if pct < 100 else "🟢 Complete")

#         def qa_str(ans, skipped, visited, total):
#             if visited == 0: return "❌ Not Started"
#             if skipped and ans: return f"⚠️ {ans} Ans, {skipped} Skip"
#             if skipped:         return f"⏭️ All {skipped} Skipped"
#             return f"✅ {ans}/{total} Answered"

#         phase_rows.append({
#             "name": phase, "focus": focus, "phase_num": pnum,
#             "dim_qa": qa_str(dim_ans, dim_skipped, dim_visited, 9),
#             "eir_qa": qa_str(eir_ans, eir_skipped, eir_visited, 9),
#             "assess": assess, "dim_grade": fmt(dim_score), "eir_grade": fmt(eir_score),
#         })

#     total_answered  = total_dim_all + total_eir_all
#     total_max       = len(phases_to_render) * 18
#     total_score_raw = total_dim_score_all + total_eir_score_all
#     if total_score_raw >= 1000: total_score = f"{total_score_raw:,.0f}"
#     elif total_score_raw >= 1:  total_score = f"{total_score_raw:.2f}"
#     else:                       total_score = f"{total_score_raw:.4f}"
#     overall_grade = round((total_answered / total_max) * 10, 1) if total_max and total_answered > 0 else 0.0

#     TH = ("font-family:Outfit,sans-serif;font-weight:700;font-size:9px;padding:6px 4px;"
#           "text-align:center;text-transform:uppercase;letter-spacing:0.3px;"
#           "border:1px solid rgba(109,40,217,0.35);color:#d1d5db;background:#2d1b69;")

#     def td(txt, color="#e2e8f0", bold=False, align="center"):
#         fs = "font-weight:700;" if bold else ""
#         return (f"<td style='padding:5px 4px;font-size:10px;color:{color};{fs}"
#                 f"border:1px solid rgba(109,40,217,0.14);text-align:{align};"
#                 f"white-space:normal;word-break:break-word;'>{txt}</td>")

#     def status_color(s):
#         return ("#86efac" if "✅" in s else "#fde68a" if "⚠️" in s else
#                 "#fca5a5" if "⏭️" in s else "#94a3b8")

#     def assess_color(s):
#         return ("#86efac" if "🟢" in s else "#fde68a" if "🟡" in s else
#                 "#f97316" if "🟠" in s else "#fca5a5")

#     pf_rows = dim_rows = eir_rows = ""
#     for i, r in enumerate(phase_rows):
#         bg        = "#0a0d2e" if i % 2 == 0 else "rgba(109,40,217,0.07)"
#         pnum      = r["phase_num"]
#         pname     = r["name"]
#         pfocus    = r["focus"]
#         dim_qa    = r["dim_qa"]
#         eir_qa    = r["eir_qa"]
#         assess    = r["assess"]
#         dim_grade = r["dim_grade"]
#         eir_grade = r["eir_grade"]
#         pf_rows  += f"<tr style='background:{bg};'>{td(f'P{pnum}: {pname}', '#c4b5fd', True, 'left')}{td(pfocus, '#fbbf24', True)}</tr>"
#         dim_rows += f"<tr style='background:{bg};'>{td(dim_qa, status_color(dim_qa))}{td(dim_grade, '#f59e0b', True)}{td(assess, assess_color(assess))}</tr>"
#         eir_rows += f"<tr style='background:{bg};'>{td(eir_qa, status_color(eir_qa))}{td(eir_grade, '#f59e0b', True)}{td(assess, assess_color(assess))}</tr>"

#     def make_table(header_label, border_color, header_color, col_defs, headers, rows_html):
#         cols = "".join(f"<col style='width:{w};'/>" for w in col_defs)
#         ths  = "".join(f"<th style='{TH}'>{h}</th>" for h in headers)
#         return (f"<div style='background:rgba(13,16,53,0.95);border:1px solid {border_color};"
#                 f"border-radius:10px;overflow:hidden;'>"
#                 f"<div style='background:#2d1b69;padding:8px 10px;font-family:Outfit,sans-serif;"
#                 f"font-weight:800;font-size:0.85em;color:{header_color};text-align:center;"
#                 f"border-bottom:2px solid {border_color};'>{header_label}</div>"
#                 f"<table style='width:100%;border-collapse:collapse;table-layout:fixed;'>"
#                 f"<colgroup>{cols}</colgroup><thead><tr>{ths}</tr></thead><tbody>{rows_html}</tbody></table></div>")

#     title_suffix = f" — {target_phase}" if target_phase else ""
#     return (f"<div style='text-align:center;margin-bottom:12px;'>"
#             f"<span style='font-family:Outfit,sans-serif;font-weight:900;font-size:1.25em;"
#             f"color:#f59e0b;'>📊 Detailed Score Card{title_suffix}</span></div>"
#             f"<div style='display:grid;grid-template-columns:0.9fr 1fr 1fr;gap:8px;width:100%;box-sizing:border-box;'>"
#             + make_table("🎯 Phase / Focus", "rgba(109,40,217,0.30)", "#c4b5fd",
#                          ["58%","42%"], ["Phase","Focus"], pf_rows)
#             + make_table("📐 Dimensions", "rgba(245,158,11,0.30)", "#fbbf24",
#                          ["42%","22%","36%"], ["Q&A Status","Grading","Assessment"], dim_rows)
#             + make_table("🐘 Elephants in the Room", "rgba(239,68,68,0.30)", "#fca5a5",
#                          ["42%","22%","36%"], ["Q&A Status","Grading","Assessment"], eir_rows)
#             + f"</div><div style='margin-top:10px;font-size:0.85em;color:#94a3b8;"
#               f"font-family:Sora,sans-serif;text-align:center;padding:8px;"
#               f"background:rgba(13,16,53,0.6);border-radius:8px;'>"
#               f"<b style='color:#f59e0b;'>Phase Grade: {overall_grade}/10</b>"
#               f" · Phase Score: <b style='color:#f59e0b;'>{total_score}</b>"
#               f" · Dim: {total_dim_all}/{len(phases_to_render)*9}"
#               f" · EIR: {total_eir_all}/{len(phases_to_render)*9}</div>")


# def get_all_phase_scorecards(all_data):
#     return [build_scorecard(all_data, target_phase=p) for p in clean_phases]


# # ══════════════════════════════════════════════════════════════════
# #  CERTIFICATE
# # ══════════════════════════════════════════════════════════════════
# def make_certificate(all_data, name, photo_path, ip_address):
#     W, H = 1500, 960
#     img  = Image.new("RGB", (W, H)); draw = ImageDraw.Draw(img)
#     for y in range(H):
#         t = y/H
#         draw.line([(0,y),(W,y)], fill=(int(6+12*t),int(8+8*t),int(24+22*t)))
#     rng = np.random.default_rng(42)
#     for _ in range(200):
#         sx, sy = int(rng.uniform(0,W)), int(rng.uniform(0,H))
#         alp = int(rng.uniform(60,190)); ss = rng.choice([1,1,2])
#         draw.ellipse([sx,sy,sx+ss,sy+ss], fill=(alp,alp,int(alp*0.9)))
#     for off, col, w in [(8,(109,40,217),2)]:
#         draw.rectangle([off,off,W-off,H-off], outline=col, width=w)
#     try:
#         fp_b = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
#         fp_r = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
#         f72=ImageFont.truetype(fp_b,72); f44=ImageFont.truetype(fp_b,44)
#         f32=ImageFont.truetype(fp_b,32); f24=ImageFont.truetype(fp_r,24)
#         f14=ImageFont.truetype(fp_r,14)
#     except:
#         f72=f44=f32=f24=f14=ImageFont.load_default()
#     cx = W//2
#     try:
#         logo_img = Image.open(BytesIO(base64.b64decode(LOGO_B64))).convert("RGBA").resize((48, 48))
#     except: logo_img = None
#     utc_now  = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
#     meta_text = f"  |  IP: {ip_address}  |  {utc_now}"
#     text_i2u  = "i2u.ai"
#     tw_i2u    = draw.textlength(text_i2u, font=f44)
#     tw_meta   = draw.textlength(meta_text, font=f24)
#     logo_w    = 48 if logo_img else 0; gap = 12 if logo_img else 0
#     total_width = logo_w + gap + tw_i2u + tw_meta
#     current_x   = cx - (total_width / 2)
#     if logo_img:
#         img.paste(logo_img, (int(current_x), int(62 - 24)), logo_img)
#         current_x += logo_w + gap
#     draw.text((current_x, 62), text_i2u, fill=(245,158,11), font=f44, anchor="lm")
#     current_x += tw_i2u
#     draw.text((current_x, 62+6), meta_text, fill=(148,163,184), font=f24, anchor="lm")
#     draw.text((cx,116), "UNICORN FOUNDATIONAL ASSESSMENT", fill=(226,232,240), font=f32, anchor="mm")
#     draw.line([(120,148),(W-120,148)], fill=(245,158,11), width=2)
#     draw.text((cx,192), "Certificate of Assessment Participation", fill=(148,163,184), font=f24, anchor="mm")
#     draw.text((cx,236), "This certifies that", fill=(100,116,139), font=f24, anchor="mm")
#     n = (name or "The Founder").strip()
#     draw.text((cx+2,342), n, fill=(92,40,0), font=f72, anchor="mm")
#     draw.text((cx,340), n, fill=(245,158,11), font=f72, anchor="mm")
#     nb = draw.textbbox((cx,340), n, font=f72, anchor="mm")
#     for lx in range(nb[0]-14, nb[2]+14):
#         a = max(0, 1-abs(lx-cx)/((nb[2]-nb[0])/2+14))
#         draw.line([(lx,nb[3]+14),(lx,nb[3]+17)], fill=(int(245*a),int(158*a),0))
#     ta  = sum(len(v) for v in all_data.values()) if all_data else 0
#     np_ = len(all_data)
#     draw.text((cx,422), "has completed the i2u.ai Unicorn Foundational Assessment", fill=(148,163,184), font=f24, anchor="mm")
#     draw.text((cx,468), f"{np_} phases  ·  {ta} questions answered", fill=(167,139,250), font=f32, anchor="mm")
#     draw.line([(110,H-90),(W-110,H-90)], fill=(20,30,60), width=1)
#     draw.text((cx,H-58), "Provisional Certificate  ·  Unicolt Quiz  ·  i2u.ai Confidential", fill=(40,55,90), font=f14, anchor="mm")
#     if photo_path:
#         try:
#             ph  = Image.open(photo_path).convert("RGBA").resize((210,210))
#             msk = Image.new("L",(210,210),0); ImageDraw.Draw(msk).ellipse([0,0,210,210],fill=255)
#             circ= Image.new("RGBA",(210,210),0); circ.paste(ph,mask=msk)
#             rgba= img.convert("RGBA"); px,py = W-255,48
#             rgba.paste(circ,(px,py),circ)
#             d2  = ImageDraw.Draw(rgba)
#             for ro,rc in [(0,(245,158,11)),(6,(109,40,217))]:
#                 d2.ellipse([px-ro-4,py-ro-4,px+210+ro+4,py+210+ro+4], outline=rc, width=2)
#             img = rgba.convert("RGB")
#         except: pass
#     return img


# # ══════════════════════════════════════════════════════════════════
# #  APP LOGIC — OPTIMIZED FLOW
# # ══════════════════════════════════════════════════════════════════
# def get_phase_num(phase_name):
#     try: return clean_phases.index(phase_name) + 1
#     except ValueError: return 1


# def make_go_to_phase(pname, phase_num):
#     def _fn(all_data):
#         all_qs  = get_all_qs(pname)
#         first_q = all_qs[0] if all_qs else ""
#         pf      = get_focus_for_phase(pname)
#         label, focus = q_label(0, pf)
#         q_display = first_q if first_q else "_No questions found_"
#         q_title   = f"{focus} {label}"

#         btn_style = ("background:rgba(109,40,217,0.18);border:1px solid rgba(109,40,217,0.45);"
#                      "border-radius:10px;color:#c4b5fd;font-family:Outfit,sans-serif;font-weight:700;"
#                      "font-size:0.85em;padding:8px 16px;cursor:pointer;margin-bottom:8px;"
#                      "text-transform:uppercase;transition:all 0.2s;")
#         hdr = (f"<div style='display:flex;align-items:center;justify-content:space-between;"
#                f"padding:10px 20px;background:linear-gradient(90deg,rgba(13,16,53,0.98),"
#                f"rgba(7,8,26,0.92));border-bottom:1px solid rgba(109,40,217,0.28);"
#                f"margin-bottom:8px;width:100%;box-sizing:border-box;'>"
#                f"<div style='display:flex;flex-direction:column;align-items:center;gap:3px;'>"
#                f"<img src='{LOGO_SRC}' style='width:44px;height:44px;border-radius:12px;object-fit:cover;'/>"
#                f"<span style='font-family:Outfit,sans-serif;font-weight:900;font-size:0.85em;"
#                f"background:linear-gradient(135deg,#f59e0b,#8b5cf6);-webkit-background-clip:text;"
#                f"-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:1px;'>i2u.ai</span>"
#                f"<span style='font-family:Sora,sans-serif;font-size:0.60em;color:#64748b;"
#                f"letter-spacing:0.5px;'>Unicolt Quiz</span></div>"
#                f"<div style='display:flex;flex-direction:column;align-items:center;flex:1;padding:0 16px;'>"
#                f"<button onclick=\"document.getElementById('hidden-back-btn').click()\" "
#                f"style=\"{btn_style}\">🏠 UNICOLT QUIZ HOME</button>"
#                f"<div style='font-family:Outfit,sans-serif;font-weight:800;font-size:1.1em;color:#e2e8f0;text-align:center;'>"
#                f"{get_emoji(pname)} Phase{phase_num}: {pname}</div></div>"
#                f"<div style='font-family:Sora,sans-serif;font-size:0.90em;color:#f59e0b;"
#                f"font-weight:700;text-align:right;min-width:120px;'>Focus: {pf}</div></div>")

#         # Only build current phase scorecard + radars on load — skip full rebuild of all tabs
#         return (
#             gr.update(visible=False), gr.update(visible=True),
#             pname, 0,
#             q_display, q_title, "Dimensions: Question 1 of 9",
#             gr.update(value=""), gr.update(value=""),
#             gr.update(visible=False), gr.update(visible=False),
#             build_dim_radar(all_data, pname, phase_num, 0),
#             build_eir_radar(all_data, pname, phase_num, 0),
#             build_scorecard(all_data, target_phase=pname),   # ← only current phase
#             build_overall_metrics_html(all_data),
#             *get_all_phase_scorecards(all_data),
#             gr.update(value="", visible=False),
#             gr.update(value=hdr),
#             build_current_phase_scorecard_html(all_data, pname),
#         )
#     return _fn


# def go_home():
#     return gr.update(visible=True), gr.update(visible=False)


# def save_and_advance(phase, q_index, text, files, all_data):
#     """
#     OPTIMIZED: UI updates instantly with status.
#     Groq call runs in a background thread and result is shown via a second yield.
#     Scorecards only rebuild for the current phase, not all phases.
#     """
#     all_qs    = get_all_qs(phase)
#     phase_num = get_phase_num(phase)

#     if not phase or not all_qs:
#         return (all_data, q_index, "⚠️ No phase loaded.",
#                 gr.update(), gr.update(), gr.update(),
#                 gr.update(visible=False), gr.update(visible=False),
#                 gr.update(), gr.update(), gr.update(),
#                 gr.update(), gr.update(),
#                 *get_all_phase_scorecards(all_data),
#                 gr.update(visible=False),
#                 gr.update(value=""))

#     current_q   = all_qs[q_index] if q_index < len(all_qs) else None
#     phase_focus = get_focus_for_phase(phase)
#     label, focus = q_label(q_index, phase_focus)
#     was_skipped  = not (text and text.strip())

#     # Save immediately
#     all_data.setdefault(phase, {})[current_q] = {
#         "response": text.strip() if text else "",
#         "skipped": was_skipped,
#         "ai_score": None,
#         "files": [f.name for f in files] if files else []
#     }

#     import hashlib
#     if was_skipped:
#         status_msg   = f"⏭️ You skipped **{label}: {focus}**. Use **← Go Back** to answer it."
#         skip_visible = True
#         ai_update    = gr.update(value="", visible=False)
#     else:
#         congrats_msgs = [
#             f"🎉 Congratulations! You've answered **{label}: {focus}** brilliantly!",
#             f"⭐ Wonderful answer on **{label}: {focus}**! Keep going!",
#             f"🌟 Fantastic response for **{label}: {focus}**! Closer to Unicorn status!",
#             f"💪 Great job on **{label}: {focus}**! Your insights are remarkable!",
#             f"🚀 Excellent! **{label}: {focus}** answered! On the path to Unicorn!",
#         ]
#         seed       = int(hashlib.md5(f"{phase}{q_index}".encode()).hexdigest()[:4], 16) % len(congrats_msgs)
#         status_msg = congrats_msgs[seed]
#         skip_visible = False
#         # Show "AI thinking..." immediately, run Groq in background
#         ai_update = gr.update(
#             value=("<div class='ai-loading'>🤖 AI Mentor is reviewing your answer..."
#                    "<span class='ai-loading-dots'><span></span><span></span><span></span></span></div>"),
#             visible=True
#         )

#     # Determine next question
#     next_idx = q_index + 1

#     # Check if dimensions complete before moving to EIR
#     if next_idx == 9 and not was_skipped:
#         dim_qs   = get_dim_qs(phase)
#         pd_      = all_data.get(phase, {})
#         dim_done = sum(1 for q in dim_qs if q in pd_ and pd_[q].get("response","").strip())
#         if dim_done < 9:
#             return (
#                 all_data, q_index, status_msg,
#                 gr.update(value=current_q),
#                 gr.update(value=f"{focus} {label}"),
#                 gr.update(value=f"Dimensions: Question {q_index+1} of 9"),
#                 gr.update(visible=True), gr.update(visible=skip_visible),
#                 gr.update(value=""),
#                 build_dim_radar(all_data, phase, phase_num, q_index),
#                 build_eir_radar(all_data, phase, phase_num, q_index),
#                 build_scorecard(all_data, target_phase=phase),   # ← current phase only
#                 build_overall_metrics_html(all_data),
#                 *get_all_phase_scorecards(all_data),
#                 ai_update,
#                 build_current_phase_scorecard_html(all_data, phase),
#             )

#     if next_idx >= len(all_qs):
#         all_qa    = [(all_qs[i], all_data.get(phase,{}).get(all_qs[i],{}).get("response",""))
#                      for i in range(len(all_qs))]
#         phase_rpt = llm_phase_report(phase, phase_focus, all_qa)
#         complete_msg = f"🏆 **All 18 questions for {phase} are complete!**\n\n---\n{phase_rpt}"
#         return (
#             all_data, q_index, complete_msg,
#             gr.update(value=f"✅ {phase} — Complete!"),
#             gr.update(value="✅ Phase Complete!"),
#             gr.update(value="🏆 Phase Complete!"),
#             gr.update(visible=False), gr.update(visible=False),
#             gr.update(value=""),
#             build_dim_radar(all_data, phase, phase_num, q_index),
#             build_eir_radar(all_data, phase, phase_num, q_index),
#             build_scorecard(all_data, target_phase=phase),
#             build_overall_metrics_html(all_data),
#             *get_all_phase_scorecards(all_data),
#             gr.update(value="", visible=False),
#             build_current_phase_scorecard_html(all_data, phase),
#         )

#     next_q = all_qs[next_idx]
#     next_label, next_focus = q_label(next_idx, phase_focus)
#     is_eir    = next_idx >= 9
#     local_idx = (next_idx - 9 + 1) if is_eir else (next_idx + 1)
#     section   = "Elephants in the Room" if is_eir else "Dimensions"
#     progress  = f"{section}: Question {local_idx} of 9"

#     return (
#         all_data, next_idx, status_msg,
#         gr.update(value=next_q),
#         gr.update(value=f"{next_focus} {next_label}"),
#         gr.update(value=progress),
#         gr.update(visible=False), gr.update(visible=skip_visible),
#         gr.update(value=""),
#         build_dim_radar(all_data, phase, phase_num, next_idx),
#         build_eir_radar(all_data, phase, phase_num, next_idx),
#         build_scorecard(all_data, target_phase=phase),   # ← current phase only (FAST)
#         build_overall_metrics_html(all_data),
#         *get_all_phase_scorecards(all_data),
#         ai_update,
#         build_current_phase_scorecard_html(all_data, phase),
#     )


# def fetch_ai_feedback(phase, q_index, text, all_data):
#     """
#     SEPARATE EVENT: Called after save_and_advance to fetch AI feedback
#     without blocking the UI. Wired to a hidden trigger.
#     Updates ai_feedback_out and scorecard once Groq responds.
#     """
#     if not text or not text.strip():
#         return gr.update(value="", visible=False), all_data, gr.update(), gr.update()

#     all_qs      = get_all_qs(phase)
#     phase_num   = get_phase_num(phase)
#     phase_focus = get_focus_for_phase(phase)
#     current_q   = all_qs[q_index] if q_index < len(all_qs) else None
#     label, focus = q_label(q_index, phase_focus)

#     # q_index points to the PREVIOUS question (already saved before advance)
#     saved_q_idx = q_index - 1
#     if saved_q_idx < 0:
#         return gr.update(value="", visible=False), all_data, gr.update(), gr.update()

#     saved_q   = all_qs[saved_q_idx]
#     saved_ans = all_data.get(phase, {}).get(saved_q, {}).get("response", "")

#     if not saved_ans.strip():
#         return gr.update(value="", visible=False), all_data, gr.update(), gr.update()

#     ai_fb = llm_evaluate_answer(phase, phase_focus, label, saved_q, saved_ans)
#     if ai_fb:
#         ai_score = parse_ai_score(ai_fb)
#         if ai_score is not None and phase in all_data and saved_q in all_data[phase]:
#             all_data[phase][saved_q]["ai_score"] = ai_score
#         ai_md = gr.update(value=f"🤖 **AI Mentor Feedback:**\n\n{ai_fb}", visible=True)
#     else:
#         ai_md = gr.update(value="", visible=False)

#     return (
#         ai_md,
#         all_data,
#         build_current_phase_scorecard_html(all_data, phase),
#         build_dim_radar(all_data, phase, phase_num, q_index),
#     )


# def go_back(phase, q_index, all_data):
#     phase_num  = get_phase_num(phase)
#     all_qs     = get_all_qs(phase)
#     prev_idx   = max(0, q_index - 1)
#     prev_q     = all_qs[prev_idx] if prev_idx < len(all_qs) else ""
#     back_focus = get_focus_for_phase(phase)
#     prev_label, prev_focus = q_label(prev_idx, back_focus)
#     is_eir    = prev_idx >= 9
#     local_idx = (prev_idx - 9 + 1) if is_eir else (prev_idx + 1)
#     section   = "Elephants in the Room" if is_eir else "Dimensions"
#     progress  = f"{section}: Question {local_idx} of 9"
#     pd_      = all_data.get(phase, {})
#     prev_ans = pd_.get(prev_q, {}).get("response", "") if prev_q in pd_ else ""
#     return (
#         all_data, prev_idx,
#         f"↩️ Went back to **{prev_label}: {prev_focus}**. Edit your answer below.",
#         gr.update(value=prev_q),
#         gr.update(value=f"{prev_focus} {prev_label}"),
#         gr.update(value=progress),
#         gr.update(visible=False), gr.update(visible=False),
#         gr.update(value=prev_ans),
#         build_dim_radar(all_data, phase, phase_num, prev_idx),
#         build_eir_radar(all_data, phase, phase_num, prev_idx),
#         build_scorecard(all_data, target_phase=phase),   # ← current phase only
#         build_overall_metrics_html(all_data),
#         *get_all_phase_scorecards(all_data),
#         gr.update(value="", visible=False),
#         build_current_phase_scorecard_html(all_data, phase),
#     )


# def gen_cert(all_data, name, photo, request: gr.Request):
#     ip_addr = request.client.host if request and request.client else "Unknown IP"
#     path = photo if isinstance(photo, str) else (photo.name if photo else None)
#     return make_certificate(all_data, name or "", path, ip_addr)


# def try_go_to_eir(phase, all_data):
#     dim_qs   = get_dim_qs(phase)
#     pd_      = all_data.get(phase, {}) if all_data else {}
#     dim_done = sum(1 for q in dim_qs if q in pd_ and pd_[q].get("response","").strip())
#     return gr.update(visible=(dim_done < 9))


# def final_submit(all_data, founder_name):
#     ta = sum(len(v) for v in all_data.values()) if all_data else 0
#     if ta == 0:
#         return "⚠️ Please answer at least one question before submitting."
#     return llm_hitl_report(all_data, founder_name or "The Founder")


# # ══════════════════════════════════════════════════════════════════
# #  THEME
# # ══════════════════════════════════════════════════════════════════
# theme = gr.themes.Base(
#     primary_hue=gr.themes.colors.violet,
#     secondary_hue=gr.themes.colors.blue,
#     neutral_hue=gr.themes.colors.slate,
#     font=[gr.themes.GoogleFont("Sora"), "system-ui"],
#     font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "monospace"],
#     radius_size=gr.themes.sizes.radius_lg,
#     spacing_size=gr.themes.sizes.spacing_md,
# ).set(
#     background_fill_primary="#07081a",
#     background_fill_secondary="#0d1035",
#     block_background_fill="#0d1035",
#     block_border_color="rgba(109,40,217,0.28)",
#     block_border_width="1px",
#     block_shadow="0 0 32px rgba(109,40,217,0.12)",
#     body_text_color="#e2e8f0",
#     body_text_color_subdued="#64748b",
#     block_label_text_color="#94a3b8",
#     button_primary_background_fill="linear-gradient(135deg,#f59e0b,#d97706)",
#     button_primary_background_fill_hover="linear-gradient(135deg,#fbbf24,#f59e0b)",
#     button_primary_text_color="#07081a",
#     button_primary_border_color="#f59e0b",
#     button_secondary_background_fill="rgba(109,40,217,0.14)",
#     button_secondary_background_fill_hover="rgba(109,40,217,0.26)",
#     button_secondary_text_color="#c4b5fd",
#     button_secondary_border_color="rgba(109,40,217,0.42)",
#     input_background_fill="#0a0c25",
#     input_border_color="rgba(109,40,217,0.40)",
#     input_border_color_focus="#f59e0b",
#     input_placeholder_color="#475569",
# )


# # ══════════════════════════════════════════════════════════════════
# #  UI
# # ══════════════════════════════════════════════════════════════════
# with gr.Blocks(title="i2u.ai — Unicolt Quiz") as demo:

#     saved_data    = gr.State({})
#     current_phase = gr.State("")
#     q_index_state = gr.State(0)
#     # Hidden state to pass last answered text to the AI feedback chain
#     last_answered_text = gr.State("")

#     hidden_back_btn = gr.Button("🏠 Unicolt Quiz Home", elem_id="hidden-back-btn",
#                                 elem_classes=["hidden-btn"])

#     LOGO_HTML = f"""
#     <div class="logo-header">
#       <img src="{LOGO_SRC}" alt="i2u.ai logo"/>
#       <div class="brand-name">i2u.ai</div>
#       <div class="tagline">Ideas to Unicorns &nbsp;·&nbsp; AI-Powered Unicolt Quiz</div>
#     </div>"""

#     # ── PAGE 1: HOME ─────────────────────────────────────────────
#     with gr.Column(visible=True) as home_page:
#         gr.HTML(LOGO_HTML)
#         gr.Markdown("### Select Your Assessment Phase", elem_classes=["c"])
#         phase_buttons = []
#         rows = [clean_phases[i:i+3] for i in range(0, len(clean_phases), 3)]
#         for row_idx, row_phases in enumerate(rows):
#             with gr.Row(equal_height=True):
#                 for col_idx, name in enumerate(row_phases):
#                     emoji     = get_emoji(name)
#                     phase_num = row_idx * 3 + col_idx + 1
#                     card_label = f"Phase{phase_num}: {emoji}  {name}"
#                     with gr.Column(scale=1, min_width=210):
#                         btn = gr.Button(card_label, variant="secondary", elem_classes=["phase-btn"])
#                         phase_buttons.append((btn, name, phase_num))
#         gr.Markdown("---\n_© i2u.ai — All submissions are private and confidential._",
#                     elem_classes=["footer-md"])

#     # ── PAGE 2: PHASE WORKSPACE ──────────────────────────────────
#     with gr.Column(visible=False) as phase_page:

#         phase_header_html = gr.HTML("")

#         with gr.Row():
#             with gr.Column(scale=5):
#                 progress_md       = gr.Markdown("Dimensions: Question 1 of 9", elem_classes=["c"])
#                 eir_nav_btn       = gr.Button("🐘 Elephants in the Room", variant="secondary", size="sm")
#                 question_title_md = gr.Markdown("**Resilience D1**", elem_classes=["question-title","c"])
#                 question_display  = gr.Markdown("_Select a phase to load questions._",
#                                                 elem_classes=["question-display"])
#                 skip_warning = gr.Markdown(
#                     "⏭️ **You skipped this question.** Use ← Go Back to answer it.",
#                     elem_classes=["skip-warning"], visible=False)
#                 user_response = gr.Textbox(
#                     label="Your Response", lines=4, max_lines=7,
#                     placeholder="Enter your response here — or press Save & Next to skip.",
#                     elem_classes=["response-box"])
#                 user_files = gr.File(
#                     file_count="multiple",
#                     file_types=[".pdf",".ppt",".pptx",".doc",".docx",".xls",".xlsx",
#                                 ".png",".jpg",".jpeg",".csv",".txt"],
#                     elem_classes=["upload-compact"], show_label=False)
#                 with gr.Row():
#                     go_back_btn = gr.Button("← Improve / Go Back", variant="secondary", size="sm")
#                     save_btn    = gr.Button("💾  Save & Next", variant="primary", size="lg")
#                 save_status     = gr.Markdown(elem_classes=["save-st"])
#                 ai_feedback_out = gr.Markdown(value="", elem_classes=["hitl-block"], visible=False)

#             with gr.Column(scale=4):
#                 eir_warning = gr.Markdown(
#                     "🔴 **Complete all 9 Dimensions questions before accessing Elephants in the Room.**",
#                     elem_classes=["eir-warning"], visible=False)

#                 with gr.Tabs():
#                     with gr.TabItem("🎓 Certificate & Submit"):
#                         gr.Markdown("### 🖊️ Certificate Details", elem_classes=["c"])
#                         founder_name = gr.Textbox(label="Your Full Name",
#                                                    placeholder="As it should appear on the certificate…")
#                         founder_photo = gr.Image(
#                             label="Drop File Here / Click to Upload",
#                             type="filepath", height=150,
#                             elem_classes=["custom-drag-drop"])
#                         gen_btn  = gr.Button("🎨 Generate Certificate Preview", variant="primary", size="lg")
#                         cert_img = gr.Image(label="", height=250)
#                         gr.Markdown("---")
#                         gr.Markdown("### 📬 Submit for Human Review", elem_classes=["c"])
#                         submit_btn    = gr.Button("✅ Confirm & Submit", variant="primary", size="lg")
#                         submit_status = gr.Markdown()

#                     with gr.TabItem("📊 Provisional Scorecards"):
#                         scorecard_outs = []
#                         with gr.Tabs():
#                             for idx, phase in enumerate(clean_phases):
#                                 with gr.TabItem(f"Phase {idx+1}"):
#                                     sco = gr.HTML()
#                                     scorecard_outs.append(sco)

#                     with gr.TabItem("🌟 Overall Provisional Scorecard"):
#                         gr.Markdown("### Part A: Aggregated Metrics", elem_classes=["c"])
#                         overall_metrics_out = gr.HTML(build_overall_metrics_html({}))

#                     with gr.TabItem("🏆 Overall Tab"):
#                         gr.Markdown("### 🏢 Complete Foundational Overview", elem_classes=["c"])
#                         global_scorecard_out = gr.HTML(build_scorecard({}, target_phase=None))

#                 dim_radar_out = gr.Plot(label=None, show_label=False)
#                 eir_radar_out = gr.Plot(label=None, show_label=False)

#         current_phase_scorecard_out = gr.HTML()

#         gr.Markdown("---")
#         gr.Markdown(
#             "### 👤  Human in the Loop Report (HITL)\n\n"
#             "After submission, an i2u.ai expert reviews your responses and delivers a validated report.",
#             elem_classes=["hitl-block"])

#     # ── WIRING ───────────────────────────────────────────────────
#     PHASE_OUTS = [
#         home_page, phase_page,
#         current_phase, q_index_state,
#         question_display, question_title_md, progress_md,
#         user_response, save_status,
#         eir_warning, skip_warning,
#         dim_radar_out, eir_radar_out,
#         global_scorecard_out,
#         overall_metrics_out,
#         *scorecard_outs,
#         ai_feedback_out,
#         phase_header_html,
#         current_phase_scorecard_out,
#     ]

#     SAVE_OUTS = [
#         saved_data, q_index_state, save_status,
#         question_display, question_title_md, progress_md,
#         eir_warning, skip_warning, user_response,
#         dim_radar_out, eir_radar_out,
#         global_scorecard_out,
#         overall_metrics_out,
#         *scorecard_outs,
#         ai_feedback_out,
#         current_phase_scorecard_out,
#     ]

#     for btn, name, num in phase_buttons:
#         btn.click(fn=make_go_to_phase(name, num), inputs=[saved_data], outputs=PHASE_OUTS)

#     hidden_back_btn.click(fn=go_home, inputs=[], outputs=[home_page, phase_page])

#     # Step 1: Save answer & advance UI instantly (no Groq wait)
#     save_btn.click(
#         fn=save_and_advance,
#         inputs=[current_phase, q_index_state, user_response, user_files, saved_data],
#         outputs=SAVE_OUTS
#     ).then(
#         # Step 2: Fire AI feedback AFTER UI has already updated
#         fn=fetch_ai_feedback,
#         inputs=[current_phase, q_index_state, user_response, saved_data],
#         outputs=[ai_feedback_out, saved_data, current_phase_scorecard_out, dim_radar_out]
#     )

#     go_back_btn.click(
#         fn=go_back,
#         inputs=[current_phase, q_index_state, saved_data],
#         outputs=SAVE_OUTS)

#     eir_nav_btn.click(
#         fn=try_go_to_eir,
#         inputs=[current_phase, saved_data],
#         outputs=[eir_warning])

#     gen_btn.click(
#         fn=gen_cert,
#         inputs=[saved_data, founder_name, founder_photo],
#         outputs=[cert_img])

#     submit_btn.click(
#         fn=final_submit,
#         inputs=[saved_data, founder_name],
#         outputs=[submit_status])

# if __name__ == "__main__":
#     demo.launch(theme=theme, css=CSS)




import gradio as gr
import pandas as pd
import re
import base64
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO
from groq import Groq

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
GROQ_MODEL  = "llama-3.3-70b-versatile"


def llm_evaluate_answer(phase_name, focus, label, question_text, user_answer):
    if not user_answer or not user_answer.strip():
        return ""
    prompt = f"""You are an expert startup mentor evaluating a founder's answer.
Phase: {phase_name}, Focus: {focus}, Question: [{label}] {question_text}
Founder's Answer: {user_answer}
Respond EXACTLY:
SCORE: X/10
FEEDBACK: (2-3 sentences)
STRENGTH: (one key strength)
GAP: (one area to improve)
Under 100 words."""
    try:
        r = groq_client.chat.completions.create(model=GROQ_MODEL,
            messages=[{"role":"user","content":prompt}], temperature=0.3)
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI Mentor unavailable: {e}"


def parse_ai_score(text):
    if not text: return None
    m = re.search(r'SCORE:\s*(\d+(?:\.\d+)?)\s*/\s*10', text, re.IGNORECASE)
    return round(min(float(m.group(1)), 10.0) / 10.0, 2) if m else None


def llm_phase_report(phase_name, focus, all_qa_pairs):
    qa_text = "\n".join([f"Q{i+1}: {q}\nA: {a if a.strip() else '[SKIPPED]'}"
                         for i,(q,a) in enumerate(all_qa_pairs)])
    prompt = f"""Senior startup mentor writing phase assessment.
Phase: {phase_name}, Focus: {focus}
{qa_text}
Write with sections: ## {phase_name} — {focus} Assessment
**Overall Score: X/10** **Executive Summary** **Key Strengths** **Critical Gaps**
**Elephants in the Room** **Mentor Recommendation**. Under 300 words."""
    try:
        r = groq_client.chat.completions.create(model=GROQ_MODEL,
            messages=[{"role":"user","content":prompt}], temperature=0.4)
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI Mentor unavailable: {e}"


def llm_hitl_report(all_data, founder_name):
    phases_summary = []
    for phase in clean_phases:
        qs = get_all_qs(phase); pd_ = all_data.get(phase, {})
        focus    = get_focus_for_phase(phase)
        answered = sum(1 for q in qs if q in pd_ and pd_[q].get("response","").strip())
        skipped  = sum(1 for q in qs if q in pd_ and not pd_[q].get("response","").strip())
        phases_summary.append(f"- {phase} [{focus}]: {answered}/18 answered, {skipped} skipped")
    summary_text = "\n".join(phases_summary)
    prompt = f"""Chief Mentor at i2u.ai writing confidential assessment.
Founder: {founder_name or 'The Founder'}
{summary_text}
HITL Report sections: Executive Overview, Unicorn Potential Score X/100,
Phase-by-Phase Analysis, Top 3 Strengths, Top 3 Risks, 90-Day Action Plan, Mentor's Verdict. Under 500 words."""
    try:
        r = groq_client.chat.completions.create(model=GROQ_MODEL,
            messages=[{"role":"user","content":prompt}], temperature=0.5)
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI Mentor unavailable: {e}"


try:
    with open('WhatsApp Image 2026-03-19 at 2.43.33 PM.jpeg','rb') as _f:
        LOGO_B64 = base64.b64encode(_f.read()).decode()
except FileNotFoundError:
    LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
LOGO_SRC = f"data:image/jpeg;base64,{LOGO_B64}"

FOCUS_LABELS = ["Resilience","Validation","Feasibility","Traction","Growth",
                "Profit","Innovation","Legacy","Stewardship"]
phase_focus_map = {}
score_data      = {}
VIBGYOR = ["#FF0000","#FF7F00","#FFFF00","#00C800","#0000FF",
           "#4B0082","#8B00FF","#00FFFF","#FF00FF"]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;900&family=Sora:wght@300;400;600&display=swap');
:root {
    --bg: #07081a;
    --card: #0d1035;
    --gold: #f59e0b;
    --violet: #6d28d9;
    --text: #e2e8f0;
    --dim: #64748b;
    --glass: rgba(13, 16, 53, 0.85);
}
.gradio-container { max-width: 100% !important; }
footer, .footer, div[class*="footer"], #footer { display: none !important; }
body, .gradio-container {
    background: var(--bg) !important;
    font-family: 'Sora', sans-serif !important;
    color: var(--text) !important;
}
h1, h2, h3, h4 { font-family: 'Outfit', sans-serif !important; }
.c, .c * { text-align: center !important; }

/* Sticky Scorecard */
.sticky-score-container {
    position: fixed !important;
    top: 20px !important;
    right: 20px !important;
    width: 320px !important;
    z-index: 1000 !important;
    max-height: 85vh !important;
    overflow-y: auto !important;
    background: var(--glass) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(109, 40, 217, 0.4) !important;
    border-radius: 16px !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.6), 0 0 20px rgba(109, 40, 217, 0.2) !important;
    padding: 12px !important;
    scrollbar-width: thin;
    scrollbar-color: var(--violet) transparent;
}
.sticky-score-container::-webkit-scrollbar { width: 6px; }
.sticky-score-container::-webkit-scrollbar-thumb { background: var(--violet); border-radius: 10px; }

/* Dashboard Grid */
.dashboard-grid {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 20px !important;
    width: 100% !important;
}
@media (max-width: 1024px) {
    .dashboard-grid { grid-template-columns: 1fr !important; }
}

.phase-header-title {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 900 !important;
    font-size: 1.8em !important;
    color: var(--gold) !important;
    text-align: center !important;
    margin: 15px 0 !important;
    letter-spacing: 1px !important;
}

input, textarea, select {
    background: #0a0c25 !important;
    border: 1px solid rgba(109,40,217,0.40) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'Sora', sans-serif !important;
}
input:focus, textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(245,158,11,0.15) !important;
    outline: none !important;
}
label span {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    color: #c4b5fd !important;
}
.logo-header {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 18px 20px 14px !important;
    background: linear-gradient(180deg, rgba(13,16,53,0.98) 0%, rgba(7,8,26,0.85) 100%) !important;
    border-bottom: 1px solid rgba(109,40,217,0.28) !important;
    margin-bottom: 8px !important;
    text-align: center !important;
    width: 100% !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
}
.logo-header img {
    width: 72px !important; height: 72px !important;
    max-width: 72px !important; max-height: 72px !important;
    border-radius: 18px !important; object-fit: cover !important;
    box-shadow: 0 4px 16px rgba(109,40,217,0.60), 0 0 0 2px rgba(245,158,11,0.45) !important;
    margin: 0 auto 10px auto !important; display: block !important;
}
.logo-header .brand-name {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.8em !important; font-weight: 900 !important;
    background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 45%, #8b5cf6 100%) !important;
    -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
    background-clip: text !important; letter-spacing: 2px !important;
}
.logo-header .tagline {
    font-family: 'Sora', sans-serif !important; font-size: 0.85em !important;
    font-weight: 300 !important; color: #94a3b8 !important; letter-spacing: 1.2px !important; margin-top: 3px !important;
}
.question-title {
    text-align: center !important; font-family: 'Outfit', sans-serif !important;
    font-weight: 900 !important; font-size: 1.45em !important; color: #f59e0b !important;
    letter-spacing: 1.5px !important; margin-bottom: 6px !important; padding: 10px 0 4px 0 !important;
}
.question-title * { text-align: center !important; color: #f59e0b !important; }
.question-display {
    background: rgba(109,40,217,0.12) !important;
    border: 1.5px solid rgba(109,40,217,0.35) !important;
    border-radius: 14px !important; padding: 18px 20px !important; margin-bottom: 12px !important;
}
.question-display p, .question-display * {
    font-size: 1.15em !important; font-weight: 700 !important;
    font-family: 'Outfit', sans-serif !important; color: #f8fafc !important;
    line-height: 1.75 !important; margin: 0 !important;
}
.response-box textarea {
    min-height: 100px !important; max-height: 160px !important;
    overflow-y: auto !important; font-size: 0.98em !important;
    line-height: 1.7 !important; border-radius: 12px !important;
    padding: 12px !important; resize: vertical !important;
}
.response-box label span { font-size: 0.70em !important; font-weight: 400 !important; color: var(--dim)!important; text-transform: uppercase !important; letter-spacing: 0.5px !important; }
.eir-warning {
    background: rgba(239,68,68,0.12) !important; border: 2px solid #ef4444 !important;
    border-radius: 12px !important; padding: 14px 18px !important; margin-bottom: 12px !important;
}
.eir-warning p, .eir-warning * { color: #fca5a5 !important; font-weight: 600 !important; font-family: 'Outfit', sans-serif !important; font-size: 0.95em !important; margin: 0 !important; }
.skip-warning {
    background: rgba(245,158,11,0.10) !important; border: 2px solid #f59e0b !important;
    border-radius: 12px !important; padding: 14px 18px !important; margin-bottom: 12px !important;
}
.skip-warning p, .skip-warning * { color: #fde68a !important; font-weight: 600 !important; font-family: 'Outfit', sans-serif !important; font-size: 0.95em !important; margin: 0 !important; }
.save-st p {
    padding: 12px 18px !important; border-radius: 12px !important;
    background: rgba(34,197,94,0.10) !important; border-left: 4px solid #22c55e !important;
    font-size: 0.92em !important; color: #86efac !important;
}
.phase-hd,.phase-hd * { text-align: center !important; font-family: 'Outfit', sans-serif !important; }
.upload-compact .wrap,.upload-compact > div:first-child{padding:0!important;border:none!important;background:transparent!important;min-height:0!important;}
.upload-compact button {
    background: rgba(109,40,217,0.18) !important;
    border: 1px solid rgba(109,40,217,0.45) !important;
    border-radius: 10px !important; color: #c4b5fd !important;
    font-family: 'Outfit', sans-serif !important; font-weight: 700 !important;
    padding: 12px 24px !important; width: 100% !important; cursor: pointer !important;
}
.upload-compact .dnd-zone, .upload-compact .dnd-zone-text, .upload-compact .or { display: none !important; }
.footer-md, .footer-md * { text-align: center !important; color: var(--dim) !important; font-size: 0.82em !important; }
.hitl-block {
    border-left: 3px solid var(--gold) !important;
    background: rgba(245,158,11,0.05) !important;
    border-radius: 0 12px 12px 0 !important; padding: 12px 16px !important;
}
.cert-photo-box { border: 1.5px dashed rgba(245,158,11,0.45) !important; border-radius: 18px !important; background: rgba(245,158,11,0.04) !important; padding: 16px !important; }
.phase-btn { position: relative !important; }
.phase-btn button {
    min-height: 130px !important; width: 100% !important;
    border-radius: 22px !important; border: 1.5px solid rgba(56,168,245,0.45) !important;
    outline: none !important; cursor: pointer !important;
    overflow: hidden !important; position: relative !important;
    font-family: 'Outfit', sans-serif !important; font-size: 0.95em !important; font-weight: 700 !important;
    line-height: 1.5 !important; white-space: normal !important; text-align: center !important;
    padding: 20px 16px !important; color: #ffffff !important;
    text-shadow: 0 1px 6px rgba(0,0,0,0.55) !important;
    background:
        linear-gradient(180deg,rgba(255,255,255,0.32) 0%,rgba(255,255,255,0.10) 30%,transparent 55%,rgba(0,0,0,0.22) 100%),
        linear-gradient(170deg,#1e3a8a 0%,#1e40af 30%,#1a3fa8 65%,#0f2472 100%) !important;
    box-shadow: inset 0 4px 8px rgba(255,255,255,0.22), inset 0 -5px 10px rgba(0,0,0,0.50), 0 8px 0 #0a1a55, 0 14px 28px rgba(0,0,0,0.70) !important;
    transition: transform 0.16s, box-shadow 0.16s !important;
    display: flex !important; flex-direction: column !important;
    align-items: center !important; justify-content: center !important;
}
.phase-btn button:hover {
    transform: translateY(-8px) scale(1.03) !important;
    box-shadow: inset 0 4px 10px rgba(255,255,255,0.38), 0 8px 0 #082a60,
        0 20px 40px rgba(0,0,0,0.80), 0 0 28px rgba(56,168,245,0.70) !important;
}
.phase-btn button:active { transform: translateY(5px) scale(0.974) !important; filter: brightness(0.78) !important; }
.hidden-btn { display: none !important; }
"""


# ══════════════════════════════════════════════════════════════════
#  DATA LOADING
# ══════════════════════════════════════════════════════════════════
def prettify_name(text):
    text = str(text).replace("_"," ").replace("-"," ")
    return re.sub(r'\s+',' ',text).strip().title()

PHASE_META = {
    "conception":{"emoji":"✨"},"spark":{"emoji":"✨"},
    "initiation":{"emoji":"🎯"},"hunt":{"emoji":"🎯"},
    "formulation":{"emoji":"🔨"},"build":{"emoji":"🔨"},
    "market entry":{"emoji":"🚀"},"launch":{"emoji":"🚀"},
    "scaling":{"emoji":"📈"},"rocket":{"emoji":"📈"},
    "efficiency":{"emoji":"⚙️"},"optimization":{"emoji":"⚙️"},
    "leadership":{"emoji":"🏛️"},"institution":{"emoji":"🏛️"},
    "unicorn":{"emoji":"🦄"},"dominance":{"emoji":"🦄"},
    "masters":{"emoji":"⭐"},"jedi":{"emoji":"⭐"},"return":{"emoji":"⭐"},
}

def get_emoji(name):
    lower = name.lower()
    for k,v in PHASE_META.items():
        if k in lower: return v["emoji"]
    return "📂"

try:
    df = pd.read_excel("Refined_Startup_Assessment_Questions.xlsx")
    df.columns = df.columns.str.strip()
    phase_col    = next((c for c in df.columns if c.lower() in ['level','phase','stage','phases']), df.columns[0])
    question_col = next((c for c in df.columns if c.lower() in ['question','questions','criteria','description']), df.columns[-1])
    score_col    = next((c for c in df.columns if c.lower() in ['base_score','score','base score']), None)
    df = df.dropna(subset=[phase_col, question_col])
    df = df[df[phase_col].astype(str).str.lower() != 'level name']
    raw_phases         = df[phase_col].astype(str).unique().tolist()
    ui_to_raw_map      = {prettify_name(p): p for p in raw_phases}
    pretty_phases_list = list(ui_to_raw_map.keys())
    excel_data         = df.groupby(phase_col)[question_col].apply(lambda x:[str(q) for q in x]).to_dict()
    if score_col:
        score_data = df.groupby(phase_col)[score_col].apply(lambda x:[float(v) for v in x]).to_dict()
except Exception as e:
    pretty_phases_list = ["Error"]
    ui_to_raw_map      = {"Error":"Error"}
    excel_data         = {"Error":[f"Could not load: {e}"]}

clean_phases = [p for p in pretty_phases_list if p.lower() not in ["level name","error"]]

try:
    _focus_col = next((c for c in df.columns if c.lower()=='focus'), None)
    if _focus_col:
        _pf = df.groupby(phase_col)[_focus_col].first().to_dict()
        for pretty, raw in ui_to_raw_map.items():
            if raw in _pf:
                phase_focus_map[pretty] = str(_pf[raw]).strip()
except Exception:
    pass

def get_focus_for_phase(phase_name):
    return phase_focus_map.get(phase_name, "Resilience")

def get_all_qs(phase):
    return excel_data.get(ui_to_raw_map.get(phase,""),[])[:18]
def get_dim_qs(phase): return get_all_qs(phase)[:9]
def get_eir_qs(phase): return get_all_qs(phase)[9:18]

def q_label(idx, phase_focus="Resilience"):
    if idx < 9: return f"D{idx+1}", phase_focus
    else:        return f"EITR{idx-8}", phase_focus


# ══════════════════════════════════════════════════════════════════
#  CHARTS
# ══════════════════════════════════════════════════════════════════
def _answered_values(qs, pd_):
    vals = []
    for q in qs:
        vals.append(1.0 if (q in pd_ and pd_[q].get("response","").strip()) else 0.0)
    while len(vals) < 9: vals.append(0.0)
    return vals

def _ai_score_values(qs, pd_):
    vals = []
    for q in qs:
        if q in pd_ and pd_[q].get("response","").strip():
            ai_s = pd_[q].get("ai_score")
            vals.append(float(ai_s) if ai_s is not None else 0.5)
        else:
            vals.append(0.0)
    while len(vals) < 9: vals.append(0.0)
    return vals

def build_dim_radar(all_data, phase_name="", phase_num=1, current_q_idx=0):
    dim_qs = get_dim_qs(phase_name) if phase_name else []
    pd_    = all_data.get(phase_name, {}) if all_data and phase_name else {}
    values = _ai_score_values(dim_qs, pd_)
    N = 9
    start_angle = np.pi/2 - (2*np.pi/N)
    angles = np.linspace(start_angle, start_angle+2*np.pi, N, endpoint=False)
    fig, ax = plt.subplots(figsize=(5.5,5.8))
    fig.patch.set_facecolor("#07081a"); ax.set_facecolor("#07081a")
    ax.set_aspect("equal"); ax.axis("off")
    for r in [0.2,0.4,0.6,0.8,1.0]:
        px = [r*np.cos(a) for a in angles]+[r*np.cos(angles[0])]
        py = [r*np.sin(a) for a in angles]+[r*np.sin(angles[0])]
        ax.plot(px, py, color="#3a4a6a", linewidth=0.8, zorder=1)
    for a in angles:
        ax.plot([0,np.cos(a)],[0,np.sin(a)], color="#3a4a6a", linewidth=0.8, zorder=1)
    dx = [v*np.cos(a) for v,a in zip(values,angles)]
    dy = [v*np.sin(a) for v,a in zip(values,angles)]
    ax.fill(dx+[dx[0]], dy+[dy[0]], color="#f59e0b", alpha=0.25, zorder=2)
    ax.plot(dx+[dx[0]], dy+[dy[0]], color="#f59e0b", linewidth=2.0, zorder=3)
    for i in range(N):
        ax.plot([0,dx[i]],[0,dy[i]], color=VIBGYOR[i], linewidth=2.0, zorder=4)
        if values[i] > 0:
            ax.plot(dx[i], dy[i], marker='D', markersize=6, color=VIBGYOR[i], zorder=5)
    for i,a in enumerate(angles):
        r_text=1.15; tx=r_text*np.cos(a); ty=r_text*np.sin(a)
        ha = "left" if tx>0.1 else "right" if tx<-0.1 else "center"
        va = "bottom" if ty>0.1 else "top" if ty<-0.1 else "center"
        ax.text(tx,ty,f"D{i+1}",ha=ha,va=va,fontsize=9,color=VIBGYOR[i],fontweight="bold")
    if all(v==0 for v in values):
        ax.text(0,0,"Awaiting\nData",ha="center",va="center",fontsize=10,fontweight="bold",color="#f59e0b",zorder=12)
    cur_focus = get_focus_for_phase(phase_name) if phase_name else FOCUS_LABELS[0]
    ax.set_title(f"Phase{phase_num}: {phase_name}\nFocus: {cur_focus}", fontsize=8.5, color="#f1f5f9", fontweight="bold", pad=20)
    ax.set_xlim(-1.35,1.35); ax.set_ylim(-1.35,1.35)
    plt.tight_layout(pad=1.2)
    return fig

def build_eir_radar(all_data, phase_name="", phase_num=1, current_q_idx=0):
    eir_qs = get_eir_qs(phase_name) if phase_name else []
    pd_    = all_data.get(phase_name, {}) if all_data and phase_name else {}
    values = _ai_score_values(eir_qs, pd_)
    N=9; start_angle=np.pi/2-(2*np.pi/N)
    angles = np.linspace(start_angle, start_angle+2*np.pi, N, endpoint=False).tolist()
    bar_w = 2*np.pi/N*0.78
    fig, ax = plt.subplots(figsize=(5.5,5.8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#07081a"); ax.set_facecolor("#0d1035")
    for i,(angle,val) in enumerate(zip(angles,values)):
        color=VIBGYOR[i]
        if val<=0: ax.bar(angle,0.05,width=bar_w,bottom=0.04,color=color,alpha=0.12,edgecolor="#2a3a5a",linewidth=0.6,zorder=3)
        else:      ax.bar(angle,val,width=bar_w,bottom=0.04,color=color,alpha=0.88,edgecolor=color,linewidth=1.2,zorder=4)
    ax.set_ylim(0,1.22); ax.set_yticks([]); ax.set_xticks([])
    ax.spines["polar"].set_color("#ef4444")
    ax.grid(color="#1e2a4a",linewidth=0.4,linestyle="-",alpha=0.3)
    label_r=1.28
    for i,angle in enumerate(angles):
        ha="left" if np.cos(angle)>0.1 else "right" if np.cos(angle)<-0.1 else "center"
        ax.text(angle, label_r, f"EITR{i+1}", ha=ha, va="center", fontsize=7.5,
                color=VIBGYOR[i], fontweight="bold", transform=ax.transData)
    if all(v==0 for v in values):
        ax.text(0,0,"Awaiting\nData",ha="center",va="center",fontsize=10,fontweight="bold",color="#fca5a5",zorder=12,transform=ax.transData)
    cur_focus = get_focus_for_phase(phase_name) if phase_name else FOCUS_LABELS[0]
    ax.set_title(f"Phase{phase_num}: {phase_name}\nFocus: {cur_focus}", fontsize=8.5, color="#fca5a5", fontweight="bold", pad=28)
    plt.tight_layout(pad=1.2)
    return fig


# ══════════════════════════════════════════════════════════════════
#  NEW: Per-phase detail table (D1-D9 rows + EITR1-EITR9 rows)
#  Layout: Phase header row, Focus row, then question rows
# ══════════════════════════════════════════════════════════════════
def build_phase_detail_table(all_data, phase, is_sticky=False):
    """Builds a detailed question-by-question table for a single phase."""
    if not phase: return ""
    dim_qs    = get_dim_qs(phase)
    eir_qs    = get_eir_qs(phase)
    pd_       = all_data.get(phase, {}) if all_data else {}
    focus     = get_focus_for_phase(phase)
    raw       = ui_to_raw_map.get(phase, "")
    pnum      = clean_phases.index(phase)+1 if phase in clean_phases else 1
    all_scores = score_data.get(raw, [])
    dim_scores = all_scores[:9]
    eir_scores = all_scores[9:18]

    # Compact styling for sticky
    fs_table = "9px" if is_sticky else "11px"
    pad_cell = "4px 3px" if is_sticky else "8px 10px"

    TH = (f"font-family:Outfit,sans-serif;font-weight:700;font-size:{fs_table};"
          f"padding:8px 6px;text-align:center;text-transform:uppercase;"
          f"letter-spacing:0.4px;border:1px solid rgba(109,40,217,0.35);"
          f"color:#d1d5db;background:#2d1b69;")

    def td(txt, color="#e2e8f0", bold=False, align="center", bg=""):
        fs_  = "font-weight:700;" if bold else ""
        bgc = f"background:{bg};" if bg else ""
        return (f"<td style='padding:{pad_cell};font-size:{fs_table};color:{color};{fs_}{bgc}"
                f"border:1px solid rgba(109,40,217,0.14);text-align:{align};"
                f"white-space:normal;word-break:break-word;'>{txt}</td>")

    def qa_color(q):
        return "#86efac" if "✅" in q else "#fde68a" if "⚠️" in q else "#fca5a5" if "⏭️" in q else "#94a3b8"

    def assess_color(a):
        return "#86efac" if "🟢" in a else "#fde68a" if "🟡" in a else "#f97316" if "🟠" in a else "#fca5a5"

    def fmt_score(s):
        if s == 0: return "—"
        if s >= 1: return f"{s:.2f}"
        return f"{s:.4f}"

    # ── HEADER block ─────────────────────────────────────────────
    header_html = f"""
    <div style='background:rgba(109,40,217,0.15); border-radius:12px; padding:12px; margin-bottom:15px; border:1.5px solid rgba(109,40,217,0.4); text-align:center;'>
      <div style='font-family:Outfit,sans-serif; font-weight:800; font-size:1.3em; color:#f59e0b;'>📊 Phase {pnum}: {phase}</div>
      <div style='font-family:Sora,sans-serif; font-size:0.95em; color:#94a3b8; margin-top:4px;'>Focus: <span style='color:#fbbf24; font-weight:bold;'>{focus}</span></div>
    </div>"""

    # ── DIMENSIONS table ──────────────────────────────────────────
    dim_rows_html = ""
    dim_total_score = 0.0; dim_answered = 0
    for i, q in enumerate(dim_qs):
        code = f"D{i+1}"
        row_bg = "#0a0d2e" if i % 2 == 0 else "rgba(109,40,217,0.07)"
        if q in pd_:
            resp = pd_[q].get("response","").strip()
            if resp:
                dim_answered += 1
                ai_s = pd_[q].get("ai_score")
                bs   = dim_scores[i] if i < len(dim_scores) else 0.1
                sc   = (ai_s * bs if ai_s is not None else bs)
                dim_total_score += sc
                qa_st, grade, assess = "✅ Answered", fmt_score(sc), "🟢 Complete"
            else: qa_st, grade, assess = "⏭️ Skipped", "—", "🟡 Skipped"
        else: qa_st, grade, assess = "❌ N/A", "—", "🔴 N/A"

        dim_rows_html += f"<tr style='background:{row_bg};'>{td(code,color=VIBGYOR[i],bold=True)}{td(qa_st,color=qa_color(qa_st))}{td(grade,color='#f59e0b',bold=True)}{td(assess,color=assess_color(assess))}</tr>"

    dim_table = f"""
    <div style='background:rgba(13,16,53,0.95);border:1px solid rgba(245,158,11,0.35);border-radius:12px;overflow:hidden;margin-bottom:15px;'>
      <div style='background:#2d1b69;padding:10px;font-family:Outfit,sans-serif;font-weight:800;font-size:1em;color:#fbbf24;text-align:center;border-bottom:2px solid rgba(245,158,11,0.5);'>📐 Dimensions</div>
      <table style='width:100%;border-collapse:collapse;table-layout:fixed;'>
        <thead><tr><th style='{TH}'>ID</th><th style='{TH}'>Status</th><th style='{TH}'>Score</th><th style='{TH}'>Grade</th></tr></thead>
        <tbody>{dim_rows_html}</tbody>
      </table>
    </div>"""

    # ── EIR table ────────────────────────────────────────────────
    eir_rows_html = ""
    eir_total_score = 0.0; eir_answered = 0
    for i, q in enumerate(eir_qs):
        code = f"EITR{i+1}"
        row_bg = "#0a0d2e" if i % 2 == 0 else "rgba(239,68,68,0.05)"
        if q in pd_:
            resp = pd_[q].get("response","").strip()
            if resp:
                eir_answered += 1
                ai_s = pd_[q].get("ai_score")
                bs   = eir_scores[i] if i < len(eir_scores) else 0.1
                sc   = (ai_s * bs if ai_s is not None else bs)
                eir_total_score += sc
                qa_st, grade, assess = "✅ Answered", fmt_score(sc), "🟢 Complete"
            else: qa_st, grade, assess = "⏭️ Skipped", "—", "🟡 Skipped"
        else: qa_st, grade, assess = "❌ N/A", "—", "🔴 N/A"

        eir_rows_html += f"<tr style='background:{row_bg};'>{td(code,color=VIBGYOR[i],bold=True)}{td(qa_st,color=qa_color(qa_st))}{td(grade,color='#f59e0b',bold=True)}{td(assess,color=assess_color(assess))}</tr>"

    eir_table = f"""
    <div style='background:rgba(13,16,53,0.95);border:1px solid rgba(239,68,68,0.35);border-radius:12px;overflow:hidden;margin-bottom:15px;'>
      <div style='background:#2d1b69;padding:10px;font-family:Outfit,sans-serif;font-weight:800;font-size:1em;color:#fca5a5;text-align:center;border-bottom:2px solid rgba(239,68,68,0.55);'>🐘 Elephants In The Room</div>
      <table style='width:100%;border-collapse:collapse;table-layout:fixed;'>
        <thead><tr><th style='{TH}'>ID</th><th style='{TH}'>Status</th><th style='{TH}'>Score</th><th style='{TH}'>Grade</th></tr></thead>
        <tbody>{eir_rows_html}</tbody>
      </table>
    </div>"""

    total_score = dim_total_score + eir_total_score
    summary = f"""
    <div style='padding:12px;background:rgba(109,40,217,0.15);border-radius:10px;text-align:center;font-family:Sora,sans-serif;font-size:0.95em;border:1px solid rgba(109,40,217,0.2);'>
      Total Answered: <b style='color:#86efac;'>{dim_answered + eir_answered}/18</b> &nbsp;|&nbsp; Phase Score: <b style='color:#f59e0b;'>{fmt_score(total_score)}</b>
    </div>"""

    if is_sticky:
        return f"<div class='sticky-score-container'>{header_html}{dim_table}{eir_table}{summary}</div>"
    else:
        return f"<div class='dashboard-grid'>{dim_table}{eir_table}</div>{summary}"



# ══════════════════════════════════════════════════════════════════
#  OVERALL SCORECARD (summary across all phases)
# ══════════════════════════════════════════════════════════════════
def build_overall_metrics_html(all_data):
    total_dim = total_eir = 0
    total_dim_sc = total_eir_sc = 0.0
    for phase in clean_phases:
        dim_qs = get_dim_qs(phase); eir_qs = get_eir_qs(phase)
        pd_    = all_data.get(phase,{}) if all_data else {}
        raw    = ui_to_raw_map.get(phase,"")
        all_sc = score_data.get(raw,[])
        for i,q in enumerate(dim_qs):
            if q in pd_ and pd_[q].get("response","").strip():
                total_dim += 1
                ai_s = pd_[q].get("ai_score"); bs = all_sc[i] if i<len(all_sc) else 0.1
                total_dim_sc += (ai_s*bs if ai_s is not None else bs)
        for i,q in enumerate(eir_qs):
            j = i+9
            if q in pd_ and pd_[q].get("response","").strip():
                total_eir += 1
                ai_s = pd_[q].get("ai_score"); bs = all_sc[j] if j<len(all_sc) else 0.1
                total_eir_sc += (ai_s*bs if ai_s is not None else bs)
    total_ans = total_dim + total_eir
    total_max = len(clean_phases)*18
    overall_grade = round((total_ans/total_max)*10,1) if total_max and total_ans>0 else 0.0
    total_score = total_dim_sc + total_eir_sc

    def fs(s):
        if s==0: return "0.00"
        if s>=1000: return f"{s:,.0f}"
        if s>=1: return f"{s:.2f}"
        return f"{s:.4f}"

    return f"""
<div style='display:flex;justify-content:space-around;align-items:center;
     background:rgba(13,16,53,0.95);border:1px solid rgba(109,40,217,0.45);
     border-radius:12px;padding:20px;margin-top:10px;'>
  <div style='text-align:center;'>
    <div style='font-family:Outfit,sans-serif;color:#94a3b8;font-size:0.9em;text-transform:uppercase;letter-spacing:1px;margin-bottom:5px;'>Overall Grade</div>
    <div style='font-family:Sora,sans-serif;color:#f59e0b;font-size:2em;font-weight:700;'>{overall_grade}/10</div>
  </div>
  <div style='width:1px;height:50px;background:rgba(109,40,217,0.3);'></div>
  <div style='text-align:center;'>
    <div style='font-family:Outfit,sans-serif;color:#94a3b8;font-size:0.9em;text-transform:uppercase;letter-spacing:1px;margin-bottom:5px;'>Overall Score</div>
    <div style='font-family:Sora,sans-serif;color:#f59e0b;font-size:2em;font-weight:700;'>{fs(total_score)}</div>
  </div>
  <div style='width:1px;height:50px;background:rgba(109,40,217,0.3);'></div>
  <div style='text-align:center;'>
    <div style='font-family:Outfit,sans-serif;color:#94a3b8;font-size:0.9em;text-transform:uppercase;letter-spacing:1px;margin-bottom:5px;'>Total DIM</div>
    <div style='font-family:Sora,sans-serif;color:#86efac;font-size:2em;font-weight:700;'>{total_dim}<span style='font-size:0.4em;color:#64748b;'>/{len(clean_phases)*9}</span></div>
  </div>
  <div style='width:1px;height:50px;background:rgba(109,40,217,0.3);'></div>
  <div style='text-align:center;'>
    <div style='font-family:Outfit,sans-serif;color:#94a3b8;font-size:0.9em;text-transform:uppercase;letter-spacing:1px;margin-bottom:5px;'>Total EIR</div>
    <div style='font-family:Sora,sans-serif;color:#fca5a5;font-size:2em;font-weight:700;'>{total_eir}<span style='font-size:0.4em;color:#64748b;'>/{len(clean_phases)*9}</span></div>
  </div>
</div>"""


def build_scorecard(all_data, target_phase=None):
    phases = [target_phase] if target_phase else clean_phases
    phase_rows=[]; total_dim_all=0; total_eir_all=0; total_dim_sc=0.0; total_eir_sc=0.0
    TH = ("font-family:Outfit,sans-serif;font-weight:700;font-size:9px;"
          "padding:6px 4px;text-align:center;text-transform:uppercase;"
          "letter-spacing:0.3px;border:1px solid rgba(109,40,217,0.35);"
          "white-space:normal;color:#d1d5db;background:#2d1b69;")

    def td(txt, color="#e2e8f0", bold=False, align="center"):
        fs="font-weight:700;" if bold else ""
        return (f"<td style='padding:5px 4px;font-size:10px;color:{color};{fs}"
                f"border:1px solid rgba(109,40,217,0.14);text-align:{align};"
                f"white-space:normal;word-break:break-word;'>{txt}</td>")

    for phase in phases:
        dim_qs=get_dim_qs(phase); eir_qs=get_eir_qs(phase)
        pd_=all_data.get(phase,{}) if all_data else {}
        focus=get_focus_for_phase(phase); raw=ui_to_raw_map.get(phase,"")
        pnum=clean_phases.index(phase)+1 if phase in clean_phases else 1
        all_sc=score_data.get(raw,[]); dim_sc=all_sc[:9]; eir_sc=all_sc[9:18]
        base=dim_sc[0] if dim_sc else 0.1
        dim_ans=0;dim_skip=0;dim_vis=0;dim_score=0.0
        for i,q in enumerate(dim_qs):
            if q in pd_:
                dim_vis+=1
                if pd_[q].get("response","").strip():
                    dim_ans+=1; ai_s=pd_[q].get("ai_score"); bs=dim_sc[i] if i<len(dim_sc) else base
                    dim_score+=(ai_s*bs if ai_s is not None else bs)
                else: dim_skip+=1
        eir_ans=0;eir_skip=0;eir_vis=0;eir_score=0.0
        for i,q in enumerate(eir_qs):
            if q in pd_:
                eir_vis+=1
                if pd_[q].get("response","").strip():
                    eir_ans+=1; ai_s=pd_[q].get("ai_score"); bs=eir_sc[i] if i<len(eir_sc) else base
                    eir_score+=(ai_s*bs if ai_s is not None else bs)
                else: eir_skip+=1
        total_dim_all+=dim_ans; total_eir_all+=eir_ans
        total_dim_sc+=dim_score; total_eir_sc+=eir_score

        def fsc(s): return "—" if s==0 else f"{s:.2f}" if s>=1 else f"{s:.4f}"
        def qa(a,sk,vi):
            if vi==0: return "❌ Not Started"
            if sk>0 and a>0: return f"⚠️ {a} Ans,{sk} Skip"
            if sk>0: return f"⏭️ All {sk} Skipped"
            return f"✅ {a}/9"
        tot=dim_ans+eir_ans; pct=int((tot/18)*100) if (dim_vis+eir_vis)>0 else 0
        ass=("🔴 Not Started" if (dim_vis+eir_vis)==0 else "🟡 In Progress" if pct<50 else "🟠 Partial" if pct<100 else "🟢 Complete")
        phase_rows.append({"name":phase,"focus":focus,"pnum":pnum,
            "dim_qa":qa(dim_ans,dim_skip,dim_vis),"eir_qa":qa(eir_ans,eir_skip,eir_vis),
            "assess":ass,"dim_grade":fsc(dim_score),"eir_grade":fsc(eir_score)})

    total_ans=total_dim_all+total_eir_all; total_max=len(phases)*18
    overall_grade=round((total_ans/total_max)*10,1) if total_max and total_ans>0 else 0.0
    ts=total_dim_sc+total_eir_sc
    tsc="0.00" if ts==0 else f"{ts:.2f}" if ts>=1 else f"{ts:.4f}"

    def mkt(rows_html, cols, headers):
        cg="".join(f"<col style='width:{w};'/>" for w in cols)
        h=f"<table style='width:100%;border-collapse:collapse;table-layout:fixed;'><colgroup>{cg}</colgroup><thead><tr>"
        for hd in headers: h+=f"<th style='{TH}'>{hd}</th>"
        h+="</tr></thead><tbody>"
        for i,r in enumerate(rows_html):
            bg="#0a0d2e" if i%2==0 else "rgba(109,40,217,0.07)"
            h+=f"<tr style='background:{bg};'>{r}</tr>"
        h+="</tbody></table>"
        return h

    pf=[]; di=[]; ei=[]
    def qc(q): return "#86efac" if "✅" in q else "#fde68a" if "⚠️" in q else "#fca5a5" if "⏭️" in q else "#94a3b8"
    def ac(a): return "#86efac" if "🟢" in a else "#fde68a" if "🟡" in a else "#f97316" if "🟠" in a else "#fca5a5"
    for r in phase_rows:
        pf.append(td(f"P{r['pnum']}: {r['name']}",color="#c4b5fd",bold=True,align="left")+td(r["focus"],color="#fbbf24",bold=True))
        di.append(td(r["dim_qa"],color=qc(r["dim_qa"]))+td(r["dim_grade"],color="#f59e0b",bold=True)+td(r["assess"],color=ac(r["assess"])))
        ei.append(td(r["eir_qa"],color=qc(r["eir_qa"]))+td(r["eir_grade"],color="#f59e0b",bold=True)+td(r["assess"],color=ac(r["assess"])))

    title_suffix=f" — {target_phase}" if target_phase else ""
    return f"""
<div style='text-align:center;margin-bottom:12px;'>
  <span style='font-family:Outfit,sans-serif;font-weight:900;font-size:1.25em;color:#f59e0b;letter-spacing:1px;'>
    📊 Detailed Score Card{title_suffix}
  </span>
</div>
<div style='display:grid;grid-template-columns:0.9fr 1fr 1fr;gap:8px;width:100%;box-sizing:border-box;'>
  <div style='background:rgba(13,16,53,0.95);border:1px solid rgba(109,40,217,0.30);border-radius:10px;overflow:hidden;'>
    <div style='background:#2d1b69;padding:8px 10px;font-family:Outfit,sans-serif;font-weight:800;font-size:0.85em;color:#c4b5fd;text-align:center;border-bottom:2px solid rgba(109,40,217,0.45);'>🎯 Phase / Focus</div>
    {mkt(pf,["58%","42%"],["Phase","Focus"])}
  </div>
  <div style='background:rgba(13,16,53,0.95);border:1px solid rgba(245,158,11,0.30);border-radius:10px;overflow:hidden;'>
    <div style='background:#2d1b69;padding:8px 10px;font-family:Outfit,sans-serif;font-weight:800;font-size:0.85em;color:#fbbf24;text-align:center;border-bottom:2px solid rgba(245,158,11,0.45);'>📐 Dimensions</div>
    {mkt(di,["42%","22%","36%"],["Q&A Status","Grading","Assessment"])}
  </div>
  <div style='background:rgba(13,16,53,0.95);border:1px solid rgba(239,68,68,0.30);border-radius:10px;overflow:hidden;'>
    <div style='background:#2d1b69;padding:8px 10px;font-family:Outfit,sans-serif;font-weight:800;font-size:0.85em;color:#fca5a5;text-align:center;border-bottom:2px solid rgba(239,68,68,0.50);'>🐘 Elephants in the Room</div>
    {mkt(ei,["42%","22%","36%"],["Q&A Status","Grading","Assessment"])}
  </div>
</div>
<div style='margin-top:10px;font-size:0.85em;color:#94a3b8;font-family:Sora,sans-serif;text-align:center;padding:8px;background:rgba(13,16,53,0.6);border-radius:8px;'>
  <b style='color:#f59e0b;font-size:1.05em;'>Grade: {overall_grade}/10</b>
  &nbsp;·&nbsp; Score: <b style='color:#f59e0b;'>{tsc}</b>
  &nbsp;·&nbsp; Dim: {total_dim_all}/{len(phases)*9}
  &nbsp;·&nbsp; EIR: {total_eir_all}/{len(phases)*9}
</div>"""

# (get_all_phase_scorecards removed)


# ══════════════════════════════════════════════════════════════════
#  CERTIFICATE
# ══════════════════════════════════════════════════════════════════
def make_certificate(all_data, name, photo_path, ip_address):
    W,H=1500,960; img=Image.new("RGB",(W,H)); draw=ImageDraw.Draw(img)
    for y in range(H):
        t=y/H; draw.line([(0,y),(W,y)],fill=(int(6+12*t),int(8+8*t),int(24+22*t)))
    rng=np.random.default_rng(42)
    for _ in range(200):
        sx,sy=int(rng.uniform(0,W)),int(rng.uniform(0,H)); alp=int(rng.uniform(60,190)); ss=rng.choice([1,1,2])
        draw.ellipse([sx,sy,sx+ss,sy+ss],fill=(alp,alp,int(alp*0.9)))
    for off,col,w in [(8,(109,40,217),2)]:
        draw.rectangle([off,off,W-off,H-off],outline=col,width=w)
    try:
        fp_b="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        fp_r="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        f72=ImageFont.truetype(fp_b,72); f44=ImageFont.truetype(fp_b,44)
        f32=ImageFont.truetype(fp_b,32); f24=ImageFont.truetype(fp_r,24); f14=ImageFont.truetype(fp_r,14)
    except:
        f72=f44=f32=f24=f14=ImageFont.load_default()
    cx=W//2
    utc_now=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    draw.text((cx,62),"🦄  i2u.ai",fill=(245,158,11),font=f44,anchor="mm")
    draw.text((cx,100),f"IP: {ip_address}  |  {utc_now}",fill=(100,116,139),font=f14,anchor="mm")
    draw.text((cx,130),"UNICORN FOUNDATIONAL ASSESSMENT",fill=(226,232,240),font=f32,anchor="mm")
    draw.line([(120,160),(W-120,160)],fill=(245,158,11),width=2)
    draw.text((cx,200),"Certificate of Assessment Participation",fill=(148,163,184),font=f24,anchor="mm")
    draw.text((cx,244),"This certifies that",fill=(100,116,139),font=f24,anchor="mm")
    n=(name or "The Founder").strip()
    draw.text((cx+2,350),n,fill=(92,40,0),font=f72,anchor="mm")
    draw.text((cx,348),n,fill=(245,158,11),font=f72,anchor="mm")
    nb=draw.textbbox((cx,348),n,font=f72,anchor="mm")
    for lx in range(nb[0]-14,nb[2]+14):
        a=max(0,1-abs(lx-cx)/((nb[2]-nb[0])/2+14))
        draw.line([(lx,nb[3]+14),(lx,nb[3]+17)],fill=(int(245*a),int(158*a),0))
    ta=sum(len(v) for v in all_data.values()) if all_data else 0
    np_=len(all_data)
    draw.text((cx,430),"has completed the i2u.ai Unicorn Foundational Assessment",fill=(148,163,184),font=f24,anchor="mm")
    draw.text((cx,476),f"{np_} phases  ·  {ta} questions answered",fill=(167,139,250),font=f32,anchor="mm")
    draw.text((cx,560),datetime.now().strftime("%B %d, %Y"),fill=(100,116,139),font=f24,anchor="mm")
    bx,by,br=cx,648,52
    draw.ellipse([bx-br,by-br,bx+br,by+br],fill=(30,10,70),outline=(245,158,11),width=3)
    draw.line([(110,H-90),(W-110,H-90)],fill=(20,30,60),width=1)
    draw.text((cx,H-58),"Provisional Certificate  ·  Unicolt Quiz  ·  i2u.ai Confidential",fill=(40,55,90),font=f14,anchor="mm")
    if photo_path:
        try:
            ph=Image.open(photo_path).convert("RGBA").resize((210,210))
            msk=Image.new("L",(210,210),0); ImageDraw.Draw(msk).ellipse([0,0,210,210],fill=255)
            circ=Image.new("RGBA",(210,210),0); circ.paste(ph,mask=msk)
            rgba=img.convert("RGBA"); px,py=W-255,48
            rgba.paste(circ,(px,py),circ)
            d2=ImageDraw.Draw(rgba)
            for ro,rc in [(0,(245,158,11)),(6,(109,40,217))]:
                d2.ellipse([px-ro-4,py-ro-4,px+210+ro+4,py+210+ro+4],outline=rc,width=2)
            img=rgba.convert("RGB")
        except: pass
    return img


# ══════════════════════════════════════════════════════════════════
#  APP LOGIC
# ══════════════════════════════════════════════════════════════════
def get_phase_num(phase_name):
    try: return clean_phases.index(phase_name)+1
    except: return 1

def make_go_to_phase(pname, phase_num):
    def _fn(all_data):
        all_qs = get_all_qs(pname); first_q = all_qs[0] if all_qs else ""
        pf = get_focus_for_phase(pname); label, focus = q_label(0, pf)
        btn_style = ("background:rgba(109,40,217,0.18);border:1px solid rgba(109,40,217,0.45);"
                     "border-radius:10px;color:#c4b5fd;font-family:Outfit,sans-serif;font-weight:700;"
                     "font-size:0.85em;padding:8px 16px;cursor:pointer;margin-bottom:8px;text-transform:uppercase;")
        logo_bar = (f"<div style='display:flex;align-items:center;justify-content:space-between;"
                    f"padding:10px 20px;background:linear-gradient(90deg,rgba(13,16,53,0.98),rgba(7,8,26,0.92));"
                    f"border-bottom:1px solid rgba(109,40,217,0.28);margin-bottom:8px;width:100%;box-sizing:border-box;'>"
                    f"<div style='display:flex;flex-direction:column;align-items:center;gap:3px;'>"
                    f"<img src='{LOGO_SRC}' style='width:44px;height:44px;border-radius:12px;object-fit:cover;'/>"
                    f"<span style='font-family:Outfit,sans-serif;font-weight:900;font-size:0.85em;"
                    f"background:linear-gradient(135deg,#f59e0b,#8b5cf6);-webkit-background-clip:text;"
                    f"-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:1px;'>i2u.ai</span>"
                    f"<span style='font-family:Sora,sans-serif;font-size:0.60em;color:#64748b;'>Unicolt Quiz</span>"
                    f"</div>"
                    f"<div style='display:flex;flex-direction:column;align-items:center;flex:1;padding:0 16px;'>"
                    f"  <button onclick=\"document.getElementById('hidden-back-btn').click()\" style=\"{btn_style}\">"
                    f"      🏠 UNICOLT QUIZ HOME</button>"
                    f"</div>"
                    f"<div style='font-family:Sora,sans-serif;font-size:0.90em;color:#f59e0b;font-weight:700;text-align:right;min-width:120px;'>"
                    f"Focus: {pf}</div></div>")
        
        phase_title = f"<div class='phase-header-title'>👉 Phase {phase_num}: {pname}</div>"
        combined_hdr = logo_bar + phase_title
        
        return (
            gr.update(visible=False), gr.update(visible=True), # home, phase pages
            pname, 0, # current_phase, q_index
            first_q, f"{focus} {label}", # question_display, question_title
            "Dimensions: Question 1 of 9", # progress
            gr.update(value=""), gr.update(value=""), # response, save_status
            gr.update(visible=False), gr.update(visible=False), # warnings
            build_dim_radar(all_data, pname, phase_num, 0),
            build_eir_radar(all_data, pname, phase_num, 0),
            build_scorecard(all_data, None),
            build_overall_metrics_html(all_data),
            # Dashboard Outputs
            build_phase_detail_table(all_data, pname, is_sticky=True),
            build_phase_detail_table(all_data, pname, is_sticky=False),
            gr.update(value="", visible=False), # ai_feedback_out
            gr.update(value=combined_hdr),      # phase_header_html
        )
    return _fn


def go_home():
    return gr.update(visible=True), gr.update(visible=False)

def save_and_advance(phase, q_index, text, files, all_data):
    import hashlib
    all_qs=get_all_qs(phase); phase_num=get_phase_num(phase)
    if not phase or not all_qs:
        return (all_data, q_index, "⚠️ No phase loaded.",
                gr.update(), gr.update(), gr.update(),
                gr.update(visible=False), gr.update(visible=False),
                gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
                gr.update(), gr.update(), gr.update(visible=False))

    current_q=all_qs[q_index]; phase_focus=get_focus_for_phase(phase); label,focus=q_label(q_index,phase_focus)
    was_skipped=not (text and text.strip())
    all_data.setdefault(phase,{})[current_q]={"response":text.strip() if text else "","skipped":was_skipped,"ai_score":None,"files":[f.name for f in files] if files else []}

    if was_skipped:
        status_msg=f"⏭️ Skipped **{label}**."; skip_visible=True; ai_update=gr.update(value="",visible=False)
    else:
        status_msg=f"✅ Saved **{label}**."; skip_visible=False
        ai_fb=llm_evaluate_answer(phase,phase_focus,label,current_q,text)
        if ai_fb:
            ai_sc=parse_ai_score(ai_fb)
            if ai_sc is not None: all_data[phase][current_q]["ai_score"]=ai_sc
            ai_update=gr.update(value=f"🤖 **AI Mentor Feedback:**\n\n{ai_fb}",visible=True)
        else: ai_update=gr.update(value="",visible=False)

    next_idx=q_index+1
    if next_idx==9 and not was_skipped:
        dim_qs=get_dim_qs(phase); pd_=all_data.get(phase,{})
        if sum(1 for q in dim_qs if q in pd_ and pd_[q].get("response","").strip())<9:
            return (all_data, q_index, status_msg, gr.update(), gr.update(), gr.update(),
                    gr.update(visible=True), gr.update(visible=skip_visible), gr.update(value=""),
                    build_dim_radar(all_data,phase,phase_num,q_index),
                    build_eir_radar(all_data,phase,phase_num,q_index),
                    build_scorecard(all_data,None), build_overall_metrics_html(all_data),
                    build_phase_detail_table(all_data, phase, True),
                    build_phase_detail_table(all_data, phase, False), ai_update)

    if next_idx>=len(all_qs):
        return (all_data, q_index, f"🏆 **{phase} complete!**",
                gr.update(value="✅ Complete!"), gr.update(value="✅ Phase Complete!"),
                gr.update(value="🏆 Phase Complete!"), gr.update(visible=False), gr.update(visible=False), gr.update(value=""),
                build_dim_radar(all_data,phase,phase_num,q_index),
                build_eir_radar(all_data,phase,phase_num,q_index),
                build_scorecard(all_data,None), build_overall_metrics_html(all_data),
                build_phase_detail_table(all_data, phase, True),
                build_phase_detail_table(all_data, phase, False), gr.update(value="",visible=False))

    next_q=all_qs[next_idx]; nl,nf=q_label(next_idx,phase_focus); is_eir=next_idx>=9; li=(next_idx-9+1) if is_eir else (next_idx+1); sec="EIR" if is_eir else "Dimensions"
    return (all_data, next_idx, status_msg,
            gr.update(value=next_q), gr.update(value=f"{nf} {nl}"),
            gr.update(value=f"{sec}: Q{li}/9"),
            gr.update(visible=False), gr.update(visible=skip_visible), gr.update(value=""),
            build_dim_radar(all_data,phase,phase_num,next_idx),
            build_eir_radar(all_data,phase,phase_num,next_idx),
            build_scorecard(all_data,None), build_overall_metrics_html(all_data),
            build_phase_detail_table(all_data, phase, True),
            build_phase_detail_table(all_data, phase, False), ai_update)

def go_back(phase, q_index, all_data):
    phase_num=get_phase_num(phase); all_qs=get_all_qs(phase); prev_idx=max(0,q_index-1); prev_q=all_qs[prev_idx]
    bf=get_focus_for_phase(phase); pl,pf=q_label(prev_idx,bf); is_eir=prev_idx>=9; li=(prev_idx-9+1) if is_eir else (prev_idx+1); sec="EIR" if is_eir else "Dimensions"
    pd_=all_data.get(phase,{}); prev_ans=pd_.get(prev_q,{}).get("response","") if prev_q in pd_ else ""
    return (all_data, prev_idx, f"↩️ Back to {pl}.",
            gr.update(value=prev_q), gr.update(value=f"{pf} {pl}"),
            gr.update(value=f"{sec}: Q{li}/9"),
            gr.update(visible=False), gr.update(visible=False), gr.update(value=prev_ans),
            build_dim_radar(all_data,phase,phase_num,prev_idx),
            build_eir_radar(all_data,phase,phase_num,prev_idx),
            build_scorecard(all_data,None), build_overall_metrics_html(all_data),
            build_phase_detail_table(all_data, phase, True),
            build_phase_detail_table(all_data, phase, False), gr.update(value="",visible=False))

def gen_cert(all_data, name, photo, request: gr.Request):
    ip_addr=request.client.host if request and request.client else "Unknown IP"
    path=photo if isinstance(photo,str) else (photo.name if photo else None)
    return make_certificate(all_data, name or "", path, ip_addr)

def try_go_to_eir(phase, all_data):
    dim_qs=get_dim_qs(phase); pd_=all_data.get(phase,{}) if all_data else {}
    dim_done=sum(1 for q in dim_qs if q in pd_ and pd_[q].get("response","").strip())
    return gr.update(visible=(dim_done<9))

def final_submit(all_data, founder_name):
    ta=sum(len(v) for v in all_data.values()) if all_data else 0
    if ta==0: return "⚠️ Please answer at least one question before submitting."
    return llm_hitl_report(all_data, founder_name or "The Founder")


# ══════════════════════════════════════════════════════════════════
#  THEME
# ══════════════════════════════════════════════════════════════════
theme = gr.themes.Base(
    primary_hue=gr.themes.colors.violet, secondary_hue=gr.themes.colors.blue,
    neutral_hue=gr.themes.colors.slate,
    font=[gr.themes.GoogleFont("Sora"),"system-ui"],
    font_mono=[gr.themes.GoogleFont("JetBrains Mono"),"monospace"],
    radius_size=gr.themes.sizes.radius_lg, spacing_size=gr.themes.sizes.spacing_md,
).set(
    background_fill_primary="#07081a", background_fill_secondary="#0d1035",
    block_background_fill="#0d1035", block_border_color="rgba(109,40,217,0.28)",
    block_border_width="1px", block_shadow="0 0 32px rgba(109,40,217,0.12)",
    body_text_color="#e2e8f0", body_text_color_subdued="#64748b",
    block_label_text_color="#94a3b8",
    button_primary_background_fill="linear-gradient(135deg,#f59e0b,#d97706)",
    button_primary_background_fill_hover="linear-gradient(135deg,#fbbf24,#f59e0b)",
    button_primary_text_color="#07081a", button_primary_border_color="#f59e0b",
    button_secondary_background_fill="rgba(109,40,217,0.14)",
    button_secondary_background_fill_hover="rgba(109,40,217,0.26)",
    button_secondary_text_color="#c4b5fd", button_secondary_border_color="rgba(109,40,217,0.42)",
    input_background_fill="#0a0c25", input_border_color="rgba(109,40,217,0.40)",
    input_border_color_focus="#f59e0b", input_placeholder_color="#475569",
)


# ══════════════════════════════════════════════════════════════════
#  UI
# ══════════════════════════════════════════════════════════════════
with gr.Blocks(title="i2u.ai — Unicolt Quiz") as demo:

    saved_data    = gr.State({})
    current_phase = gr.State("")
    q_index_state = gr.State(0)

    hidden_back_btn = gr.Button("🏠 Unicolt Quiz Home", elem_id="hidden-back-btn", elem_classes=["hidden-btn"])

    LOGO_HTML = f"""
    <div class="logo-header">
      <img src="{LOGO_SRC}" alt="i2u.ai logo"
           style="width:72px;height:72px;max-width:72px;max-height:72px;
                  border-radius:18px;object-fit:cover;display:block;margin:0 auto 10px auto;"/>
      <div class="brand-name">i2u.ai</div>
      <div class="tagline">Ideas to Unicorns &nbsp;·&nbsp; AI-Powered Unicolt Quiz</div>
    </div>"""

    # ── PAGE 1: HOME ─────────────────────────────────────────────
    with gr.Group(visible=True) as home_page:
        gr.HTML(LOGO_HTML)
        gr.Markdown("### Select Your Assessment Phase", elem_classes=["c"])
        phase_buttons = []
        rows = [clean_phases[i:i+3] for i in range(0, len(clean_phases), 3)]
        for row_idx, row_phases in enumerate(rows):
            with gr.Row(equal_height=True):
                for col_idx, name in enumerate(row_phases):
                    emoji = get_emoji(name); phase_num = row_idx*3+col_idx+1
                    card_label = f"Phase{phase_num}: {emoji}  {name}"
                    with gr.Column(scale=1, min_width=210):
                        btn = gr.Button(card_label, variant="secondary", elem_classes=["phase-btn"])
                        phase_buttons.append((btn, name, phase_num))
        gr.Markdown("---\n_© i2u.ai — All submissions are private and confidential._",
                    elem_classes=["footer-md"])

    # ── PAGE 2: WORKSPACE ────────────────────────────────────────
    # ── PAGE 2: WORKSPACE ────────────────────────────────────────
    with gr.Group(visible=False) as phase_page:

        scorecard_sticky = gr.HTML(elem_classes=["sticky-score-container"])
        phase_header_html = gr.HTML(elem_classes=["phase-hd"])

        with gr.Row():
            with gr.Column(scale=1):
                dim_radar_out = gr.Plot(label=None, show_label=False)
            with gr.Column(scale=1):
                eir_radar_out = gr.Plot(label=None, show_label=False)

        with gr.Row():
            with gr.Column(scale=5):
                progress_md       = gr.Markdown("Dimensions: Question 1 of 9", elem_classes=["c"])
                eir_nav_btn       = gr.Button("🐘 Elephants in the Room", variant="secondary", size="sm")
                question_title_md = gr.Markdown("**Resilience D1**", elem_classes=["question-title","c"])
                question_display  = gr.Markdown("_Select a phase to load questions._",
                                                elem_classes=["question-display"])
                skip_warning = gr.Markdown("⏭️ **You skipped this question.**",
                                           elem_classes=["skip-warning"], visible=False)
                user_response = gr.Textbox(label="Your Response", lines=4, max_lines=7,
                                            placeholder="Enter your response here...",
                                            elem_classes=["response-box"])
                user_files = gr.File(file_count="multiple", show_label=False)
                with gr.Row():
                    go_back_btn = gr.Button("← Improve / Go Back", variant="secondary", size="sm")
                    save_btn    = gr.Button("💾  Save & Next", variant="primary", size="lg")
                save_status     = gr.Markdown(elem_classes=["save-st"])
                ai_feedback_out = gr.Markdown(value="", elem_classes=["hitl-block"], visible=False)

            with gr.Column(scale=4):
                eir_warning = gr.Markdown("🔴 **Complete all 9 Dimensions questions first.**",
                                          elem_classes=["eir-warning"], visible=False)
                with gr.Tabs():
                    with gr.TabItem("🎓 Certificate & Submit"):
                        founder_name  = gr.Textbox(label="Your Full Name")
                        founder_photo = gr.Image(label="Upload Photo", type="filepath", height=150)
                        gen_btn  = gr.Button("🎨 Generate Preview", variant="primary", size="lg")
                        cert_img = gr.Image(label="", height=250)
                        submit_btn = gr.Button("✅ Confirm & Submit", variant="primary", size="lg")
                        submit_status = gr.Markdown()

                    with gr.TabItem("🌟 Overall Metrics"):
                        overall_metrics_out = gr.HTML(build_overall_metrics_html({}))
                    
                    with gr.TabItem("🏆 All Phases"):
                        global_scorecard_out = gr.HTML(build_scorecard({}, target_phase=None))

        gr.Markdown("---")
        # Redesigned core section: Dashboard Grade Layout
        scorecard_inline = gr.HTML()

        gr.Markdown("---")
        gr.Markdown("### 👤 Human in the Loop Report (HITL)", elem_classes=["hitl-block"])

    # ── WIRING ────────────────────────────────────────────────────
    PHASE_OUTS = [
        home_page, phase_page,
        current_phase, q_index_state,
        question_display, question_title_md, progress_md,
        user_response, save_status,
        eir_warning, skip_warning,
        dim_radar_out, eir_radar_out,
        global_scorecard_out,
        overall_metrics_out,
        # Redesigned Dashboard outputs
        scorecard_sticky,
        scorecard_inline,
        ai_feedback_out,
        phase_header_html,
    ]

    SAVE_OUTS = [
        saved_data, q_index_state, save_status,
        question_display, question_title_md, progress_md,
        eir_warning, skip_warning, user_response,
        dim_radar_out, eir_radar_out,
        global_scorecard_out,
        overall_metrics_out,
        # Redesigned Dashboard outputs
        scorecard_sticky,
        scorecard_inline,
        ai_feedback_out,
    ]

    for btn, name, num in phase_buttons:
        btn.click(fn=make_go_to_phase(name, num), inputs=[saved_data], outputs=PHASE_OUTS)

    hidden_back_btn.click(fn=go_home, inputs=[], outputs=[home_page, phase_page])

    save_btn.click(fn=save_and_advance,
                   inputs=[current_phase, q_index_state, user_response, user_files, saved_data],
                   outputs=SAVE_OUTS)

    go_back_btn.click(fn=go_back,
                      inputs=[current_phase, q_index_state, saved_data],
                      outputs=SAVE_OUTS)

    eir_nav_btn.click(fn=try_go_to_eir, inputs=[current_phase, saved_data], outputs=[eir_warning])

    gen_btn.click(fn=gen_cert, inputs=[saved_data, founder_name, founder_photo], outputs=[cert_img])

    submit_btn.click(fn=final_submit, inputs=[saved_data, founder_name], outputs=[submit_status])

if __name__ == "__main__":
    demo.launch(theme=theme, css=CSS)