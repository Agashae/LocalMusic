# 🎵 YouTube Music Downloader

Un projet simple et efficace pour télécharger des musiques et vidéos depuis YouTube en local (pour PC et iPhone).  
Ce script télécharge la musique, la convertit au format idéal (MP3 ou MP4 pour iPhone), ajoute les métadonnées de base (Titre, Artiste) et intègre automatiquement la miniature YouTube comme pochette (Cover Art).

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

1. Lancez le script en double-cliquant sur `DownloadYTMP3.py` ou via un terminal :
   ```bash
   python DownloadYTMP3.py
   ```
2. Collez l'URL YouTube de votre choix lorsqu'on vous le demande.
3. Choisissez le format : tapez `1` pour MP3 (Audio) ou `2` pour MP4 (Vidéo optimisée iPhone).
4. Le téléchargement se lance, et vous retrouverez votre fichier prêt à l'emploi (avec pochette et métadonnées) dans le dossier `Musique/` !

## 🎨 Modification manuelle (via Mp3tag)

Le script automatise le maximum de choses, mais si la pochette ou le titre récupéré par YouTube ne vous convient pas, tout est prévu :
1. Placez l'image de votre choix dans le dossier `Cover/`.
2. Lancez **Mp3tag** depuis le dossier `Mp3tag/` (si vous y avez bien ajouté la version portable).
3. Glissez-déposez votre MP3 fraîchement téléchargé (situé dans `Musique/`) dans Mp3tag.
4. Modifiez le titre, l'artiste, et ajoutez votre nouvelle image depuis le dossier `Cover/`, puis sauvegardez !

## 📄 Licence
Ce projet est libre de droits. N'hésitez pas à le modifier ou l'améliorer selon vos besoins !
