import streamlit as st
import whisper
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# FFmpeg setup
os.environ["PATH"] += os.pathsep + "/usr/bin"

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

st.set_page_config(layout="wide")
st.title("🎬 Burmese Auto Captions Pro")

# --- Sidebar: Style Tools ---
st.sidebar.header("🎨 CapCut Style Tools")
text_color = st.sidebar.color_picker("စာလုံးအရောင်", "#FFFF00")
stroke_color = st.sidebar.color_picker("ဘောင်အရောင်", "#00FF00")
font_size = st.sidebar.slider("Font Size", 20, 100, 45)
line_spacing = st.sidebar.slider("စာကြောင်းကြားအကွာအဝေး", 0, 50, 10)

# --- Main App ---
uploaded_file = st.file_uploader("ဗီဒီယိုဖိုင်တင်ပါ (MP4)", type=["mp4"])

if uploaded_file:
    with open("input.mp4", "wb") as f: f.write(uploaded_file.getbuffer())
    st.video("input.mp4")

    if 'segments' not in st.session_state:
        with st.spinner("AI စာသားထုတ်ယူနေသည်..."):
            model = load_whisper_model()
            result = model.transcribe("input.mp4", language="my")
            st.session_state['segments'] = result['segments']

    # Edit & Add Text Section
    st.subheader("📝 စာသားများ ပြင်ဆင်ရန်")
    for i, seg in enumerate(st.session_state['segments']):
        st.session_state['segments'][i]['text'] = st.text_input(f"စာကြောင်း {i+1}", seg['text'])

    if st.button("➕ စာသားအသစ် ထပ်ထည့်မည်"):
        st.session_state['segments'].append({'start': 0, 'end': 5, 'text': 'အသစ်'})

    # Rendering
    if st.button("🚀 ဗီဒီယိုထဲသို့ စာတန်းထိုးမည် (Export)"):
        with st.spinner("ဗီဒီယို Process လုပ်နေသည်..."):
            cap = cv2.VideoCapture("input.mp4")
            w, h = int(cap.get(3)), int(cap.get(4))
            out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), cap.get(5), (w, h))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                
                # စာသားထည့်ခြင်း
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.truetype("Pyidaungsu.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                
                for s in st.session_state['segments']:
                    if s['start'] <= time <= s['end']:
                        draw.multiline_text((w/2, h-100), s['text'], font=font, fill=text_color, 
                                           stroke_width=3, stroke_fill=stroke_color, 
                                           anchor="mm", align="center", spacing=line_spacing)
                
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                out.write(frame)
            
            cap.release()
            out.release()
            
            st.success("ပြီးပါပြီ! အောက်တွင် ကြည့်ရှုနိုင်ပါသည်။")
            st.video("output.mp4") # App ထဲမှာတင် ပြန်ပြပေးမယ်
            with open("output.mp4", "rb") as file:
                st.download_button("📥 ဒေါင်းလုဒ်လုပ်ရန်", file, "final_video.mp4")
