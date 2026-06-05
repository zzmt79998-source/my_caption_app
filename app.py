import streamlit as st
import whisper
import os

# Model ကို load လုပ်မယ်
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

    # ခလုတ်ကို ဒီမှာ သေချာ ထည့်ထားပါတယ်
    if st.button("စာတန်းစထိုးမည်"):
        with st.spinner("AI စာတန်းထိုးနေပြီ..."):
            model = load_whisper_model()
            result = model.transcribe(video_path)
            st.success("စာသားရရှိပါပြီ!")
            st.write(result['text'])
