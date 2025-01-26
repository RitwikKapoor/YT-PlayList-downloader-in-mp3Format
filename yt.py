import os
import yt_dlp
from concurrent.futures import ProcessPoolExecutor
import sys
import time


def download_audio(video_url, output_dir):
    if not os.path.exists(output_dir):
        print("output directory does not exist")
        sys.exit(1)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        },
            {
            'key': 'FFmpegMetadata',
        }],
        'ignoreerrors': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
        except yt_dlp.utils.DownloadError as e:
            print(f"Error downloading {video_url}: {str(e)}")


def download_playlist_audio(playlist_url, output_dir):
    if not os.path.exists(output_dir):
        print("output directory does not exist")
        sys.exit(1)

    # Fetch all video URLs in the playlist
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        if playlist_info is None:
            print(f"Failed to fetch playlist information from {playlist_url}")
            return

        playlist_videos = [video['webpage_url']
                           for video in playlist_info.get('entries', []) if video]

    with ProcessPoolExecutor() as executor:
        futures = []
        for video_url in playlist_videos:
            futures.append(executor.submit(
                download_audio, video_url, output_dir))

        # Wait for all downloads to complete
        for future in futures:
            future.result()


if __name__ == "__main__":

    playlist_url = input("Enter YouTube playlist URL: ").strip()
    output_dir = input("Enter output directory path: ").strip()

    if not playlist_url or not output_dir:
        print("Error: Playlist URL and output directory are required.")
        sys.exit(1)

    start = time.perf_counter()

    download_playlist_audio(playlist_url, output_dir)

    finish = time.perf_counter()

    print(f'Finished in {round(finish - start, 2)} second(s)')
