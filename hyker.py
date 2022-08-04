import cv2
import pyautogui as pyauto
import argparse
import os
import subprocess
from PIL import Image

pyauto.FAILSAFE = True

parser = argparse.ArgumentParser("Hyker", description="An (atm) very very simple script to rip chapters from Hyke comic using the advanced technology of screeenshots.")

parser.add_argument("-w", "--WACK", help="Run the output through WACK after finishing (WACK must be in the same folder)", default=True, action="store_false")
parser.add_argument("-s", "--SkipLoad", help="Skip preloading the chapter", default=False, action="store_true")
args = parser.parse_args()

res = pyauto.size()
midPoint = res[0]/2, res[1]/2

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
    try:
        os.mkdir("chapter")
    except:
        print("Directory already exists")
    #Initialise I
    i=0
    #Setup a while loop to look for the like icon at the end of chapters
    while(pyauto.locateCenterOnScreen("HeartIcon.png") != True):
        #Take a screenshot of the visible page
        pyauto.moveTo(0, midPoint[1]/2)
        pyauto.screenshot("chapter/screenshot " + str(i) + ".png", region=(int(res[0]*0.34), int(res[1]*0.05), int(res[0]*0.31), int(res[1]*0.98)))
        #Move the mouse to the bottom middle of the chapter
        pyauto.moveTo(midPoint[0], int(res[1]*0.97))
        #Move the chapter up a bit
        pyauto.dragRel(0, int(res[1]*0.95)*-1, duration=5)
        i+=1

def FixAlignment():
    print("TODO")

def WACK():
    #For now I'm just gonna set the defaults to what I use (png, max quality, and MDex's height limit)
    subprocess.run("python", "wack", "-i", "chapter", "-q", "100", "-c", "png", "10000")

def main():
    input("Please make sure the command line isn't covering the center point of the screen. Once you have, press Enter")
    if(not args.skipload):
        loadChapter()
    rollingScreenshot()
    FixAlignment()
    if(args.WACK == True):
        WACK()

main()