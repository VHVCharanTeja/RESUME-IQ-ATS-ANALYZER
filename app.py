import streamlit as st
from resume_parser.extract_text import extract_text_from_pdf
from resume_parser.extract_skills import extract_skills
from ats.ats_score import calculate_ats_score
import json
from utils.interview_helper import get_questions
from utils.suggestions import generate_suggestions
from utils.report_generator import generate_report
from utils.jd_matcher import (
    extract_jd_skills,
    calculate_jd_match
)
from utils.resume_rewriter import generate_rewrite_suggestions
from utils.roadmap_generator import generate_learning_roadmap
from utils.strengths import get_strengths_weaknesses
from utils.breakdown import calculate_breakdown
from utils.career_recommender import recommend_roles
from utils.resume_rating import calculate_resume_rating, calculate_improvement_potential
from utils.mock_interview import evaluate_answer
from utils.interview_answers import get_answers


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeIQ – ATS Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #090d14;
    color: #e2e8f0;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1280px; }

/* ════════════════════════════════════════
   COLOR RAMPS
   Purple  — branding / navigation
   Teal    — matched / success
   Blue    — informational / external
   Amber   — roadmap / warnings
   Red     — missing / error
   ════════════════════════════════════════ */

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0f1520 0%, #090d14 55%, #110d1f 100%);
    border: 1px solid #1e2535;
    border-radius: 20px;
    padding: 2.75rem 3rem 2.5rem 3rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -100px; right: -100px;
    width: 360px; height: 360px;
    background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 40%;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(20,184,166,0.07) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-eyebrow {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #818cf8;
    margin-bottom: 0.65rem;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1.15;
    margin-bottom: 0.65rem;
}
.hero-title .accent-purple { color: #818cf8; }
.hero-sub {
    font-size: 0.93rem;
    color: #94a3b8;
    max-width: 540px;
    line-height: 1.65;
    margin-bottom: 1.5rem;
}

/* ── Hero badge row ── */
.hero-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-top: 0.25rem;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.3rem 0.85rem;
    border-radius: 20px;
}
.badge-purple { background: #1e1b4b; color: #a5b4fc; border: 1px solid #3730a3; }
.badge-teal   { background: #042f2e; color: #5eead4; border: 1px solid #0f766e; }
.badge-blue   { background: #0c1a3a; color: #93c5fd; border: 1px solid #1d4ed8; }
.badge-amber  { background: #1c1200; color: #fcd34d; border: 1px solid #92400e; }

/* ── Section label ── */
.section-label {
    font-size: 0.67rem;
    font-weight: 600;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 0.45rem;
}

/* ── Cards ── */
.card {
    background: #0f1520;
    border: 1px solid #1e2535;
    border-radius: 14px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.25rem;
}
.card-title {
    font-size: 0.79rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    margin-bottom: 1rem;
}

/* Card accent borders */
.card-teal  { border-left: 3px solid #0d9488; }
.card-red   { border-left: 3px solid #b91c1c; }
.card-blue  { border-left: 3px solid #1d4ed8; }
.card-amber { border-left: 3px solid #b45309; }
.card-purple{ border-left: 3px solid #6366f1; }

/* ── Score ring wrapper ── */
.score-wrap {
    background: #0f1520;
    border: 1px solid #1e2535;
    border-radius: 14px;
    padding: 2.25rem 1.5rem;
    text-align: center;
    margin-bottom: 1.25rem;
}
.score-number {
    font-size: 4.2rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
    margin-bottom: 0.35rem;
}
.score-label {
    font-size: 0.78rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.score-verdict {
    margin-top: 0.8rem;
    font-size: 0.84rem;
    font-weight: 500;
    padding: 0.35rem 1rem;
    border-radius: 20px;
    display: inline-block;
}

/* ── Skill pills ── */
.pill-wrap { display: flex; flex-wrap: wrap; gap: 0.45rem; }
.pill {
    font-size: 0.76rem;
    font-weight: 500;
    padding: 0.28rem 0.8rem;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
}
.pill-teal  { background: #042f2e; color: #5eead4; border: 1px solid #0f766e; }
.pill-blue  { background: #0c1a3a; color: #93c5fd; border: 1px solid #1d4ed8; }
.pill-red   { background: #2d0a0a; color: #fca5a5; border: 1px solid #7f1d1d; }
.pill-amber { background: #1c1200; color: #fcd34d; border: 1px solid #92400e; }
.pill-purple{ background: #1e1b4b; color: #a5b4fc; border: 1px solid #3730a3; }

/* legacy alias used by render_pills */
.pill-green { background: #042f2e; color: #5eead4; border: 1px solid #0f766e; }

/* ── Link styles ── */
a.link-purple { color: #818cf8; text-decoration: none; border-bottom: 1px solid #4338ca; }
a.link-purple:hover { color: #a5b4fc; border-color: #6366f1; }
a.link-teal   { color: #5eead4; text-decoration: none; border-bottom: 1px solid #0f766e; }
a.link-teal:hover { color: #99f6e4; border-color: #14b8a6; }
a.link-blue   { color: #93c5fd; text-decoration: none; border-bottom: 1px solid #1d4ed8; }
a.link-blue:hover { color: #bfdbfe; border-color: #3b82f6; }
a.link-amber  { color: #fcd34d; text-decoration: none; border-bottom: 1px solid #92400e; }
a.link-amber:hover { color: #fde68a; border-color: #b45309; }

/* ── Gradient progress bars ── */
.stProgress > div > div > div > div {
    border-radius: 4px;
}
.stProgress > div > div > div {
    background: #1e2535;
    border-radius: 4px;
    height: 8px !important;
}
/* Named progress classes applied via JS workaround – use inline style override per metric */
.bar-purple .stProgress > div > div > div > div { background: linear-gradient(90deg,#6366f1,#8b5cf6); }
.bar-teal   .stProgress > div > div > div > div { background: linear-gradient(90deg,#0d9488,#14b8a6); }
.bar-blue   .stProgress > div > div > div > div { background: linear-gradient(90deg,#1d4ed8,#3b82f6); }
.bar-amber  .stProgress > div > div > div > div { background: linear-gradient(90deg,#b45309,#f59e0b); }
/* Default fallback */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
}

/* ── Selectbox & uploader ── */
.stSelectbox > div > div {
    background: #0f1520 !important;
    border: 1px solid #2d3748 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}
.stFileUploader > div {
    background: #0f1520 !important;
    border: 1px dashed #2d3748 !important;
    border-radius: 12px !important;
}
.stFileUploader label { color: #94a3b8 !important; }

/* ── Text area ── */
.stTextArea textarea {
    background: #090d14 !important;
    border: 1px solid #1e2535 !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e2535 20%, #1e2535 80%, transparent);
    margin: 2rem 0;
}

/* ── Tip / info boxes ── */
.tip-box {
    background: #0c1a3a;
    border-left: 3px solid #3b82f6;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.2rem;
    font-size: 0.84rem;
    color: #93c5fd;
    line-height: 1.6;
    margin-top: 0.75rem;
}
.tip-box strong { color: #bfdbfe; }

.tip-teal {
    background: #042f2e;
    border-left: 3px solid #14b8a6;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.2rem;
    font-size: 0.84rem;
    color: #5eead4;
    line-height: 1.6;
    margin-top: 0.75rem;
}
.tip-amber {
    background: #1c1200;
    border-left: 3px solid #f59e0b;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.2rem;
    font-size: 0.84rem;
    color: #fcd34d;
    line-height: 1.6;
    margin-top: 0.75rem;
}

/* ── Step badges (colored per step) ── */
.step-row { display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 1.1rem; }
.step-badge {
    width: 28px; height: 28px;
    border-radius: 50%;
    font-size: 0.7rem;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    margin-top: 2px;
}
.step-1 { background: #1e1b4b; color: #a5b4fc; border: 1px solid #3730a3; }
.step-2 { background: #042f2e; color: #5eead4; border: 1px solid #0f766e; }
.step-3 { background: #0c1a3a; color: #93c5fd; border: 1px solid #1d4ed8; }
.step-4 { background: #1c1200; color: #fcd34d; border: 1px solid #92400e; }
.step-text { font-size: 0.87rem; color: #94a3b8; line-height: 1.5; }
.step-text strong { color: #e2e8f0; display: block; margin-bottom: 0.15rem; }

/* ── Metric stat row ── */
.stat-row { display: flex; gap: 1.5rem; margin-top: 1rem; flex-wrap: wrap; }
.stat-block { text-align: center; }
.stat-num {
    font-size: 1.5rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}
.stat-lbl {
    font-size: 0.7rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

/* ── Career path cards ── */
.career-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #0f1520;
    border: 1px solid #1e2535;
    border-left: 3px solid #14b8a6;
    border-radius: 10px;
    padding: 0.75rem 1.1rem;
    margin-bottom: 0.6rem;
    font-size: 0.88rem;
    color: #e2e8f0;
}
.career-match {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #5eead4;
    background: #042f2e;
    border: 1px solid #0f766e;
    border-radius: 12px;
    padding: 0.2rem 0.65rem;
}

/* ── Before/After rewrite cards ── */
.rewrite-pair {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    margin-bottom: 1.1rem;
}
.rewrite-before {
    background: #1a0a0a;
    border: 1px solid #7f1d1d;
    border-radius: 10px;
    padding: 1rem 1.1rem;
}
.rewrite-after {
    background: #042f2e;
    border: 1px solid #0f766e;
    border-radius: 10px;
    padding: 1rem 1.1rem;
}
.rewrite-label {
    font-size: 0.67rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.rewrite-before .rewrite-label { color: #f87171; }
.rewrite-after  .rewrite-label { color: #5eead4; }
.rewrite-text { font-size: 0.84rem; color: #cbd5e1; line-height: 1.55; }

/* ── Roadmap numbered items ── */
.roadmap-item {
    display: flex;
    align-items: flex-start;
    gap: 0.9rem;
    padding: 0.85rem 1rem;
    background: #0f1520;
    border: 1px solid #1e2535;
    border-radius: 10px;
    margin-bottom: 0.55rem;
}
.roadmap-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    width: 28px; height: 28px;
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.roadmap-week {
    font-size: 0.67rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.15rem 0.55rem;
    border-radius: 10px;
    margin-bottom: 0.3rem;
    display: inline-block;
}
.week-1 { background: #1e1b4b; color: #a5b4fc; }
.week-2 { background: #042f2e; color: #5eead4; }
.week-3 { background: #0c1a3a; color: #93c5fd; }
.week-4 { background: #1c1200; color: #fcd34d; }
.roadmap-body { font-size: 0.86rem; color: #94a3b8; line-height: 1.5; }

/* ── Strength bar rows ── */
.strength-row { margin-bottom: 1rem; }
.strength-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: #94a3b8;
    margin-bottom: 0.35rem;
}
.strength-label span { color: #e2e8f0; font-weight: 600; }
.bar-track {
    height: 8px;
    background: #1e2535;
    border-radius: 4px;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.6s ease;
}
.fill-teal   { background: linear-gradient(90deg,#0d9488,#14b8a6); }
.fill-blue   { background: linear-gradient(90deg,#1d4ed8,#3b82f6); }
.fill-amber  { background: linear-gradient(90deg,#b45309,#f59e0b); }
.fill-purple { background: linear-gradient(90deg,#6366f1,#8b5cf6); }

/* ── JD match score badge ── */
.jd-score-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: #1c1200;
    border: 1px solid #92400e;
    border-radius: 10px;
    padding: 0.5rem 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: #fcd34d;
    margin-bottom: 1.25rem;
}
.jd-score-badge small {
    font-size: 0.75rem;
    color: #b45309;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #475569;
}
.empty-icon { font-size: 2.8rem; margin-bottom: 0.85rem; }
.empty-text { font-size: 0.92rem; line-height: 1.6; }

/* ── Section header with colored accent line ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.1rem;
    margin-top: 0.5rem;
}
.section-header-line {
    flex: 1;
    height: 1px;
    background: #1e2535;
}
.section-header-label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #e2e8f0;
    white-space: nowrap;
}

/* ── Interview question rows ── */
.interview-q {
    background: #0f1520;
    border: 1px solid #1e2535;
    border-left: 3px solid #6366f1;
    border-radius: 0 10px 10px 0;
    padding: 0.75rem 1.1rem;
    margin-bottom: 0.55rem;
    font-size: 0.88rem;
    color: #cbd5e1;
    line-height: 1.5;
}
.interview-q .q-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #818cf8;
    margin-bottom: 0.25rem;
}

/* ── Suggestion items ── */
.suggestion-item {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.8rem 1rem;
    background: #0f1520;
    border: 1px solid #1e2535;
    border-radius: 10px;
    margin-bottom: 0.55rem;
    font-size: 0.86rem;
    color: #94a3b8;
    line-height: 1.5;
}
.suggestion-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #5eead4;
    margin-top: 5px;
    flex-shrink: 0;
}

/* ── Rating badge ── */
.rating-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    border-radius: 12px;
    padding: 0.5rem 1.25rem;
    font-size: 0.88rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.rating-expert  { background: #042f2e; color: #5eead4; border: 1px solid #0f766e; }
.rating-strong  { background: #0c1a3a; color: #93c5fd; border: 1px solid #1d4ed8; }
.rating-good    { background: #1e1b4b; color: #a5b4fc; border: 1px solid #3730a3; }
.rating-avg     { background: #1c1200; color: #fcd34d; border: 1px solid #92400e; }
.rating-weak    { background: #2d0a0a; color: #fca5a5; border: 1px solid #7f1d1d; }
</style>
""", unsafe_allow_html=True)


# ── Load role data ─────────────────────────────────────────────────────────────
@st.cache_data
def load_roles():
    with open("datasets/roles_skills.json", "r") as f:
        return json.load(f)

roles_data = load_roles()


# ── Score styling helpers ──────────────────────────────────────────────────────
def score_color(score):
    if score >= 75:
        return "#5eead4"   # teal — success
    elif score >= 50:
        return "#fcd34d"   # amber — moderate
    else:
        return "#f87171"   # red — weak

def score_verdict(score):
    if score >= 75:
        return ("✓ Strong match", "background:#042f2e; color:#5eead4; border:1px solid #0f766e;")
    elif score >= 50:
        return ("⚡ Moderate — some gaps", "background:#1c1200; color:#fcd34d; border:1px solid #92400e;")
    else:
        return ("✗ Weak — significant gaps", "background:#2d0a0a; color:#f87171; border:1px solid #7f1d1d;")

def render_pills(items, pill_class):
    if not items:
        return "<span style='color:#475569;font-size:0.82rem;'>None detected</span>"
    pills = "".join(f'<span class="pill {pill_class}">{s}</span>' for s in sorted(items))
    return f'<div class="pill-wrap">{pills}</div>'

def strength_bar(label, value, fill_class, icon=""):
    return f"""
    <div class="strength-row">
        <div class="strength-label">{icon} {label}<span>{value}%</span></div>
        <div class="bar-track"><div class="bar-fill {fill_class}" style="width:{value}%;"></div></div>
    </div>
    """

def roadmap_num_style(i):
    styles = [
        ("background:#1e1b4b;color:#a5b4fc;", "week-1"),
        ("background:#042f2e;color:#5eead4;", "week-2"),
        ("background:#0c1a3a;color:#93c5fd;", "week-3"),
        ("background:#1c1200;color:#fcd34d;", "week-4"),
    ]
    return styles[i % len(styles)]

def rating_badge_class(rating):
    if rating >= 9: return "rating-expert",  "🏆 Expert Level Resume"
    if rating >= 8: return "rating-strong",  "💪 Strong Resume"
    if rating >= 7: return "rating-good",    "✅ Good Resume"
    if rating >= 6: return "rating-avg",     "⚠️ Average Resume"
    return "rating-weak", "🔴 Needs Major Improvement"


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ AI-Powered Resume Intelligence</div>
    <div class="hero-title">ResumeIQ — <span class="accent-purple">ATS Analyzer</span></div>
    <div class="hero-sub">
        Upload your resume and pick a target role. ResumeIQ checks your skills against
        what real ATS systems look for, tells you exactly what's missing, and shows
        you how to fix it before you apply.
    </div>
    <div class="hero-badges">
        <span class="hero-badge badge-purple">⚡ Instant ATS Score</span>
        <span class="hero-badge badge-teal">✓ Skill Gap Analysis</span>
        <span class="hero-badge badge-blue">📋 Interview Prep</span>
        <span class="hero-badge badge-amber">🧭 Learning Roadmap</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Layout ─────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 2], gap="large")


# ╔══════════════════════════════╗
# ║   LEFT — Input panel         ║
# ╚══════════════════════════════╝
with col_left:

    st.markdown('<div class="section-label">Step 1 — Target Role</div>', unsafe_allow_html=True)
    selected_role = st.selectbox(
        label="target_role",
        options=list(roles_data.keys()),
        label_visibility="collapsed",
    )

    role_skill_count = len(roles_data.get(selected_role, []))
    st.markdown(
        f'<div style="font-size:0.78rem;color:#64748b;margin-top:0.3rem;margin-bottom:1.5rem;">'
        f'This role checks for <strong style="color:#a5b4fc;">{role_skill_count} skills</strong>.</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">Step 2 — Upload Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        label="resume_upload",
        type=["pdf"],
        label_visibility="collapsed",
        help="PDF only. Max 10 MB.",
    )

    st.markdown('<div class="section-label">Step 3 — Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area("Paste Job Description Here", height=180)

    st.markdown(
        '<div style="font-size:0.75rem;color:#475569;margin-top:0.4rem;">'
        'PDF format only. Your file is processed locally and never stored.</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # How it works — colored step badges
    st.markdown('<div class="section-label">How it works</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-top:0.75rem;">
        <div class="step-row">
            <div class="step-badge step-1">1</div>
            <div class="step-text"><strong>Text extraction</strong>
            Your resume is parsed to pull out raw text, regardless of formatting.</div>
        </div>
        <div class="step-row">
            <div class="step-badge step-2">2</div>
            <div class="step-text"><strong>Skill detection</strong>
            A curated NLP model identifies technical and soft skills in your resume.</div>
        </div>
        <div class="step-row">
            <div class="step-badge step-3">3</div>
            <div class="step-text"><strong>ATS scoring</strong>
            Your skills are matched against the role's required set to calculate a fit score.</div>
        </div>
        <div class="step-row">
            <div class="step-badge step-4">4</div>
            <div class="step-text"><strong>Gap report</strong>
            Missing skills are surfaced so you know exactly what to add before applying.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ╔══════════════════════════════╗
# ║   RIGHT — Results panel      ║
# ╚══════════════════════════════╝
with col_right:

    if not uploaded_file:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📄</div>
            <div class="empty-text">
                Upload your resume on the left to see your ATS score,<br>
                matched skills, and a personalized gap report.
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # ── Processing ─────────────────────────────────────────────────────
        with st.spinner("Parsing resume…"):
            resume_text = extract_text_from_pdf(uploaded_file)

        with st.spinner("Detecting skills…"):
            detected_skills = extract_skills(resume_text)
            jd_skills = []
            jd_score = 0
            jd_matched = []
            jd_missing = []
            if job_description.strip():
                jd_skills = extract_jd_skills(
                    job_description,
                    roles_data[selected_role]
                )

        with st.spinner("Calculating ATS score…"):
            score, matched_skills, missing_skills = calculate_ats_score(
                selected_role, detected_skills
            )
            if jd_skills:
                jd_score, jd_matched, jd_missing = calculate_jd_match(
                    detected_skills,
                    jd_skills
                )

        score = int(score)
        color = score_color(score)
        verdict_text, verdict_style = score_verdict(score)

        # ── Score + breakdown ───────────────────────────────────────────────
        r1_left, r1_right = st.columns([1, 2], gap="medium")

        with r1_left:
            st.markdown(f"""
            <div class="score-wrap">
                <div class="score-number" style="color:{color};">{score}<span style="font-size:1.5rem;color:#475569;">%</span></div>
                <div class="score-label">ATS Match Score</div>
                <div class="score-verdict" style="{verdict_style}">{verdict_text}</div>
            </div>
            """, unsafe_allow_html=True)

        with r1_right:
            st.markdown('<div class="card card-purple">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Score Breakdown</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div style="font-size:0.8rem;color:#64748b;margin-bottom:0.5rem;">'
                f'Overall fit for <strong style="color:#e2e8f0;">{selected_role}</strong></div>',
                unsafe_allow_html=True,
            )
            st.progress(score / 100)

            matched_pct = len(matched_skills)
            missing_pct = len(missing_skills)

            st.markdown(f"""
            <div class="stat-row">
                <div class="stat-block">
                    <div class="stat-num" style="color:#5eead4;">{matched_pct}</div>
                    <div class="stat-lbl">Matched</div>
                </div>
                <div class="stat-block">
                    <div class="stat-num" style="color:#f87171;">{missing_pct}</div>
                    <div class="stat-lbl">Missing</div>
                </div>
                <div class="stat-block">
                    <div class="stat-num" style="color:#93c5fd;">{len(detected_skills)}</div>
                    <div class="stat-lbl">Detected</div>
                </div>
                <div class="stat-block">
                    <div class="stat-num" style="color:#a5b4fc;">{role_skill_count}</div>
                    <div class="stat-lbl">Role Requires</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── JD Match ────────────────────────────────────────────────────────
        if jd_skills:
            st.markdown("""
            <div class="section-header">
                <div class="section-header-label">🎯 Job Description Match</div>
                <div class="section-header-line"></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f'<div class="jd-score-badge">{jd_score}% <small>JD Match Score</small></div>',
                unsafe_allow_html=True
            )

            jd_col1, jd_col2 = st.columns(2)
            with jd_col1:
                st.markdown('<div class="card card-teal">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">✓ Matched JD Skills</div>', unsafe_allow_html=True)
                st.markdown(render_pills(jd_matched, "pill-teal"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with jd_col2:
                st.markdown('<div class="card card-red">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">✗ Missing JD Skills</div>', unsafe_allow_html=True)
                st.markdown(render_pills(jd_missing, "pill-red"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── Skills ──────────────────────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
            <div class="section-header-label">🔍 Role Skill Match</div>
            <div class="section-header-line"></div>
        </div>
        """, unsafe_allow_html=True)

        s1, s2 = st.columns(2, gap="medium")

        with s1:
            st.markdown('<div class="card card-teal">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">✓ Matched Skills</div>', unsafe_allow_html=True)
            st.markdown(render_pills(matched_skills, "pill-teal"), unsafe_allow_html=True)
            if matched_skills:
                st.markdown(
                    f'<div style="font-size:0.75rem;color:#475569;margin-top:0.9rem;">'
                    f'{len(matched_skills)} of {role_skill_count} required skills found.</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

        with s2:
            st.markdown('<div class="card card-red">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">✗ Missing Skills</div>', unsafe_allow_html=True)
            st.markdown(render_pills(missing_skills, "pill-red"), unsafe_allow_html=True)
            if missing_skills:
                st.markdown(
                    '<div class="tip-box">'
                    '<strong>Quick win:</strong> Add these skills to your resume summary '
                    'or a dedicated Skills section — even listing them improves ATS ranking '
                    'significantly before a recruiter sees your file.'
                    '</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── Strengths / Weaknesses ───────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
            <div class="section-header-label">💪 Strengths &amp; Weaknesses</div>
            <div class="section-header-line"></div>
        </div>
        """, unsafe_allow_html=True)

        strengths, weaknesses = get_strengths_weaknesses(matched_skills, missing_skills)

        sw1, sw2 = st.columns(2, gap="medium")
        with sw1:
            st.markdown('<div class="card card-teal"><div class="card-title">✓ Strengths</div>', unsafe_allow_html=True)
            for skill in strengths:
                st.markdown(
                    f'<div class="suggestion-item"><div class="suggestion-dot" style="background:#5eead4;"></div>{skill}</div>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)

        with sw2:
            st.markdown('<div class="card card-amber"><div class="card-title">⚠ Weaknesses</div>', unsafe_allow_html=True)
            for skill in weaknesses:
                st.markdown(
                    f'<div class="suggestion-item"><div class="suggestion-dot" style="background:#fcd34d;"></div>{skill}</div>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── Resume Strength Meter ────────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
            <div class="section-header-label">📊 Resume Strength Meter</div>
            <div class="section-header-line"></div>
        </div>
        """, unsafe_allow_html=True)

        skills_strength     = min(score, 100)
        project_strength    = 80 if len(matched_skills) >= 5 else 50
        keyword_strength    = min(len(matched_skills) * 10, 100)
        improvement_strength= max(100 - len(missing_skills) * 10, 0)

        breakdown = calculate_breakdown(matched_skills, missing_skills, detected_skills, jd_score)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            strength_bar("Technical Skills",    skills_strength,      "fill-teal",   "🛠"),
            unsafe_allow_html=True
        )
        st.markdown(
            strength_bar("Projects",            project_strength,     "fill-blue",   "📁"),
            unsafe_allow_html=True
        )
        st.markdown(
            strength_bar("ATS Keywords",        keyword_strength,     "fill-amber",  "🔑"),
            unsafe_allow_html=True
        )
        st.markdown(
            strength_bar("Improvement Potential", improvement_strength, "fill-purple","📈"),
            unsafe_allow_html=True
        )

        for section, value in breakdown.items():
            st.markdown(
                strength_bar(section, value, "fill-teal"),
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Resume Rating ────────────────────────────────────────────────────
        resume_rating, rating_verdict = calculate_resume_rating(
            score, jd_score, matched_skills, missing_skills
        )
        badge_cls, badge_text = rating_badge_class(resume_rating)

        st.markdown(f"""
        <div class="card card-purple" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
            <div>
                <div class="card-title">⭐ Resume Rating</div>
                <div style="font-size:2.5rem;font-weight:700;font-family:'JetBrains Mono',monospace;color:#a5b4fc;line-height:1;">{resume_rating}<span style="font-size:1rem;color:#475569;">/10</span></div>
                <div style="font-size:0.84rem;color:#94a3b8;margin-top:0.35rem;">{rating_verdict}</div>
            </div>
            <div class="rating-badge {badge_cls}">{badge_text}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Improvement Potential ────────────────────────────────────────────
        possible_gain, improved_score = calculate_improvement_potential(score, missing_skills)
        st.markdown(f"""
        <div class="card card-amber">
            <div class="card-title">📈 Improvement Potential</div>
            <div class="stat-row">
                <div class="stat-block">
                    <div class="stat-num" style="color:#fcd34d;">{score}%</div>
                    <div class="stat-lbl">Current Score</div>
                </div>
                <div class="stat-block">
                    <div class="stat-num" style="color:#5eead4;">+{possible_gain}%</div>
                    <div class="stat-lbl">Possible Gain</div>
                </div>
                <div class="stat-block">
                    <div class="stat-num" style="color:#a5b4fc;">{improved_score}%</div>
                    <div class="stat-lbl">Projected Score</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Career Paths ─────────────────────────────────────────────────────
        st.markdown("""
        <div class="section-header" style="margin-top:1.5rem;">
            <div class="section-header-label">🚀 Recommended Career Paths</div>
            <div class="section-header-line"></div>
        </div>
        """, unsafe_allow_html=True)

        recommended = recommend_roles(detected_skills)
        for i, role in enumerate(recommended):
            match_pct = max(90 - i * 8, 55)
            st.markdown(f"""
            <div class="career-card">
                <span>🎯 {role}</span>
                <span class="career-match">{match_pct}% match</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── Tabs ─────────────────────────────────────────────────────────────
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Interview Questions",
            "💡 Suggestions",
            "✍️ Resume Rewrite",
            "🧭 Learning Roadmap",
            "🎤 Mock Interview"
        ])

        # — Tab 1: Interview Questions —
        with tab1:
            questions = get_questions(selected_role)
            if questions:
                for i, question in enumerate(questions[:15], start=1):
                    st.markdown(f"""
                    <div class="interview-q">
                        <div class="q-num">Q{i:02d}</div>
                        {question}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No interview questions found.")

        # — Tab 2: Suggestions —
        with tab2:
            suggestions = generate_suggestions(missing_skills, score)
            for suggestion in suggestions:
                st.markdown(f"""
                <div class="suggestion-item">
                    <div class="suggestion-dot"></div>
                    {suggestion}
                </div>
                """, unsafe_allow_html=True)

        # — Tab 3: Resume Rewrite (Before/After cards) —
        with tab3:
            rewrite_suggestions = generate_rewrite_suggestions(
                resume_text, missing_skills, selected_role
            )
            st.markdown("""
            <div style="font-size:0.8rem;color:#64748b;margin-bottom:1rem;">
                Each suggestion shows how to rephrase your existing content to pass ATS filters.
            </div>
            """, unsafe_allow_html=True)

            for i, suggestion in enumerate(rewrite_suggestions):
                # If suggestion is a string, show as simple styled card
                if isinstance(suggestion, str):
                    # Attempt to split on "→" or "->" for before/after display
                    if "→" in suggestion or "->" in suggestion:
                        sep = "→" if "→" in suggestion else "->"
                        parts = suggestion.split(sep, 1)
                        before = parts[0].strip()
                        after = parts[1].strip() if len(parts) > 1 else ""
                        st.markdown(f"""
                        <div class="rewrite-pair">
                            <div class="rewrite-before">
                                <div class="rewrite-label">Before</div>
                                <div class="rewrite-text">{before}</div>
                            </div>
                            <div class="rewrite-after">
                                <div class="rewrite-label">After</div>
                                <div class="rewrite-text">{after}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="suggestion-item">
                            <div class="suggestion-dot" style="background:#a5b4fc;"></div>
                            {suggestion}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("📝", suggestion)

        # — Tab 4: Learning Roadmap —
        with tab4:
            roadmap = generate_learning_roadmap(missing_skills, selected_role)
            week_labels = ["Week 1–2", "Week 3–4", "Week 5–6", "Week 7–8"]
            week_classes = ["week-1", "week-2", "week-3", "week-4"]
            num_styles   = [
                "background:#1e1b4b;color:#a5b4fc;",
                "background:#042f2e;color:#5eead4;",
                "background:#0c1a3a;color:#93c5fd;",
                "background:#1c1200;color:#fcd34d;",
            ]
            for i, item in enumerate(roadmap):
                n = i % 4
                st.markdown(f"""
                <div class="roadmap-item">
                    <div class="roadmap-num" style="{num_styles[n]}">{i+1:02d}</div>
                    <div>
                        <div class="roadmap-week {week_classes[n]}">{week_labels[n]}</div>
                        <div class="roadmap-body">{item}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # — Tab 5: Mock Interview —
        with tab5:
            answers = get_answers(selected_role)
            answer_items = answers.get("questions", [])

            if answer_items:
                question_options = [item.get("question", "") for item in answer_items]
                selected_question = st.selectbox("Choose a Question", question_options)
                user_answer = st.text_area("Your Answer")

                ideal_answer = ""
                for item in answer_items:
                    if item.get("question", "").strip().lower() == selected_question.strip().lower():
                        ideal_answer = item.get("ideal_answer", "")
                        break

                col_eval, col_ideal = st.columns(2)
                with col_eval:
                    if st.button("Evaluate Answer"):
                        eval_score, feedback = evaluate_answer(user_answer, ideal_answer)
                        st.markdown(f"""
                        <div class="card card-{'teal' if eval_score >= 8 else 'amber' if eval_score >= 5 else 'red'}">
                            <div class="card-title">Interview Performance</div>
                            <div style="font-size:2rem;font-weight:700;font-family:'JetBrains Mono',monospace;color:{'#5eead4' if eval_score >= 8 else '#fcd34d' if eval_score >= 5 else '#f87171'};">{eval_score}/10</div>
                            <div style="font-size:0.86rem;color:#94a3b8;margin-top:0.5rem;">{feedback}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        if eval_score >= 8:
                            st.markdown('<div class="tip-teal">✅ <strong>Strong answer.</strong> You explained the concept very well.</div>', unsafe_allow_html=True)
                        elif eval_score >= 5:
                            st.markdown('<div class="tip-amber">⚠️ <strong>Average answer.</strong> Add more technical details and examples.</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="tip-box" style="border-color:#b91c1c;background:#2d0a0a;color:#fca5a5;">❌ <strong>Needs work.</strong> Explain the concept clearly and include key terms.</div>', unsafe_allow_html=True)

                with col_ideal:
                    if st.button("Show Ideal Answer"):
                        if ideal_answer:
                            st.markdown(f"""
                            <div class="card card-blue">
                                <div class="card-title">💡 Ideal Answer</div>
                                <div style="font-size:0.86rem;color:#93c5fd;line-height:1.6;">{ideal_answer}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.warning("No ideal answer available.")
            else:
                st.warning("No interview questions found for this role.")


# ── Download Report ────────────────────────────────────────────────────────────
if "score"          not in locals(): score = 0
if "matched_skills" not in locals(): matched_skills = []
if "missing_skills" not in locals(): missing_skills = []
if "detected_skills"not in locals(): detected_skills = []
if "resume_text"    not in locals(): resume_text = ""

report_file = generate_report(selected_role, score, matched_skills, missing_skills)

with open(report_file, "rb") as file:
    st.download_button(
        "📥 Download ATS Report",
        file,
        file_name="ResumeIQ_Report.pdf",
        mime="application/pdf"
    )

# ── All detected skills ────────────────────────────────────────────────────────
with st.expander("All detected skills from your resume", expanded=False):
    if detected_skills:
        st.markdown(render_pills(detected_skills, "pill-blue"), unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-size:0.75rem;color:#475569;margin-top:0.9rem;">'
            f'{len(detected_skills)} skills identified across all sections of your resume.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("No skills detected.")

# ── Raw resume text ────────────────────────────────────────────────────────────
with st.expander("View extracted resume text", expanded=False):
    st.markdown(
        '<div style="font-size:0.78rem;color:#64748b;margin-bottom:0.6rem;">'
        'Raw text extracted from your resume. If something looks wrong, '
        'the PDF may use non-standard fonts or image-based text.</div>',
        unsafe_allow_html=True,
    )
    st.text_area(
        label="extracted_text",
        value=resume_text,
        height=300,
        label_visibility="collapsed",
    )