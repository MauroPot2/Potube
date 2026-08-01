# potube/downloader.py
import os
import shutil
import subprocess


SUPPORTED_QUALITIES = {"128", "192", "256", "320"}


def download_audio_from_url(url, quality="192", playlist=False):
    if quality not in SUPPORTED_QUALITIES:
        raise ValueError(
            f"Qualità non supportata: {quality}. "
            f"Valori ammessi: {', '.join(sorted(SUPPORTED_QUALITIES))}"
        )

    output_folder = os.path.expanduser("~/Music")
    os.makedirs(output_folder, exist_ok=True)

    if playlist:
        output_template = os.path.join(
            output_folder,
            "%(playlist_title)s",
            "%(playlist_index)02d - %(title)s.%(ext)s",
        )
    else:
        output_template = os.path.join(
            output_folder,
            "%(title)s.%(ext)s",
        )

    yt_dlp_path = shutil.which("yt-dlp")
    if not yt_dlp_path:
        print(
            "\n❌ yt-dlp non è installato."
            "\nSu macOS installalo con:"
            "\n\nbrew install yt-dlp"
        )
        return 1

    if not shutil.which("ffmpeg"):
        print(
            "\n❌ ffmpeg non è installato."
            "\nSu macOS installalo con:"
            "\n\nbrew install ffmpeg"
        )
        return 1

    command = [
        yt_dlp_path,
        "--extract-audio",
        "--audio-format",
        "mp3",
        "--audio-quality",
        f"{quality}K",
        "--output",
        output_template,
    ]

    command.append("--yes-playlist" if playlist else "--no-playlist")
    command.append(url)

    mode = "playlist" if playlist else "brano"
    print(
        f"\n🎵 Download {mode} in corso..."
        f"\n🎚️ Qualità: {quality} kbps\n"
    )

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as error:
        print(
            "\n❌ Download non riuscito."
            f"\nCodice errore: {error.returncode}"
            "\nVerifica la connessione, disattiva eventuali VPN/proxy "
            "e riprova."
        )
        return error.returncode or 1

    print(
        "\n✅ Download completato."
        f"\n📁 File salvato in: {output_folder}"
    )
    return 0
