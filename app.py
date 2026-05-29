import sys
sys.setrecursionlimit(5000)

import streamlit as st

# MoviePy ကို ဒီလိုပုံစံနဲ့ အရင်စမ်းပါ
try:
    from moviepy.editor import VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

st.title("Burmese Auto-Caption Generator")

if MOVIEPY_AVAILABLE:
    st.success("MoviePy is correctly installed!")
    uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])
    if uploaded_file is not None:
        st.video(uploaded_file)
        st.write("Processing video...")
else:
    st.error("MoviePy ကို မတွေ့ရှိပါ။ ကျေးဇူးပြု၍ requirements.txt ကို ပြန်စစ်ပါ။")
