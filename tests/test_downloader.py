import os
import unittest
from pathlib import Path
from unittest.mock import patch

from potube.downloader import build_command, default_output_folder, failure_hints


class DownloaderTests(unittest.TestCase):
    def test_build_command_single_track(self):
        command = build_command(
            yt_dlp_path="/opt/homebrew/bin/yt-dlp",
            url="https://youtu.be/test",
            quality="192",
            playlist=False,
            output_folder=Path("/tmp/music"),
        )

        self.assertIn("--ignore-config", command)
        self.assertIn("--embed-metadata", command)
        self.assertIn("--no-playlist", command)
        self.assertNotIn("--cookies-from-browser", command)
        self.assertEqual(command[-1], "https://youtu.be/test")

    def test_build_command_with_browser_playlist_and_thumbnail(self):
        command = build_command(
            yt_dlp_path="yt-dlp",
            url="https://youtube.com/playlist?list=test",
            quality="320",
            playlist=True,
            output_folder=Path("/tmp/music"),
            browser="safari",
            embed_thumbnail=True,
        )

        self.assertIn("--yes-playlist", command)
        self.assertIn("--embed-thumbnail", command)
        browser_index = command.index("--cookies-from-browser")
        self.assertEqual(command[browser_index + 1], "safari")

    def test_bot_detection_hint_mentions_vpn_and_browser(self):
        hints = failure_hints("Sign in to confirm you’re not a bot")
        text = " ".join(hints).lower()
        self.assertIn("vpn", text)
        self.assertIn("--browser", text)

    @patch.dict(os.environ, {"POTUBE_MUSIC_DIR": "~/CustomPotube"}, clear=False)
    def test_env_output_folder(self):
        self.assertEqual(default_output_folder(), Path("~/CustomPotube").expanduser())


if __name__ == "__main__":
    unittest.main()
