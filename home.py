import streamlit as st

def show_home(switch_page_callback):
    # ── GLOBAL LANDING PAGE CSS ──
    st.html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Manrope:wght@300;400;500;600;700&display=swap');
    
    .main, [data-testid="stAppViewContainer"] { background: #050608 !important; }
    
    /* Premium Float Animation */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* SaaS Glass Card */
    .feature-card {
        background: rgba(18, 21, 30, 0.4);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 30px;
        transition: all 0.4s cubic-bezier(0.2, 0.95, 0.4, 1.1);
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-10px);
        border-color: #4DFFC3;
        box-shadow: 0 15px 35px rgba(77, 255, 195, 0.1);
        background: rgba(18, 21, 30, 0.8);
    }
    
    /* Text Gradients */
    .text-gradient {
        background: linear-gradient(90deg, #4DFFC3 0%, #00d2ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .text-gradient-gold {
        background: linear-gradient(90deg, #FFBE57 0%, #F59E0B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Comparison Table */
    .comp-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    .comp-table th, .comp-table td { padding: 16px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05); font-family: 'Manrope', sans-serif; color: #ECE9E2; }
    .comp-table th { font-family: 'Syne', sans-serif; font-weight: 700; color: #818DA0; }
    .comp-table tr:hover { background: rgba(255,255,255,0.02); }
    
    /* Hide default Streamlit button UI to style it fully */
    button[kind="primary"] {
        background: linear-gradient(135deg, #4DFFC3 0%, #00d2ff 100%) !important;
        color: #050608 !important;
        border-radius: 50px !important;
        padding: 12px 32px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    button[kind="primary"]:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 10px 30px rgba(77, 255, 195, 0.3) !important;
    }
    </style>
    """)

    # ── SECTION 1: HERO (WITH PURE CSS ANIMATION) ──
    st.html("""
    <style>
    /* Floating Effect for Cards and Visuals */
    .floating-container {
        animation: float 4s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-12px); }
        100% { transform: translateY(0px); }
    }
    </style>
    """)

    col_hero_left, col_hero_right = st.columns([1.3, 1], gap="large")
    
    with col_hero_left:
        st.html("""
        <div style="padding-top: 2rem;">
            <div style="font-family:'Manrope',sans-serif;font-size:12px;letter-spacing:0.2em;text-transform:uppercase;color:#4DFFC3;font-weight:600;margin-bottom:16px;">
                ◈ Next-Gen Career Copilot
            </div>
            <h1 style="font-family:'Syne',sans-serif;font-size:4.2rem;font-weight:800;color:#ECE9E2;line-height:1.05;margin:0 0 20px 0;letter-spacing:-0.03em;">
                AI Career <span class="text-gradient">Intelligence</span> Platform
            </h1>
            <p style="font-family:'Manrope',sans-serif;font-size:1.15rem;color:#818DA0;max-width:540px;margin:0 0 35px 0;line-height:1.7;">
                Analyze your resume text against modern ATS criteria. Uncover optimization gaps, execute instant AI modifications, and practice with real-time vocal mock interviews.
            </p>
        </div>
        """)
        
        # Launch Button placed elegantly under text
        if st.button("🚀 Launch Analyzer Platform", type="primary"):
            switch_page_callback("analyzer")

    with col_hero_right:
        st.html("""
        <style>
        .orb-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            padding-top: 2rem;
        }
        
        /* The Morphing AI Brain */
        .ai-aurora-orb {
            width: 340px;
            height: 340px;
            /* Using your brand colors: Neon Green, Cyan, and Amber */
            background: linear-gradient(45deg, #4DFFC3, #00d2ff, #FFBE57, #4DFFC3);
            background-size: 300% 300%;
            animation: 
                orb-morph 8s ease-in-out infinite, 
                orb-spin 10s linear infinite, 
                float 6s ease-in-out infinite;
            box-shadow:
                0 0 80px rgba(77, 255, 195, 0.25),   /* Outer neon glow */
                inset 0 0 60px rgba(0, 0, 0, 0.6),   /* Inner shadow for 3D depth */
                inset 0 0 20px rgba(255, 255, 255, 0.4); /* Inner glass highlight */
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        
        /* The glowing center star */
        .ai-aurora-orb::before {
            content: "✦";
            font-size: 90px;
            color: #050608;
            text-shadow: 0 0 30px rgba(255,255,255,0.6);
            animation: pulse-star 3s ease-in-out infinite alternate;
        }
        
        /* Smooth organic shape shifting */
        @keyframes orb-morph {
            0% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
            50% { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; }
            100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
        }
        
        /* Color gradient shifting */
        @keyframes orb-spin {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Star pulsing */
        @keyframes pulse-star {
            0% { transform: scale(0.85); opacity: 0.7; }
            100% { transform: scale(1.1); opacity: 1; text-shadow: 0 0 50px rgba(255,255,255,0.9); }
        }
        </style>
        
        <div class="orb-container">
            <div class="ai-aurora-orb"></div>
        </div>
        """)

    # ── SECTION 2: STATS ──
    st.html("<div style='height:4rem;'></div>")
    s1, s2, s3, s4 = st.columns(4)
    def stat_card(col, num, label):
        col.html(f"""
        <div style="text-align:center;border-right:1px solid rgba(255,255,255,0.05);">
            <div style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;color:#ECE9E2;">{num}</div>
            <div style="font-family:'Manrope',sans-serif;font-size:12px;text-transform:uppercase;letter-spacing:0.1em;color:#4DFFC3;">{label}</div>
        </div>""")
    stat_card(s1, "25k+", "Resumes Analyzed")
    stat_card(s2, "95%", "ATS Accuracy")
    stat_card(s3, "5", "AI Modules")
    stat_card(s4, "100+", "Interview Scenarios")

    # ── SECTION 3: FEATURE CARDS ──
    st.html("""<div style="text-align:center;margin:6rem 0 3rem;"><h2 style="font-family:'Syne',sans-serif;font-size:2.5rem;color:#ECE9E2;">Everything you need to <span class="text-gradient-gold">get hired.</span></h2></div>""")
    
    f1, f2, f3 = st.columns(3)
    def feature(col, icon, title, desc):
        col.html(f"""
        <div class="feature-card">
            <div style="font-size:2.5rem;margin-bottom:16px;">{icon}</div>
            <h3 style="font-family:'Syne',sans-serif;font-size:1.3rem;color:#ECE9E2;margin:0 0 10px 0;">{title}</h3>
            <p style="font-family:'Manrope',sans-serif;font-size:14px;color:#818DA0;line-height:1.6;margin:0;">{desc}</p>
        </div>""")
    
    feature(f1, "📑", "ATS Analysis", "Deep-scan your PDF to extract technical skills and calculate your baseline ATS match score.")
    feature(f2, "🎯", "JD Matching", "Compare your profile against target Job Descriptions to uncover critical missing keywords.")
    feature(f3, "✨", "Resume Rewrite", "Our FAANG-trained AI rewrites your weakest bullet points into quantifiable impact metrics.")
    
    st.html("<div style='height:1.5rem;'></div>")
    f4, f5, f6 = st.columns(3)
    feature(f4, "🧠", "Interview Prep", "Generate hyper-specific mock interview questions based on the exact overlap of your resume and the JD.")
    feature(f5, "🎙️", "Voice AI", "Practice live. The AI asks a question aloud, transcribes your spoken answer, and grades you.")
    feature(f6, "📈", "Career Insights", "Track your technical depth, interview readiness, and overall hiring probability in one dashboard.")

    # ── SECTION 4: TIMELINE ──
    st.html("""
    <div style="margin:6rem 0;padding:40px;background:rgba(255,255,255,0.02);border-radius:24px;">
        <h3 style="font-family:'Syne',sans-serif;text-align:center;color:#ECE9E2;margin-bottom:30px;">How It Works</h3>
        <div style="display:flex;justify-content:space-between;align-items:center;font-family:'Manrope',sans-serif;color:#818DA0;text-align:center;font-weight:600;font-size:14px;">
            <div><div style="font-size:24px;color:#4DFFC3;margin-bottom:8px;">1</div>Upload Resume</div>
            <div style="opacity:0.3;">━━━━</div>
            <div><div style="font-size:24px;color:#4DFFC3;margin-bottom:8px;">2</div>ATS Analysis</div>
            <div style="opacity:0.3;">━━━━</div>
            <div><div style="font-size:24px;color:#4DFFC3;margin-bottom:8px;">3</div>AI Feedback</div>
            <div style="opacity:0.3;">━━━━</div>
            <div><div style="font-size:24px;color:#4DFFC3;margin-bottom:8px;">4</div>Mock Interview</div>
            <div style="opacity:0.3;">━━━━</div>
            <div><div style="font-size:24px;color:#FFBE57;margin-bottom:8px;">5</div>Get Hired</div>
        </div>
    </div>
    """)

    # ── SECTION 6: COMPARISON TABLE ──
    st.html("""
    <div style="margin:6rem auto; max-width: 800px;">
        <h2 style="font-family:'Syne',sans-serif;font-size:2.5rem;color:#ECE9E2;text-align:center;margin-bottom:2rem;">Why Choose Us</h2>
        <table class="comp-table">
            <tr>
                <th style="text-align:left;">Feature</th>
                <th style="color:#4DFFC3;">Our AI Platform</th>
                <th>Traditional ATS</th>
            </tr>
            <tr><td style="text-align:left;">Live Voice Interviews</td><td>✅</td><td>❌</td></tr>
            <tr><td style="text-align:left;">Contextual JD Matching</td><td>✅</td><td>❌</td></tr>
            <tr><td style="text-align:left;">Generative Resume Rewrites</td><td>✅</td><td>❌</td></tr>
            <tr><td style="text-align:left;">Custom Interview Prep</td><td>✅</td><td>❌</td></tr>
            <tr><td style="text-align:left;">Keyword Extraction</td><td>✅</td><td>✅</td></tr>
        </table>
    </div>
    """)

    # ── SECTION 8: FINAL CTA ──
    st.html("""
    <div style="text-align:center;padding:5rem 2rem;background:linear-gradient(180deg, rgba(77,255,195,0.05) 0%, transparent 100%);border-top:1px solid rgba(77,255,195,0.1);margin-top:4rem;">
        <h2 style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;color:#ECE9E2;margin-bottom:1rem;">Ready to upgrade your career?</h2>
        <p style="font-family:'Manrope',sans-serif;color:#818DA0;margin-bottom:2rem;">Stop guessing what recruiters want. Let AI build your roadmap.</p>
    </div>
    """)
    
    col4, col5, col6 = st.columns([1, 1, 1])
    with col5:
        if st.button("⚡ Get Started Now", type="primary", use_container_width=True):
            switch_page_callback("analyzer")