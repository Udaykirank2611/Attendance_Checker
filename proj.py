import streamlit as st
import math

# --- Page Configuration ---
st.set_page_config(page_title="Attendance Tracker", layout="centered")

# --- Title ---
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📊 Attendance Tracker</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Input Section ---
st.subheader("📥 Enter Your Details")
class_held = st.number_input("📘 Number of Classes Held", min_value=0, step=1, format="%d")
class_attended = st.number_input("🧑‍🏫 Number of Classes Attended", min_value=0, step=1, format="%d")

college = st.selectbox("🏫 Select Your College", ["MVSREC 2nd Year", "MVSREC 3rd Year", "Others"])

# Branch and total classes logic
if college == "MVSREC 3rd Year":
    branch = st.selectbox("🧪 Select Your Branch", ['CSE', 'DS', 'AIML', 'IoT', 'IT', 'ECE', 'EEE', 'OTHERS'])

    total_classes = {
        'CSE': 350,
        'DS': 324,
        'AIML': 330,
        'IoT': 340,
        'IT': 360,
        'ECE': 350,
        'EEE': 320
    }.get(branch, st.number_input("Enter Total Number of Classes", min_value=0, step=1, format="%d"))
else:
    total_classes = st.number_input("Enter Total Number of Classes", min_value=0, step=1, format="%d")

# Minimum percentage requirement
min_percent_str = st.selectbox("🎯 Required Attendance Percentage", ['65%', '70%', '75%', '80%'])
min_percent = int(min_percent_str.strip('%'))

# --- Notes ---
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

# --- Footer ---
footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #262730;
    color: #f1f1f1;
    text-align: center;
    padding: 10px;
    font-size: 14px;
}
</style>
<div class="footer">
    Developed by <b>Uday Kiran</b> | 📧 245122750006@mvsrec.edu.in
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
