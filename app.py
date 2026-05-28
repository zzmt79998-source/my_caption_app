import streamlit as st
import whisper
import textwrap
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

st.title("Burmese Auto-Caption Generator")

# ၁။ Control Panel (UI)
video_file = st.file_uploader("ဗီဒီယိုဖိုင်တင်ပါ", type=['mp4', 'mov'])
font_size = st.slider("Font အရွယ်အစား", 20, 100, 40)
text_color = st.color_picker("စာလုံးအရောင်ရွေးပါ", "#ADFF2F") # Yellow-Green default

if st.button("Auto စာတန်းထိုးရန်"):
    if video_file:
        # ၂။ Processing
        with open("temp.mp4", "wb") as f: f.write(video_file.getbuffer())
        model = whisper.load_model("base")
        result = model.transcribe("temp.mp4")
        
        # ၃။ Auto 2-Lines Wrap
        wrapped_text = textwrap.fill(result["text"], width=25)
        
        # ၄။ ဗီဒီယိုစာတန်းထိုးခြင်း
        video = VideoFileClip("temp.mp4")
        txt_clip = TextClip(wrapped_text, fontsize=font_size, color=text_color, 
                            font='Arial-Bold', method='caption', size=(video.w*0.9, None))
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(video.duration)
        
        final = CompositeVideoClip([video, txt_clip])
        final.write_videofile("output.mp4")
        
        st.video("output.mp4")
        st.success("ပြီးပါပြီ! ဒေါင်းလုဒ်လုပ်နိုင်ပါပြီ။")
