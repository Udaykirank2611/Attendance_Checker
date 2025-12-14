import streamlit as st
import math
import plotly.graph_objects as go
import datetime
from fpdf import FPDF

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="BUNK CHECKER", page_icon="📊", layout="centered")

# --- SESSION STATE INITIALIZATION ---
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

# --- FEATURE: RESET DATA (Sidebar) ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    # THEME SWITCHER
    theme_toggle = st.toggle("🌞 Light Mode", value=(st.session_state.theme == 'Light'))
    if theme_toggle:
        st.session_state.theme = 'Light'
    else:
        st.session_state.theme = 'Dark'
        
    st.divider()
    
    # RESET BUTTON
    if st.button("🧹 Reset All Data", type="primary"):
        st.query_params.clear()
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# --- DYNAMIC CSS LOADING ---
if st.session_state.theme == 'Dark':
    bg_color = "radial-gradient(circle at 10% 20%, rgb(17, 24, 39) 0%, rgb(10, 10, 10) 90%)"
    text_color = "#ffffff"
    glass_bg = "rgba(30, 41, 59, 0.4)"
    glass_border = "rgba(255, 255, 255, 0.08)"
    input_bg = "#0f172a"
    input_text = "white"
    stat_box_bg = "rgba(255,255,255,0.05)"
    sub_text = "#94a3b8"
else:
    # Light Mode Colors
    bg_color = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
    text_color = "#1e293b"
    glass_bg = "rgba(255, 255, 255, 0.7)"
    glass_border = "rgba(255, 255, 255, 0.4)"
    input_bg = "#ffffff"
    input_text = "#1e293b"
    stat_box_bg = "rgba(0,0,0,0.05)"
    sub_text = "#475569"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    .stApp {{
        background: {bg_color};
        font-family: 'Outfit', sans-serif;
        color: {text_color};
    }}

    /* Header Styling */
    .title-text {{
        color: {text_color};
        font-weight: 700;
        font-size: 2.2rem;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #4f46e5, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }}
    
    /* Navbar */
    .nav-bar {{
        background: {glass_bg};
        border: 1px solid {glass_border};
        backdrop-filter: blur(10px);
        padding: 10px 20px;
        border-radius: 50px;
        display: flex;
        justify-content: center;
        width: fit-content;
        margin: 0 auto 30px auto;
    }}
    .nav-bar a {{
        color: {text_color};
        text-decoration: none;
        font-weight: 500;
        padding: 8px 16px;
        border-radius: 30px;
        transition: all 0.3s ease;
    }}
    .nav-bar a:hover {{
        background: rgba(79, 70, 229, 0.2);
        color: #6366f1;
    }}

    /* Cards */
    .glass-container {{
        background: {glass_bg};
        border-radius: 24px;
        border: 1px solid {glass_border};
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        padding: 32px;
        margin-bottom: 20px;
        backdrop-filter: blur(12px);
    }}

    .cert-container {{
        background: rgba(234, 179, 8, 0.1);
        border: 1px solid rgba(234, 179, 8, 0.3);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
    }}

    .sim-container {{
        background: {glass_bg};
        border-radius: 20px;
        border: 1px solid #6366f1;
        padding: 24px;
    }}
    
    .sim-result-box {{
        background: {stat_box_bg};
        border-radius: 16px;
        padding: 20px;
        margin-top: 20px;
        border: 1px solid {glass_border};
    }}

    /* Badges */
    .badge {{
        display: inline-block;
        padding: 5px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }}
    .badge-scholar {{ background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #059669; }}
    .badge-safe {{ background: rgba(59, 130, 246, 0.2); color: #3b82f6; border: 1px solid #2563eb; }}
    .badge-risk {{ background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid #d97706; }}
    .badge-danger {{ background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #dc2626; }}

    /* Inputs */
    .stSelectbox label, .stNumberInput label, .stSlider label {{
        color: {text_color} !important;
        font-weight: 600;
    }}
    .stSelectbox > div > div, .stNumberInput > div > div > input {{
        background-color: {input_bg} !important;
        border: 1px solid #334155 !important;
        color: {input_text} !important;
        border-radius: 12px !important;
    }}
    
    /* === FIX: BUTTON STYLING (Both Regular & Download) === */
    div.stButton > button, div.stDownloadButton > button {{
        width: 100%;
        background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%) !important;
        color: #ffffff !important; /* Force white text */
        border-radius: 12px !important;
        border: none !important;
        padding: 0.6rem 1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(6, 182, 212, 0.3);
        transition: all 0.3s ease;
    }}
    div.stButton > button:hover, div.stDownloadButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5);
        filter: brightness(1.1);
        color: #ffffff !important;
    }}
    div.stButton > button p {{
        color: #ffffff !important; 
    }}

    /* Stats */
    .stat-box {{
        text-align: center; 
        background: {stat_box_bg}; 
        padding: 10px; 
        border-radius: 12px;
    }}
    .stat-val {{ font-size: 1.5rem; font-weight: bold; color: {text_color}; }}
    .stat-lbl {{ font-size: 0.8rem; color: {sub_text}; }}
    
    h3, h4 {{ color: {text_color} !important; }}

    /* Footer */
    .footer {{
        text-align: center;
        color: {sub_text};
        font-size: 0.85rem;
        margin-top: 40px;
        padding-bottom: 20px;
        border-top: 1px solid {glass_border};
        padding-top: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# --- QUERY PARAMS (AUTO-SAVE) ---
query_params = st.query_params
default_held = int(query_params.get("held", 0))
default_attended = int(query_params.get("att", 0))
default_total = int(query_params.get("total", 0))

# --- HELPER: PDF GENERATOR ---
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Attendance Strategy Report', 0, 1, 'C')
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(held, attended, total, pct, required, bunks, certs):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(200, 10, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='L')
    pdf.ln(10)
    data = [
        ("Metric", "Value"),
        ("Classes Held", str(held)),
        ("Classes Attended", str(attended)),
        ("Current Percentage", f"{pct}%"),
        ("Classes Remaining", str(total - held)),
    ]
    pdf.set_font("Arial", 'B', 12)
    for row in data:
        pdf.cell(95, 10, row[0], 1, 0, 'L', 1)
        pdf.cell(95, 10, row[1], 1, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Action Plan", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    if required > 0:
        pdf.set_text_color(220, 50, 50)
        pdf.cell(200, 10, txt=f"CRITICAL: You MUST attend {required} more classes.", ln=True)
    else:
        pdf.set_text_color(50, 200, 50)
        pdf.cell(200, 10, txt=f"SAFE: You are in the safe zone.", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt=f"Bunking Capacity: {bunks} classes.", ln=True)
    if certs > 0:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Medical Certificate Requirement", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=f"To reach your target immediately, submit certificates for {certs} classes.")
    return pdf.output(dest='S').encode('latin-1')

# --- HELPER: DONUT CHART ---
def create_donut_chart(attended, bunked, remaining):
    colors = ['#0bc8a9', '#ef4444', '#64748b'] 
    labels = ['Attended', 'Missed', 'Future']
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=[attended, bunked, remaining], hole=.75,
        marker=dict(colors=colors, line=dict(color='rgba(255,255,255,0.1)', width=1)),
        textinfo='none', hoverinfo='label+value+percent'
    )])
    current_pct = round((attended / (attended + bunked)) * 100) if (attended+bunked) > 0 else 0
    t_col = "white" if st.session_state.theme == 'Dark' else "#1e293b"
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10), height=220,
        annotations=[dict(text=f"<span style='font-size:28px; font-weight:bold; color:{t_col}'>{current_pct}%</span><br><span style='color:#94a3b8; font-size:12px'>Current</span>", x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    return fig

# --- UI LAYOUT ---
st.markdown("""
<div class="nav-bar">
    <a href="https://mvsrpapers.streamlit.app" target="_blank">📚 Papers</a>
    <a href="#">📊 Tracker Pro</a>
</div>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title-text">BUNK CHECKER</h1>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        class_held = st.number_input("Classes Held", min_value=0, step=1, format="%d", value=default_held)
    with col2:
        class_attended = st.number_input("Classes Attended", min_value=0, step=1, format="%d", value=default_attended)

    college = st.selectbox("Select Year/College", ["MVSREC 2nd Year", "MVSREC 4th Year", "Others"])
    total_classes = 0
    if college == "MVSREC 4th Year":
        branch = st.selectbox("Select Branch", ['CSE', 'DS', 'AIML', 'IoT', 'IT', 'ECE', 'EEE', 'OTHERS'])
        totals_dict = {'CSE': 310, 'DS': 433, 'AIML': 350, 'IoT': 350, 'IT': 350, 'ECE': 350, 'EEE': 350}
        if branch in totals_dict:
            st.info(f"💡 Default total for {branch} is {totals_dict[branch]}.")
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
        st.query_params["held"] = str(class_held)
        st.query_params["att"] = str(class_attended)
        st.query_params["total"] = str(total_classes)
    st.markdown('</div>', unsafe_allow_html=True)

# --- RESULTS LOGIC ---
if st.session_state.calculated:
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
        required_more = max(0, min_required - class_attended)
        # --- FIX: NEGATIVE BUNK NUMBERS ---
        bunks_possible = max(0, remaining_classes - required_more)
        
        target_ratio = min_percent / 100
        consecutive_bunks = 0
        if target_ratio > 0:
            max_held_for_target = class_attended / target_ratio
            consecutive_bunks = math.floor(max_held_for_target - class_held)
            if consecutive_bunks < 0: consecutive_bunks = 0

        def get_badge(pct):
            if pct >= 85: return '<span class="badge badge-scholar">🤓 SCHOLAR ZONE</span>'
            elif pct >= 75: return '<span class="badge badge-safe">🛡️ SAFE ZONE</span>'
            elif pct >= 65: return '<span class="badge badge-risk">💸 CONDONATION RISK</span>'
            else: return '<span class="badge badge-danger">💀 DETAINED ZONE</span>'
        badge_html = get_badge(current_pct)

        # --- MEME LOGIC ---
        meme_url = ""
        meme_caption = ""
        if current_pct >= 85:
            meme_url = "https://media.giphy.com/media/xT0GqssRweIhlz209i/giphy.gif"
            meme_caption = "Like a Boss! 😎"
        elif current_pct >= 75:
            meme_url = "https://media.giphy.com/media/l0HlHJGHe3yAMhdQY/giphy.gif"
            meme_caption = "Safe... for now. 😌"
        elif current_pct >= 65:
            meme_url = "https://media.giphy.com/media/l4FATJpd4LWgeruTK/giphy.gif"
            meme_caption = "Getting intense! 😅"
        else:
            meme_url = "https://media.giphy.com/media/13Cmju3maIjStW/giphy.gif"
            meme_caption = "DANGER! 💀"

        # --- DASHBOARD ---
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.5])
        with c1:
            st.plotly_chart(create_donut_chart(class_attended, missed_classes, remaining_classes), use_container_width=True)
            st.markdown(f"<div style='text-align:center; margin-top:-20px;'><img src='{meme_url}' width='100' style='border-radius:10px;'><br><small>{meme_caption}</small></div>", unsafe_allow_html=True)
        
        with c2:
            st.markdown(f"### Status Report {badge_html}", unsafe_allow_html=True)
            t_col = "white" if st.session_state.theme == 'Dark' else "#1e293b"
            st.markdown(f"<p style='font-size:1.1rem; font-weight:600; color:{t_col}; margin-bottom:10px;'>Exact Percentage: <span style='color:#0bc8a9'>{current_pct}%</span></p>", unsafe_allow_html=True)
            
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

        # --- CERTIFICATE ---
        target_for_current_held = math.ceil(class_held * (min_percent / 100))
        certs_needed = target_for_current_held - class_attended
        current_real_percent = (class_attended / class_held) * 100 if class_held > 0 else 0
        if certs_needed > 0 and current_real_percent < min_percent:
            st.markdown('<div class="cert-container">', unsafe_allow_html=True)
            st.markdown(f"### 📜 Medical/Event Certificate Calculator")
            st.write(f"You are currently at **{round(current_real_percent, 2)}%** (below {min_percent}%).")
            if certs_needed <= missed_classes:
                st.markdown(f"**Solution:** Submit certificates for **{certs_needed}** classes.")
            else:
                st.error(f"Not enough missed classes to cover with certificates.")
            st.markdown('</div>', unsafe_allow_html=True)
        elif consecutive_bunks > 0:
             st.markdown(f"""<div class="glass-container" style="border-left: 5px solid #0bc8a9;"><h4 style="margin:0; color:#fff;">🏖️ Vacation Mode</h4><p style="color:#cbd5e1; margin-top:5px;">You can skip the next <b>{consecutive_bunks} classes in a row</b> before your percentage drops to {min_percent}%.</p></div>""", unsafe_allow_html=True)

        # --- SIMULATOR ---
        st.markdown('<div class="sim-container">', unsafe_allow_html=True)
        st.markdown("### 🔮 Advanced Prediction")
        col_s1, col_s2 = st.columns(2)
        with col_s1: future_bunks = st.slider("Classes you will be ABSENT:", 0, 200, 0)
        with col_s2: medical_certs = st.slider("Classes you keep CERTIFICATE:", 0, 200, 0)

        sim_numerator = class_attended + medical_certs
        sim_denominator = class_held + future_bunks
        if sim_denominator > 0:
            sim_pct = round((sim_numerator / sim_denominator) * 100, 2)
            if sim_pct > 100: sim_pct = 100.0
            
            sim_remaining = remaining_classes - future_bunks 
            if sim_remaining < 0: sim_remaining = 0
            
            sim_missed_chart = sim_denominator - sim_numerator
            if sim_missed_chart < 0: sim_missed_chart = 0
            
            sim_req_total = math.ceil(total_classes * min_percent / 100)
            sim_req_more = max(0, sim_req_total - sim_numerator)
            
            # --- FIX: NEGATIVE SIMULATED BUNK NUMBERS ---
            sim_bunks_possible = max(0, sim_remaining - sim_req_more)
            
            st.markdown('<div class="sim-result-box">', unsafe_allow_html=True)
            c_sim1, c_sim2 = st.columns([1, 1.5])
            with c_sim1:
                 st.plotly_chart(create_donut_chart(sim_numerator, sim_missed_chart, sim_remaining), use_container_width=True, key="sim_chart")
            with c_sim2:
                st.markdown(f"### Status Report {get_badge(sim_pct)}", unsafe_allow_html=True)
                t_col = "white" if st.session_state.theme == 'Dark' else "#1e293b"
                st.markdown(f"<p style='font-size:1.1rem; font-weight:600; color:{t_col}; margin-bottom:10px;'>Predicted Percentage: <span style='color:#0bc8a9'>{sim_pct}%</span></p>", unsafe_allow_html=True)
                if sim_pct >= min_percent:
                    st.success(f"🎉 **SAFE!** With this plan, you hit {min_percent}%!")
                elif sim_req_more > sim_remaining:
                    st.error(f"⚠️ **IMPOSSIBLE** to reach {min_percent}%.")
                else:
                    st.warning(f"You MUST attend **{sim_req_more}** more classes.")
                    
                st.markdown("""<div style="display:flex; gap:10px; margin-top:10px;">""", unsafe_allow_html=True)
                col_sa, col_sb = st.columns(2)
                with col_sa:
                    st.markdown(f"<div class='stat-box'><div class='stat-val'>{sim_req_more}</div><div class='stat-lbl'>Need to Attend</div></div>", unsafe_allow_html=True)
                with col_sb:
                    st.markdown(f"<div class='stat-box'><div class='stat-val'>{sim_bunks_possible}</div><div class='stat-lbl'>Can Bunk</div></div>", unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- DOWNLOADS ---
        pdf_bytes = generate_pdf(class_held, class_attended, total_classes, current_pct, required_more, bunks_possible, certs_needed)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_bytes,
            file_name=f"Attendance_Report_{datetime.datetime.now().strftime('%Y-%m-%d')}.pdf",
            mime="application/pdf",
            type="primary"
        )

# --- FOOTER ---
st.markdown("""
<div class="footer">
    Developed by <span>Uday Kiran</span> | Contact: 245122750006@mvsrec.edu.in
</div>
""", unsafe_allow_html=True)
