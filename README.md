# YT-PlayList-downloader-in-mp3Format

This program downloads all the videos in a youtube playlist into our system in audio(mp3) format.

Steps involved:
1) Program downloads the videos in mp4 format in a folder using pytube.
2) Then it converts mp4 files to mp3 files using moviepy (could not find a library that can download directly in mp3).
3) Then it deletes the folder having mp4 files using shutil.
