import streamlit as st
import math

st.set_page_config(page_title="Attendance Tracker", layout="centered")

# ===================== PAGE STYLES =======================
st.markdown("""
<style>
body, .stApp {
    background: linear-gradient(135deg, #6d83f2 0%, #0bc8a9 100%) !important;
    min-height: 100vh;
}

/* ==== GLASS MENU BAR ==== */
.top-menu {
    background: rgba(0,24,48, 0.75);
    padding: 18px 5px 13px 5px;
    border-radius: 0 0 26px 26px;
    box-shadow: 0 6px 18px rgba(31,74,138,0.08);
    margin-bottom: 28px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.top-menu a {
    margin: 0 15px;
    text-decoration: none;
    color: #fff;
    font-weight: 600;
    letter-spacing: 1px;
    transition: all .22s;
    padding: 7px 18px;
    border-radius: 20px;
}

.top-menu a:hover {
    background: #0bc8a9;
    color: #2b2b2b;
    box-shadow: 0 2px 12px rgba(17,228,215,0.18);
    text-decoration: none;
    transform: translateY(-2px) scale(1.06);
}

/* ==== Main glass card ==== */
.main-card {
    max-width: 670px;
    margin: 32px auto 32px auto;
    background: rgba(255,255,255,0.10);
    box-shadow: 0 8px 32px 0 rgba(21,27,80,.15);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.3);
    padding: 32px 32px 24px 32px;
    font-family: 'Segoe UI', 'Poppins', Arial, sans-serif;
}

/* Title */
.cool-title {
    font-size: 2.44rem;
    color: #fff;
    text-align: center;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 8px;
    text-shadow: 0 2px 18px #4e6ce470;
    margin-top: 10px;
}

.stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
    color: #fff !important;
    margin-top: 20px;
    margin-bottom: 14px;
    text-shadow: 0 2px 10px #3b68aa30;
}

/* Inputs/glass */
.stNumberInput > div, .stSelectbox > div, .stTextInput > div {
    background: rgba(255,255,255,0.11);
    border-radius: 14px !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 12px 0 #5786e9cc, 0 1.5px 8px 0 #0bc8a966;
    font-family: 'Segoe UI', 'Poppins', Arial, sans-serif !important;
    margin-bottom: 9px;
    color: #f6efff !important;
}

label, .css-1cpxqw2, .css-1jy7b63 {
    font-size: 1.09rem!important;
    color: #ecebff !important;
    margin-bottom: 4px;
    font-weight: 600;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(90deg,#5dd6ff 0,#7b6ffb 100%) !important;
    color: #fff !important;
    border: none;
    font-size: 1.19rem;
    border-radius: 15px;
    font-weight: 700;
    margin-top: 12px;
    padding: .44rem 1.7rem;
    box-shadow: 0 2px 10px #869bff70;
    letter-spacing: 1px;
    transition: all .16s;
}
.stButton > button:hover {
    background: linear-gradient(90deg,#0bc8a9 0,#7b6ffb 90%);
    box-shadow: 0 4px 24px #869bffad;
}

/* Alerts styling */
.stAlert {
    border-radius: 14px !important;
    backdrop-filter: blur(8px);
    color: #fff !important;
}
.stAlert-success {
    background-color: rgba(40,230,180,0.25)!important;
}
.stAlert-error {
    background-color: rgba(228,54,158,0.23)!important;
}
.stAlert-info {
    background-color: rgba(92,141,255,0.17)!important;
}
.stAlert-warning {
    background-color: rgba(255,226,93,0.27)!important;
    color: #292700 !important;
}

/* Info icon and tooltip */
.info-container {
    display: flex;
    align-items: center;
    gap: 0.4em;
    margin-bottom: 4px;
}
.info-icon {
    position: relative;
    width: 20px;
    height: 20px;
    cursor: pointer;
    color: #0bc8a9;
    background: rgba(255,255,255,0.21);
    border-radius: 50%;
    font-weight: bold;
    font-size: 15px;
    text-align: center;
    line-height: 20px;
    transition: box-shadow .18s;
    box-shadow: 0 2px 6px #1281d044;
}

.info-icon:hover {
    box-shadow: 0 2px 16px #12ffd077;
    background: #e4fffb;
    color: #299f8c;
}

.info-icon .tooltip-text {
    visibility: hidden;
    width: 270px;
    background: #2f415aee;
    color: #fff;
    text-align: left;
    border-radius: 8px;
    padding: 9px 13px;
    position: absolute;
    z-index: 100;
    left: 120%;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0.96rem;
    box-shadow: 0 3px 18px #16354e90;
    opacity: 0;
    transition: opacity 0.25s;
}

.info-icon:hover .tooltip-text {
    visibility: visible;
    opacity: 1;
}

@media (max-width: 700px) {
    .info-icon .tooltip-text {
        left: unset;
        right: 120%;
    }
}

@media (max-width: 1000px) {
    .main-card { padding: 13px 6px 2px 6px; }
    .cool-title { font-size: 1.6rem; }
}
</style>
""", unsafe_allow_html=True)

# ===================== TOP MENU BAR ==========================
st.markdown("""
<div class="top-menu">
    <a href="https://mvsrpapers.streamlit.app" target="_blank">MVSREC Papers</a>
</div>
""", unsafe_allow_html=True)

# ================= MAIN CARD START ================================
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown("<div class='cool-title'>📊 Attendance Tracker</div>", unsafe_allow_html=True)
st.markdown("---")

st.subheader("📥 Enter Your Details")

class_held = st.number_input("📘 Number of Classes Held", min_value=0, step=1, format="%d")
class_attended = st.number_input("🧑‍🏫 Number of Classes Attended", min_value=0, step=1, format="%d")

college = st.selectbox("🏫 Select Your College", ["MVSREC 2nd Year", "MVSREC 3rd Year", "Others"])

# ---------- TOTAL NUMBER OF CLASSES with INFO ICON -------------
def render_total_classes_input(college_choice):
    total_label_html = """
    <div class='info-container'>
        <span>Enter Total Number of Classes</span>
        <span class='info-icon'>
            ℹ
            <span class='tooltip-text'>
                To calculate total number of classes, check how many classes are there per week and multiply by 15 or 16.
            </span>
        </span>
    </div>
    """
    st.markdown(total_label_html, unsafe_allow_html=True)

    if college_choice == "MVSREC 3rd Year":
        branch = st.selectbox("🧪 Select Your Branch", ['CSE', 'DS', 'AIML', 'IoT', 'IT', 'ECE', 'EEE', 'OTHERS'])
        # Default totals for branches
        totals_dict = {
            'CSE': 350,
            'DS': 324,
            'AIML': 330,
            'IoT': 340,
            'IT': 360,
            'ECE': 350,
            'EEE': 320
        }

        if branch in totals_dict:
            default_total = totals_dict[branch]
            st.number_input("Total Number of Classes (Default)", value=default_total, disabled=True, key="total_classes_disabled")
            total_classes = st.number_input("Or enter Total Number of Classes (override)", min_value=0, step=1, format="%d", key="total_classes_override")
            if total_classes == 0:
                total_classes = default_total
        else:
            total_classes = st.number_input("", min_value=0, step=1, format="%d", key="total_classes_manual")
    else:
        total_classes = st.number_input("", min_value=0, step=1, format="%d", key="total_classes_other")

    return total_classes

total_classes = render_total_classes_input(college)

min_percent_str = st.selectbox("🎯 Required Attendance Percentage", ['65%', '70%', '75%', '80%'])
min_percent = int(min_percent_str.strip('%'))

st.markdown("---")
st.subheader("ℹ️ Notes")
st.info("These numbers are approximate and may vary by 1–2% depending on extra or cancelled classes.\nThe portal will be updated upon schedule changes.")

min_required = math.ceil(total_classes * min_percent / 100)
remaining_classes = total_classes - class_held
required_more = min_required - class_attended
bunks_possible = remaining_classes - required_more

if st.button("✅ Check Attendance"):
    st.markdown("---")
    st.subheader("📋 Result Summary")

    if class_attended > class_held:
        st.error("❌ Classes attended cannot be more than classes held.")
    elif total_classes == 0:
        st.error("❌ Total classes cannot be 0.")
    else:
        max_possible_percent = round(((class_attended + remaining_classes) / total_classes) * 100, 2)

        if class_attended >= min_required:
            st.success(f"🎉 You've already reached the required {min_percent}% attendance.")
            st.info(f"You can skip all remaining classes and still stay above {min_percent}%.")
        elif required_more > remaining_classes:
            st.error(f"⚠️ You cannot reach {min_percent}% even if you attend every remaining class.")
            st.error(f"Max possible attendance: {max_possible_percent}%")
        else:
            st.info(f"You can safely bunk up to **{bunks_possible}** classes.")
            st.info(f"You must attend **{required_more}** more classes out of **{remaining_classes}** to maintain {min_percent}%.")
            if bunks_possible < 15:
                st.warning(f"⚠️ Limited room to skip. Max attendance if you attend all: {max_possible_percent}%")
            else:
                st.success(f"👍 You're on track! Max possible attendance: {max_possible_percent}%")

        st.markdown("---")
        st.subheader("📊 Detailed Breakdown")
        st.write(f"• Total Classes Scheduled: **{total_classes}**")
        st.write(f"• Classes Held: **{class_held}**")
        st.write(f"• Classes Attended: **{class_attended}**")
        st.write(f"• Required for {min_percent}%: **{min_required}**")
        st.write(f"• Remaining Classes: **{remaining_classes}**")

st.markdown('</div>', unsafe_allow_html=True)

# ============= FOOTER ================
footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100vw;
    background: rgba(25,30,43,0.28);
    color: #fff;
    text-align: center;
    padding: 10px 0;
    font-size: 1.02rem;
    letter-spacing: 2px;
    z-index: 99;
    font-weight: 400;
    user-select: none;
    box-shadow: 0 -2px 8px #1b2c556e;
    backdrop-filter: blur(6px);
}
@media (max-width: 1000px) {
    .footer { font-size: .95rem; }
}
</style>
<div class="footer">
    Developed by <b>Uday Kiran</b> | 📧 245122750006@mvsrec.edu.in
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
