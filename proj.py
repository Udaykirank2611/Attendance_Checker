import streamlit as st
import math

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Attendance Tracker", page_icon="📊", layout="centered")

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
    
    .subtitle-text {
        text-align: center;
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 2rem;
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
        margin-bottom: 30px;
        backdrop-filter: blur(12px);
    }

    /* Input Fields Styling */
    .stSelectbox label, .stNumberInput label {
        color: #e2e8f0 !important;
        font-weight: 500;
        font-size: 0.95rem;
    }
    .stSelectbox > div > div, .stNumberInput > div > div > input {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        color: white !important;
        border-radius: 12px !important;
    }
    
    /* Button Styling */
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

    /* Custom Alert Styling to match Dark Theme */
    .stAlert {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #e2e8f0 !important;
        border-radius: 12px !important;
    }

    /* Result Cards */
    .result-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 20px;
        margin-top: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stat-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding-bottom: 8px;
    }
    .stat-label { color: #94a3b8; }
    .stat-val { color: #fff; font-weight: 600; }

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
    .footer span { color: #94a3b8; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# --- UI LAYOUT ---

# 1. Navigation
st.markdown("""
<div class="nav-bar">
    <a href="https://mvsrpapers.streamlit.app" target="_blank">📚 MVSREC Papers</a>
    <a href="#">📊 BunkChecker</a>
</div>
""", unsafe_allow_html=True)

# 2. Title
st.markdown('<h1 class="title-text">ATTENDANCE TRACKER</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Calculate your bunks safely without falling below the limit.</p>', unsafe_allow_html=True)

# 3. Main Logic Container
with st.container():
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    # Input Row 1
    col1, col2 = st.columns(2)
    with col1:
        class_held = st.number_input("Classes Held", min_value=0, step=1, format="%d", help="Total classes conducted by the college so far.")
    with col2:
        class_attended = st.number_input("Classes Attended", min_value=0, step=1, format="%d", help="How many you actually sat in.")

    # College Selection
    college = st.selectbox("Select Your College/Year", ["MVSREC 2nd Year", "MVSREC 3rd Year", "Others"])

    # Total Classes Logic
    total_classes = 0
    
    if college == "MVSREC 3rd Year":
        branch = st.selectbox("Select Branch", ['CSE', 'DS', 'AIML', 'IoT', 'IT', 'ECE', 'EEE', 'OTHERS'])
        
        # Default totals map
        totals_dict = {
            'CSE': 350, 'DS': 324, 'AIML': 330, 'IoT': 340,
            'IT': 360, 'ECE': 350, 'EEE': 320
        }
        
        if branch in totals_dict:
            default_total = totals_dict[branch]
            # Use columns to show the default and allow override
            st.info(f"💡 Default total for {branch} is usually **{default_total}**.")
            total_classes = st.number_input(
                "Total Classes (Estimate)", 
                value=default_total, 
                step=1, 
                help="To calculate manually: Classes per week × 16 weeks."
            )
        else:
            total_classes = st.number_input("Total Classes (Estimate)", min_value=0, step=1, help="To calculate manually: Classes per week × 16 weeks.")
    else:
        total_classes = st.number_input("Total Classes (Estimate)", min_value=0, step=1, help="To calculate manually: Classes per week × 16 weeks.")

    # Percentage Requirement
    min_percent_str = st.selectbox("Required Percentage", ['65%', '70%', '75%', '80%'], index=2)
    min_percent = int(min_percent_str.strip('%'))

    # Calculate Button
    check_btn = st.button("Calculate Bunks")

    st.markdown('</div>', unsafe_allow_html=True) # End Input Container

# --- RESULTS DISPLAY ---

if check_btn:
    # Calculations
    min_required = math.ceil(total_classes * min_percent / 100)
    remaining_classes = total_classes - class_held
    
    # Logic Checks
    if class_attended > class_held:
        st.error("❌ Classes attended cannot be higher than classes held!")
    elif total_classes == 0:
        st.error("❌ Total classes cannot be zero.")
    else:
        required_more = min_required - class_attended
        bunks_possible = remaining_classes - required_more
        current_percentage = round((class_attended / class_held) * 100, 2) if class_held > 0 else 0
        max_possible_percent = round(((class_attended + remaining_classes) / total_classes) * 100, 2)

        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.subheader("📋 Result Summary")
        
        # Display Logic
        if class_attended >= min_required:
            st.success(f"🎉 **Safe Zone!** You have already crossed {min_percent}% attendance.")
            st.caption(f"You can bunk all remaining {remaining_classes} classes if you want.")
        
        elif required_more > remaining_classes:
            st.error(f"⚠️ **Danger!** You cannot reach {min_percent}% even if you attend every single class.")
            st.write(f"Maximum possible: **{max_possible_percent}%**")
        
        else:
            # Main Result
            st.info(f"You can safely bunk **{bunks_possible}** more classes.")
            
            if bunks_possible < 10:
                st.warning(f"⚠️ **Tight Schedule:** You must attend **{required_more}** out of the remaining **{remaining_classes}** classes.")
            else:
                st.success(f"👍 **On Track:** You only need to attend **{required_more}** out of the remaining **{remaining_classes}** classes.")

        # Detailed Stats Table
        st.markdown("""
        <div class="result-card">
            <h4 style="color:#fff; margin-bottom:15px; font-size:1.1rem;">📊 Detailed Breakdown</h4>
        """, unsafe_allow_html=True)
        
        stats = [
            ("Current Percentage", f"{current_percentage}%"),
            ("Total Classes Scheduled", total_classes),
            ("Classes Held So Far", class_held),
            ("Classes Attended", class_attended),
            ("Classes Remaining", remaining_classes),
            (f"Required for {min_percent}%", min_required)
        ]
        
        for label, value in stats:
            st.markdown(f"""
            <div class="stat-row">
                <span class="stat-label">{label}</span>
                <span class="stat-val">{value}</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True) # End Result Container

# --- FOOTER ---
st.markdown("""
<div class="footer">
    Developed by <span>Uday Kiran</span> | Contact: 245122750006@mvsrec.edu.in
</div>
""", unsafe_allow_html=True)
