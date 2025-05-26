# potube/__main__.py
import argparse
from potube.downloader import download_audio_from_url


def main():
    parser = argparse.ArgumentParser(description="Scarica e converti un video YouTube in MP3")
    parser.add_argument('--url', required=True, help='URL del video YouTube')
    args = parser.parse_args()

    download_audio_from_url(args.url)


if __name__ == "__main__":
    main()
