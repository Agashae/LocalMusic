# 🎵 YouTube Music Downloader

Un projet simple et efficace pour télécharger des musiques et vidéos depuis YouTube en local (pour PC et iPhone).  
Ce script télécharge la musique, la convertit au format idéal (MP3 ou MP4 pour iPhone), ajoute les métadonnées de base (Titre, Artiste) et intègre automatiquement la miniature YouTube comme pochette (Cover Art).

Il permet aussi d'importer directement vos **titres likés Spotify** : chaque titre est recherché sur YouTube, téléchargé en MP3, puis retagué avec les vraies métadonnées Spotify (titre, artiste, album, pochette).

## 📁 Structure du Projet

L'arborescence a été pensée pour être propre et centralisée. Chaque dossier a un rôle précis :

- `DownloadYTMP3.py` : Le script principal à exécuter.
- `MusiquesInstallees/` : Le dossier où toutes vos musiques/vidéos téléchargées seront automatiquement sauvegardées.
- `CoverSiBesoin/` : Un dossier dédié pour y stocker vos propres images de pochettes d'albums. Utile si l'utilisateur souhaite changer la pochette automatiquement récupérée sur YouTube et souhaite centraliser ses images.
- `Mp3tagSiBesoin/` : Un dossier prévu pour que l'utilisateur y place lui-même la **version portable de Mp3Tag** (téléchargeable ici : [Mp3Tag Portable](https://www.mp3tag.de/en/portable.html)). Cela permet d'avoir l'outil de modification de métadonnées directement sous la main, au sein même du projet !

*(Note: Ces dossiers sont générés automatiquement au premier lancement du script si vous ne les avez pas créés.)*

## ⚙️ Prérequis

Avant de pouvoir utiliser ce projet, vous devez vous assurer d'avoir les éléments suivants :

1. **Python 3** : Assurez-vous d'avoir Python installé sur votre machine.
2. **FFmpeg** : Requis par `yt-dlp` pour la conversion en MP3 et l'incrustation des pochettes.
   - Sur Windows : Téléchargez-le (ex: via [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)) et ajoutez-le à vos variables d'environnement (`PATH`).
3. **yt-dlp** : La librairie Python qui gère le téléchargement.

### Installation de la librairie Python

Ouvrez un terminal dans le dossier du projet et exécutez la commande suivante :

```bash
pip install -r requirements.txt
```

## 🚀 Utilisation

1. Lancez le script via un terminal :
   ```bash
   python DownloadYTMP3.py
   ```
2. Un menu s'affiche :
   - **1)** Télécharger une URL YouTube précise (MP3 ou MP4).
   - **2)** Importer tous vos titres likés Spotify en MP3 (voir ci-dessous).
3. Vous retrouverez vos fichiers prêts à l'emploi (avec pochette et métadonnées) dans le dossier `MusiquesInstallees/` !

### ❌ Erreur "HTTP Error 403: Forbidden"

Cette erreur vient de YouTube qui bloque certaines requêtes de yt-dlp. Le script contourne déjà la majorité des cas (client Android + en-têtes navigateur), mais si l'erreur persiste :

1. Mettez à jour yt-dlp, YouTube change régulièrement ses protections :
   ```bash
   pip install -U yt-dlp
   ```
2. Si ça ne suffit pas, donnez au script l'accès à vos cookies YouTube (vous devez être connecté dans le navigateur choisi) :
   ```bash
   # Windows (PowerShell)
   $env:YTDLP_COOKIES_FROM_BROWSER="chrome"
   # macOS / Linux
   export YTDLP_COOKIES_FROM_BROWSER=chrome
   ```
   Vous pouvez aussi définir cette variable dans votre fichier `.env` (voir `.env.example`).

## 🎧 Importer vos titres likés Spotify

Spotify ne permet pas de télécharger l'audio brut (ce serait contraire à ses conditions d'utilisation). À la place, le script :
1. Se connecte à votre compte Spotify (OAuth) pour lister vos "Titres likés".
2. Cherche l'équivalent de chaque titre sur YouTube et le télécharge en MP3.
3. Retague le MP3 avec le vrai titre/artiste/album/pochette venant de Spotify (plus fiable que le titre YouTube).
4. Passe automatiquement les titres déjà téléchargés si vous relancez l'import plus tard.

### Configuration (une seule fois)

1. Créez une application sur le [tableau de bord développeur Spotify](https://developer.spotify.com/dashboard).
2. Dans les paramètres de l'app, ajoutez l'URI de redirection : `http://127.0.0.1:8888/callback`.
3. Copiez `.env.example` en `.env` puis renseignez `SPOTIFY_CLIENT_ID` et `SPOTIFY_CLIENT_SECRET` (visibles sur le tableau de bord).
4. Installez les dépendances si ce n'est pas déjà fait : `pip install -r requirements.txt`.

### Lancement

```bash
python DownloadYTMP3.py
```
Choisissez ensuite l'option `2`. Une fenêtre de navigateur s'ouvre pour autoriser l'accès à votre bibliothèque Spotify (lecture seule), puis l'import démarre automatiquement.

## 🎨 Modification manuelle (via Mp3tag)

Le script automatise le maximum de choses, mais si la pochette ou le titre récupéré par YouTube ne vous convient pas, tout est prévu :
1. Placez l'image de votre choix dans le dossier `Cover/`.
2. Lancez **Mp3tag** depuis le dossier `Mp3tag/` (si vous y avez bien ajouté la version portable).
3. Glissez-déposez votre MP3 fraîchement téléchargé (situé dans `Musique/`) dans Mp3tag.
4. Modifiez le titre, l'artiste, et ajoutez votre nouvelle image depuis le dossier `Cover/`, puis sauvegardez !

## 📄 Licence
Ce projet est libre de droits. N'hésitez pas à le modifier ou l'améliorer selon vos besoins !
