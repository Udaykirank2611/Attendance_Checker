import streamlit as st
import math
import plotly.graph_objects as go
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Attendance Tracker Pro", page_icon="📊", layout="centered")

# --- FEATURE 5: AUTO-SAVE (Query Parameters) ---
# Retrieve values from URL if they exist
query_params = st.query_params
default_held = int(query_params.get("held", 0))
default_attended = int(query_params.get("att", 0))
default_total = int(query_params.get("total", 0))

# --- SESSION STATE INITIALIZATION ---
if 'calculated' not in st.session_state:
    st.session_state.calculated = False

# --- CUSTOM CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(17, 24, 39) 0%, rgb(10, 10, 10) 90%);
        font-family: 'Outfit', sans-serif;
    }

    /* Header Styling */
    .title-text {
        color: #ffffff;
        font-weight: 700;
        font-size: 2.2rem;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #4f46e5, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Navbar */
    .nav-bar {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 10px 20px;
        border-radius: 50px;
        display: flex;
        justify-content: center;
        width: fit-content;
        margin: 0 auto 30px auto;
    }
    .nav-bar a {
        color: #e2e8f0;
        text-decoration: none;
        font-weight: 500;
        padding: 8px 16px;
        border-radius: 30px;
        transition: all 0.3s ease;
    }
    .nav-bar a:hover {
        background: rgba(79, 70, 229, 0.2);
        color: #6366f1;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
    }

    /* Cards */
    .glass-container {
        background: rgba(30, 41, 59, 0.4);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        padding: 32px;
        margin-bottom: 20px;
        backdrop-filter: blur(12px);
    }

    .cert-container {
        background: rgba(234, 179, 8, 0.1);
        border: 1px solid rgba(234, 179, 8, 0.3);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .sim-container {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        padding: 24px;
    }

    /* FEATURE 4 CSS: Badges */
    .badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }
    .badge-scholar { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #059669; }
    .badge-safe { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid #2563eb; }
    .badge-risk { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #d97706; }
    .badge-danger { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #dc2626; }

    /* Inputs */
    .stSelectbox label, .stNumberInput label, .stSlider label {
        color: #e2e8f0 !important;
        font-weight: 500;
    }
    .stSelectbox > div > div, .stNumberInput > div > div > input {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        color: white !important;
        border-radius: 12px !important;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.6rem 1rem !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(6, 182, 212, 0.3);
        transition: all 0.3s ease;
        margin-top: 10px;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5);
    }

    /* Stats */
    .stat-box {
        text-align: center; 
        background: rgba(255,255,255,0.05); 
        padding: 10px; 
        border-radius: 12px;
    }
    .stat-val { font-size: 1.5rem; font-weight: bold; color: #fff; }
    .stat-lbl { font-size: 0.8rem; color: #94a3b8; }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 40px;
        padding-bottom: 20px;
        border-top: 1px solid rgba(255,255,255,0.05);
        padding-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def create_donut_chart(attended, bunked, remaining):
    colors = ['#0bc8a9', '#ef4444', '#64748b'] 
    labels = ['Attended', 'Missed', 'Future']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=[attended, bunked, remaining],
        hole=.75,
        marker=dict(colors=colors, line=dict(color='rgba(255,255,255,0.1)', width=1)),
        textinfo='none', 
        hoverinfo='label+value+percent'
    )])

    total = attended + bunked + remaining
    current_pct = round((attended / (attended + bunked)) * 100) if (attended+bunked) > 0 else 0
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        height=220,
        annotations=[dict(text=f"<span style='font-size:28px; font-weight:bold; color:white'>{current_pct}%</span><br><span style='color:#94a3b8; font-size:12px'>Current</span>", x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    return fig

# --- UI LAYOUT ---
st.markdown("""
<div class="nav-bar">
    <a href="https://mvsrpapers.streamlit.app" target="_blank">📚 Papers</a>
    <a href="#">📊 Tracker Pro</a>
</div>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title-text">ATTENDANCE PRO</h1>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        # Pre-fill with default value from URL or 0
        class_held = st.number_input("Classes Held", min_value=0, step=1, format="%d", value=default_held)
    with col2:
        class_attended = st.number_input("Classes Attended", min_value=0, step=1, format="%d", value=default_attended)

    college = st.selectbox("Select Year/College", ["MVSREC 2nd Year", "MVSREC 4th Year", "Others"])
    
    total_classes = 0
    if college == "MVSREC 4th Year":
        branch = st.selectbox("Select Branch", ['CSE', 'DS', 'AIML', 'IoT', 'IT', 'ECE', 'EEE', 'OTHERS'])
        totals_dict = {'CSE': 400, 'DS': 433, 'AIML': 400, 'IoT': 400, 'IT': 410, 'ECE': 400, 'EEE': 400}
        
        if branch in totals_dict:
            st.info(f"💡 Default total for {branch} is {totals_dict[branch]}.")
            # If default_total exists in URL use it, otherwise use dict value
            val = default_total if default_total > 0 else totals_dict[branch]
            total_classes = st.number_input("Total Classes (Est.)", value=val, step=1)
        else:
            total_classes = st.number_input("Total Classes (Est.)", min_value=0, step=1, value=default_total)
    else:
        total_classes = st.number_input("Total Classes (Est.)", min_value=0, step=1, value=default_total)

    min_percent_str = st.selectbox("Target Percentage", ['65%', '70%', '75%', '80%'], index=2)
    min_percent = int(min_percent_str.strip('%'))

    if st.button("Analyze Attendance"):
        st.session_state.calculated = True
        # UPDATE URL with new values
        st.query_params["held"] = str(class_held)
        st.query_params["att"] = str(class_attended)
        st.query_params["total"] = str(total_classes)

    st.markdown('</div>', unsafe_allow_html=True)

# --- RESULTS LOGIC ---
if st.session_state.calculated:
    # Calculations
    min_required = math.ceil(total_classes * min_percent / 100)
    remaining_classes = total_classes - class_held
    missed_classes = class_held - class_attended
    if missed_classes < 0: missed_classes = 0 
    current_pct = round((class_attended / class_held) * 100, 2) if class_held > 0 else 0

    if class_attended > class_held:
        st.error("❌ Attended cannot be > Held")
    elif total_classes == 0:
        st.error("❌ Total classes cannot be 0")
    else:
        required_more = min_required - class_attended
        if required_more < 0: required_more = 0
        bunks_possible = remaining_classes - required_more
        
        # Vacation Mode (Consecutive Bunks)
        target_ratio = min_percent / 100
        consecutive_bunks = 0
        if target_ratio > 0:
            max_held_for_target = class_attended / target_ratio
            consecutive_bunks = math.floor(max_held_for_target - class_held)
            if consecutive_bunks < 0: consecutive_bunks = 0

        # --- FEATURE 4: RISK BADGES ---
        badge_html = ""
        if current_pct >= 85:
            badge_html = '<span class="badge badge-scholar">🤓 SCHOLAR ZONE</span>'
        elif current_pct >= 75:
            badge_html = '<span class="badge badge-safe">🛡️ SAFE ZONE</span>'
        elif current_pct >= 65:
            badge_html = '<span class="badge badge-risk">💸 CONDONATION RISK</span>'
        else:
            badge_html = '<span class="badge badge-danger">💀 DETAINED ZONE</span>'

        # --- MAIN DASHBOARD ---
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.5])
        
        with c1:
            st.plotly_chart(create_donut_chart(class_attended, missed_classes, remaining_classes), use_container_width=True)
        
        with c2:
            st.markdown(f"### Status Report {badge_html}", unsafe_allow_html=True)
            
            if class_attended >= min_required:
                st.success(f"🎉 **SAFE!** You've hit {min_percent}%!")
                st.write(f"You can skip the remaining **{remaining_classes}** classes.")
            elif required_more > remaining_classes:
                max_reach = round(((class_attended + remaining_classes)/total_classes)*100, 1)
                st.error(f"⚠️ **IMPOSSIBLE** to reach {min_percent}%.")
                st.write(f"Max possible: **{max_reach}%**")
            else:
                st.info(f"You can bunk **{bunks_possible}** more classes total.")
                st.warning(f"You MUST attend **{required_more}** / {remaining_classes} remaining.")

            st.markdown("""<div style="display:flex; gap:10px; margin-top:10px;">""", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"<div class='stat-box'><div class='stat-val'>{required_more}</div><div class='stat-lbl'>Need to Attend</div></div>", unsafe_allow_html=True)
            with col_b:
                st.markdown(f"<div class='stat-box'><div class='stat-val'>{bunks_possible}</div><div class='stat-lbl'>Can Bunk</div></div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

        # --- FEATURE: CERTIFICATE CALCULATOR ---
        target_for_current_held = math.ceil(class_held * (min_percent / 100))
        certs_needed = target_for_current_held - class_attended
        current_real_percent = (class_attended / class_held) * 100 if class_held > 0 else 0
        
        if certs_needed > 0 and current_real_percent < min_percent:
            st.markdown('<div class="cert-container">', unsafe_allow_html=True)
            st.markdown(f"### 📜 Medical/Event Certificate Calculator")
            st.write(f"You are currently at **{round(current_real_percent, 2)}%** (below {min_percent}%).")
            
            if certs_needed <= missed_classes:
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:15px; margin-top:10px;">
                    <div style="font-size:2.5rem;">🚑</div>
                    <div>
                        <span style="font-size:1.1rem; color:#fde047;">Solution:</span><br>
                        You need to submit certificates for <b>{certs_needed}</b> classes.
                        <br><span style="font-size:0.9rem; opacity:0.8;">This will boost your current attendance to exactly {min_percent}%.</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"Even if you cover all {missed_classes} missed classes with certificates, you won't reach {min_percent}% based on current classes held.")
            
            st.markdown('</div>', unsafe_allow_html=True)

        # --- VACATION MODE MSG ---
        elif consecutive_bunks > 0:
             st.markdown(f"""
             <div class="glass-container" style="border-left: 5px solid #0bc8a9;">
                <h4 style="margin:0; color:#fff;">🏖️ Vacation Mode</h4>
                <p style="color:#cbd5e1; margin-top:5px;">
                    You can skip the next <b>{consecutive_bunks} classes in a row</b> 
                    before your percentage drops to {min_percent}%.
                </p>
             </div>
             """, unsafe_allow_html=True)

        # --- SIMULATOR ---
        st.markdown('<div class="sim-container">', unsafe_allow_html=True)
        st.markdown("### 🔮 Future Simulator")
        st.caption("Slide to see what happens if you skip the next few classes.")
        
        max_sim = min(20, remaining_classes) if remaining_classes > 0 else 10
        if max_sim > 0:
            sim_bunks = st.slider("Skip next X classes:", 0, max_sim, 0)
            sim_held = class_held + sim_bunks
            sim_attended = class_attended 
            sim_pct = round((sim_attended / sim_held) * 100, 2)
            
            if sim_pct >= min_percent:
                st.markdown(f"<h3 style='color:#0bc8a9; text-align:center;'>Result: {sim_pct}% (Safe ✅)</h3>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h3 style='color:#ef4444; text-align:center;'>Result: {sim_pct}% (Danger ⚠️)</h3>", unsafe_allow_html=True)
        else:
            st.write("No remaining classes to simulate!")

        st.markdown('</div>', unsafe_allow_html=True)

        # --- FEATURE 3: DOWNLOAD REPORT ---
        report_text = f"""
        ATTENDANCE STRATEGY REPORT
        Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
        ----------------------------------------
        Classes Held:     {class_held}
        Classes Attended: {class_attended}
        Current %:        {current_pct}%
        Target %:         {min_percent}%
        ----------------------------------------
        ACTION PLAN:
        - Classes Remaining: {remaining_classes}
        - You MUST attend:   {required_more} classes
        - You CAN bunk:      {bunks_possible} classes
        
        CERTIFICATES:
        {f"Need {certs_needed} certificates to hit target immediately." if (certs_needed > 0 and current_real_percent < min_percent) else "No certificates needed right now."}
        
        Generated by Attendance Tracker Pro
        """
        
        st.download_button(
            label="📄 Download Strategy Report (TXT)",
            data=report_text,
            file_name=f"Attendance_Plan_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt",
            mime="text/plain",
            type="secondary"
        )

# --- FOOTER ---
st.markdown("""
<div class="footer">
    Developed by <span>Uday Kiran</span> | Contact: 245122750006@mvsrec.edu.in
</div>
""", unsafe_allow_html=True)
