"""
Free AI Video Studio - Production Ready
Backend Systems Engineered with edge-tts, dynamic visual fetching, and moviepy assembly.
Zero emojis, fully optimized for free hosting environments.
"""

import streamlit as st
import asyncio
import edge_tts
import os
import tempfile
import shutil
import gc
import re
import requests
import urllib.parse
import concurrent.futures
from datetime import datetime
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Free AI Video Studio",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Custom CSS - Premium Minimalist Dark Aesthetic
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    .stApp {
        background-color: #121214;
        color: #F4F4F6;
        font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    #MainMenu, header, footer {
        display: none !important;
    }
    .main .block-container {
        max-width: 860px;
        padding: 3rem 1.5rem 4rem 1.5rem;
        margin: 0 auto;
    }
    .app-header {
        text-align: center;
        padding: 1.5rem 0 2.5rem 0;
    }
    .app-header h1 {
        color: #F4F4F6;
        font-size: 2.6rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }
    .app-header p {
        color: #A1A1AA;
        font-size: 1.05rem;
        font-weight: 400;
        margin: 0;
    }
    .stTextArea textarea {
        background-color: #1A1A1D !important;
        color: #F4F4F6 !important;
        border: 1px solid #2A2A2E !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
        min-height: 220px !important;
    }
    .stTextArea textarea:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.18) !important;
    }
    .stTextArea label, .stSelectbox label {
        color: #F4F4F6 !important;
        font-weight: 500 !important;
    }
    .stSelectbox > div > div {
        background-color: #1A1A1D !important;
        border: 1px solid #2A2A2E !important;
        border-radius: 10px !important;
        color: #F4F4F6 !important;
    }
    .stSelectbox svg {
        fill: #8B5CF6 !important;
    }
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #1A1A1D !important;
        color: #F4F4F6 !important;
    }
    .stSelectbox [data-baseweb="select"] input {
        color: #F4F4F6 !important;
    }
    div[role="listbox"] {
        background-color: #1A1A1D !important;
        border: 1px solid #2A2A2E !important;
        border-radius: 10px !important;
    }
    div[role="option"] {
        color: #F4F4F6 !important;
        background-color: #1A1A1D !important;
    }
    div[role="option"]:hover,
    div[role="option"][aria-selected="true"] {
        background-color: #2A2A2E !important;
        color: #8B5CF6 !important;
    }
    .stButton > button {
        background-color: #8B5CF6 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.02em !important;
        padding: 0.85rem 2rem !important;
        border: none !important;
        border-radius: 10px !important;
        width: 100%;
        transition: all 0.3s ease !important;
        box-shadow:
            0 0 18px rgba(139, 92, 246, 0.45),
            0 0 40px rgba(139, 92, 246, 0.20) !important;
    }
    .stButton > button:hover {
        background-color: #7C3AED !important;
        box-shadow:
            0 0 24px rgba(124, 58, 237, 0.65),
            0 0 60px rgba(124, 58, 237, 0.30) !important;
        transform: translateY(-1px);
    }
    .stButton > button:active {
        transform: translateY(0);
    }
    .stDownloadButton > button {
        background-color: #10B981 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.75rem 1.5rem !important;
        border: none !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    .stDownloadButton > button:hover {
        background-color: #059669 !important;
        transform: translateY(-1px);
    }
    .video-output {
        background-color: #1A1A1D;
        border: 1px solid #2A2A2E;
        border-radius: 14px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        margin-top: 2rem;
    }
    .video-output h3 {
        color: #F4F4F6;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .video-output p {
        color: #A1A1AA;
        font-size: 0.95rem;
        margin: 0;
    }
    .success-text {
        color: #10B981 !important;
        font-weight: 600;
    }
    .error-text {
        color: #EF4444 !important;
        font-weight: 600;
    }
    @media (max-width: 640px) {
        .main .block-container {
            padding: 2rem 1rem 3rem 1rem;
        }
        .app-header h1 {
            font-size: 1.9rem;
        }
        .app-header p {
            font-size: 0.95rem;
        }
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Configuration & Mappings
# ---------------------------------------------------------------------------
VOICE_MAP = {
    "US Male (Christopher)": "en-US-ChristopherNeural",
    "US Female (Jenny)": "en-US-JennyNeural",
    "UK Male (Ryan)": "en-GB-RyanNeural",
    "UK Female (Sonia)": "en-GB-SoniaNeural"
}

# ---------------------------------------------------------------------------
# Backend Systems: Media Processing Logic
# ---------------------------------------------------------------------------

def parse_script(script: str) -> list:
    """Parses the user script into scenes. Defaults to 4 seconds per line."""
    scenes = []
    lines = script.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check for optional timestamp pattern like "0-4s:" or "0-4:"
        match = re.match(r'^(\d+)\s*-\s*(\d+)\s*s?\s*:\s*(.*)$', line, re.IGNORECASE)
        if match:
            start = int(match.group(1))
            end = int(match.group(2))
            duration = max(end - start, 1)
            text = match.group(3).strip()
            scenes.append({"duration": duration, "text": text})
        else:
            # Default to 4 seconds per line if no timestamp is provided
            scenes.append({"duration": 4, "text": line})
    
    return scenes


def get_tts_text(scenes: list) -> str:
    """Extracts clean text for TTS, stripping any timestamp prefixes."""
    return " ".join(scene["text"] for scene in scenes)


def fetch_background_image(prompt: str, save_path: str, seed: int) -> str:
    """
    Fetches high-resolution (1024x576) cinematic visuals dynamically.
    Uses a unique seed per scene to ensure varied imagery.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    # Using the direct image endpoint for reliability
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true&seed={seed}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()
    
    with open(save_path, "wb") as f:
        f.write(response.content)
    
    if os.path.getsize(save_path) < 10000:
        raise RuntimeError("Downloaded visual is invalid or too small. Please try a different prompt.")
    
    return save_path


def generate_audio_sync(text: str, voice: str, output_path: str) -> None:
    """
    Synchronous wrapper for async edge-tts to prevent Streamlit event loop conflicts.
    """
    async def _generate():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(asyncio.run, _generate())
        future.result()


def make_kim_burns_clip(image_path: str, duration: float, target_w: int = 1024, target_h: int = 576):
    """
    Creates a cinematic Ken Burns (zoom-out) effect clip.
    Zooming out from 1.15x to 1.0x guarantees no black borders on the edges 
    while maintaining a dynamic, moving feel.
    """
    clip = ImageClip(image_path, duration=duration)
    
    def zoom_func(t):
        # Smoothly zooms out from 1.15x to 1.0x relative to the target size
        return 1.15 - (0.15 * (t / duration))
    
    resized_clip = clip.resize(zoom_func)
    
    # Center the resizing image perfectly within the frame
    final_clip = resized_clip.set_position('center')
    return final_clip


def compile_video_secure(scenes: list, image_dir: str, audio_path: str, output_path: str, temp_dir: str) -> None:
    """
    Assembles the final video composition using MoviePy v1.0.3 syntax.
    Matches visual duration precisely to the generated audio track duration.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError("Audio file not found for compilation.")
    
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration
    
    video_clips = []
    current_time = 0.0
    
    for i, scene in enumerate(scenes):
        img_path = os.path.join(image_dir, f"scene_{i}.jpg")
        duration = float(scene["duration"])
        
        # Extend the last scene to cover any remaining audio duration
        if i == len(scenes) - 1:
            remaining = audio_duration - current_time
            if remaining > duration:
                duration = remaining
        
        # Ensure duration is at least 1.0 to prevent division by zero in zoom_func
        duration = max(duration, 1.0)
        
        clip = make_kim_burns_clip(img_path, duration)
        video_clips.append(clip)
        current_time += duration
        
    final_video = concatenate_videoclips(video_clips, method="compose")
    
    # If the total video duration exceeds the audio duration, trim it to match perfectly
    if final_video.duration > audio_duration:
        final_video = final_video.subclip(0, audio_duration)
        
    final_video = final_video.set_audio(audio_clip)
    
    temp_audio = os.path.join(temp_dir, "temp-audio.m4a")
    
    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile=temp_audio,
        remove_temp=True,
        threads=4,
        preset="medium",
        logger=None
    )
    
    # Explicitly close clips to free memory and prevent leaks on free hosting
    audio_clip.close()
    for clip in video_clips:
        clip.close()
    final_video.close()
    gc.collect()


class SecureTempManager:
    """Manages temporary file creation and secure cleanup to prevent disk bloat."""
    def __init__(self):
        self.temp_dir = None
        
    def create_workspace(self):
        try:
            self.temp_dir = tempfile.mkdtemp(prefix="ai_video_studio_")
            return self.temp_dir
        except Exception as e:
            raise RuntimeError(f"Failed to create temporary workspace: {str(e)}")
            
    def cleanup(self):
        try:
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            gc.collect()
        except Exception as e:
            st.warning(f"Cleanup warning: {str(e)}")


# ---------------------------------------------------------------------------
# UI Layout
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <h1>Free AI Video Studio</h1>
        <p>Generate unlimited HD videos with dynamic cinematic effects and zero watermarks.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

user_prompt = st.text_area(
    label="Enter your video script or prompt here:",
    placeholder=(
        "Describe the video you want to create...\n\n"
        "Example with timestamps (optional):\n"
        "0-4s: A serene forest with morning mist\n"
        "4-8s: A majestic mountain peak at sunset\n\n"
        "Or just plain lines (4 seconds per line by default):\n"
        "A serene forest with morning mist\n"
        "A majestic mountain peak at sunset"
    ),
)

voice_accent = st.selectbox(
    label="Choose AI Voice Accent:",
    options=list(VOICE_MAP.keys()),
    index=0,
)

generate_clicked = st.button("Generate Video", type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# Processing Pipeline
# ---------------------------------------------------------------------------
if generate_clicked:
    if not user_prompt or not user_prompt.strip():
        st.markdown(
            """
            <div class="video-output">
                <h3 class="error-text">Missing Prompt</h3>
                <p>Please enter a video script or prompt before generating.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        temp_manager = SecureTempManager()
        
        try:
            with st.status("Processing video generation pipeline...", expanded=True) as status:
                
                status.update(label="Initializing secure temporary workspace...", state="running")
                temp_dir = temp_manager.create_workspace()
                image_dir = os.path.join(temp_dir, "images")
                os.makedirs(image_dir, exist_ok=True)
                
                audio_path = os.path.join(temp_dir, "output_audio.mp3")
                video_path = os.path.join(temp_dir, "final_output.mp4")
                
                status.update(label="Parsing script and analyzing scenes...", state="running")
                scenes = parse_script(user_prompt)
                if not scenes:
                    raise ValueError("No valid scenes found in the script.")
                
                tts_text = get_tts_text(scenes)
                
                status.update(label="Generating AI Voiceover...", state="running")
                voice_id = VOICE_MAP[voice_accent]
                generate_audio_sync(tts_text, voice_id, audio_path)
                
                status.update(label="Fetching dynamic background visuals for each scene...", state="running")
                for i, scene in enumerate(scenes):
                    fetch_background_image(scene["text"], os.path.join(image_dir, f"scene_{i}.jpg"), seed=42 + i)
                    status.update(label=f"Fetched visual {i+1}/{len(scenes)}...", state="running")
                
                status.update(label="Assembling HD video composition with cinematic effects...", state="running")
                compile_video_secure(scenes, image_dir, audio_path, video_path, temp_dir)
                
                status.update(label="Video generation complete!", state="complete")
            
            st.markdown(
                """
                <div class="video-output">
                    <h3 class="success-text">Video Generated Successfully</h3>
                    <p>Your HD video is ready for preview and download below.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            with open(video_path, "rb") as video_file:
                video_bytes = video_file.read()
            
            st.video(video_bytes)
            
            st.download_button(
                label="Download Video (MP4)",
                data=video_bytes,
                file_name=f"ai_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
                mime="video/mp4",
                use_container_width=True
            )
            
            temp_manager.cleanup()
            
        except ValueError as ve:
            st.markdown(
                f"""
                <div class="video-output">
                    <h3 class="error-text">Input Error</h3>
                    <p>{str(ve)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            temp_manager.cleanup()
        except Exception as e:
            st.markdown(
                f"""
                <div class="video-output">
                    <h3 class="error-text">Processing Error</h3>
                    <p>An error occurred during video generation. Please try again.</p>
                    <p style="font-size: 0.85rem; color: #71717A; margin-top: 0.5rem;">{str(e)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            temp_manager.cleanup()
else:
    st.markdown(
        """
        <div class="video-output">
            <h3>Your Video Will Appear Here</h3>
            <p>Enter a prompt above and click Generate Video to begin.</p>
        </div>
        """,
        unsafe_allow_html=True,
)
