import os
from mutagen.mp3 import MP3

# Directory containing your MP3 files
mp3_directory = r'C:\Users\JOEL\Music\B.o.B - Somnia'

# List to store song titles
song_titles = []

# Iterate over MP3 files in the directory
for filename in os.listdir(mp3_directory):
    if filename.endswith('.mp3'):
        mp3_file = os.path.join(mp3_directory, filename)
        try:
            audio = MP3(mp3_file)
            title = audio.get('TIT2', [''])[0]
            artist = audio.get('TPE1', [''])[0]
            if title and artist:
                song_titles.append(f'{artist} - {title}')
            else:
                song_titles.append(filename)  # Use filename if tags are missing
        except Exception as e:
            print(f'Error processing {filename}: {e}')

# Print the list of song titles
for title in song_titles:
    print(title)

# Optionally, export the list to a text file
with open('song_titles.txt', 'w', encoding='utf-8') as file:
    for title in song_titles:
        file.write(title + '\n')
