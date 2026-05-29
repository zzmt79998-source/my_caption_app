import sys
sys.setrecursionlimit(5000)

import streamlit as st
import whisper

# ဒီနေရာမှာ import လုပ်ပုံကို နည်းနည်းပြင်ပေးပါ
try:
    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
except ImportError:
    st.error("Moviepy မရှိသေးပါ၊ ကျေးဇူးပြု၍ requirements.txt ကို စစ်ဆေးပါ")

st.title("Burmese Auto-Caption Generator")

uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])
if uploaded_file is not None:
    st.video(uploaded_file)
    st.write("Processing...")
