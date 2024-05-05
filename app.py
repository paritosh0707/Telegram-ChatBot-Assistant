import streamlit as st
import os

st.title("TelBot Starter")

start_button = st.button("start")

if start_button:
    os.system("python bot.py")
    st.write("Service Started")
