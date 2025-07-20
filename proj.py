import streamlit as st
import math

st.set_page_config(page_title="Attendance Tracker", layout="centered")

# ... [Your global CSS here, as previous answer] ...

st.markdown("""
<style>
.info-container {
    display: flex;
    align-items: center;
    gap: 0.4em;
    margin-bottom: 4px;
}
.info-icon {
    display: inline-block;
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
@media (max-width:700px){
    .info-icon .tooltip-text {
        left:unset;
        right:120%;
    }
}
</style>
""", unsafe_allow_html=True)

# ... open <div class="main-card"> ...

# --- In your form section, for total_classes ---
if st.session_state.get("college", "MVSREC 2nd Year") == "MVSREC 3rd Year":
    branch = st.selectbox("🧪 Select Your Branch", ['CSE', 'DS', 'AIML', 'IoT', 'IT', 'ECE', 'EEE', 'OTHERS'])
    st.session_state["college"] = "MVSREC 3rd Year"  # so later check works

    total_label = (
        "<div class='info-container'>"
        "<span>Enter Total Number of Classes</span>"
        "<span class='info-icon'>"
            "ℹ"
            "<span class='tooltip-text'>"
            "To calculate total number of classes, check how many classes are there per week and multiply by 15 or 16."
            "</span>"
        "</span>"
        "</div>"
    )

    if branch in ['CSE', 'DS', 'AIML', 'IoT', 'IT', 'ECE', 'EEE']:
        total_classes_dict = {
            'CSE': 350,
            'DS': 324,
            'AIML': 330,
            'IoT': 340,
            'IT': 360,
            'ECE': 350,
            'EEE': 320
        }
        total_classes = total_classes_dict[branch]
        st.markdown(total_label, unsafe_allow_html=True)
        st.number_input("Total Number of Classes", value=total_classes, disabled=True, key="tot_class_input")
    else:
        st.markdown(total_label, unsafe_allow_html=True)
        total_classes = st.number_input("", min_value=0, step=1, format="%d", key="tot_class_input")
else:
    st.session_state["college"] = "OTHER"
    total_label = (
        "<div class='info-container'>"
        "<span>Enter Total Number of Classes</span>"
        "<span class='info-icon'>"
            "ℹ"
            "<span class='tooltip-text'>"
            "To calculate total number of classes, check how many classes are there per week and multiply by 15 or 16."
            "</span>"
        "</span>"
        "</div>"
    )
    st.markdown(total_label, unsafe_allow_html=True)
    total_classes = st.number_input("", min_value=0, step=1, format="%d", key="tot_class_input")

min_percent_str = st.selectbox("🎯 Required Attendance Percentage", ['65%', '70%', '75%', '80%'])
min_percent = int(min_percent_str.strip('%'))

st.markdown("---")
st.subheader("ℹ️ Notes")
st.info("These numbers are approximate and may vary by 1–2% depending on extra or cancelled classes.\nThe portal will be updated upon schedule changes.")

# --- Calculation ---
min_required = math.ceil(total_classes * min_percent / 100)
remaining_classes = total_classes - class_held
required_more = min_required - class_attended
bunks_possible = remaining_classes - required_more

# --- Button and Output ---
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

        # --- Detailed Breakdown ---
        st.markdown("---")
        st.subheader("📊 Detailed Breakdown")
        st.write(f"• Total Classes Scheduled: **{total_classes}**")
        st.write(f"• Classes Held: **{class_held}**")
        st.write(f"• Classes Attended: **{class_attended}**")
        st.write(f"• Required for {min_percent}%: **{min_required}**")
        st.write(f"• Remaining Classes: **{remaining_classes}**")

st.markdown('</div>', unsafe_allow_html=True) # Close main-card

# --- FOOTER (Matches other page) ---
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
