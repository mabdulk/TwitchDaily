# pip install webdriver-manager
from ast import Try
from re import search
import string
from urllib.request import Request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests
import time
import os 
import json
import Shared
from os import listdir, walk


def downloadVideos(clipsData: json, generalDownloadsPath: string):
    Clips = clipsData.copy()

    for clip in Clips:
        Shared.Log(f"Downloading clip: {clip['title']}")
        chrome_options = Options()
        chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])

        s=Service(ChromeDriverManager().install())
    
        limit = 10
        notDownloaded = True
        while(notDownloaded):            
            try:
                driver = webdriver.Chrome(service=s, options=chrome_options)
                fileNames = os.listdir(generalDownloadsPath)
                driver.get('https://clipr.xyz/')
                textInput = driver.find_element("xpath", "//form[1]/div[1]/div[2]/input")
                textInput = textInput.send_keys(clip['url'])
                driver.execute_script("window.scrollTo(0, 600)")
                el=driver.find_element("xpath", "//form[1]/div[2]/div[2]/button")
                el.click()

                time.sleep(5)
                driver.execute_script("window.scrollTo(0, 800)") 
                download = driver.find_element("xpath", "/html/body/div[1]/main/div/div[1]/div[2]/div[2]/div/div[2]/ul/div/li[1]/div[3]/a")
                download.click()
                time.sleep(10)
                driver.close()
                notDownloaded = False
            except Exception as e:
                driver.close()
                time.sleep(5)
                limit = limit -1
                if(limit == 0):
                    notDownloaded = False
                    raise Exception(f"unable to download the following clip: {clip['title']}") 
                Shared.Log(f"Failed to download clip: {clip['title']}, Trying again..")
                
        Shared.download_wait(generalDownloadsPath)
        newFileNames = os.listdir(generalDownloadsPath)
        fileName = [x for x in newFileNames if x not in fileNames][0]

        old_name = generalDownloadsPath + f"//{fileName}"
        new_name = generalDownloadsPath + "//UploadToYoutube" + f"//{clip['title']}_{clip['tracking_id']}.mp4"
        
        try:
            os.rename(old_name, new_name)
        except Exception as e:
            error = str(e)
            if 'Cannot create a file when that file already exists' in error:
                Shared.Log("Skipping")
            else:
                raise Exception(e)
                
        clipsData.remove(clip)
        with open('clipsData.json', 'w', encoding='utf-8') as f:
          json.dump(clipsData, f, ensure_ascii=False, indent=4)
