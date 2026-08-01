from __future__ import annotations

import argparse
from typing import Optional, Sequence

from potube import __version__
from potube.downloader import (
    SUPPORTED_BROWSERS,
    SUPPORTED_QUALITIES,
    doctor,
    download_audio_from_url,
)


EXAMPLES = """examples:
  potube "https://www.youtube.com/watch?v=VIDEO_ID"
  potube "URL" -q 320
  potube "URL_PLAYLIST" --playlist
  potube "URL" --output ~/Downloads/Music
  potube "URL" --browser chrome
  potube --doctor
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="potube",
        description="Scarica audio da YouTube e convertilo in MP3 con yt-dlp.",
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="URL del video o della playlist YouTube",
    )
    parser.add_argument(
        "--url",
        dest="legacy_url",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-q",
        "--quality",
        choices=SUPPORTED_QUALITIES,
        default="192",
        help="bitrate MP3 di ricodifica in kbps (default: 192)",
    )
    parser.add_argument(
        "-p",
        "--playlist",
        action="store_true",
        help="scarica l'intera playlist; senza questa opzione scarica un solo video",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="DIR",
        help="cartella di destinazione (default: ~/Music o $POTUBE_MUSIC_DIR)",
    )
    parser.add_argument(
        "--browser",
        choices=SUPPORTED_BROWSERS,
        help="usa i cookie del browser, solo quando YouTube richiede autenticazione",
    )
    parser.add_argument(
        "--thumbnail",
        action="store_true",
        help="incorpora la miniatura come cover art (se supportato dall'ambiente)",
    )
    parser.add_argument(
        "--no-metadata",
        action="store_false",
        dest="metadata",
        default=True,
        help="non incorporare metadata nel file MP3",
    )
    parser.add_argument(
        "--doctor",
        action="store_true",
        help="controlla yt-dlp, ffmpeg e la cartella di output, poi esce",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"Potube {__version__}",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.doctor:
        return doctor(output_folder=args.output)

    if args.url and args.legacy_url:
        parser.error("Usa l'URL posizionale oppure --url, non entrambi.")

    url = args.url or args.legacy_url
    if not url:
        parser.error("Devi specificare un URL oppure usare --doctor.")

    return download_audio_from_url(
        url=url,
        quality=args.quality,
        playlist=args.playlist,
        output_folder=args.output,
        browser=args.browser,
        embed_metadata=args.metadata,
        embed_thumbnail=args.thumbnail,
    )


if __name__ == "__main__":
    raise SystemExit(main())
