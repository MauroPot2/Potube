# setup.py
from setuptools import setup, find_packages

setup(
    name='potube',
    version='1.0.0',
    description='Scarica e converti video YouTube in MP3',
    author='Mauro Potestio',
    author_email='tuo@email.it',
    packages=find_packages(),
    install_requires=[
        'pytubefix'
    ],
    entry_points={
        'console_scripts': [
            'potube = potube.__main__:main'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
