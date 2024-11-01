import yt_dlp
def download_music(query: str):
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '256',
        }],
        'outtmpl': f'{query}.%(ext)s',
        'default_search': 'ytsearch',
        'noplaylist': True,
        'writethumbnail': True,  
        'socket_timeout': 120,
    }
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(query, download=True)  
            music_file = f"{info_dict['title']}.mp3" 
            thumbnail_file = f"{info_dict['title']}.webp"  
            return music_file, thumbnail_file  
    except Exception as e:
        print(f"Error downloading music: {e}")
        return None, None  
