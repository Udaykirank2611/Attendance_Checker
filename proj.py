import streamlit as st
import math
st.title("Attendence")
classs = st.number_input("Number of classes held",value=0, step=1, format="%d")
atten = st.number_input("Number of classes attended", value=0, step=1, format="%d")
clg = st.selectbox("Enter your college details: ",
                   ["MVSREC 2nd Year","Others"])
if clg == "MVSREC 3rd Year":

    branch = st.selectbox("Select Your branch: ",
                     ['CSE', 'DS','AIML','IoT','IT','ECE','EEE','OTHERS'])
#total = st.number_input("Total Number of classes (330 for cse,373 for cse-ds,360 for ece)", value=0, step=1, format="%d")
    if branch=='CSE':
        total = 350
    elif branch=="DS":
        total = 324
    elif branch == "IT":
        total = 360
    elif branch == "ECE":
        total = 350
    elif branch=="EEE":
        total = 320
    elif branch == "AIML":
        total = 330
    elif branch == "IoT":
        total = 340
    else:
        total = st.number_input("Total Number of classes", value=0, step=1, format="%d")
else:
    total = st.number_input("Total Number of classes", value=0, step=1, format="%d")
min_p = st.selectbox("Required attendance percentage: ",
                     ['65%', '70%', '75%','80%'])
st.subheader("NOTE : ")
st.text("These numbers are approximate and not exact.\nThey may vary by 1 or 2 percent depending on additional classes taken.\nWhenever there is a holiday confirmation or class cancellation, the website will be updated")
percent = int(min_p[:2])
min_75 = math.ceil(total*0.01*percent)
remaining = total-classs
req = min_75-atten
bunks = remaining-req
if(st.button('Check attendence')):
    if atten>classs:
        st.error("classes held should be more than the classes attended")
    elif total == 0:
        st.error("total classes cannot be 0.")
    else:
        max_percen = ((atten+remaining)/total)*100
        max_percen = round(max_percen,2)
        if atten >= min_75:
         st.success("You have reached the attendence criteria")
         st.info("even if you dont come to college from now your attendence will be above {}%".format(percent))
        elif req>remaining:
            st.error("You cant reach {}% even if you attend every class".format(percent))
            st.error("Maximum percentage you can reach if you attend every class is {}%".format(max_percen))
        else:
            bunks = remaining-req
            st.info("you can bunk {} classes.".format(bunks))
            if(bunks<15):
                st.info("you have to attend {} more classes out of remaining {} classes to maintain {}%.".format(min_75-atten,remaining,percent))
                st.warning("Maximum percentage you can reach if you attend every class is {}%".format(max_percen))
                st.warning("You have to come to college regularly")
            else:
                st.info("you have to attend {} more classes out of remaining {} classes to maintain {}%.".format(min_75-atten,remaining,percent))
                st.success("Maximum percentage you can reach if you attend every class is {}%".format(max_percen))
                st.success("You can take a few days off")
        st.header("Details")
        st.text("total number of classes : {}".format(total))
        st.text("number of classes held : {}".format(classs))
        st.text("number of classes attended : {}".format(atten))
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
