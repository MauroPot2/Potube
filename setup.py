# setup.py
from setuptools import setup, find_packages

setup(
    name="potube",
    version="1.1.0",
    description="Scarica audio da YouTube e convertilo in MP3 tramite yt-dlp",
    author="Mauro Potestio",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "potube = potube.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
