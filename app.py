import sys
sys.setrecursionlimit(2000)

import streamlit as st
import whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import textwrap

st.title("Burmese Auto-Caption Generator")

# ကျန်တဲ့ ကုဒ်တွေရှိရင် ဒီအောက်မှာ ဆက်ထည့်ပါ
# ဥပမာ -
uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])

if uploaded_file is not None:
    st.video(uploaded_file)
    st.write("Processing...")
    # သင်လုပ်မယ့် လုပ်ဆောင်ချက်တွေကို ဒီအောက်မှာ ဆက်ရေးပါ
