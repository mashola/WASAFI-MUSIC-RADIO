import subprocess
import time
import os

# --- CONFIGURATION ---
IMAGE_URL = "https://huggingface.co/datasets/MASHOLA/YOUTUBE/resolve/main/IMAGES/WASAFI%20MUSIC%20RADIO.png?download=true"

# Add all your audio links here
AUDIO_LINKS = [
    "https://huggingface.co/datasets/MASHOLA/YOUTUBE/resolve/main/MUSIC/WASAFI%20MUSIC%20RADIO.wav?download=true",
    "https://huggingface.co/datasets/MASHOLA/YOUTUBE/resolve/main/MUSIC/WASAFI%20MUSIC%20RADIO.wav?download=true" # Replace with your 2nd link
]

STREAM_URL = "rtmp://a.rtmp.youtube.com/live2/"
# Reads from GitHub Secrets for security
STREAM_KEY = os.getenv("STREAM_KEY", "3zy9-9xek-e8vu-ef3z-c77u") 
STATE_FILE = "state.txt"

def get_last_index():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def save_index(index):
    with open(STATE_FILE, "w") as f:
        f.write(str(index))

def start_streaming():
    while True:
        current_index = get_last_index()
        
        for i in range(current_index, len(AUDIO_LINKS)):
            audio_url = AUDIO_LINKS[i]
            save_index(i)
            
            print(f"Now Streaming Song #{i+1}...")

            # Simplified FFmpeg Command without filter_complex
            cmd = [
                'ffmpeg',
                '-re',
                '-loop', '1', '-i', IMAGE_URL,    # Input 0: Image
                '-i', audio_url,                  # Input 1: Audio
                '-c:v', 'libx264',                # Video Codec
                '-preset', 'veryfast', 
                '-b:v', '3000k',                  # Video Bitrate
                '-maxrate', '3000k', 
                '-bufsize', '6000k',
                '-pix_fmt', 'yuv420p',            # Ensures compatibility with YouTube
                '-c:a', 'aac',                    # Audio Codec
                '-b:a', '128k', 
                '-ar', '44100',
                '-shortest',                       # Stop when the audio ends
                '-f', 'flv', f"{STREAM_URL}{STREAM_KEY}"
            ]

            process = subprocess.Popen(cmd)
            process.wait() 
            
            if i == len(AUDIO_LINKS) - 1:
                save_index(0)

        print("Restarting playlist...")
        time.sleep(2)

if __name__ == "__main__":
    start_streaming()
