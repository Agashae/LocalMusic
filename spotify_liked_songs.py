"""Importe les titres likés d'un compte Spotify et les télécharge en MP3.

Le contenu audio de Spotify n'est jamais accessible directement : pour chaque
titre liké, on recherche le meilleur résultat correspondant sur YouTube (via
yt-dlp) puis on retague le MP3 obtenu avec les vraies métadonnées Spotify
(titre, artiste, album, pochette).
"""

import os
import re
import time
import urllib.request

import yt_dlp

import DownloadYTMP3 as core

SCOPE = "user-library-read"
INVALID_CHARS = re.compile(r'[\\/*?:"<>|]')


def _sanitize(name):
    return INVALID_CHARS.sub("", name).strip()


def _get_spotify_client():
    try:
        import spotipy
        from spotipy.oauth2 import SpotifyOAuth
    except ImportError as e:
        raise RuntimeError(
            "spotipy n'est pas installé. Lancez : pip install -r requirements.txt"
        ) from e

    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")

    if not client_id or not client_secret:
        raise RuntimeError(
            "SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET manquants.\n"
            "   Créez une app sur https://developer.spotify.com/dashboard puis\n"
            "   renseignez ces valeurs dans un fichier .env (voir .env.example)."
        )

    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=SCOPE,
        cache_path=os.path.join(core.BASE_DIR, ".spotify_cache"),
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def fetch_liked_tracks(sp):
    """Récupère la liste complète des titres de la bibliothèque Spotify (Titres likés)."""
    tracks = []
    limit = 50
    offset = 0

    while True:
        page = sp.current_user_saved_tracks(limit=limit, offset=offset)
        items = page.get("items", [])
        if not items:
            break

        for item in items:
            track = item.get("track")
            if not track:
                continue
            images = track.get("album", {}).get("images") or []
            tracks.append({
                "title": track["name"],
                "artists": ", ".join(a["name"] for a in track.get("artists", [])),
                "album": track.get("album", {}).get("name", ""),
                "cover_url": images[0]["url"] if images else None,
            })

        offset += limit
        if len(items) < limit:
            break

    return tracks


def _already_downloaded(filename_base):
    return os.path.exists(os.path.join(core.MUSIC_DIR, filename_base + ".mp3"))


def _tag_mp3(path, track):
    try:
        from mutagen.easyid3 import EasyID3
        from mutagen.id3 import ID3, APIC
        from mutagen.mp3 import MP3
    except ImportError:
        print("   ⚠️  mutagen n'est pas installé, métadonnées Spotify non appliquées.")
        return

    try:
        audio = MP3(path, ID3=ID3)
        if audio.tags is None:
            audio.add_tags()
            audio.save()

        tags = EasyID3(path)
        tags["title"] = track["title"]
        tags["artist"] = track["artists"]
        if track["album"]:
            tags["album"] = track["album"]
        tags.save()

        if track.get("cover_url"):
            with urllib.request.urlopen(track["cover_url"]) as resp:
                cover_data = resp.read()
            id3 = ID3(path)
            id3.delall("APIC")
            id3.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=cover_data))
            id3.save()
    except Exception as e:
        print(f"   ⚠️  Impossible d'appliquer les métadonnées Spotify : {e}")


def import_liked_songs():
    core.init_folders()

    try:
        sp = _get_spotify_client()
    except RuntimeError as e:
        print(f"❌ {e}")
        return

    print("🔎 Récupération de vos titres likés depuis Spotify...")
    try:
        tracks = fetch_liked_tracks(sp)
    except Exception as e:
        print(f"❌ Impossible de récupérer vos titres likés : {e}")
        return

    print(f"✅ {len(tracks)} titre(s) liké(s) trouvé(s).")
    if not tracks:
        return

    ok, skipped, failed = 0, 0, 0

    for i, track in enumerate(tracks, start=1):
        label = f"{track['artists']} - {track['title']}"
        filename_base = _sanitize(label)
        print(f"\n[{i}/{len(tracks)}] {label}")

        if _already_downloaded(filename_base):
            print("   ⏭️  Déjà téléchargé, on passe.")
            skipped += 1
            continue

        outtmpl = os.path.join(core.MUSIC_DIR, filename_base + ".%(ext)s")
        ydl_opts = core.build_ydl_opts(audio_only=True, outtmpl=outtmpl, embed_thumbnail=False)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"ytsearch1:{label} audio"])

            mp3_path = os.path.join(core.MUSIC_DIR, filename_base + ".mp3")
            if os.path.exists(mp3_path):
                _tag_mp3(mp3_path, track)
                print("   ✅ Téléchargé et tagué.")
                ok += 1
            else:
                print("   ⚠️  Fichier MP3 introuvable après téléchargement.")
                failed += 1
        except Exception as e:
            print(f"   ❌ Échec : {e}")
            failed += 1

        # Petite pause pour éviter de se faire limiter/bloquer par YouTube.
        time.sleep(1)

    print(f"\n🎉 Import terminé : {ok} réussi(s), {skipped} déjà présent(s), {failed} échec(s).")
