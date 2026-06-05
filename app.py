import streamlit as st
import whisper
import cv2
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont

# Streamlit Cloud အတွက် FFmpeg Path ချိန်ခြင်း
os.environ["PATH"] += os.pathsep + "/usr/bin"

# Whisper Model ကို Load လုပ်ခြင်း
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

st.set_page_config(page_title="Burmese Auto Captions Pro", layout="wide")
st.title("🎬 Burmese Auto Captions Pro (CapCut Style)")

# --- Sidebar: CapCut Pro Style Tools ---
st.sidebar.header("🎛️ Caption Style Tools")

# အရောင်ရွေးချယ်မှုများ
text_col = st.sidebar.color_picker("Text Color (စာလုံးအရောင်)", "#F3FF00") # အဝါရောင်
stroke_col = st.sidebar.color_picker("Stroke Color (ဘောင်အရောင်)", "#CCFF00") # အစိမ်းရောင်
shadow_col = st.sidebar.color_picker("Shadow Color (အရိပ်အရောင်)", "#000000") # အမည်းရောင်

# အရွယ်အစားနှင့် အကွာအဝေးများ
f_size = st.sidebar.slider("Font Size", 20, 100, 45)
s_width = st.sidebar.slider("Stroke Width (ဘောင်အထူ)", 0, 15, 5)
shadow_offset = st.sidebar.slider("Shadow Offset (အရိပ်အကွာအဝေး)", 0, 10, 3)
line_spacing = st.sidebar.slider("Line Spacing (စာကြောင်းကြားအကွာအဝေး)", 0, 50, 10)

# --- Video ပေါ်မှာ စာသားရေးဆွဲသည့် Function ---
def draw_styled_text(frame, text, color, s_color, shadow_c, size, s_w, sh_off, l_space):
    # OpenCV Frame ကို Pillow Image ပြောင်းလဲခြင်း
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    width, height = img_pil.size

    # Font Load လုပ်ခြင်း
    try:
        font = ImageFont.truetype("Pyidaungsu.ttf", size)
    except:
        st.error("Pyidaungsu.ttf ဖောင့်ဖိုင်ကို ရှာမတွေ့ပါ။ GitHub တွင် တင်ထားပေးပါ။")
        font = ImageFont.load_default()

    # စာတန်းကို နှစ်ကြောင်းခွဲသည့် Logic (စာလုံး ၃၀ ထက်ကျော်လျှင် ခွဲမည်)
    if len(text) > 30:
        mid = len(text) // 2
        split_idx = text.find(" ", mid) # အလယ်နားက space မှာ ခွဲမယ်
        if split_idx == -1: split_idx = mid
        line1 = text[:split_idx]
        line2 = text[split_idx:].strip()
        display_text = f"{line1}\n{line2}"
    else:
        display_text = text

    # စာသားတည်မည့်နေရာ (ဗီဒီယိုအောက်ခြေ အလယ်)
    position = (width // 2, height - 120)

    # ၁။ Shadow (အရိပ်) ရင်ရေးမည်
    if sh_off > 0:
        sh_pos = (position[0] + sh_off, position[1] + sh_off)
        draw.multiline_text(sh_pos, display_text, font=font, fill=shadow_c, anchor="mm", align="center", spacing=l_space)

    # ၂။ Stroke (ဘောင်) နှင့် စာလုံးအရောင် ရေးမည်
    draw.multiline_text(position, display_text, font=font, fill=color, 
                        stroke_width=s_w, stroke_fill=s_color, 
                        anchor="mm", align="center", spacing=l_space)

    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

# --- Main App Logic ---
uploaded_file = st.file_uploader("ဗီဒီယိုဖိုင်တင်ပါ (MP4)", type=["mp4"])

if uploaded_file:
    # ဖိုင်သိမ်းခြင်း
    with open("input_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.video("input_video.mp4")

    if st.button("🚀 စာတန်းထိုးပြီး Export လုပ်မည်"):
        with st.spinner("AI က မြန်မာစာတန်းထိုးနေပါပြီ... ခဏစောင့်ပါ..."):
            # ၁။ Transcription (Forced Burmese)
            model = load_whisper_model()
            result = model.transcribe("input_video.mp4", language="my")
            
            # ၂။ Video Processing
            cap = cv2.VideoCapture("input_video.mp4")
            fps = cap.get(cv2.CAP_PROP_FPS)
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            output_path = "final_output.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
            
            segments = result['segments']
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                
                # လက်ရှိအချိန်ကို စက္ကန့်ဖြင့်ယူခြင်း
                timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                
                # သက်ဆိုင်ရာ စာတန်းကို ရှာဖွေခြင်း
                for seg in segments:
                    if seg['start'] <= timestamp <= seg['end']:
                        frame = draw_styled_text(frame, seg['text'], text_col, stroke_col, shadow_col, f_size, s_width, shadow_offset, line_spacing)
                        break
                
                out.write(frame)
            
            cap.release()
            out.release()
            
            st.success("စာတန်းထိုးခြင်း အောင်မြင်ပါသည်။ ဗီဒီယိုကို အောက်တွင် ကြည့်ရှု/ဒေါင်းလုဒ်လုပ်ပါ။")
            st.video(output_path)
            st.download_button("📥 Capioned Video ကို ဒေါင်းလုဒ်လုပ်ရန်", open(output_path, "rb"), "burmese_captioned.mp4")
