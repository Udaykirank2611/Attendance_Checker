# --- DYNAMIC CSS LOADING ---
# Define colors based on theme
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
    
    /* === FIX: BUTTON STYLING === */
    div.stButton > button {{
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
    div.stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5);
        filter: brightness(1.1);
        color: #ffffff !important;
    }}
    div.stButton > button p {{
        color: #ffffff !important; /* Extra safety for Streamlit inner text elements */
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
