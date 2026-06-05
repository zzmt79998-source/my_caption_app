import streamlit as st
import whisper
import cv2
import numpy as np
import os

# Whisper model ကို load လုပ်မယ်
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

st.title("Burmese Auto-Caption Generator")

uploaded_file = st.file_uploader("Video ဖိုင်တင်ပေးပါ", type=["mp4"])

if uploaded_file is not None:
    video_path = "temp_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())
    
    st.video(video_path)

    if st.button("စာတန်းစထိုးမည်"):
        with st.spinner("AI စာတန်းထိုးနေပြီ..."):
            # ၁။ Whisper နဲ့ အသံဖမ်းမယ်
            model = load_whisper_model()
            result = model.transcribe(video_path)
            caption_text = result['text']
            
            # ၂။ ရလဒ်ကို ဖော်ပြပေးမယ်
            st.success("စာသားရရှိပါပြီ!")
            st.text_area("ရရှိလာသော စာသား -", caption_text)
            
            # နောက်ထပ် ဗီဒီယို processing လုပ်ချင်ရင် ဒီအောက်မှာ ဆက်ရေးလို့ရပါတယ်
