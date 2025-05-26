# 🎵 Potube

**Potube** è un semplice downloader audio da YouTube scritto in Python, che converte automaticamente i video in file `.mp3` di alta qualità, salvandoli nella cartella `~/Musica`.

> Basato su [pytubefix](https://pypi.org/project/pytubefix/) e `ffmpeg`.

---

## 🖥️ Requisiti

- Python 3.9 o superiore
- `ffmpeg` installato nel sistema
- Sistema operativo Linux o compatibile (testato su Ubuntu/Zorin/EndeavourOS)

---

## ⚙️ Installazione

Clona il repository e installa le dipendenze in un ambiente virtuale:

```bash
git clone https://github.com/MauroPot2/potube.git
cd potube
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
