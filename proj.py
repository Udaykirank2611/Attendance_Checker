import streamlit as st
st.title("Attendence")
classs = st.number_input("Eppativarak enni classes ainai")
atten = st.number_input("Enni attend ainav")
total = st.number_input("Motham enni classes aitai anukuntunav (350 for csd)")
min_75 = int(total*0.75)
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

