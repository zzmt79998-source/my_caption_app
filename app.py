import streamlit as st
import whisper
import cv2
import numpy as np
import os

# Whisper model ကို တစ်ခါပဲ load လုပ်မယ်
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

st.title("Burmese Auto-Caption Generator (OpenCV)")

uploaded_file = st.file_uploader("Video ဖိုင်တင်ပေးပါ", type=["mp4"])

if uploaded_file is not None:
    # ဗီဒီယိုကို သိမ်းမယ်
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("temp_video.mp4")

    if st.button("စာတန်းစထိုးမည်"):
        with st.spinner("AI စာတန်းထိုးနေပြီ..."):
            # ၁။ Whisper နဲ့ အသံဖမ်းမယ်
            model = load_whisper_model()
            result = model.transcribe("temp_video.mp4")
            
            # ၂။ OpenCV နဲ့ ဗီဒီယိုဖတ်မယ်
            cap = cv2.VideoCapture("temp_video.mp4")
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            # Output ဖိုင်ဆောက်မယ်
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (width, height))
            
            # စာတန်းထိုးခြင်း (ရိုးရှင်းအောင် ပထမဆုံး စာသားကိုပဲ Frame အားလုံးပေါ်တင်ပေးမယ်)
            caption_text = result['text']
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                
                # စာသားထည့်ခြင်း
                cv2.putText(frame, caption_text, (50, height - 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
                out.write(frame)
                
            cap.release()
            out.release()
            
            st.success("ပြီးပါပြီ!")
            st.video("output_video.mp4")
