import streamlit as st
from moviepy.editor import VideoFileClip
import os

# App ရဲ့ ခေါင်းစဉ်
st.title("Burmese Auto-Caption Generator")

# ဗီဒီယို ဖိုင်တင်ခြင်း
uploaded_file = st.file_uploader("ဗီဒီယိုဖိုင်ကို ရွေးချယ်ပါ (MP4)...", type=["mp4"])

if uploaded_file is not None:
    # ဖိုင်ကို ခေတ္တ သိမ်းဆည်းခြင်း
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.video("temp_video.mp4")
    st.success("ဗီဒီယိုဖိုင် အောင်မြင်စွာ တင်ပြီးပါပြီ။")

    # ဒီနေရာမှာ နောက်ထပ် လုပ်ဆောင်ချက်များ (ဥပမာ- Caption ထုတ်ခြင်း) ကို ဆက်ရေးပါ
    if st.button("Processing..."):
        st.info("ဗီဒီယိုကို စတင် လုပ်ဆောင်နေပါပြီ...")
        # MoviePy ကို ဒီနေရာမှာ သုံးလို့ရပါပြီ
        video = VideoFileClip("temp_video.mp4")
        st.write(f"ဗီဒီယိုကြာချိန်: {video.duration} စက္ကန့်")
