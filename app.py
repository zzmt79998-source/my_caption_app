import sys
# Recursion Error မတက်အောင် Limit ကို တိုးပေးထားခြင်း
sys.setrecursionlimit(5000)

import streamlit as st
import whisper
# moviepy ကို သေချာတင်နိုင်အောင် import လုပ်ပုံ
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

st.title("Burmese Auto-Caption Generator")

uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])

if uploaded_file is not None:
    st.video(uploaded_file)
    st.write("Processing... please wait.")
    
    # ဤနေရာတွင် အစ်ကို့ရဲ့ Whisper ကုဒ်များကို ဆက်လက်ရေးသားနိုင်ပါသည်။
    # st.success("Video processed successfully!")
