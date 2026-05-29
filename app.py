import streamlit as st
from moviepy.editor import VideoFileClip
import os

# App ခေါင်းစဉ်
st.title("Burmese Auto-Caption Generator")

# ဗီဒီယိုဖိုင် တင်ရန်
uploaded_file = st.file_uploader("ဗီဒီယိုဖိုင်ကို ရွေးချယ်ပါ (MP4)...", type=["mp4"])

if uploaded_file is not None:
    # ဗီဒီယိုကို ခေတ္တသိမ်းခြင်း
    temp_file_path = "temp_video.mp4"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.video(temp_file_path)
    st.success("ဗီဒီယိုဖိုင် အောင်မြင်စွာ တင်ပြီးပါပြီ။")

    # Processing ခလုတ်
    if st.button("ဗီဒီယိုကို စတင်လုပ်ဆောင်ရန်"):
        try:
            st.info("ဗီဒီယိုကို စတင် လုပ်ဆောင်နေပါပြီ...")
            
            # MoviePy ကို သုံးခြင်း
            video = VideoFileClip(temp_file_path)
            
            # ရလဒ်ပြသခြင်း
            st.write(f"ဗီဒီယိုကြာချိန်: {video.duration:.2f} စက္ကန့်")
            
            # လုပ်ဆောင်ချက်ပြီးဆုံးကြောင်း
            st.success("ဗီဒီယို Processing ပြီးဆုံးပါပြီ!")
            
            # ဗီဒီယိုကို ပိတ်ပေးခြင်း (Memory သန့်ရှင်းရန်)
            video.close()
            
        except Exception as e:
            st.error(f"Error ဖြစ်ပေါ်နေသည်: {e}")
