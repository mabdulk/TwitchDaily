from datetime import date
from importlib.metadata import files
import os
import re
import time

def download_wait(path_to_downloads):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 20:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
    return seconds

def Log(text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open('log.txt', "a+") as file_object:   
         # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)


def deleteAllMP4FilesInFolder(folder_path):
    files = os.listdir(folder_path)
    for name in files:
        
        try:
            getextension = os.path.splitext(name)
            new = folder_path + "\\" + name
           
            if os.path.isfile(folder_path + "\\" + name) and getextension[1] == ".mp4":
                os.remove(new)
                print(f"{name} File has been deleted")

        except Exception as e:
            Log(f"ERORR! :{e}")

def CleanUpTitles(clipsData):
    for clip in clipsData:
        clip['title'] = re.sub(r'[^a-zA-Z]', '', clip['title'])

        if clip['title'] == '':
            clip['title'] = f"{clip['broadcaster']['name']}_{int(str(clip['tracking_id'])[:3]) }"
    return clipsData


def xml_editor(title, Clipsdata):
    

##################Replace XML with template
    xml_file = open("YMU_v1.0//YMU//Upload_Configuration_template.xml","r") 
    
    string_list = xml_file.readlines() 

    xml_file.close() 

    xml_file = open("YMU_v1.0//YMU//Upload_Configuration.xml","w") 

    new_file_contents="".join(string_list)

    xml_file.write(new_file_contents)
    xml_file.close()    
###################

 
    desc = ""
    count = 10
    for clip in reversed(Clipsdata):
        desc = desc + f"\n{count}- {clip['url']}"

        count = count - 1

    

    title_xml = "        <title>" + title + "</title>\n"
    desc_xml = "        <description>\n Top 10 twitch videos of the day" + desc + "</description>\n" 
    #print(desc_xml)



    xml_file = open("YMU_v1.0//YMU//Upload_Configuration.xml","r") ##Opens XML file to read it

    string_list = xml_file.readlines() #storing a list of strings, each string represents a line in the xml file

    xml_file.close() #closing it because it can go fuck itself now, we dont need it anymore


    string_list[4] = title_xml #line 4 in the XML file is the title, so we overwrite it with the new title
    string_list[5] = desc_xml #line 5 in the XML file is the desc, so we overwrite it with the new desc

    xml_file = open("YMU_v1.0//YMU//Upload_Configuration.xml","w") #opening the file with writing capability 

    new_file_contents = "".join(string_list) 
    new_file_contents = new_file_contents.replace("tt_medium=clips_api&tt_content=url","") #deleting buggy texts

    xml_file.write(new_file_contents)
    xml_file.close()

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%d%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

def getTwitchApiQueryByCategory(category):
    if(category == "All"):
        return {'period': 'month', 'trending': 'true', 'limit': '10'} 
    return {'period': 'month', 'trending': 'true', 'limit': '10', 'game': f"{category}"}

def getYoutubeVideoTitleByCategory(category):
    if(category == "All"):
        return f"TOP 10 MOST VIEWED TWITCH CLIPS OF THE DAY ({date.today()})"
    return f"TOP 10 MOST VIEWED TWITCH CLIPS OF THE DAY - {category} Edition ({date.today()})"


