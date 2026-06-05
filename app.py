import streamlit as st
import whisper
import cv2
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont

# FFmpeg setup
os.environ["PATH"] += os.pathsep + "/usr/bin"

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

st.set_page_config(page_title="Burmese Auto Captions", layout="wide")
st.title("✨ Burmese Auto Captions Pro")

# Sidebar - CapCut Pro Style Tools
st.sidebar.header("🎛️ CapCut Pro Style Tools")
text_color = st.sidebar.color_picker("Text Color (စာလုံးအရောင်)", "#FFFF00")
stroke_color = st.sidebar.color_picker("Stroke Color (ဘောင်အရောင်)", "#00FF00")
font_size = st.sidebar.slider("Font Size", 20, 100, 50)
stroke_width = st.sidebar.slider("Stroke Width", 1, 10, 3)

def render_caption(frame, text, color, stroke_col, size, stroke_w):
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    try:
        font = ImageFont.truetype("Pyidaungsu.ttf", size)
    except:
        font = ImageFont.load_default()
    
    # Text Centering Logic
    w, h = img_pil.size
    draw.text((w/2, h-100), text, font=font, fill=color, 
              stroke_width=stroke_w, stroke_fill=stroke_col, anchor="mm")
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

# Main UI
uploaded_file = st.file_uploader("ဗီဒီယိုဖိုင်တင်ရန်", type=["mp4"])

if uploaded_file:
    video_path = "input.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.video(video_path)

    if st.button("🚀 စာတန်းထိုးပြီး Export Video လုပ်မည်"):
        with st.spinner("AI စာတန်းထိုးနေပြီ..."):
            model = load_whisper_model()
            result = model.transcribe(video_path, language="my")
            
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
            
            segments = result['segments']
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                
                time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                for s in segments:
                    if s['start'] <= time <= s['end']:
                        frame = render_caption(frame, s['text'], text_color, stroke_color, font_size, stroke_width)
                out.write(frame)
            
            cap.release()
            out.release()
            st.success("Export ပြီးပါပြီ!")
            st.download_button("📥 ဒေါင်းလုဒ်လုပ်ရန်", open("output.mp4", "rb"), "captioned_video.mp4")
