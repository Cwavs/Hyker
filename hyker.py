import cv2
import pyautogui as pyauto
import argparse
import os
import subprocess
from PIL import Image

pyauto.FAILSAFE = True

parser = argparse.ArgumentParser("Hyker", description="An (atm) very very simple script to rip chapters from Hyke comic using the advanced technology of screeenshots.", usage="Naviagte to a chapter on Hyke and open it, run this and let it do the rest.")

parser.add_argument("WACK", help="Run the output through WACK after finishing (WACK must be in the same folder)", type=bool, default=True)
args = parser.parse_args()

res = pyauto.size()
midPoint = res[0]/2, res[1]/2

def pil2CV(pillImage:Image):
    from numpy import array
    openCVImage = array(pillImage)
    return openCVImage[:, :, ::-1].copy()

#Pyautogui won't detect the image for some reason (I think, idk because it fucking does is return None, which the docs explicitly say it shouldn't, but after looking over the code I've come to the conclusion that the docs might be wrong, not that it'd if they were right, because I still have no fucking idea why its returning None), so I'm gonna use open-cv to do it myself
def openCVFindImage(image:str):
    method=cv2.TM_SQDIFF_NORMED
    
    img = cv2.imread(image)
    screenshot = pil2CV(pyauto.screenshot())
    
    result = cv2.matchTemplate(img, screenshot, method)
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)
    MPx,MPy = mnLoc
    trows,tcols = img.shape[:2]

    cv2.rectangle(screenshot, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)

    # Display the original image with the rectangle around the match.
    cv2.imshow('output',screenshot)

    # The image is only displayed if we call this
    cv2.waitKey(0)

    return (x, y, trows, tcols)

def loadChapter():
    #Click at the midpoint to bring up the scroll wheel and top and bottom bars.
    pyauto.click(midPoint)
    pyauto.sleep(1)
    #Find the Scroll wheel
    scroll = pyauto.locateCenterOnScreen("ScrollIcon.png")
    #Move mouse over scroll wheel
    pyauto.moveTo(scroll)
    #Drag the scroll wheel down to the bottom and then back up
    pyauto.dragRel(0, int(res[1]*0.83), duration=30)
    pyauto.dragRel(0, int(res[1]*0.83)*-1, duration=30)
    #Click in the middle to close them
    pyauto.click(midPoint[0], midPoint[1])

def rollingScreenshot():
    #Make a directory for the pages
    os.mkdir("chapter")
    #Initialise I
    i=0
    #Setup a while loop to look for the like icon at the end of chapters
    while(pyauto.locateCenterOnScreen("HeartIcon.png") != True):
        #Take a screenshot of the visible page
        pyauto.moveTo(0,0)
        pyauto.screenshot("chapter/screenshot " + str(i) + ".png", region=(int(res[0]*0.34), int(res[1]*0.05), int(res[0]*0.64), int(res[0]*0.99)))
        #Move the mouse to the bottom middle of the chapter
        pyauto.moveTo(midPoint[0], int(res[1]*0.97))
        #Move the chapter up a bit
        pyauto.dragRel(0, int(res[1]*0.97)*-1, duration=10)
        i=+1

def FixAlignment():
    print("TODO")

def WACK():
    #For now I'm just gonna set the defaults to what I use (png, max quality, and MDex's height limit)
    subprocess.run("python", "wack", "-i", "chapter", "-q", "100", "-c", "png", "10000")

def main():
    input("Please make sure the command line isn't covering the center point of the screen. Once you have, press Enter")
    loadChapter()
    rollingScreenshot()
    FixAlignment()
    if(args[0] == True):
        WACK()

main()