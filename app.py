import streamlit as st
import subprocess
import sys

# လိုအပ်တဲ့ library တွေကို အခုချက်ချင်း install လုပ်ခိုင်းခြင်း
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    st.warning("MoviePy ကို install လုပ်နေပါပြီ၊ ခဏစောင့်ပေးပါ...")
    install("moviepy")
    from moviepy.editor import VideoFileClip

st.title("Burmese Auto-Caption Generator")
st.success("MoviePy အဆင်သင့်ဖြစ်ပါပြီ!")

uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])
if uploaded_file is not None:
    st.video(uploaded_file)
