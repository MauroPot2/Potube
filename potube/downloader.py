# potube/downloader.py
import os
import subprocess
import re
from pytubefix import YouTube


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    downloaded = total_size - bytes_remaining
    percent = downloaded / total_size * 100
    print(f"Download progress: {percent:.2f}%", end='\r')


def download_audio_from_url(url):
    yt = YouTube(url, on_progress_callback=on_progress)
    safe_title = re.sub(r'[\\/*?:"<>|]', "", yt.title).strip()
    print(f"\nTitolo del video: {yt.title}")

    audio_file = yt.streams.get_audio_only().download(filename=f"{safe_title}.webm")
    output_folder = os.path.expanduser("~/Musica")
    os.makedirs(output_folder, exist_ok=True)
    mp3_file = os.path.join(output_folder, f"{safe_title}.mp3")

    command = [
        "ffmpeg",
        "-i", audio_file,
        "-vn",
        "-acodec", "libmp3lame",
        "-ar", "44100",
        "-ac", "2",
        "-ab", "192k",
        "-y",
        mp3_file
    ]

    subprocess.run(command)
    os.remove(audio_file)
    print(f"\n✅ Salvato in: {mp3_file}")
