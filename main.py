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
        
        # Loop through the links
        for i in range(current_index, len(AUDIO_LINKS)):
            audio_url = AUDIO_LINKS[i]
            save_index(i)
            
            print(f"Now Streaming Song #{i+1}...")

            # FFmpeg Command
            # showwaves creates the visualizer
            # colors=white@0.8 sets 80% transparency
            cmd = [
                'ffmpeg',
                '-re',
                '-loop', '1', '-i', IMAGE_URL,
                '-i', audio_url,
                '-filter_complex', 
                "[1:a]showwaves=s=1280x250:mode=line:colors=white@0.8[v_wave];" + 
                "[0:v][v_wave]overlay=0:H-250:format=auto,format=yuv420p[outv]",
                '-map', '[outv]', 
                '-map', '1:a',
                '-c:v', 'libx264', '-preset', 'veryfast', '-b:v', '3000k',
                '-maxrate', '3000k', '-bufsize', '6000k',
                '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
                '-f', 'flv', f"{STREAM_URL}{STREAM_KEY}"
            ]

            process = subprocess.Popen(cmd)
            process.wait() # Wait for song to finish
            
            # Reset to beginning if list ends
            if i == len(AUDIO_LINKS) - 1:
                save_index(0)

        print("Restarting playlist...")
        time.sleep(2)

if __name__ == "__main__":
    start_streaming()
