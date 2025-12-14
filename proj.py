import streamlit as st
import math
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Attendance Tracker Pro", page_icon="📊", layout="centered")

# --- SESSION STATE INITIALIZATION ---
# This ensures the results stay visible when you use the 'What If' slider
if 'calculated' not in st.session_state:
    st.session_state.calculated = False

# --- CUSTOM CSS STYLING ---
st.markdown("""
<style>
    /* Global Reset & Background */
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
    
    /* Top Navigation Bar */
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

    /* Main Glass Card */
    .glass-container {
        background: rgba(30, 41, 59, 0.4);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        padding: 32px;
        margin-bottom: 20px;
        backdrop-filter: blur(12px);
    }

    /* Simulator Card (Darker) */
    .sim-container {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        padding: 24px;
        margin-top: 20px;
    }

    /* Input Fields & Buttons */
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

    /* Stats Row */
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
    """Creates a glassmorphism donut chart using Plotly"""
    colors = ['#0bc8a9', '#ef4444', '#64748b'] # Green (Attended), Red (Bunked), Grey (Remaining)
    labels = ['Attended', 'Missed', 'Future']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=[attended, bunked, remaining],
        hole=.75,
        marker=dict(colors=colors, line=dict(color='rgba(255,255,255,0.1)', width=1)),
        textinfo='none', # Hide labels on chart to keep it clean
        hoverinfo='label+value+percent'
    )])

    # Center Text
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

# Navigation
st.markdown("""
<div class="nav-bar">
    <a href="https://mvsrpapers.streamlit.app" target="_blank">📚 Papers</a>
    <a href="#">📊 Tracker Pro</a>
</div>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title-text">ATTENDANCE PRO</h1>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    # Inputs
    col1, col2 = st.columns(2)
    with col1:
        class_held = st.number_input("Classes Held", min_value=0, step=1, format="%d")
    with col2:
        class_attended = st.number_input("Classes Attended", min_value=0, step=1, format="%d")

    # Advanced Total Calculation
    college = st.selectbox("Select Year/College", ["MVSREC 2nd Year", "MVSREC 3rd Year", "Others"])
    
    total_classes = 0
    if college == "MVSREC 3rd Year":
        branch = st.selectbox("Select Branch", ['CSE', 'DS', 'AIML', 'IoT', 'IT', 'ECE', 'EEE', 'OTHERS'])
        totals_dict = {'CSE': 350, 'DS': 324, 'AIML': 330, 'IoT': 340, 'IT': 360, 'ECE': 350, 'EEE': 320}
        
        if branch in totals_dict:
            st.info(f"💡 Default total for {branch} is {totals_dict[branch]}.")
            total_classes = st.number_input("Total Classes (Est.)", value=totals_dict[branch], step=1)
        else:
            total_classes = st.number_input("Total Classes (Est.)", min_value=0, step=1)
    else:
        total_classes = st.number_input("Total Classes (Est.)", min_value=0, step=1)

    min_percent_str = st.selectbox("Target Percentage", ['65%', '70%', '75%', '80%'], index=2)
    min_percent = int(min_percent_str.strip('%'))

    if st.button("Analyze Attendance"):
        st.session_state.calculated = True

    st.markdown('</div>', unsafe_allow_html=True)

# --- RESULTS LOGIC ---

if st.session_state.calculated:
    # Basic Calcs
    min_required = math.ceil(total_classes * min_percent / 100)
    remaining_classes = total_classes - class_held
    missed_classes = class_held - class_attended
    if missed_classes < 0: missed_classes = 0 # Safety check

    # Error Handling
    if class_attended > class_held:
        st.error("❌ Attended cannot be > Held")
    elif total_classes == 0:
        st.error("❌ Total classes cannot be 0")
    else:
        # --- FEATURE 1: DASHBOARD & CHART ---
        required_more = min_required - class_attended
        if required_more < 0: required_more = 0
        bunks_possible = remaining_classes - required_more
        
        # Max Consecutive Bunks (Vacation Mode) Logic
        # Solve: Attended / (Held + x) = Target%
        # x = (Attended / Target%) - Held
        target_ratio = min_percent / 100
        if target_ratio > 0:
            max_held_for_target = class_attended / target_ratio
            consecutive_bunks = math.floor(max_held_for_target - class_held)
            if consecutive_bunks < 0: consecutive_bunks = 0
        else:
            consecutive_bunks = 999

        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        
        # Layout: Chart on Left, Stats on Right
        c1, c2 = st.columns([1, 1.5])
        
        with c1:
            st.plotly_chart(create_donut_chart(class_attended, missed_classes, remaining_classes), use_container_width=True)
        
        with c2:
            st.markdown("### Status Report")
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

            # Quick Stats Row
            st.markdown("""<div style="display:flex; gap:10px; margin-top:10px;">""", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"<div class='stat-box'><div class='stat-val'>{required_more}</div><div class='stat-lbl'>Need to Attend</div></div>", unsafe_allow_html=True)
            with col_b:
                st.markdown(f"<div class='stat-box'><div class='stat-val'>{bunks_possible}</div><div class='stat-lbl'>Can Bunk</div></div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

        # --- FEATURE 3: SAFE BUNK (VACATION MODE) ---
        if consecutive_bunks > 0 and class_attended >= min_required == False:
             st.markdown(f"""
             <div class="glass-container" style="border-left: 5px solid #0bc8a9;">
                <h4 style="margin:0; color:#fff;">🏖️ Vacation Mode</h4>
                <p style="color:#cbd5e1; margin-top:5px;">
                    Based on your current attendance, you can skip the next <b>{consecutive_bunks} classes in a row</b> 
                    before your percentage drops exactly to {min_percent}%.
                </p>
             </div>
             """, unsafe_allow_html=True)


        # --- FEATURE 2: WHAT-IF SIMULATOR ---
        st.markdown('<div class="sim-container">', unsafe_allow_html=True)
        st.markdown("### 🔮 What If Simulator")
        st.caption("Slide to see what happens if you skip the next few classes.")
        
        # Slider for next X classes
        # Limit slider to remaining classes or a reasonable number (e.g., 20)
        max_sim = min(20, remaining_classes) if remaining_classes > 0 else 10
        
        if max_sim > 0:
            sim_bunks = st.slider("Skip next X classes:", 0, max_sim, 0)
            
            # Simulated Calculation
            sim_held = class_held + sim_bunks
            sim_attended = class_attended # Attended stays same, Held increases
            sim_pct = round((sim_attended / sim_held) * 100, 2)
            
            # Dynamic Feedback
            if sim_pct >= min_percent:
                st.markdown(f"<h3 style='color:#0bc8a9; text-align:center;'>Result: {sim_pct}% (Safe ✅)</h3>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h3 style='color:#ef4444; text-align:center;'>Result: {sim_pct}% (Danger ⚠️)</h3>", unsafe_allow_html=True)
        else:
            st.write("No remaining classes to simulate!")

        st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    Developed by <span>Uday Kiran</span> | Contact: 245122750006@mvsrec.edu.in
</div>
""", unsafe_allow_html=True)
