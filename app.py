# import streamlit as st
# import google.generativeai as genai
# import asyncio
# import edge_tts
# from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

import streamlit as st
import google.generativeai as genai
import asyncio
import edge_tts
import os

# Updated Import for MoviePy 1.0.3
from moviepy.editor import ImageClip, AudioFileClip

# Setup Google Gemini (The Free Brain)
genai.configure(api_key=st.secrets["GEMINI_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Machine Engine", layout="centered")
st.title("⚙️ Inside the Machine")

# --- MOBILE UI TABS ---
tab1, tab2, tab3 = st.tabs(["💡 Topic", "📝 Script", "🎬 Create"])

# with tab1:
#     if st.button("Find New Topic"):
#         response = model.generate_content("Suggest one specific vintage or modern machine to explain. Just the name.")
#         st.session_state.topic = response.text
#         st.success(f"Today's Topic: {st.session_state.topic}")

with tab1:
    if st.button("Find New Topic"):
        try:
            # Try the most stable model name
            model_name = 'gemini-1.5-flash'
            model = genai.GenerativeModel(model_name)
            
            response = model.generate_content("Suggest one specific vintage or modern machine to explain. Just the name.")
            st.session_state.topic = response.text
            st.success(f"Today's Topic: {st.session_state.topic}")
            
        except Exception as e:
            st.error(f"Error: {e}")
            
            # DEBUG MODE: This will show you exactly what models your key can see
            st.info("Searching for available models for your account...")
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            st.write("Try one of these model names instead:")
            st.json(available_models)

with tab2:
    if 'topic' in st.session_state:
        if st.button("Generate Script"):
            prompt = f"Write a 30-second viral script for a Reel about {st.session_state.topic}. Use a curious tone."
            script_resp = model.generate_content(prompt)
            st.session_state.script = script_resp.text
            st.text_area("Your Script:", st.session_state.script, height=200)

with tab3:
    if 'script' in st.session_state:
        if st.button("Build Video"):
            st.warning("Stitching video... This takes 1 minute.")
            # 1. GENERATE VOICE (Free with edge-tts)
            communicate = edge_tts.Communicate(st.session_state.script, "en-US-ChristopherNeural")
            asyncio.run(communicate.save("voice.mp3"))
            
            # 2. GENERATE IMAGE (Free with Pollinations)
            img_url = f"https://image.pollinations.ai/prompt/inside_view_of_{st.session_state.topic.replace(' ', '_')}_cinematic_lighting?width=1080&height=1920"
            st.image(img_url, caption="Generated Visual")
            
            st.success("Video Ready! Download below and post.")
            st.audio("voice.mp3") 
            # (In the final version, MoviePy will combine the img_url and voice.mp3 here)
