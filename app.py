import streamlit as st
import whisper
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Whisper Model Load လုပ်ခြင်း
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

st.title("✨ Advanced Burmese Auto Captions")

# --- Sidebar: CapCut Style Tools ---
st.sidebar.header("🎨 Style Settings")
text_color = st.sidebar.color_picker("စာလုံးအရောင်", "#FFFF00") # default အဝါ
stroke_color = st.sidebar.color_picker("ဘောင်အရောင်", "#00FF00") # default အစိမ်း
font_size = st.sidebar.slider("Font Size", 20, 100, 45)

# ၁။ Video တင်ခြင်း
uploaded_file = st.file_uploader("ဗီဒီယိုဖိုင်တင်ပါ (MP4)", type=["mp4"])
if uploaded_file:
    with open("input.mp4", "wb") as f: f.write(uploaded_file.getbuffer())
    
    # AI နဲ့ စာသားထုတ်ခြင်း
    if 'segments' not in st.session_state:
        with st.spinner("AI စာသားထုတ်ယူနေသည်..."):
            model = load_whisper_model()
            result = model.transcribe("input.mp4", language="my")
            st.session_state['segments'] = result['segments']

    # ၂။ စာသား Edit လုပ်ခြင်း
    st.subheader("📝 စာသားများ ပြင်ဆင်ရန်")
    for i, seg in enumerate(st.session_state['segments']):
        st.session_state['segments'][i]['text'] = st.text_input(f"စာကြောင်း {i+1}", seg['text'])

    # ၃။ Video Render လုပ်ခြင်း
    if st.button("🚀 ဗီဒီယိုထဲသို့ စာတန်းထိုးမည် (Export)"):
        cap = cv2.VideoCapture("input.mp4")
        w, h = int(cap.get(3)), int(cap.get(4))
        out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), cap.get(5), (w, h))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            
            for s in st.session_state['segments']:
                if s['start'] <= time <= s['end']:
                    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    draw = ImageDraw.Draw(img)
                    # GitHub မှာတင်ထားတဲ့ pyidaungsu.ttf နာမည်အတိုင်း ဖြစ်ရပါမယ်
                    try:
                        font = ImageFont.truetype("pyidaungsu.ttf", font_size)
                    except:
                        font = ImageFont.load_default()
                    
                    # စာတန်းထိုးခြင်း (အဝါ/အစိမ်း အရောင်စုံ)
                    draw.text((w/2, h-100), s['text'], font=font, fill=text_color, 
                              stroke_width=4, stroke_fill=stroke_color, anchor="mm")
                    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame)
        cap.release()
        out.release()
        st.video("output.mp4")
        st.download_button("📥 ဒေါင်းလုဒ်လုပ်ရန်", open("output.mp4", "rb"), "final.mp4")
