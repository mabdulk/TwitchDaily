import json, string, time, win32api, win32con, keyboard

import pyautogui


'''
    x -> int 
    y -> int
    use x and y to click that position on the screen with mouse
'''
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0,0)
    time.sleep(1)

'''
    text -> string 
    writes text 
'''
def writeText(text):
    keyboard.write(text)
    time.sleep(1)
'''
    text -> string 
    writes text and clicks enter
'''
def enterText(text):
    writeText(text)
    keyboard.press_and_release('enter')
    time.sleep(1)

#pyautogui.displayMousePosition()

def uploadVideo(title: string, clipsData: json):
    #type s to start the program (send chrome left before typing s)
    keyboard.wait('s')

    #Create new tab
    keyboard.press_and_release('ctrl+t')
    #search bar: 400, 85
    click(400, 85)
    enterText('studio.youtube.com')
    time.sleep(4)

    #click upload videos: 1545 315
    click(1545, 385)

    #click select files: 860 950
    click(860, 950)

    #click windows key left
    keyboard.press_and_release('left windows+left')

    #click path bar: 660, 55 and go to this path Downloads/{NameOfVideo}.mp4
    click(660, 55)
    enterText('C:\\Users\\Ddave\\Downloads\\UploadToYoutube')

    #go to file name and write file name
    click(800, 1270)
    #title = video name
    enterText(title)
    time.sleep(5)

    #Add description
    click(900, 800)
    writeText('This is a description!') #tags go here

    #click next
    click(1500, 1250)

    #click yes its made for kids: 100, 650
    click(230, 945)

    #click next
    click(1500, 1250)

    #click next
    click(1500, 1250)

    #click next
    click(1500, 1250)

    #click public: 305, 880
    click(305, 880)

    #click publish
    click(1500, 1250)

