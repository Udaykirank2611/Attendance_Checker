import streamlit as st
st.title("Attendence")
classs = st.number_input("Eppativarak enni classes ainai")
atten = st.number_input("Enni attend ainav")
total = st.number_input("Motham enni classes aitai anukuntunav (350 for csd)")
min_75 = round(total*0.75)
remaining = total-classs
req = min_75-atten
bunks = remaining-req
if(st.button('Check attendence')):
    if atten >= min_75:
        st.success("IGA nuv clg ranakarle")
    elif req>remaining:
        st.error("nuv roju vochina attendence 75 kadu")
    else:
        bunks = remaining-req
        st.text("nuv inka {} classes bunk kotochu".format(bunks))
        st.warning("daily clg ra iga")
    st.header("Details")
    st.text("total number of classes : {}".format(total))
    st.text("total number of classes took place : {}".format(classs))
    st.text("total number of classes attended : {}".format(atten))
    st.text("min number of classes for 75%".format(min_75))
    st.text("number of classes left : {}".format(remaining))                                                           
