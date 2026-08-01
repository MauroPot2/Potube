from __future__ import annotations

import os
import platform
import shutil
import subprocess
from collections import deque
from pathlib import Path
from typing import Iterable, Optional

SUPPORTED_QUALITIES = ("128", "192", "256", "320")
SUPPORTED_BROWSERS = (
    "brave",
    "chrome",
    "chromium",
    "edge",
    "firefox",
    "safari",
    "vivaldi",
)


def default_output_folder() -> Path:
    configured = os.environ.get("POTUBE_MUSIC_DIR")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / "Music"


def _resolve_output_folder(output_folder: Optional[str]) -> Path:
    folder = Path(output_folder).expanduser() if output_folder else default_output_folder()
    return folder.resolve()


def _tool_version(executable: str, args: Iterable[str]) -> str:
    try:
        result = subprocess.run(
            [executable, *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return "versione non disponibile"

    text = (result.stdout or result.stderr).strip()
    return text.splitlines()[0] if text else "versione non disponibile"


def doctor(output_folder: Optional[str] = None) -> int:
    """Check the local environment without performing a download."""
    print("\n🩺 Potube doctor\n")

    ok = True
    yt_dlp = shutil.which("yt-dlp")
    ffmpeg = shutil.which("ffmpeg")

    if yt_dlp:
        print(f"✅ yt-dlp: {_tool_version(yt_dlp, ['--version'])}")
    else:
        print("❌ yt-dlp: non trovato (macOS: brew install yt-dlp)")
        ok = False

    if ffmpeg:
        print(f"✅ ffmpeg: {_tool_version(ffmpeg, ['-version'])}")
    else:
        print("❌ ffmpeg: non trovato (macOS: brew install ffmpeg)")
        ok = False

    folder = _resolve_output_folder(output_folder)
    try:
        folder.mkdir(parents=True, exist_ok=True)
        print(f"✅ output: {folder}")
    except OSError as error:
        print(f"❌ output: impossibile usare {folder} ({error})")
        ok = False

    print(f"✅ sistema: {platform.system()} {platform.release()}")
    print("\nTutto pronto." if ok else "\nCi sono problemi da correggere.")
    return 0 if ok else 1


def build_command(
    *,
    yt_dlp_path: str,
    url: str,
    quality: str = "192",
    playlist: bool = False,
    output_folder: Path,
    browser: Optional[str] = None,
    embed_metadata: bool = True,
    embed_thumbnail: bool = False,
) -> list[str]:
    if quality not in SUPPORTED_QUALITIES:
        raise ValueError(
            f"Qualità non supportata: {quality}. "
            f"Valori ammessi: {', '.join(SUPPORTED_QUALITIES)}"
        )

    if browser and browser not in SUPPORTED_BROWSERS:
        raise ValueError(
            f"Browser non supportato: {browser}. "
            f"Valori ammessi: {', '.join(SUPPORTED_BROWSERS)}"
        )

    if playlist:
        output_template = str(
            output_folder
            / "%(playlist_title)s"
            / "%(playlist_index)02d - %(title)s.%(ext)s"
        )
    else:
        output_template = str(output_folder / "%(title)s.%(ext)s")

    command = [
        yt_dlp_path,
        "--ignore-config",
        "--newline",
        "--extract-audio",
        "--audio-format",
        "mp3",
        "--audio-quality",
        f"{quality}K",
        "--output",
        output_template,
    ]

    if embed_metadata:
        command.append("--embed-metadata")

    if embed_thumbnail:
        command.append("--embed-thumbnail")

    if browser:
        command.extend(["--cookies-from-browser", browser])

    command.append("--yes-playlist" if playlist else "--no-playlist")
    command.append(url)
    return command


def failure_hints(output: str, browser: Optional[str] = None) -> list[str]:
    text = output.lower()
    hints: list[str] = []

    if "sign in to confirm you’re not a bot" in text or "sign in to confirm you're not a bot" in text:
        hints.append("Disattiva VPN/proxy: gli IP condivisi vengono spesso bloccati da YouTube.")
        if browser:
            hints.append(f"I cookie di {browser} erano già abilitati; prova ad aggiornare yt-dlp.")
        else:
            hints.append("Se serve autenticazione, riprova con --browser chrome (o il browser che usi).")
    elif "http error 429" in text or "too many requests" in text:
        hints.append("YouTube sta limitando temporaneamente le richieste: evita VPN/proxy e riprova più tardi.")
    elif "video unavailable" in text or "private video" in text:
        hints.append("Il video può essere privato, rimosso, con restrizioni geografiche o non disponibile.")
    elif "unsupported url" in text:
        hints.append("Controlla l'URL: Potube è pensato principalmente per URL YouTube/YouTube Music.")
    else:
        hints.append("Aggiorna yt-dlp e riprova: brew upgrade yt-dlp")

    return hints


def download_audio_from_url(
    url: str,
    quality: str = "192",
    playlist: bool = False,
    output_folder: Optional[str] = None,
    browser: Optional[str] = None,
    embed_metadata: bool = True,
    embed_thumbnail: bool = False,
) -> int:
    if not url or not url.strip():
        print("\n❌ URL mancante.")
        return 2

    yt_dlp_path = shutil.which("yt-dlp")
    if not yt_dlp_path:
        print("\n❌ yt-dlp non è installato.\nSu macOS: brew install yt-dlp")
        return 1

    if not shutil.which("ffmpeg"):
        print("\n❌ ffmpeg non è installato.\nSu macOS: brew install ffmpeg")
        return 1

    folder = _resolve_output_folder(output_folder)
    try:
        folder.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"\n❌ Impossibile creare la cartella di output {folder}: {error}")
        return 1

    command = build_command(
        yt_dlp_path=yt_dlp_path,
        url=url.strip(),
        quality=quality,
        playlist=playlist,
        output_folder=folder,
        browser=browser,
        embed_metadata=embed_metadata,
        embed_thumbnail=embed_thumbnail,
    )

    mode = "playlist" if playlist else "brano"
    print(f"\n🎵 Potube — download {mode}")
    print(f"🎚️ MP3: {quality} kbps")
    print(f"📁 Output: {folder}")
    if browser:
        print(f"🍪 Cookie browser: {browser}")
    print()

    recent_output: deque[str] = deque(maxlen=100)
    process: Optional[subprocess.Popen[str]] = None

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        if process.stdout is not None:
            for line in process.stdout:
                print(line, end="")
                recent_output.append(line)

        return_code = process.wait()
    except KeyboardInterrupt:
        if process and process.poll() is None:
            process.terminate()
        print("\n\n⏹️ Download annullato.")
        return 130
    except OSError as error:
        print(f"\n❌ Impossibile avviare yt-dlp: {error}")
        return 1

    if return_code != 0:
        print("\n❌ Download non riuscito.")
        for hint in failure_hints("".join(recent_output), browser=browser):
            print(f"   • {hint}")
        print("   • Diagnostica ambiente: potube --doctor")
        return return_code or 1

    print(f"\n✅ Download completato.\n📁 {folder}")
    return 0
