import streamlit as st
import math
import plotly.graph_objects as go
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Attendance Tracker Pro", page_icon="📊", layout="centered")

# --- AUTO-SAVE (Query Parameters) ---
query_params = st.query_params
default_held = int(query_params.get("held", 0))
default_attended = int(query_params.get("att", 0))
default_total = int(query_params.get("total", 0))

# --- SESSION STATE ---
if 'calculated' not in st.session_state:
    st.session_state.calculated = False

# --- CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(17, 24, 39) 0%, rgb(10, 10, 10) 90%);
        font-family: 'Outfit', sans-serif;
    }
    .title-text {
        color: #ffffff; font-weight: 700; font-size: 2.2rem; text-align: center;
        background: -webkit-linear-gradient(45deg, #4f46e5, #06b6d4);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;
    }
    .nav-bar {
        background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px); padding: 10px 20px; border-radius: 50px;
        display: flex; justify-content: center; width: fit-content; margin: 0 auto 30px auto;
    }
    .nav-bar a { color: #e2e8f0; text-decoration: none; font-weight: 500; padding: 8px 16px; transition: all 0.3s ease; }
    .nav-bar a:hover { color: #6366f1; }
    
    .glass-container {
        background: rgba(30, 41, 59, 0.4); border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); padding: 32px; margin-bottom: 20px; backdrop-filter: blur(12px);
    }
    .sim-container {
        background: rgba(15, 23, 42, 0.8); border-radius: 20px; border: 1px solid rgba(99, 102, 241, 0.3); padding: 24px;
    }
    .badge { padding: 5px 12px; border-radius: 12px; font-weight: 700; font-size: 0.8rem; }
    .badge-scholar { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #059669; }
    .badge-safe { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid #2563eb; }
    .badge-risk { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #d97706; }
    .badge-danger { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #dc2626; }
    
    /* Input Styling */
    .stNumberInput > div > div > input, .stSelectbox > div > div {
        background-color: #0f172a !important; color: white !important; border: 1px solid #334155 !important; border-radius: 12px;
    }
    .stButton > button {
        width: 100%; background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
        color: white; border-radius: 12px; border: none; padding: 0.6rem; font-weight: 600;
    }
    .footer { text-align: center; color: #64748b; margin-top: 40px; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# --- CHART HELPER ---
def create_donut_chart(attended, bunked, remaining):
    colors = ['#0bc8a9', '#ef4444', '#64748b'] 
    fig = go.Figure(data=[go.Pie(
        labels=['Attended', 'Missed', 'Future'], values=[attended, bunked, remaining], hole=.75,
        marker=dict(colors=colors, line=dict(color='rgba(255,255,255,0.1)', width=1)),
        textinfo='none', hoverinfo='label+value+percent'
    )])
    current_pct = round((attended / (attended + bunked)) * 100) if (attended+bunked) > 0 else 0
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0), height=220,
        annotations=[dict(text=f"<span style='font-size:28px; font-weight:bold; color:white'>{current_pct}%</span><br><span style='color:#94a3b8; font-size:12px'>Current</span>", x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    return fig

# --- UI START ---
st.markdown("""
<div class="nav-bar">
    <a href="https://mvsrpapers.streamlit.app" target="_blank">📚 Papers</a>
    <a href="#">📊 Tracker Pro</a>
</div>
""", unsafe_allow_html=True)
st.markdown('<h1 class="title-text">ATTENDANCE PRO</h1>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        class_held = st.number_input("Classes Held", min_value=0, step=1, value=default_held, format="%d")
    with c2:
        class_attended = st.number_input("Classes Attended", min_value=0, step=1, value=default_attended, format="%d")

    college = st.selectbox("Select Year/College", ["MVSREC 2nd Year", "MVSREC 4th Year", "Others"])
    total_classes = 0
    if college == "MVSREC 4th Year":
        branch = st.selectbox("Select Branch", ['CSE', 'DS', 'AIML', 'IoT', 'IT', 'ECE', 'EEE', 'OTHERS'])
        totals_dict = {'CSE': 400, 'DS': 433, 'AIML': 400, 'IoT': 400, 'IT': 410, 'ECE': 400, 'EEE': 400}
        val = default_total if default_total > 0 else (totals_dict[branch] if branch in totals_dict else 0)
        total_classes = st.number_input("Total Classes (Est.)", value=val, step=1)
    else:
        total_classes = st.number_input("Total Classes (Est.)", min_value=0, step=1, value=default_total)

    min_percent_str = st.selectbox("Target Percentage", ['65%', '70%', '75%', '80%'], index=2)
    min_percent = int(min_percent_str.strip('%'))

    if st.button("Analyze Attendance"):
        st.session_state.calculated = True
        st.query_params["held"] = str(class_held)
        st.query_params["att"] = str(class_attended)
        st.query_params["total"] = str(total_classes)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANALYSIS ENGINE ---
if st.session_state.calculated:
    min_required = math.ceil(total_classes * min_percent / 100)
    remaining_classes = total_classes - class_held
    missed_classes = class_held - class_attended
    if missed_classes < 0: missed_classes = 0
    current_pct = round((class_attended / class_held) * 100, 2) if class_held > 0 else 0
    
    # Validation
    if class_attended > class_held:
        st.error("❌ Attended cannot be greater than Held.")
    elif total_classes == 0:
        st.error("❌ Total classes cannot be zero.")
    else:
        required_more = max(0, min_required - class_attended)
        bunks_possible = remaining_classes - required_more
        
        # Badge Logic
        badge = ""
        if current_pct >= 85: badge = '<span class="badge badge-scholar">🤓 SCHOLAR</span>'
        elif current_pct >= 75: badge = '<span class="badge badge-safe">🛡️ SAFE ZONE</span>'
        elif current_pct >= 65: badge = '<span class="badge badge-risk">💸 RISK ZONE</span>'
        else: badge = '<span class="badge badge-danger">💀 DANGER</span>'

        # --- MAIN REPORT CARD ---
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.5])
        with c1:
            st.plotly_chart(create_donut_chart(class_attended, missed_classes, remaining_classes), use_container_width=True)
        with c2:
            st.markdown(f"### Report {badge}", unsafe_allow_html=True)
            if class_attended >= min_required:
                st.success(f"🎉 Safe! You hit {min_percent}%.")
                st.write(f"You can skip all **{remaining_classes}** remaining classes.")
            elif required_more > remaining_classes:
                st.error(f"⚠️ Cannot reach {min_percent}%. Max: {round(((class_attended+remaining_classes)/total_classes)*100,1)}%")
            else:
                st.warning(f"Attend **{required_more}** more classes.")
                st.info(f"You have **{bunks_possible}** safe bunks left.")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- NEW & IMPROVED SIMULATOR ---
        st.markdown('<div class="sim-container">', unsafe_allow_html=True)
        st.markdown("### 🔮 Advanced Prediction")
        st.caption("Use sliders to calculate impact of Medical Certificates and Future Absences.")
        
        col_sim1, col_sim2 = st.columns(2)
        with col_sim1:
            future_bunks = st.slider("Future Absences (Classes you will skip)", 0, 200, 0)
        with col_sim2:
            medical_certs = st.slider("Medical Certificates (Classes to cover)", 0, 200, 0)
        
        # LOGIC: 
        # Numerator: Attended + Medical Certificates
        # Denominator: Held + Future Bunks (Absences increase the held count but not attended count)
        
        sim_numerator = class_attended + medical_certs
        sim_denominator = class_held + future_bunks
        
        # Prevent math errors
        if sim_denominator > 0:
            sim_pct = round((sim_numerator / sim_denominator) * 100, 2)
            
            # Cap at 100% just in case user inputs weird data
            if sim_pct > 100: sim_pct = 100.0

            # Visual Result
            color = "#0bc8a9" if sim_pct >= min_percent else "#ef4444"
            
            st.markdown("---")
            st.markdown(f"""
            <div style="text-align:center;">
                <p style="color:#94a3b8; margin-bottom:5px;">Prediction Calculation</p>
                <h2 style="color:{color}; margin:0;">{sim_pct}%</h2>
                <p style="color:#cbd5e1; font-family:monospace; margin-top:5px;">
                    {sim_numerator} (Attended) / {sim_denominator} (Total)
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Tips based on simulation
            if sim_pct < min_percent:
                st.caption(f"⚠️ You are still lagging by {round(min_percent - sim_pct, 2)}%. Try increasing certificates or reducing absences.")
        else:
            st.write("Waiting for inputs...")

        st.markdown('</div>', unsafe_allow_html=True)

        # --- DOWNLOAD BUTTON ---
        report_text = f"Subject: Attendance Report\nCurrent: {current_pct}%\nTarget: {min_percent}%\nNeed to attend: {required_more}\n\nGenerated by Attendance Tracker Pro"
        st.download_button("⬇️ Download Report", report_text, file_name="attendance.txt")

# --- FOOTER ---
st.markdown('<div class="footer">Developed by Uday Kiran</div>', unsafe_allow_html=True)
