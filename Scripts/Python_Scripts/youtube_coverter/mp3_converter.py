##################################################
# Date: 2026-09-07
# Script name: mp3_converter
# Author: Wayne Stock
# updated: 2026-09-07
# discription: Convert YouTube Videos to mp3 
#################################################

import yt_dlp

url = input("Enter YouTube video URL: ")

ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "%(title)s.%(ext)s",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3"
    }],
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Download complete")