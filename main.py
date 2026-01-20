import subprocess
import time
import os

# --- CONFIGURATION ---
IMAGE_URL = "https://huggingface.co/datasets/MASHOLA/YOUTUBE/resolve/main/IMAGES/WASAFI%20MUSIC%20RADIO.png?download=true"

# Add your links to this list
AUDIO_LINKS = [
    "https://huggingface.co/datasets/MASHOLA/YOUTUBE/resolve/main/MUSIC/WASAFI%20MUSIC%20RADIO.wav?download=true",
    "https://INSERT_YOUR_SECOND_LINK_HERE.wav" 
]

STREAM_URL = "rtmp://a.rtmp.youtube.com/live2/"
STREAM_KEY = "3zy9-9xek-e8vu-ef3z-c77u"
STATE_FILE = "state.txt"

def get_last_index():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return int(f.read().strip())
    return 0

def save_index(index):
    with open(STATE_FILE, "w") as f:
        f.write(str(index))

def start_streaming():
    while True:
        current_index = get_last_index()
        
        # Ensure the index isn't out of bounds if you removed a link
        if current_index >= len(AUDIO_LINKS):
            current_index = 0

        for i in range(current_index, len(AUDIO_LINKS)):
            audio_url = AUDIO_LINKS[i]
            save_index(i) # Save current song index
            
            print(f"Streaming Audio {i+1} of {len(AUDIO_LINKS)}...")

            # FFmpeg Command
            cmd = [
                'ffmpeg',
                '-re',
                '-loop', '1', '-i', IMAGE_URL,
                '-i', audio_url,
                '-filter_complex', 
                "[1:a]showwaves=s=1280x200:mode=line:colors=white@0.8[v_wave];" + 
                "[0:v][v_wave]overlay=0:H-200:format=auto,format=yuv420p[outv]",
                '-map', '[outv]', 
                '-map', '1:a',
                '-c:v', 'libx264', '-preset', 'veryfast', '-b:v', '3000k',
                '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
                '-f', 'flv', f"{STREAM_URL}{STREAM_KEY}"
            ]

            process = subprocess.Popen(cmd)
            process.wait() # Wait for this song to finish
            
            # If it finishes naturally, move to the next
            if i == len(AUDIO_LINKS) - 1:
                save_index(0) # Reset to first song if we hit the end

        print("Playlist finished. Restarting from the beginning...")
        time.sleep(2)

if __name__ == "__main__":
    start_streaming()
