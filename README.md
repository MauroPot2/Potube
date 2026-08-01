# 🎵 Potube

**Potube** è una CLI Python per scaricare audio da YouTube e convertirlo automaticamente in MP3 tramite `yt-dlp` e `ffmpeg`.

I file vengono salvati nella cartella `~/Music` su macOS/Linux.

---

## ⚠️ Avviso legale / Disclaimer

Questo progetto è fornito **solo a scopo didattico e di studio**.

- L’utente è l’unico responsabile dell’utilizzo del software e dei contenuti scaricati/convertiti.
- Utilizza il software solo per contenuti di cui possiedi i diritti, rilasciati con licenze compatibili o per cui hai esplicita autorizzazione.
- Gli autori e i contributori non si assumono responsabilità per usi impropri o violazioni di copyright o termini di servizio di piattaforme terze.

---

## 🖥️ Requisiti

- Python 3.9 o superiore
- `yt-dlp`
- `ffmpeg`

### macOS

Con Homebrew:

```bash
brew install yt-dlp ffmpeg
```

### Linux

Installa `yt-dlp` e `ffmpeg` usando il package manager della tua distribuzione.

---

## ⚙️ Installazione

```bash
git clone https://github.com/MauroPot2/Potube.git
cd Potube
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## 🚀 Uso

### Scaricare un singolo brano

```bash
potube "https://www.youtube.com/watch?v=VIDEO_ID"
```

Qualità predefinita: **192 kbps**.

### Scegliere la qualità MP3

```bash
potube "URL" --quality 320
```

Qualità disponibili:

- `128`
- `192`
- `256`
- `320`

Forma abbreviata:

```bash
potube "URL" -q 320
```

### Scaricare una playlist

```bash
potube "URL_PLAYLIST" --playlist
```

oppure:

```bash
potube "URL_PLAYLIST" -p
```

Le playlist vengono salvate in una sottocartella con il nome della playlist e i brani vengono numerati automaticamente.

### Playlist a 320 kbps

```bash
potube "URL_PLAYLIST" --playlist --quality 320
```

---

## ♻️ Compatibilità con la vecchia sintassi

La vecchia forma continua a funzionare:

```bash
potube --url "URL"
```

La sintassi consigliata è però:

```bash
potube "URL"
```

---

## 📁 Output

Su macOS e Linux i file vengono salvati in:

```text
~/Music
```

Per una playlist:

```text
~/Music/Nome Playlist/
01 - Titolo.mp3
02 - Titolo.mp3
...
```

---

## 🔧 Risoluzione problemi

Se YouTube mostra errori di bot detection o autenticazione:

- prova senza VPN o proxy;
- aggiorna `yt-dlp`;
- verifica che la connessione non utilizzi un IP condiviso/bloccato.

Aggiornamento Homebrew:

```bash
brew upgrade yt-dlp
```

Verifica installazione:

```bash
yt-dlp --version
ffmpeg -version
```
