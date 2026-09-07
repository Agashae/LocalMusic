import os

import yt_dlp

# Définition de l'arborescence du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(BASE_DIR, "MusiquesInstallees")
COVER_DIR = os.path.join(BASE_DIR, "CoverSiBesoin")
MP3TAG_DIR = os.path.join(BASE_DIR, "Mp3tagSiBesoin")

# YouTube renvoie parfois 403 Forbidden au client "web" par défaut de yt-dlp
# (vérifications de signature renforcées). Se faire passer pour le client
# "android" en plus du "web" contourne la majorité de ces blocages.
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
COOKIES_FILE = os.environ.get("YTDLP_COOKIES_FILE")
COOKIES_FROM_BROWSER = os.environ.get("YTDLP_COOKIES_FROM_BROWSER")


def init_folders():
    """Crée les dossiers nécessaires au projet s'ils n'existent pas déjà."""
    for folder in [MUSIC_DIR, COVER_DIR, MP3TAG_DIR]:
        os.makedirs(folder, exist_ok=True)


def build_ydl_opts(audio_only=True, outtmpl=None, embed_thumbnail=True):
    """Construit les options yt-dlp communes (téléchargement manuel et import Spotify)."""
    ydl_opts = {
        'outtmpl': outtmpl or os.path.join(MUSIC_DIR, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'writethumbnail': embed_thumbnail,
        'quiet': False,
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'http_headers': {'User-Agent': USER_AGENT},
        'retries': 10,
        'fragment_retries': 10,
        'nocheckcertificate': True,
    }

    if COOKIES_FILE:
        ydl_opts['cookiefile'] = COOKIES_FILE
    elif COOKIES_FROM_BROWSER:
        ydl_opts['cookiesfrombrowser'] = (COOKIES_FROM_BROWSER,)

    thumbnail_pp = [{'key': 'EmbedThumbnail', 'already_have_thumbnail': False}] if embed_thumbnail else []

    if audio_only:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
                {'key': 'FFmpegMetadata', 'add_metadata': True},
            ] + thumbnail_pp,
        })
    else:
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'postprocessors': [
                {'key': 'FFmpegMetadata', 'add_metadata': True},
            ] + thumbnail_pp,
        })

    return ydl_opts


def download_media(url, audio_only=True):
    try:
        ydl_opts = build_ydl_opts(audio_only=audio_only)

        print("\n⏳ Téléchargement et traitement en cours...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"✅ Téléchargement terminé ! (Fichier sauvegardé dans '{MUSIC_DIR}')")
        return True

    except yt_dlp.utils.DownloadError as e:
        if "403" in str(e) or "Forbidden" in str(e):
            print(
                "❌ Erreur 403 Forbidden : YouTube bloque la requête.\n"
                "   → Mettez d'abord yt-dlp à jour : pip install -U yt-dlp\n"
                "   → Si ça persiste, fournissez vos cookies YouTube en définissant\n"
                "     la variable d'environnement YTDLP_COOKIES_FROM_BROWSER=chrome\n"
                "     (ou firefox/edge...) avant de relancer le script."
            )
        else:
            print(f"❌ Erreur lors du téléchargement : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement : {e}")
        return False


def run_menu():
    print("🎵 Outil de téléchargement YouTube (MP3/MP4) optimisé 🎵")

    init_folders()

    print(f"📁 Vos musiques seront enregistrées dans : {MUSIC_DIR}")
    print(f"🖼️  Dossier pour vos covers personnalisées : {COVER_DIR}")
    print(f"🏷️  Dossier pour l'outil Mp3tag (si besoin) : {MP3TAG_DIR}")

    while True:
        print("\n1) Télécharger une URL YouTube")
        print("2) Importer mes titres likés Spotify (en MP3)")
        print("q) Quitter")
        choix = input("Votre choix : ").strip().lower()

        if choix == 'q':
            print("👋 Fin du programme.")
            break

        elif choix == '1':
            url = input("Entrez l'URL YouTube : ").strip()
            if not url:
                continue
            fmt = input("Télécharger en MP3 (1) ou MP4 (2) ? ").strip()
            download_media(url, audio_only=(fmt != '2'))

        elif choix == '2':
            try:
                from spotify_liked_songs import import_liked_songs
            except ImportError as e:
                print(f"❌ Le module Spotify n'est pas disponible : {e}")
                print("   Installez les dépendances : pip install -r requirements.txt")
                continue
            import_liked_songs()

        else:
            print("Choix invalide.")


if __name__ == "__main__":
    run_menu()
