import sys
sys.setrecursionlimit(5000)

import streamlit as st
from moviepy.editor import VideoFileClip

st.title("Test App: Moviepy check")

uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])

if uploaded_file is not None:
    st.video(uploaded_file)
    st.write("Moviepy import success!")
