# 🎵 Potube

**Potube** è un semplice downloader audio da YouTube scritto in Python, che converte automaticamente i video in file `.mp3` di alta qualità, salvandoli nella cartella `~/Musica`.

> Basato su [pytubefix](https://pypi.org/project/pytubefix/) e `ffmpeg`.

---

## ⚠️ Avviso legale / Disclaimer

Questo progetto è fornito **solo a scopo didattico e di studio**.

- L’utente è **l’unico responsabile** dell’utilizzo del software e dei contenuti scaricati/convertiti.
- Gli autori e i contributori **non si assumono alcuna responsabilità legale** per eventuali usi impropri, violazioni di copyright, o violazioni dei termini di servizio di piattaforme terze.
- Utilizza questo software **solo** per contenuti di cui possiedi i diritti, per contenuti rilasciati con licenze che ne consentano il download/riuso, o dove hai esplicita autorizzazione.
- In caso di dubbi, **non utilizzare** il software.

L’utilizzo del progetto implica l’accettazione di questo disclaimer.

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
