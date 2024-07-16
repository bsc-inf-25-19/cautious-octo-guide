import os
from mutagen.mp3 import MP3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Spotify credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# Authenticate with Spotify
scope = 'user-library-modify'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

# Directory containing your MP3 files
mp3_directory = r'C:\Users\JOEL\Music\6LACK - 6PC Hot (EP)'

# List to store song titles and artists
song_data = []

def clean_title(title):
    """Remove unwanted patterns from the song title."""
    unwanted_patterns = [' SongsLover.com', ' | Hiphopde.com', '[SPOTIFY-DOWNLOADER.COM] ', ' - ']
    for pattern in unwanted_patterns:
        title = title.replace(pattern, '')
    return title.strip()

# Iterate over MP3 files in the directory
for filename in os.listdir(mp3_directory):
    if filename.endswith('.mp3'):
        mp3_file = os.path.join(mp3_directory, filename)
        try:
            audio = MP3(mp3_file)
            title = audio.get('TIT2', [''])[0]
            artist = audio.get('TPE1', [''])[0]
            if title and artist:
                clean_title_str = clean_title(title)
                song_data.append((artist, clean_title_str))
            else:
                song_data.append((None, clean_title(filename)))  # Use filename if tags are missing
        except Exception as e:
            print(f'Error processing {filename}: {e}')

# Search for each song on Spotify and add to the library
for artist, title in song_data:
    if artist and title:
        query = f'artist:{artist} track:{title}'
    else:
        query = title

    try:
        result = sp.search(q=query, type='track', limit=1)
        if result['tracks']['items']:
            track_id = result['tracks']['items'][0]['id']
            sp.current_user_saved_tracks_add(tracks=[track_id])
            print(f'Added {artist} - {title} to library.')
        else:
            print(f'Song not found on Spotify: {artist} - {title}')
    except Exception as e:
        print(f'Error adding {artist} - {title}: {e}')
