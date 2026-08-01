# Changelog

## 1.2.0

- nuova diagnostica `potube --doctor`
- cartella di destinazione configurabile con `--output` o `POTUBE_MUSIC_DIR`
- supporto opzionale ai cookie del browser con `--browser`
- metadata MP3 incorporati di default e cover opzionale con `--thumbnail`
- gestione mirata degli errori di bot detection, rate limit e video non disponibili
- `potube --version`
- packaging moderno tramite `pyproject.toml`
- test automatici e GitHub Actions su Python 3.9 e 3.13
- compatibilità mantenuta con la vecchia sintassi `potube --url URL`

## 1.1.0

- migrazione da `pytubefix` a `yt-dlp`
- nuova sintassi `potube URL`
- qualità MP3 selezionabile
- supporto playlist
