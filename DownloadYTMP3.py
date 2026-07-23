import yt_dlp
import os

# Définition de l'arborescence du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(BASE_DIR, "MusiquesInstallees")
COVER_DIR = os.path.join(BASE_DIR, "CoverSiBesoin")
MP3TAG_DIR = os.path.join(BASE_DIR, "Mp3tagSiBesoin")

def init_folders():
    """Crée les dossiers nécessaires au projet s'ils n'existent pas déjà."""
    for folder in [MUSIC_DIR, COVER_DIR, MP3TAG_DIR]:
        os.makedirs(folder, exist_ok=True)

def download_media(url, audio_only=True):
    try:
        # Options communes de base
        ydl_opts = {
            'outtmpl': os.path.join(MUSIC_DIR, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'writethumbnail': True,  # Télécharge la miniature pour la cover
            'quiet': False,
        }

        if audio_only:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [
                    {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
                    {'key': 'FFmpegMetadata', 'add_metadata': True},
                    {'key': 'EmbedThumbnail', 'already_have_thumbnail': False},
                ],
            })
        else:
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'postprocessors': [
                    {'key': 'FFmpegMetadata', 'add_metadata': True},
                    {'key': 'EmbedThumbnail', 'already_have_thumbnail': False},
                ],
            })

        print("\n⏳ Téléchargement et traitement en cours...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"✅ Téléchargement terminé ! (Fichier sauvegardé dans '{MUSIC_DIR}')")

    except Exception as e:
        print(f"❌ Erreur lors du téléchargement : {e}")

if __name__ == "__main__":
    print("🎵 Outil de téléchargement YouTube (MP3/MP4) optimisé 🎵")
    
    # Création automatique de la structure des dossiers
    init_folders()
    
    print(f"📁 Vos musiques seront enregistrées dans : {MUSIC_DIR}")
    print(f"🖼️  Dossier pour vos covers personnalisées : {COVER_DIR}")
    print(f"🏷️  Dossier pour l'outil Mp3tag (si besoin) : {MP3TAG_DIR}")

    while True:
        url = input("\nEntrez l'URL YouTube ('q' pour quitter) : ").strip()
        if url.lower() == 'q':
            print("👋 Fin du programme.")
            break

        choix = input("Télécharger en MP3 (1) ou MP4 (2) ? ").strip()
        audio_only = choix == "1"

        download_media(url, audio_only)