import streamlit as st
import whisper
import os

# Whisper Model ကို load လုပ်မယ် (Cache ထားလို့ မြန်ပါတယ်)
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

st.title("Burmese Auto-Caption Generator")

# ဗီဒီယိုဖိုင်တင်ရန်
uploaded_file = st.file_uploader("ဗီဒီယိုဖိုင်တင်ပေးပါ (MP4 format)", type=["mp4"])

if uploaded_file is not None:
    # 1. ဗီဒီယိုဖိုင်ကို သိမ်းဆည်းခြင်း (ပိုမြန်အောင် ပြင်ထားပါတယ်)
    video_path = "temp_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # 2. ဗီဒီယိုကို ပြပေးခြင်း
    st.video(video_path)
    st.success("ဗီဒီယိုဖိုင် တင်ပြီးပါပြီ။")

    # 3. AI စာတန်းထိုးရန် ခလုတ်
    if st.button("စာတန်းစထိုးမည်"):
        with st.spinner("AI စာတန်းထိုးနေပြီ... ခဏစောင့်ပေးပါ..."):
            try:
                # Whisper model load လုပ်ခြင်း
                model = load_whisper_model()
                
                # အသံကို စာသားဖြစ်အောင် ပြောင်းခြင်း
                result = model.transcribe(video_path)
                
                # ရလဒ်ကို ဖော်ပြပေးခြင်း
                st.subheader("ရရှိလာသော စာသားများ:")
                st.text_area("စာသားများ -", value=result['text'], height=200)
                
            except Exception as e:
                st.error(f"Error ဖြစ်သွားပါသည်: {e}")

# အသုံးပြုသူအတွက် ရှင်းလင်းချက်
st.info("မှတ်ချက်: AI Model ပထမဆုံး အလုပ်လုပ်သည့်အခါ အနည်းငယ် စောင့်ရနိုင်ပါသည်။")
