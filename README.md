# Free AI Video Studio

**Transform text scripts into cinematic, long-form videos with dynamic AI visuals and high-quality voiceovers.**

Free AI Video Studio is a production-ready, open-source web application that automates the video creation process. Built for creators, marketers, and developers, it eliminates the need for expensive video editing software or complex pipelines. Simply input your script, choose a voice, and let the engine handle the rest.

---

## ✨ Core Features

- 🎬 **Dynamic Scene Generation**: Automatically parses your script and fetches unique, high-resolution (1080p) AI-generated images for every scene using the Pollinations AI API.
- 🎥 **Cinematic Ken Burns Effect**: Applies smooth, dynamic zoom and pan animations to static images, ensuring your video feels alive, engaging, and professional.
- 🎙️ **High-Quality AI Voiceovers**: Powered by `edge-tts` to generate natural, human-like speech synthesis with support for multiple global accents (US, UK, etc.).
- ⏱️ **Precise Timestamp Control**: Supports custom scene durations (e.g., `0-4s: A serene forest`) or intelligently defaults to 4-second intervals per line for seamless pacing.
- ☁️ **Optimized for Free Hosting**: Engineered with secure temporary file management and zero external API key requirements, making it perfectly suited for Streamlit Community Cloud.
- 🎨 **Premium Minimalist UI**: A sleek, dark-mode interface built with custom CSS for a distraction-free, professional user experience.

---

## 🚀 Installation & Local Development

Follow these steps to run the project locally on your machine.

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/free-ai-video-studio.git
cd free-ai-video-studio
