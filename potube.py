import os
import subprocess
import re
from pytubefix import YouTube


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = bytes_downloaded / total_size * 100
    print(f"Download progress: {percentage:.2f}%", end='\r')


# Percorso assoluto alla cartella ~/Musica
output_folder = os.path.expanduser("~/Musica")

# Crea la cartella se non esiste
os.makedirs(output_folder, exist_ok=True)

# Richiesta URL
url = input("Inserisci l'URL del video: ")

# Inizializza oggetto YouTube con callback di progresso
yt = YouTube(url, on_progress_callback=on_progress)

# Pulisce il titolo del video per usarlo come nome file valido
safe_title = re.sub(r'[\\/*?:"<>|]', "", yt.title).strip()

print(f"Titolo del video: {yt.title}")

# Scarica il file audio (nella directory corrente)
audio_file = yt.streams.get_audio_only().download(filename=f"{safe_title}.webm")

# Percorso completo del file MP3 di destinazione
mp3_file = os.path.join(output_folder, f"{safe_title}.mp3")

# Comando ffmpeg per la conversione
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

# Esegui ffmpeg
subprocess.run(command)

# Elimina il file originale .webm
os.remove(audio_file)

print(f"\n✅ Audio convertito e salvato in: {mp3_file}")
