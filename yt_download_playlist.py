from pytube import Playlist, YouTube
from moviepy.editor import *
import os
import shutil

playlist_link = input("Enter playlist link:")
p_list = Playlist(playlist_link)

print('start download')
directory = "E:/tempList"
os.mkdir(directory)

for video_link in p_list:
    yt = YouTube(video_link)
    yt_video = yt.streams.get_by_itag(22)
    yt_video.download(output_path='E:/tempList')

for filename in os.listdir(directory):
    mp4_file = "E:/tempList" + "/" + filename
    videoClip = VideoFileClip(mp4_file)
    audioClip = videoClip.audio
    os.chdir("E:/audioList")
    audioClip.write_audiofile(filename[:-4] + ".mp3")
    audioClip.close()
    videoClip.close()

shutil.rmtree(directory)

print("download done")


