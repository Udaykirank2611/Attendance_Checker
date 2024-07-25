import streamlit as st
import math
st.title("Attendence")
classs = st.number_input("Number of classes held",value=0, step=1, format="%d")
atten = st.number_input("Number of classes attended", value=0, step=1, format="%d")
total = st.number_input("Total Number of classes (371 for csd)", value=0, step=1, format="%d")
min_p = st.selectbox("Attendance percentage: ",
                     ['65%', '70%', '75%','80%'])
percent = int(min_p[:2])
min_75 = math.ceil(total*0.01*percent)
remaining = total-classs
req = min_75-atten
bunks = remaining-req
if(st.button('Check attendence')):
    if atten>classs:
        st.error("classes held should be more than the classes attended")
    else:
        if atten >= min_75:
         st.success("You have reached the attendence criteria")
         st.info("even if you dont come to college from now your attendence will be above {}%".format(percent))
        elif req>remaining:
            st.error("You cant reach {}% even if you attend every class".format(percent))
        else:
            bunks = remaining-req
            st.text("you can bunk {} classes.".format(bunks))
            if(bunks<15):
                st.warning("You have to come to college regularly")
            else:
                st.success("You can take a few days off")
        st.header("Details")
        st.text("total number of classes : {}".format(total))
        st.text("total number of classes took place : {}".format(classs))
        st.text("total number of classes attended : {}".format(atten))
        st.text("min number of classes for {}% : {}".format(percent,min_75))
        st.text("number of classes left : {}".format(remaining))      
footer = """
<style>
.footer {
    position: relative;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: var(--footer-background-color);
    color: var(--footer-text-color);
    text-align: center;
    padding: 10px;
    margin-top: 20px;
}
@media (prefers-color-scheme: dark) {
    :root {
        --footer-background-color: #333;
        --footer-text-color: #f1f1f1;
    }
}
@media (prefers-color-scheme: light) {
    :root {
        --footer-background-color: #f1f1f1;
        --footer-text-color: #333;
    }
}
</style>
<div class="footer">
    <p>Developed by Uday Kiran</p>
    <p>Contact: 245122750006@mvsrec.edu.in</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
