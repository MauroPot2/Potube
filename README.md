# 🎵 Potube

**Potube** è una piccola CLI Python per scaricare l'audio di contenuti YouTube consentiti e convertirlo in MP3 tramite `yt-dlp` e `ffmpeg`.

È pensato per essere rapido da usare dal Terminale su macOS e Linux:

```bash
potube "https://www.youtube.com/watch?v=VIDEO_ID"
```

> Usa Potube solo per contenuti di cui possiedi i diritti, contenuti con licenza che ne consenta il download/riuso o contenuti per cui hai esplicita autorizzazione. Sei responsabile del rispetto del copyright e dei termini dei servizi utilizzati.

## Requisiti

- Python 3.9+
- `yt-dlp`
- `ffmpeg`

Su macOS con Homebrew:

```bash
brew install yt-dlp ffmpeg pipx
```

## Installazione consigliata su macOS

Per avere `potube` disponibile globalmente in ogni Terminale:

```bash
cd ~/Documents/Potube
pipx install -e .
```

Se Potube era già installato con `pipx`, dopo un aggiornamento del repository basta normalmente:

```bash
cd ~/Documents/Potube
git pull
```

Con installazione editable, il comando globale usa il codice aggiornato.

In alternativa, per sviluppo locale:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Uso

Scarica un singolo brano a 192 kbps:

```bash
potube "URL"
```

Scegli il bitrate MP3:

```bash
potube "URL" -q 320
```

Valori disponibili: `128`, `192`, `256`, `320`.

**Nota sulla qualità:** impostare 320 kbps non aggiunge dettaglio che non esiste nella sorgente YouTube. Indica il bitrate della ricodifica MP3; una sorgente compressa non diventa lossless o di qualità superiore ricodificandola a un bitrate maggiore.

Scarica una playlist:

```bash
potube "URL_PLAYLIST" --playlist
```

Scegli una cartella diversa:

```bash
potube "URL" --output ~/Downloads/Music
```

Puoi anche impostare una destinazione predefinita:

```bash
export POTUBE_MUSIC_DIR="$HOME/Downloads/Music"
```

Per incorporare la miniatura come cover art:

```bash
potube "URL" --thumbnail
```

I metadata vengono incorporati di default. Per disabilitarli:

```bash
potube "URL" --no-metadata
```

## Bot detection e autenticazione

Per i contenuti pubblici prova prima **senza cookie**. Se YouTube risponde con `Sign in to confirm you're not a bot`:

1. disattiva eventuali VPN/proxy;
2. aggiorna `yt-dlp`;
3. solo se necessario, usa i cookie del tuo browser.

Esempio:

```bash
potube "URL" --browser chrome
```

Sono supportati `brave`, `chrome`, `chromium`, `edge`, `firefox`, `safari` e `vivaldi`.

`--browser` passa a `yt-dlp` l'opzione `--cookies-from-browser`; usala soltanto quando serve, perché consente al processo di leggere i cookie del profilo browser selezionato.

## Diagnostica

```bash
potube --doctor
```

Controlla:

- presenza e versione di `yt-dlp`;
- presenza e versione di `ffmpeg`;
- accessibilità della cartella di output;
- sistema operativo.

Versione Potube:

```bash
potube --version
```

Help completo:

```bash
potube --help
```

## Output

Default:

```text
~/Music
```

Singolo brano:

```text
~/Music/Titolo.mp3
```

Playlist:

```text
~/Music/Nome Playlist/
01 - Titolo.mp3
02 - Titolo.mp3
...
```

## Risoluzione problemi

Aggiorna `yt-dlp` installato con Homebrew:

```bash
brew upgrade yt-dlp
```

Se compare bot detection, la prima cosa da controllare è una VPN/proxy o un IP condiviso. Se il problema resta, prova `--browser chrome` (o il browser che usi). `yt-dlp` supporta ufficialmente l'estrazione dei cookie dal browser per i casi in cui è richiesta autenticazione.

Se qualcosa non torna:

```bash
potube --doctor
```

## Sviluppo

Esegui i test:

```bash
python -m unittest discover -s tests -v
```

Il repository esegue gli stessi test con GitHub Actions su Python 3.9 e 3.13.

## Compatibilità

La vecchia sintassi resta accettata:

```bash
potube --url "URL"
```

La forma consigliata è:

```bash
potube "URL"
```
