import json
import os
import time
from typing import final
import TwitchDownloader, VideoEditor, Shared
import requests
from datetime import date, datetime
from pathlib import Path


try:   
  Shared.Log(f"\nInitiating process: At Time: {datetime.now()}")
  Shared.Log("opening Twitch Top Videos List..")
  
  f = open('TwitchTopVideosList.json', encoding="utf8")
  TwitchTopVideos = json.load(f)

  Shared.Log(TwitchTopVideos["date"])
  Shared.Log(datetime.today().strftime('%Y-%m-%d'))
  Shared.Log("Determining Category..")
  if(TwitchTopVideos["date"] != datetime.today().strftime('%Y-%m-%d')):
    TwitchTopVideos["date"] = datetime.today().strftime('%Y-%m-%d')
    TwitchTopVideos["categories"] = ["All", "Just Chatting", "Grand Theft Auto V","League of Legends","Minecraft", "VALORANT"]
    with open('TwitchTopVideosList.json', 'w', encoding='utf-8') as f:
      json.dump(TwitchTopVideos, f, ensure_ascii=False, indent=4, default=str)    

  categories = TwitchTopVideos["categories"].copy()
  for category in categories:  

    Shared.Log(f"Category: {category}")

    f = open('clipsData.json', encoding="utf8")
    clipsData = json.load(f)

    f_backup = open('clipsDataBackup.json', encoding="utf8")
    clipsDataBackup = json.load(f_backup)

    homepath = Path.home()
    generalDownloadsPath = f"{homepath}\\Downloads"

    videoClipsPath = f"{homepath}\\Downloads\\UploadToYoutube"
    introClipPath = "Videos\\Introtopten.mp4"
    outroClipPath = "Videos\\outrotopten.mp4"

    if (len(clipsData) == 0):
            response = requests.get('https://api.twitch.tv/kraken/clips/top', Shared.getTwitchApiQueryByCategory(category), 
                            headers={'Accept':'application/vnd.twitchtv.v5+json',
                                    'Client-ID':'kimne78kx3ncx6brgo4mv6wki5h1ko'})
                                    
            clipsData = Shared.CleanUpTitles(response.json()['clips'])
            clipsDataBackup = Shared.CleanUpTitles(response.json()['clips'])            
            with open('clipsData.json', 'w', encoding='utf-8') as f:
              json.dump(clipsData, f, ensure_ascii=False, indent=4)
            with open('clipsDataBackup.json', 'w', encoding='utf-8') as f:
              json.dump(clipsData, f, ensure_ascii=False, indent=4)


    Shared.Log("Downloading clips")
    TwitchDownloader.downloadVideos(clipsData, generalDownloadsPath)

    Shared.Log("Download complete")
    Shared.Log("Combining clips")

    VideoEditor.editVideos(videoClipsPath, introClipPath, outroClipPath, clipsDataBackup)

    Shared.Log("Top Ten video is generated")
    Shared.Log("Uploading....")

    Shared.xml_editor(Shared.getYoutubeVideoTitleByCategory(category),clipsDataBackup)

    os.system(f'dotnet YMU_v1.0\\YMU\\YMU.Console.dll YMU_v1.0\YMU\\Upload_Configuration.xml')

    Shared.Log("Process Complete")
    Shared.Log("Deletion in progress..")
    time.sleep(10)
    Shared.deleteAllMP4FilesInFolder(videoClipsPath) 
    Shared.deleteAllMP4FilesInFolder(generalDownloadsPath)
    Shared.Log("MP4 files in UploadToYoutube and Downloads folders are deleted.")

    Shared.Log(f"Video has been successfully uploaded to youtube for category: {category}")
    TwitchTopVideos["categories"].remove(category)
    with open('TwitchTopVideosList.json', 'w', encoding='utf-8') as f:
      json.dump(TwitchTopVideos, f, ensure_ascii=False, indent=4, default=str)

except Exception as e:
  Shared.Log(f"ERORR! {datetime.now()} :{e}")
finally:
  Shared.Log("################################################################################################")
