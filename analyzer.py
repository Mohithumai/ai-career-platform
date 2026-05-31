import streamlit as st
import pdfplumber
import math
import time
import json
import io
import streamlit.components.v1 as components
from groq import Groq
from streamlit_mic_recorder import mic_recorder
import plotly.graph_objects as go

def show_analyzer(switch_page_callback):
    # --- Put a 'Back to Home' button at the top ---
    if st.button("← Back to Dashboard"):
        switch_page_callback("home")
    st.markdown("---")

    # -----------------------------------
    # SESSION STATE
    # -----------------------------------
    for _key in ["voice_q", "voice_transcript", "voice_eval", "full_rewrite"]:
        if _key not in st.session_state:
            st.session_state[_key] = None

    # -----------------------------------
    # LIVE PARTICLE BACKGROUND
    # -----------------------------------
    def render_particle_background():
        st.html("""
        <style>
            iframe {
                position: fixed !important;
                top: 0 !important; left: 0 !important;
                width: 100vw !important; height: 100vh !important;
                z-index: -1 !important;
                pointer-events: none !important;
            }
            .stApp, [data-testid="stApp"], [data-testid="stAppViewContainer"], .main, .block-container, header {
                background: transparent !important;
            }
        </style>
        """)
        components.html("""
        <!DOCTYPE html>
        <html><head><meta charset="UTF-8">
        <style>body{margin:0;padding:0;background:#08090C;overflow:hidden;}#p{position:absolute;width:100%;height:100%;}</style>
        <script src="https://cdn.jsdelivr.net/npm/tsparticles@2/tsparticles.bundle.min.js"></script>
        </head><body><div id="p"></div>
        <script>
        tsParticles.load("p",{fpsLimit:60,particles:{color:{value:"#4DFFC3"},links:{color:"#4DFFC3",distance:150,enable:true,opacity:0.15,width:1},move:{enable:true,speed:0.8,outModes:{default:"bounce"}},number:{density:{enable:true,area:800},value:50},opacity:{value:0.4,animation:{enable:true,speed:1,minimumValue:0.1}},shape:{type:"circle"},size:{value:{min:1.5,max:3.5}}},interactivity:{events:{onHover:{enable:true,mode:"repulse"},resize:true},modes:{repulse:{distance:100,duration:0.4}}},detectRetina:true});
        </script></body></html>
        """, height=0)

    render_particle_background()

    # -----------------------------------
    # GLOBAL CSS & TAB STYLING
    # -----------------------------------
    st.html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Manrope:wght@300;400;500;600;700&display=swap');

    :root {
        --bg: #08090C; --surface: #0D1018; --card: #12151E;
        --border: rgba(255,255,255,0.07); --border-hi: rgba(255,255,255,0.12);
        --accent: #4DFFC3; --warn: #FFBE57; --err: #FF6B6B;
        --text: #ECE9E2; --sub: #818DA0; --muted: #3A3F4E;
    }

    #MainMenu, footer, .stDeployButton { display: none !important; }
    [data-testid="stToolbar"] { visibility: hidden !important; }

    .block-container { padding-top: 2rem !important; max-width: 1040px !important; font-family: 'Manrope', sans-serif !important; }

    p, div, li, label { font-family: 'Manrope', sans-serif !important; color: var(--text) !important; }
    h1, h2, h3 { font-family: 'Syne', sans-serif !important; letter-spacing: -0.025em !important; color: var(--text) !important; }

    /* Custom Streamlit Tabs Styling */
    [data-baseweb="tab-list"] { gap: 12px; margin-bottom: 24px; background: rgba(18,21,30,0.5); padding: 8px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); }
    [data-baseweb="tab"] { font-family: 'Syne', sans-serif !important; font-weight: 700 !important; color: #818DA0 !important; background: transparent !important; border-radius: 8px !important; padding: 10px 20px !important; border: 1px solid transparent !important; }
    [aria-selected="true"] { color: #08090C !important; background: #4DFFC3 !important; border: 1px solid rgba(77,255,195,0.4) !important; box-shadow: 0 4px 15px rgba(77,255,195,0.2) !important; }

    .stButton > button { background: #1C2030 !important; color: #C8C4BC !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 8px !important; font-family: 'Syne', sans-serif !important; font-weight: 600 !important; font-size: 13px !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; height: 44px !important; transition: all 0.2s ease !important; }
    .stButton > button:hover { background: #252B3D !important; color: #ECE9E2 !important; border-color: rgba(255,255,255,0.22) !important; transform: translateY(-1px) !important; box-shadow: 0 6px 20px rgba(0,0,0,0.35) !important; }
    .stButton > button:active { transform: translateY(1px) scale(0.98) !important; }

    [data-testid="stFileUploader"] > div:first-child { background: rgba(18,21,30,0.85) !important; backdrop-filter: blur(8px) !important; border: 1px dashed var(--border-hi) !important; border-radius: 14px !important; padding: 2rem !important; transition: all 0.3s ease !important; }
    [data-testid="stFileUploader"] > div:first-child:hover { border-color: var(--accent) !important; }
    [data-testid="stFileUploader"] label, [data-testid="stFileUploader"] [data-testid="stWidgetLabel"], [data-testid="stFileUploaderDropzoneInstructions"] { display: none !important; }
    [data-testid="stFileUploaderDropzone"] * { font-size: 0 !important; color: transparent !important; }
    [data-testid="stFileUploaderDropzone"] button { display: inline-flex !important; align-items: center !important; justify-content: center !important; min-width: 120px !important; min-height: 38px !important; font-size: 0 !important; color: transparent !important; background: rgba(77,255,195,0.1) !important; border: 1px solid rgba(77,255,195,0.3) !important; border-radius: 8px !important; padding: 8px 22px !important; cursor: pointer !important; transition: all 0.2s ease !important; }
    [data-testid="stFileUploaderDropzone"] button:hover { background: rgba(77,255,195,0.18) !important; transform: translateY(-2px) !important; }
    [data-testid="stFileUploaderDropzone"] button::after { content: "Browse Files"; font-size: 13px !important; font-family: 'Syne', sans-serif !important; font-weight: 700 !important; letter-spacing: 0.06em !important; color: #4DFFC3 !important; text-transform: uppercase !important; }
    [data-testid="stFileUploader"] small { color: var(--sub) !important; }

    .stSpinner > div > div { border-top-color: var(--accent) !important; }

    textarea, [data-testid="stTextInput"] input { background: rgba(13,16,24,0.85) !important; backdrop-filter: blur(8px) !important; color: var(--sub) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; font-size: 12px !important; transition: all 0.2s ease !important; }
    textarea:focus, [data-testid="stTextInput"] input:focus { border-color: var(--accent) !important; box-shadow: 0 0 8px rgba(77,255,195,0.2) !important; color: var(--text) !important; }

    details { background: rgba(18,21,30,0.85) !important; backdrop-filter: blur(8px) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; padding: 4px 16px !important; transition: all 0.2s ease !important; }
    details:hover { border-color: var(--accent) !important; }
    details summary { color: var(--sub) !important; font-size: 13px !important; cursor: pointer !important; }
    details summary:hover { color: var(--accent) !important; }

    hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1.5rem 0 !important; }
    ::-webkit-scrollbar { width: 3px; height: 3px; }
    ::-webkit-scrollbar-thumb { background: var(--muted); border-radius: 2px; }

    @keyframes fadeUp { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:translateY(0); } }
    @keyframes spin { 100% { transform:rotate(360deg); } }
    .fade-in   { animation: fadeUp 0.4s ease 0.0s both; }
    .fade-in-2 { animation: fadeUp 0.4s ease 0.1s both; }
    .fade-in-3 { animation: fadeUp 0.4s ease 0.2s both; }

    .metric-card { transition: all 0.3s cubic-bezier(0.2,0.95,0.4,1.1) !important; cursor: pointer !important; }
    .metric-card:hover { transform: scale(1.04) translateY(-4px) !important; border-color: #4DFFC3 !important; box-shadow: 0 18px 32px -12px rgba(77,255,195,0.25) !important; }

    .ats-card { transition: all 0.3s ease !important; cursor: pointer !important; }
    .ats-card:hover { transform: scale(1.01) translateY(-2px) !important; border-color: #4DFFC3 !important; box-shadow: 0 18px 28px -12px rgba(0,0,0,0.6), 0 0 0 1px rgba(77,255,195,0.3) !important; }

    .skill-chip { display:inline-block; padding:7px 16px; background:rgba(77,255,195,0.08); border:1px solid rgba(77,255,195,0.2); border-radius:100px; font-family:'Manrope',sans-serif; font-size:12px; font-weight:500; color:#4DFFC3; margin:3px 4px 3px 0; transition:all 0.2s ease !important; cursor:pointer; }
    .skill-chip:hover { transform:translateY(-2px) scale(1.05) !important; background:rgba(77,255,195,0.2) !important; box-shadow:0 4px 12px rgba(77,255,195,0.15) !important; border-color:#4DFFC3 !important; }

    .job-card { display:flex; align-items:center; justify-content:space-between; padding:15px 18px; background:rgba(13,16,24,0.85); border:1px solid rgba(255,255,255,0.07); border-radius:10px; margin-bottom:8px; transition:all 0.25s ease !important; cursor:pointer; }
    .job-card:hover { transform:translateX(8px) scale(1.01) !important; border-left:3px solid #4DFFC3 !important; background:rgba(17,22,31,0.95) !important; box-shadow:0 5px 14px rgba(0,0,0,0.4) !important; }
    
    [data-testid="stDataFrame"] { background: rgba(18,21,30,0.85) !important; border-radius: 12px; }
    </style>
    """)

    # -----------------------------------
    # DATABASES & FUNCTIONS
    # -----------------------------------
    skill_categories = {
        "Frontend": ["html", "css", "javascript", "react"],
        "Backend": ["python", "java", "c++", "node", "django", "rest apis"],
        "Database": ["sql", "mysql", "mongodb"],
        "Data & ML": ["machine learning", "tensorflow"],
        "DevOps & Tools": ["git", "github", "aws", "docker", "ci/cd"],
        "Mobile": ["flutter", "dart"]
    }
    skills_db = [skill for category in skill_categories.values() for skill in category]
    job_roles = {
        "Python Developer":           ["python", "sql", "git"],
        "Frontend Developer":         ["html", "css", "javascript", "react"],
        "Backend Developer":          ["python", "mongodb", "sql", "rest apis"],
        "Machine Learning Engineer":  ["python", "machine learning", "tensorflow"],
        "DevOps Engineer":            ["aws", "docker", "ci/cd", "git", "linux"],
        "Flutter Developer":          ["flutter", "dart"]
    }

    def extract_text_from_pdf(file):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted: text += extracted.lower() + "\n"
        return text

    def extract_skills(text): return [s for s in skills_db if s.lower() in text]
    def calculate_ats_score(skills): return round((len(skills) / len(skills_db)) * 100)
    def calculate_match_percentage(skills):
        t = ["python","sql","git","machine learning","react"]
        return round((sum(1 for s in t if s in skills) / len(t)) * 100)
    def give_suggestions(skills):
        out = []
        if "react" not in skills:           out.append("Learn React — essential for frontend roles.")
        if "mongodb" not in skills:         out.append("Add MongoDB to strengthen backend profiles.")
        if "machine learning" not in skills: out.append("ML projects dramatically increase tech profile relevance.")
        return out
    def recommend_jobs(skills): return [r for r, req in job_roles.items() if sum(1 for s in req if s in skills) >= 2]
    def calculate_power_score(text, skills):
        score = min(len(skills) / len(skills_db) * 45, 45)
        if any(w in text for w in ["project", "built", "developed", "created", "designed"]): score += 20
        if any(w in text for w in ["internship", "intern", "experience", "worked", "employed"]): score += 20
        if any(w in text for w in ["certified", "certification", "certificate", "award"]): score += 8
        if any(w in text for w in ["bachelor", "master", "degree", "university", "btech", "b.tech"]): score += 7
        return min(round(score), 100)
    def calculate_interview_ready(text, skills):
        score = min(len(skills) * 4, 35)
        if any(w in text for w in ["project", "github", "portfolio", "demo"]): score += 20
        if any(w in text for w in ["internship", "experience", "worked", "led", "managed"]): score += 25
        if any(c.isdigit() for c in text): score += 12
        if any(w in text for w in ["team", "collaborated", "communication"]): score += 8
        return min(round(score), 100)

    # -----------------------------------
    # HEADER + PROMINENT API KEY SETUP
    # -----------------------------------
    st.html("""
    <div class="fade-in" style="margin-bottom:1.5rem;">
        <span style="font-family:'Manrope',sans-serif;font-size:11px;letter-spacing:0.16em;text-transform:uppercase;color:#4DFFC3;font-weight:600;">◈ Career Intelligence</span>
        <h1 style="font-family:'Syne',sans-serif;font-size:2.9rem;font-weight:800;letter-spacing:-0.04em;line-height:1.05;margin:10px 0 14px;color:#ECE9E2;">Resume <span style="color:#4DFFC3;">Analyzer</span></h1>
        <p style="font-family:'Manrope',sans-serif;font-size:14px;color:#818DA0;margin:0;max-width:500px;line-height:1.8;">Upload your PDF for instant ATS scoring, skill detection, job role matching, and improvement suggestions.</p>
    </div>
    """)

    # The API Key is now directly on the main page, impossible to miss!
    st.markdown("""
    <div class="fade-in" style="background:rgba(18,21,30,0.85);backdrop-filter:blur(8px);border:1px solid rgba(77,255,195,0.3);border-radius:14px;padding:20px 24px;margin-bottom:1rem;">
        <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:700;color:#4DFFC3;margin-bottom:8px;">🔑 Groq API Key Required</div>
        <div style="font-family:'Manrope',sans-serif;font-size:13px;color:#818DA0;margin-bottom:16px;">This key powers the AI Resume Rewrite and the Voice Interviewer. It is never stored. Get a free key at console.groq.com.</div>
    """, unsafe_allow_html=True)
    
    api_key = st.text_input("API Key", type="password", placeholder="gsk_...", label_visibility="collapsed")
    st.markdown("</div><br>", unsafe_allow_html=True)

    # -----------------------------------
    # FILE UPLOAD
    # -----------------------------------
    uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

    # -----------------------------------
    # MAIN LOGIC (TABBED INTERFACE)
    # -----------------------------------
    if uploaded_file:

        loader_placeholder = st.empty()
        for stage in ["Initializing ATS parsing engine...", "Extracting document structure...", "Identifying technical skills...", "Calculating alignment scores..."]:
            loader_placeholder.html(f"""
            <div class="fade-in" style="background:rgba(18,21,30,0.85);backdrop-filter:blur(8px);border:1px solid rgba(77,255,195,0.3);border-radius:12px;padding:20px 24px;margin-bottom:20px;display:flex;align-items:center;gap:16px;">
                <div style="width:20px;height:20px;border:2px solid rgba(77,255,195,0.15);border-top-color:#4DFFC3;border-radius:50%;animation:spin 0.7s linear infinite;flex-shrink:0;"></div>
                <div style="font-family:'Syne',sans-serif;font-size:14px;font-weight:600;color:#ECE9E2;">{stage}</div>
            </div>""")
            time.sleep(0.4)
        loader_placeholder.empty()

        resume_text      = extract_text_from_pdf(uploaded_file)
        skills           = extract_skills(resume_text)
        ats_score        = calculate_ats_score(skills)
        match_percentage = calculate_match_percentage(skills)
        suggestions      = give_suggestions(skills)
        recommended_jobs = recommend_jobs(skills)
        power_score      = calculate_power_score(resume_text, skills)
        interview_score  = calculate_interview_ready(resume_text, skills)

        if ats_score >= 80: st.balloons()

        tab_dashboard, tab_matcher, tab_ai, tab_voice = st.tabs([
            "📊 Executive Dashboard", 
            "🎯 JD Alignment", 
            "✨ AI Enhancer", 
            "🎙️ Voice Interview"
        ])

        # ==========================================
        # TAB 1: EXECUTIVE DASHBOARD
        # ==========================================
        with tab_dashboard:
            st.html(f"""
            <div class="fade-in-2" style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:10px 0 22px;">
                <div class="metric-card" style="background:rgba(18,21,30,0.85);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:22px 24px;">
                    <div style="font-family:'Manrope',sans-serif;font-size:10px;letter-spacing:0.13em;text-transform:uppercase;color:#818DA0;margin-bottom:8px;">ATS Score</div>
                    <div style="font-family:'Syne',sans-serif;font-size:2.5rem;font-weight:800;color:#ECE9E2;line-height:1;">{ats_score}</div>
                    <div style="font-family:'Manrope',sans-serif;font-size:11px;color:#3A3F4E;margin-top:5px;">/100 points</div>
                </div>
                <div class="metric-card" style="background:rgba(18,21,30,0.85);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:22px 24px;">
                    <div style="font-family:'Manrope',sans-serif;font-size:10px;letter-spacing:0.13em;text-transform:uppercase;color:#818DA0;margin-bottom:8px;">Skills Found</div>
                    <div style="font-family:'Syne',sans-serif;font-size:2.5rem;font-weight:800;color:#ECE9E2;line-height:1;">{len(skills)}</div>
                    <div style="font-family:'Manrope',sans-serif;font-size:11px;color:#3A3F4E;margin-top:5px;">of {len(skills_db)} tracked</div>
                </div>
                <div class="metric-card" style="background:rgba(18,21,30,0.85);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:22px 24px;">
                    <div style="font-family:'Manrope',sans-serif;font-size:10px;letter-spacing:0.13em;text-transform:uppercase;color:#818DA0;margin-bottom:8px;">Job Matches</div>
                    <div style="font-family:'Syne',sans-serif;font-size:2.5rem;font-weight:800;color:#ECE9E2;line-height:1;">{len(recommended_jobs)}</div>
                    <div style="font-family:'Manrope',sans-serif;font-size:11px;color:#3A3F4E;margin-top:5px;">roles matched</div>
                </div>
                <div class="metric-card" style="background:rgba(18,21,30,0.85);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:22px 24px;">
                    <div style="font-family:'Manrope',sans-serif;font-size:10px;letter-spacing:0.13em;text-transform:uppercase;color:#818DA0;margin-bottom:8px;">Resume Match</div>
                    <div style="font-family:'Syne',sans-serif;font-size:2.5rem;font-weight:800;color:#ECE9E2;line-height:1;">{match_percentage}%</div>
                    <div style="font-family:'Manrope',sans-serif;font-size:11px;color:#3A3F4E;margin-top:5px;">Industry alignment</div>
                </div>
            </div>""")

            r = 58; circ = 2 * math.pi * r; dash = (ats_score / 100) * circ; gap  = circ - dash
            if ats_score >= 70:   arc_color, rating, tip = "#4DFFC3", "Excellent", "Strong profile. Tailor per role for best results."
            elif ats_score >= 40: arc_color, rating, tip = "#FFBE57", "Good",      "Solid base. A few more skills will push you to Excellent."
            else:                 arc_color, rating, tip = "#FF6B6B", "Needs Work","Expand skill set and use more job-specific keywords."

            st.html(f"""
            <div class="ats-card fade-in-3" style="background:rgba(18,21,30,0.85);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:28px 32px;margin-bottom:20px;display:flex;align-items:center;gap:36px;flex-wrap:wrap;">
                <div style="position:relative;width:148px;height:148px;flex-shrink:0;">
                    <svg width="148" height="148" viewBox="0 0 148 148" style="transform:rotate(-90deg);display:block;">
                        <circle cx="74" cy="74" r="{r}" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="10"/>
                        <circle cx="74" cy="74" r="{r}" fill="none" stroke="{arc_color}" stroke-width="10" stroke-dasharray="{dash:.2f} {gap:.2f}" stroke-linecap="round"/>
                    </svg>
                    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;">
                        <div style="font-family:'Syne',sans-serif;font-size:2.1rem;font-weight:800;color:#ECE9E2;line-height:1;">{ats_score}</div>
                        <div style="font-family:'Manrope',sans-serif;font-size:10px;color:#3A3F4E;">/100</div>
                    </div>
                </div>
                <div>
                    <div style="font-family:'Manrope',sans-serif;font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:#818DA0;margin-bottom:7px;">ATS Score Rating</div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.7rem;font-weight:700;color:{arc_color};margin-bottom:10px;">{rating}</div>
                    <div style="font-family:'Manrope',sans-serif;font-size:13px;color:#818DA0;line-height:1.75;max-width:380px;">{tip}</div>
                </div>
            </div>""")

            col_radar, col_power = st.columns([1, 1])
            with col_radar:
                cat_scores = {cat: min(5, sum(1 for s in cat_skills if s in skills) * 2) for cat, cat_skills in skill_categories.items()}
                categories, values = list(cat_scores.keys()), list(cat_scores.values())
                categories.append(categories[0]); values.append(values[0])
                fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself', fillcolor='rgba(77, 255, 195, 0.2)', line=dict(color='#4DFFC3', width=2), marker=dict(color='#4DFFC3', size=8)))
                fig.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 5]), angularaxis=dict(tickfont=dict(color="#818DA0", size=12, family="Manrope"), linecolor="rgba(255,255,255,0.1)"), bgcolor="rgba(0,0,0,0)"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False, margin=dict(l=40, r=40, t=20, b=20), height=320)
                st.html("""<div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;color:#ECE9E2;margin-bottom:10px;">Technical Footprint</div>""")
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            with col_power:
                def _bar(label, val, color): return f"""<div style="margin-bottom:18px;"><div style="display:flex;justify-content:space-between;margin-bottom:6px;"><span style="font-family:'Manrope',sans-serif;font-size:12px;color:#818DA0;">{label}</span><span style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:{color};">{val}</span></div><div style="background:rgba(255,255,255,0.05);border-radius:100px;height:6px;"><div style="width:{val}%;background:{color};height:6px;border-radius:100px;transition:width 1s ease;"></div></div></div>"""
                bars = _bar("ATS Score", ats_score, arc_color) + _bar("Resume Power", power_score, "#818DA0") + _bar("Industry Match", match_percentage,"#818DA0") + _bar("Interview Ready", interview_score, "#818DA0")
                st.html(f"""<div style="background:rgba(18,21,30,0.85);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:24px 28px;height:100%;"><div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:#ECE9E2;margin-bottom:20px;">Resume Power Score</div>{bars}</div>""")

            # Health Audit
            st.html("""<div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:700;color:#ECE9E2;margin:2.5rem 0 1rem;">Document <span style="color:#FFBE57;">Health Audit</span></div>""")
            words = resume_text.split(); word_count = len(words); metrics_count = sum(1 for w in words if any(c.isdigit() for c in w))
            strong_verbs = ["led", "developed", "optimized", "managed", "created", "spearheaded", "designed", "architected", "implemented", "built", "engineered"]
            weak_verbs = ["helped", "worked", "assisted", "responsible", "did", "handled", "participated"]
            found_strong = list(set([v for v in strong_verbs if v in resume_text]))
            found_weak = list(set([v for v in weak_verbs if v in resume_text]))

            len_status = "Good" if 300 <= word_count <= 800 else "Too Short" if word_count < 300 else "Too Long"
            len_color = "#4DFFC3" if len_status == "Good" else "#FF6B6B"
            met_status = "Excellent" if metrics_count > 8 else ("Needs More" if metrics_count > 3 else "Critical Gap")
            met_color = "#4DFFC3" if metrics_count > 8 else ("#FFBE57" if metrics_count > 3 else "#FF6B6B")
            verb_status = "Strong" if len(found_strong) >= len(found_weak) and len(found_strong) > 0 else "Weak"
            verb_color = "#4DFFC3" if verb_status == "Strong" else "#FFBE57"

            h1, h2, h3 = st.columns(3)
            def health_card(col, title, value, status, color, desc): col.html(f"""<div class="feature-card fade-in-3" style="background:rgba(18,21,30,0.85);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.07);border-top:3px solid {color};border-radius:12px;padding:20px;height:100%;"><div style="font-family:'Manrope',sans-serif;font-size:11px;letter-spacing:0.1em;text-transform:uppercase;color:#818DA0;margin-bottom:12px;font-weight:700;">{title}</div><div style="display:flex;align-items:baseline;gap:10px;margin-bottom:12px;"><div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;color:#ECE9E2;line-height:1;">{value}</div><div style="font-family:'Manrope',sans-serif;font-size:11px;font-weight:800;color:{color};background:{color}15;padding:4px 10px;border-radius:100px;text-transform:uppercase;letter-spacing:0.05em;border:1px solid {color}40;">{status}</div></div><div style="font-family:'Manrope',sans-serif;font-size:13px;color:#818DA0;line-height:1.6;">{desc}</div></div>""")
            health_card(h1, "Brevity & Length", f"{word_count}", len_status, len_color, "Ideal resumes are 400-800 words.")
            health_card(h2, "Impact & Metrics", f"{metrics_count}", met_status, met_color, "Quantify achievements using numbers and percentages.")
            health_card(h3, "Action Verbs", f"{len(found_strong)}", verb_status, verb_color, f"Avoid passive terms. Strong verbs found: {', '.join(found_strong[:3]) if found_strong else 'None'}.")

            # Action Plan Module
            st.html("""<div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:700;color:#ECE9E2;margin:3rem 0 1rem;">✅ Your Instant <span style="color:#4DFFC3;">Action Plan</span></div>""")
            tasks = []
            if ats_score < 70: tasks.append("Add 3-5 more technical keywords from our skill database to boost ATS match.")
            if len(skills) < 10: tasks.append("List your explicitly known technologies in a dedicated 'Technical Skills' section.")
            if "project" not in resume_text.lower(): tasks.append("Add a 'Projects' section detailing 2-3 technical builds with quantified results.")
            if metrics_count <= 3: tasks.append("Review your bullet points and add specific metrics (percentages, user counts, performance gains).")
            if not recommended_jobs: tasks.append("Use the JD Alignment tab to target a specific role and discover missing keywords.")
            if not tasks: tasks.append("Your resume format is stellar. Move to the Voice Interview tab to practice your delivery!")

            for i, task in enumerate(tasks):
                st.checkbox(task, key=f"task_{i}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            report_json = {"ats_score": ats_score, "skills_detected": skills, "action_items": tasks}
            st.download_button("📥 Download Full Report (JSON)", data=json.dumps(report_json, indent=2), file_name="resume_report.json", mime="application/json", use_container_width=True)


        # ==========================================
        # TAB 2: JD ALIGNMENT (WITH GROQ GAP ANALYSIS)
        # ==========================================
        with tab_matcher:
            col_match1, col_match2 = st.columns([1, 1])
            with col_match1:
                st.html("""<div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;color:#ECE9E2;margin-bottom:14px;">Detected Keywords</div>""")
                chips = "".join([f'<span class="skill-chip">{s}</span>' for s in skills]) if skills else "<span style='color:#818DA0;font-size:12px;'>No skills found.</span>"
                st.html(f"""<div style="background:rgba(18,21,30,0.85);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:20px;margin-bottom:20px;">{chips}</div>""")

            with col_match2:
                st.html("""<div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;color:#ECE9E2;margin-bottom:14px;">Role Suggestions</div>""")
                role_icons = {"Python Developer":"⬡","Frontend Developer":"◻","Backend Developer":"▨","Machine Learning Engineer":"◈","Flutter Developer":"◇"}
                if recommended_jobs:
                    jcards = "".join([f"""<div class="job-card"><div style="display:flex;align-items:center;gap:14px;"><div style="width:36px;height:36px;border-radius:8px;background:rgba(77,255,195,0.07);border:1px solid rgba(77,255,195,0.15);display:flex;align-items:center;justify-content:center;font-size:16px;color:#4DFFC3;">{role_icons.get(j,"◉")}</div><div><div style="font-family:'Syne',sans-serif;font-weight:600;font-size:14px;color:#ECE9E2;">{j}</div></div></div></div>""" for j in recommended_jobs])
                    st.html(f"""<div style="background:rgba(18,21,30,0.85);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:15px;margin-bottom:20px;">{jcards}</div>""")
                else: st.warning("Expand your skills to unlock role suggestions.")

            st.html("""<div style="margin-top:1.5rem;margin-bottom:1rem;"><h2 style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:700;color:#ECE9E2;margin:5px 0 0 0;">Target Role <span style="color:#FFBE57;">Cross-Reference</span></h2><p style="font-family:'Manrope',sans-serif;font-size:13px;color:#818DA0;margin-top:8px;">Paste the exact Job Description you are applying for below.</p></div>""")
            jd_text = st.text_area("Job Description", height=200, placeholder="Paste JD here...", label_visibility="collapsed")
            
            if jd_text:
                with st.spinner("Analyzing explicit and implied JD gaps..."):
                    time.sleep(0.6)
                    jd_skills_set = set(extract_skills(jd_text.lower())); resume_skills_set = set(skills)
                    matched = jd_skills_set & resume_skills_set; missing = jd_skills_set - resume_skills_set
                    
                    if not jd_skills_set: 
                        st.warning("No trackable technical skills found explicitly in this JD.")
                    else:
                        jd_score = round((len(matched) / len(jd_skills_set)) * 100)
                        mc = "#4DFFC3" if jd_score >= 75 else ("#FFBE57" if jd_score >= 40 else "#FF6B6B")
                        m_chips = "".join([f'<span style="display:inline-block;padding:6px 14px;background:rgba(255,107,107,0.08);border:1px solid rgba(255,107,107,0.3);border-radius:100px;font-family:Manrope,sans-serif;font-size:11px;font-weight:600;color:#FF6B6B;margin:3px 4px 3px 0;">{s}</span>' for s in missing]) or "<span style='color:#818DA0;font-size:12px;'>None!</span>"
                        g_chips = "".join([f'<span class="skill-chip" style="font-size:11px;padding:6px 14px;">{s}</span>' for s in matched]) or "<span style='color:#818DA0;font-size:12px;'>No matches.</span>"
                        st.html(f"""<div style="background:rgba(18,21,30,0.85);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:28px 32px;margin-top:15px;"><div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(255,255,255,0.05);padding-bottom:20px;margin-bottom:20px;"><div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;color:#ECE9E2;">Alignment Results</div><div style="text-align:right;"><div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:{mc};line-height:1;">{jd_score}%</div><div style="font-family:'Manrope',sans-serif;font-size:10px;text-transform:uppercase;color:#818DA0;">JD Match</div></div></div><div style="margin-bottom:24px;"><div style="font-family:'Manrope',sans-serif;font-size:11px;text-transform:uppercase;color:#FF6B6B;font-weight:700;margin-bottom:10px;">Missing Explicit Keywords</div><div>{m_chips}</div></div><div><div style="font-family:'Manrope',sans-serif;font-size:11px;text-transform:uppercase;color:#4DFFC3;font-weight:700;margin-bottom:10px;">Matched Keywords</div><div>{g_chips}</div></div></div>""")

                    # Semantic AI Gap Analysis
                    if api_key:
                        try:
                            client = Groq(api_key=api_key)
                            prompt = f"From this job description, identify exactly 4 'implied' or secondary skills/tools required that are NOT these explicitly found keywords ({', '.join(matched)}). Return ONLY a comma-separated list of the 4 skill names: {jd_text[:1500]}"
                            implied_resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}], temperature=0.3)
                            implied_skills = [s.strip() for s in implied_resp.choices[0].message.content.split(',') if s.strip()]

                            st.html("""<div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;color:#ECE9E2;margin-top:30px;margin-bottom:15px;">📊 Actionable Gap Analysis</div>""")
                            
                            gap_data = {"Skill / Requirement": [], "Status": [], "Action to Take": []}
                            for m in list(missing)[:3]:
                                gap_data["Skill / Requirement"].append(m.title())
                                gap_data["Status"].append("❌ Explicitly Missing")
                                gap_data["Action to Take"].append("Add to resume skills/projects")
                            for imp in implied_skills[:3]:
                                gap_data["Skill / Requirement"].append(imp.title())
                                gap_data["Status"].append("⚠️ AI Detected (Implied)")
                                gap_data["Action to Take"].append("Weave into bullet points")

                            st.dataframe(gap_data, use_container_width=True, hide_index=True)
                        except Exception as e:
                            pass
                    else:
                        st.info("Enter your Groq API key at the top of the page to unlock deep semantic gap analysis.")

        # ==========================================
        # TAB 3: AI ENHANCER (SIDE-BY-SIDE COMPARISON)
        # ==========================================
        with tab_ai:
            st.html("""<div style="margin-bottom:1.5rem;"><h2 style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:700;color:#ECE9E2;margin:5px 0 0 0;">Generative AI <span style="color:#4DFFC3;">Copilot</span></h2><p style="font-family:'Manrope',sans-serif;font-size:13px;color:#818DA0;margin-top:8px;">Generate a complete ATS-optimized rewrite of your resume below.</p></div>""")

            if st.button("✨ Generate Full Resume Rewrite", use_container_width=True):
                if not api_key: 
                    st.error("Please enter your Groq API key at the top of the page.")
                else:
                    with st.spinner("Rewriting entire resume for maximum impact..."):
                        try:
                            client = Groq(api_key=api_key)
                            prompt = f"You are an expert FAANG resume writer. Rewrite this entire resume text to be highly professional, impactful, and ATS-optimized. Upgrade the action verbs, format it cleanly, and infer reasonable professional metrics where appropriate to show impact. \n\nResume Text:\n{resume_text}\n\nReturn ONLY the newly written resume text. Do not include introductory or concluding remarks."
                            resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}], temperature=0.6)
                            st.session_state.full_rewrite = resp.choices[0].message.content
                        except Exception as e: 
                            st.error(f"API Error: {e}")

            # --- THE SPLIT VIEW UI (DARK MODE STYLING) ---
            if st.session_state.full_rewrite:
                st.html("""<div style="margin-top:2.5rem;margin-bottom:1rem;"><h3 style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;color:#ECE9E2;">Document <span style="color:#4DFFC3;">Comparison</span></h3></div>""")
                
                c_orig, c_enh = st.columns(2)
                
                with c_orig:
                    st.html(f"""
                    <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07); border-radius:12px; padding:24px; height:550px; overflow-y:auto; font-family:'Manrope',sans-serif; font-size:13px; color:#818DA0; line-height:1.8; white-space:pre-wrap;">
                        <div style="font-weight:800; color:#ECE9E2; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:15px; font-size:11px;">📄 Original Text</div>
                        {resume_text}
                    </div>
                    """)
                
                with c_enh:
                    st.html(f"""
                    <div style="background:rgba(18,21,30,0.85); border:1px solid rgba(77,255,195,0.3); border-radius:12px; padding:24px; height:550px; overflow-y:auto; font-family:'Manrope',sans-serif; font-size:13px; color:#ECE9E2; line-height:1.8; white-space:pre-wrap; box-shadow:inset 0 0 20px rgba(77,255,195,0.02);">
                        <div style="font-weight:800; color:#4DFFC3; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:15px; font-size:11px;">✨ AI Enhanced Version</div>
                        {st.session_state.full_rewrite}
                    </div>
                    """)
                
                st.html("<br>")
                st.download_button(
                    label="📥 Download Enhanced Resume (.txt)",
                    data=st.session_state.full_rewrite,
                    file_name="AI_Enhanced_Resume.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                st.info("Click the generate button above to see the AI comparison.")

        # ==========================================
        # TAB 4: VOICE INTERVIEW (WITH DYNAMIC FOLLOW-UPS)
        # ==========================================
        with tab_voice:
            st.html("""<div style="margin-bottom:1.5rem;"><h2 style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:700;color:#ECE9E2;margin:5px 0 0 0;">Live <span style="color:#FFBE57;">Mock Interview</span></h2><p style="font-family:'Manrope',sans-serif;font-size:13px;color:#818DA0;margin-top:8px;">AI asks a question aloud → you speak your answer → Groq transcribes & scores.</p></div>""")

            if st.button("🎯 Generate Custom Question"):
                if not api_key: st.error("Enter your Groq API key at the top of the page.")
                else:
                    with st.spinner("Generating..."):
                        try:
                            client = Groq(api_key=api_key)
                            q_resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "system", "content": "You are a technical interviewer. Output ONLY the question text."}, {"role": "user", "content": f"Skills: {', '.join(skills)}. Generate one sharp technical interview question."}], temperature=0.85)
                            st.session_state.voice_q = q_resp.choices[0].message.content.strip()
                            st.session_state.voice_transcript = None; st.session_state.voice_eval = None
                        except Exception as e: st.error(f"Error: {e}")

            if st.session_state.voice_q:
                st.html(f"""<div style="background:rgba(18,21,30,0.85);backdrop-filter:blur(8px);border:1px solid rgba(77,255,195,0.25);border-radius:16px;padding:24px;margin:16px 0;"><div style="font-family:'Manrope',sans-serif;font-size:10px;text-transform:uppercase;color:#4DFFC3;margin-bottom:10px;font-weight:700;">◈ Interview Question</div><div style="font-family:'Syne',sans-serif;font-size:1.2rem;color:#ECE9E2;line-height:1.5;">{st.session_state.voice_q}</div></div>""")
                
                if st.button("🔊 Read Aloud"):
                    components.html(f"""<script>window.speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance({json.dumps(st.session_state.voice_q)}); u.rate=0.9; window.speechSynthesis.speak(u);</script>""", height=0)

                st.html("""<div style="font-family:'Manrope',sans-serif;font-size:12px;text-transform:uppercase;color:#818DA0;margin:20px 0 6px;font-weight:600;">🎙️ Record Your Answer</div>""")
                audio_input = st.audio_input("", key="phase5_recorder", label_visibility="collapsed")
                audio_bytes = audio_input.read() if audio_input else None

                if audio_bytes and len(audio_bytes) > 2000:
                    with st.spinner("Transcribing..."):
                        try:
                            client = Groq(api_key=api_key)
                            st.session_state.voice_transcript = client.audio.transcriptions.create(file=("answer.wav", audio_bytes), model="whisper-large-v3", response_format="text")
                        except Exception as e: st.error(f"Error: {e}")

            if st.session_state.voice_transcript:
                st.html(f"""<div style="background:rgba(13,16,24,0.9);border-left:3px solid #4DFFC3;padding:20px;margin-bottom:16px;"><div style="font-family:'Manrope',sans-serif;font-size:10px;color:#4DFFC3;margin-bottom:8px;">📝 Transcribed Answer</div><div style="font-style:italic;color:#ECE9E2;">"{st.session_state.voice_transcript}"</div></div>""")
                if st.button("⚡ Evaluate Answer"):
                    with st.spinner("Analyzing..."):
                        try:
                            client = Groq(api_key=api_key)
                            eval_res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "system", "content": "You are a strict technical interviewer."}, {"role": "user", "content": f"Q: {st.session_state.voice_q}\nA: {st.session_state.voice_transcript}\n\nEvaluate: Score X/10, Strengths, Gaps, Hint."}], temperature=0.5)
                            st.session_state.voice_eval = eval_res.choices[0].message.content
                        except Exception as e: st.error(f"Error: {e}")

            if st.session_state.voice_eval:
                st.html(f"""<div style="background:rgba(18,21,30,0.85);border:1px solid rgba(77,255,195,0.4);border-radius:16px;padding:28px;margin-top:15px;"><div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:700;color:#4DFFC3;margin-bottom:16px;">⚡ AI Evaluation</div><div style="font-family:'Manrope',sans-serif;font-size:14px;color:#ECE9E2;line-height:1.9;white-space:pre-wrap;">{st.session_state.voice_eval}</div></div>""")
                
                # --- Adaptive Follow-Up Question ---
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🎤 Hit me with a Follow-Up Question", type="primary", use_container_width=True):
                    with st.spinner("Analyzing your response to generate follow-up..."):
                        try:
                            client = Groq(api_key=api_key)
                            prompt = f"The candidate was asked '{st.session_state.voice_q}'. They answered: '{st.session_state.voice_transcript}'. Ask ONE short, challenging technical follow-up question digging deeper into their answer. Plain text only."
                            follow_up = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], temperature=0.7)
                            st.session_state.voice_q = follow_up.choices[0].message.content.strip()
                            st.session_state.voice_transcript = None
                            st.session_state.voice_eval = None
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

    else:
        st.html("""
        <div class="fade-in-2" style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:4rem 2rem;text-align:center;background:rgba(18,21,30,0.4);border:1px dashed rgba(255,255,255,0.05);border-radius:16px;margin-bottom:2rem;backdrop-filter:blur(4px);">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#4DFFC3" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:1.5rem;opacity:0.9;filter:drop-shadow(0 0 12px rgba(77,255,195,0.3));">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>
            </svg>
            <h3 style="font-family:'Syne',sans-serif;font-size:1.5rem;color:#ECE9E2;margin:0 0 10px 0;">Awaiting Document</h3>
            <p style="font-family:'Manrope',sans-serif;font-size:14px;color:#818DA0;max-width:420px;margin:0;line-height:1.7;">Upload your resume PDF above to initialize the ATS engine and unlock all 5 AI phases.</p>
        </div>""")

    # -----------------------------------
    # FOOTER
    # -----------------------------------
    st.html("""<div style="border-top:1px solid rgba(255,255,255,0.07);margin-top:2rem;text-align:center;padding:20px;color:#3A3F4E;font-size:12px;font-family:'Manrope',sans-serif;">Built with ❤️ using Python, Streamlit, Groq &amp; Whisper<br>AI Career Intelligence Platform</div>""")