import streamlit as st

st.write("Hello Streamlit..")
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)
st.write(add_selectbox)