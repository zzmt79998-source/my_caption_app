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

# --- Style Settings ---
st.sidebar.header("🎨 Style Settings")
text_color = st.sidebar.color_picker("စာလုံးအရောင်", "#FFFF00")
stroke_color = st.sidebar.color_picker("ဘောင်အရောင်", "#00FF00")
shadow_color = st.sidebar.color_picker("အရိပ်အရောင်", "#000000")
font_size = st.sidebar.slider("Font Size", 20, 100, 45)
stroke_width = st.sidebar.slider("ဘောင်အထူ", 0, 15, 3)
shadow_offset = st.sidebar.slider("အရိပ်အကွာအဝေး", 0, 10, 3)
line_spacing = st.sidebar.slider("စာကြောင်းကြားအကွာအဝေး", 0, 50, 10)

uploaded_file = st.file_uploader("ဗီဒီယိုဖိုင်တင်ပါ (MP4)", type=["mp4"])

if uploaded_file:
    with open("input.mp4", "wb") as f: f.write(uploaded_file.getbuffer())
    st.video("input.mp4")

    # စာသားထုတ်ယူခြင်း (language="my" ကို သေချာထည့်ထားပါ)
    if 'segments' not in st.session_state:
        with st.spinner("AI စာသားထုတ်ယူနေသည် (မြန်မာဘာသာ)..."):
            model = load_whisper_model()
            result = model.transcribe("input.mp4", language="my", fp16=False)
            st.session_state['segments'] = result['segments']

    st.subheader("📝 စာသားများ ပြင်ဆင်ရန်")
    # အကယ်၍ အရင်က အင်္ဂလိပ်လို ဖြစ်နေခဲ့ရင် ဒီနေရာမှာ မြန်မာလို အစားထိုးရိုက်ထည့်လို့ရပါပြီ
    for i, seg in enumerate(st.session_state['segments']):
        st.session_state['segments'][i]['text'] = st.text_input(f"စာကြောင်း {i+1}", seg['text'])

    if st.button("🚀 ဗီဒီယိုထဲသို့ စာတန်းထိုးမည် (Export)"):
        with st.spinner("Rendering လုပ်နေသည်..."):
            cap = cv2.VideoCapture("input.mp4")
            w, h = int(cap.get(3)), int(cap.get(4))
            out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), cap.get(5), (w, h))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                
                # Pillow Image သို့ပြောင်း
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.truetype("pyidaungsu.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                
                for s in st.session_state['segments']:
                    if s['start'] <= time <= s['end']:
                        # 1. Shadow
                        draw.multiline_text((w/2 + shadow_offset, h-100 + shadow_offset), s['text'], 
                                           font=font, fill=shadow_color, anchor="mm", align="center", spacing=line_spacing)
                        # 2. Main Text
                        draw.multiline_text((w/2, h-100), s['text'], font=font, fill=text_color, 
                                           stroke_width=stroke_width, stroke_fill=stroke_color, 
                                           anchor="mm", align="center", spacing=line_spacing)
                
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                out.write(frame)
            cap.release()
            out.release()
            st.success("ပြီးပါပြီ!")
            st.video("output.mp4") # ဗီဒီယိုကို ဒီမှာပဲ ဖွင့်ပြပါမယ်
            with open("output.mp4", "rb") as file:
                st.download_button("📥 ဒေါင်းလုဒ်လုပ်ရန်", file, "final_video.mp4")
