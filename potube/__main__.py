# potube/__main__.py
import argparse

from potube.downloader import download_audio_from_url


def main():
    parser = argparse.ArgumentParser(
        description="Scarica audio da YouTube e convertilo in MP3"
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="URL del video o della playlist YouTube",
    )
    parser.add_argument(
        "--url",
        dest="legacy_url",
        help="Compatibilità con la vecchia sintassi: potube --url URL",
    )
    parser.add_argument(
        "-q",
        "--quality",
        choices=("128", "192", "256", "320"),
        default="192",
        help="Bitrate MP3 in kbps (default: 192)",
    )
    parser.add_argument(
        "-p",
        "--playlist",
        action="store_true",
        help="Scarica l'intera playlist invece del solo video",
    )

    args = parser.parse_args()

    if args.url and args.legacy_url:
        parser.error("Usa l'URL posizionale oppure --url, non entrambi.")

    url = args.url or args.legacy_url
    if not url:
        parser.error("Devi specificare un URL YouTube.")

    return download_audio_from_url(
        url=url,
        quality=args.quality,
        playlist=args.playlist,
    )


if __name__ == "__main__":
    raise SystemExit(main())
