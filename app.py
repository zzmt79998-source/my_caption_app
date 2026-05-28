import sys
# အရေးကြီး: Recursion limit ကို တိုးပေးထားခြင်းက Error မတက်အောင် ကာကွယ်ပေးပါတယ်
sys.setrecursionlimit(5000)

import streamlit as st
import whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

st.title("Burmese Auto-Caption Generator")

uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])

if uploaded_file is not None:
    st.video(uploaded_file)
    st.write("Processing... please wait.")
    
    # ဤနေရာတွင် အစ်ကို့ရဲ့ Whisper
