import os
import subprocess
from pytubefix import YouTube
from pytubefix.cli import on_progress

# URL del video YouTube
url = input("Inserisci l'URL del video: ")

# Creazione dell'oggetto YouTube e download dell'audio
yt = YouTube(url, on_progress_callback=on_progress)
print(f"Titolo del video: {yt.title}")

# Ottieni solo il flusso audio
ys = yt.streams.get_audio_only()

# Scarica l'audio
audio_file = ys.download(filename=yt.title)

# Percorso di destinazione per il file MP3
mp3_file = audio_file.replace(".webm", ".mp3")

# Converte il file .webm in .mp3 usando ffmpeg
command = [
    "ffmpeg",
    "-i", audio_file,   # Input file (il file .webm)
    "-vn",              # No video
    "-acodec", "libmp3lame",  # Codifica in mp3
    "-ar", "44100",      # Frequenza di campionamento (opzionale)
    "-ac", "2",          # Canali stereo
    "-ab", "192k",       # Bitrate
    mp3_file             # File di output
]

# Esegui il comando ffmpeg
subprocess.run(command)

# Rimuovi il file originale per liberare spazio
os.remove(audio_file)

print(f"Audio convertito e salvato come: {yt.title}")
