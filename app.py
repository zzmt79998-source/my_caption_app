import streamlit as st
import whisper
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

os.environ["PATH"] += os.pathsep + "/usr/bin"

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

st.set_page_config(layout="wide")
st.title("🎬 Burmese Auto Captions Pro")

# --- Style Settings ---
st.sidebar.header("🎨 Style Settings")
colors = ["#FFFF00", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFA500", "#800080", "#FFC0CB", "#000000"]
text_color = st.sidebar.selectbox("စာလုံးအရောင်", colors, index=0)
stroke_color = st.sidebar.color_picker("ဘောင်အရောင်", "#000000")
shadow_color = st.sidebar.color_picker("အရိပ်အရောင်", "#000000")

font_size = st.sidebar.slider("Font Size", 20, 100, 50)
stroke_width = st.sidebar.slider("ဘောင်အထူ", 0, 10, 2)

uploaded_file = st.file_uploader("ဗီဒီယိုဖိုင်တင်ပါ (MP4)", type=["mp4"])

if uploaded_file:
    with open("input.mp4", "wb") as f: f.write(uploaded_file.getbuffer())
    
    # AI Processing - language="my" ကို သေချာထည့်ထားပါ
    if 'segments' not in st.session_state:
        with st.spinner("AI စာသားထုတ်ယူနေသည်..."):
            model = load_whisper_model()
            result = model.transcribe("input.mp4", language="my", fp16=False)
            st.session_state['segments'] = result['segments']

    st.subheader("📝 စာသားများ ပြင်ဆင်ရန် (မြန်မာလို ပြန်ရိုက်ပါ)")
    # ဒီနေရာမှာ AI ထုတ်ပေးတဲ့စာသား English ဖြစ်နေရင် မြန်မာလို ပြန်ပြင်ရိုက်ပါ
    for i, seg in enumerate(st.session_state['segments']):
        st.session_state['segments'][i]['text'] = st.text_input(f"စာကြောင်း {i+1}", seg['text'])
    
    if st.button("🚀 ဗီဒီယိုထဲသို့ စာတန်းထိုးမည်"):
        with st.spinner("Rendering..."):
            cap = cv2.VideoCapture("input.mp4")
            w, h = int(cap.get(3)), int(cap.get(4))
            fps = cap.get(cv2.CAP_PROP_FPS)
            out = cv2.VideoWriter('temp.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(img)
                # ဖောင့်နာမည် pyidaungsu.ttf ကို သေချာစစ်ပါ
                font = ImageFont.truetype("pyidaungsu.ttf", font_size)
                
                for s in st.session_state['segments']:
                    if s['start'] <= time <= s['end']:
                        draw.text((w/2, h-100), s['text'], font=font, fill=text_color, 
                                  stroke_width=stroke_width, stroke_fill=stroke_color, anchor="mm")
                out.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
            cap.release(); out.release()

            subprocess.run(["ffmpeg", "-y", "-i", "temp.mp4", "-vcodec", "libx264", "-acodec", "aac", "final.mp4"])
            st.success("ပြီးပါပြီ!")
            st.video(open('final.mp4', 'rb').read())
