import unittest
from unittest.mock import patch

from potube.__main__ import main


class CliTests(unittest.TestCase):
    @patch("potube.__main__.download_audio_from_url")
    def test_positional_url_and_options(self, download):
        download.return_value = 0

        code = main(
            [
                "https://www.youtube.com/watch?v=test",
                "-q",
                "320",
                "--playlist",
                "--output",
                "~/Downloads/Music",
                "--browser",
                "chrome",
                "--thumbnail",
                "--no-metadata",
            ]
        )

        self.assertEqual(code, 0)
        download.assert_called_once_with(
            url="https://www.youtube.com/watch?v=test",
            quality="320",
            playlist=True,
            output_folder="~/Downloads/Music",
            browser="chrome",
            embed_metadata=False,
            embed_thumbnail=True,
        )

    @patch("potube.__main__.download_audio_from_url")
    def test_legacy_url_still_works(self, download):
        download.return_value = 0
        code = main(["--url", "https://youtu.be/test"])
        self.assertEqual(code, 0)
        self.assertEqual(download.call_args.kwargs["url"], "https://youtu.be/test")

    @patch("potube.__main__.doctor")
    def test_doctor_does_not_require_url(self, doctor):
        doctor.return_value = 0
        self.assertEqual(main(["--doctor"]), 0)
        doctor.assert_called_once_with(output_folder=None)


if __name__ == "__main__":
    unittest.main()
