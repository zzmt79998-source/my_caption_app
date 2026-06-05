import streamlit as st
import whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

st.title("Burmese Auto-Caption Generator")

uploaded_file = st.file_uploader("ဗီဒီယိုဖိုင်ကို ရွေးချယ်ပါ", type=["mp4"])

if uploaded_file is not None:
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.video("temp_video.mp4")
    
    # စာတန်းချိန်ညှိချက်များ
    color = st.color_picker("စာတန်းအရောင် ရွေးပါ", "#FFFF00")
    font_size = st.slider("စာတန်း အရွယ်အစား", 20, 100, 50)
    
    if st.button("ဗီဒီယိုကို စတင် လုပ်ဆောင်ရန်"):
        with st.spinner('AI စာတန်းထိုးနေပါပြီ... ခဏစောင့်ပါ'):
            try:
                # 1. Whisper Model ကို load လုပ်ခြင်း
                model = whisper.load_model("base")
                result = model.transcribe("temp_video.mp4")
                
                st.success("စာတန်းထိုးပြီးပါပြီ!")
                st.write(result["text"]) # ရလာတဲ့ စာသားကိုပြခြင်း
                
            except Exception as e:
                st.error(f"Error တက်နေသည်: {e}")
