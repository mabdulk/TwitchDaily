import string
from moviepy.editor import *
import json
from datetime import date
import Shared

'''
Takes clips from path and combines them into one, adds intro, adds top 10
videosPath - path to clips 
IntroPath - path to intro clip
'''
def editVideos(videosPath: string, introPath: string, outroPath: string, clipsData: json):
    fileNames = os.listdir(videosPath)
    count = 10 
    compositeClips = []

    intro = VideoFileClip(introPath)
    outro = VideoFileClip(outroPath)
    compositeClips.append(intro)

    clips = []

    count = len(clipsData)
    clipOrderCount = 10
    for clipData in clipsData[::-1]: 
        
        title = f"{clipData['title']}_{clipData['tracking_id']}.mp4"

        clips.append( VideoFileClip(f"{videosPath}//{title}"))
        # Generate a text clip 
        v = clipData['broadcaster']['display_name']
        txt_clip = TextClip(f"{Shared.human_format(clipData['views'])} Views\n {clipData['title']}\nby {clipData['broadcaster']['display_name']} - {clipData['game']}", fontsize = 30, color = 'black', align='West') 

        # setting position of text in the center and duration 
        # txt_clip = txt_clip.set_pos(("right","bottom")).set_duration(clip.duration) 
        txt_clip = txt_clip.set_pos((0.19,0.88), relative=True).set_duration(5) # was .73 then 30, .50, 60, 65, 66, 67, 0.44, .87 to 

        # txt_clip.set_position((0.3,0.7), relative=True)
        
        logo = (ImageClip(f"topTenImages\\top{clipOrderCount}.jpg")
          .set_duration(5)
          .resize(height=150) # if you need to resize...
          .margin(right=8, top=8, opacity=0) # (optional) logo-border padding
        #   .set_pos(("right","bottom"))
          .set_position((0.0,0.85), relative=True) #.48 .25
          .set_opacity(.8))
        video = CompositeVideoClip([clips[-1],logo, txt_clip])

        compositeClips.append(video)

        count = count - 1
        clipOrderCount = clipOrderCount - 1
        
    compositeClips.append(outro)
    final_clip = concatenate_videoclips(compositeClips, method = 'compose')
    final_clip.write_videofile(videosPath + "\\TopTen.mp4", fps = 30, threads=4, logger=None)

    
    for clip in clips:
      clip.close()

