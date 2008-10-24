#!/usr/bin/python2.5

import os
#import time
from math import *
from random import *
from libavg import avg, anim, draggable

global Player
imageList=[]

def populateLightbox(): 
    path="./images"
    dirList=os.listdir(path)
    for fname in dirList:
        print "adding ",fname
        newImage=Player.createNode("image", {"href":path+"/"+fname})
        Player.getElementByID("lightbox").appendChild(newImage)
        root=Player.getRootNode()
        newImage.x=randint(0,root.width/2)
        newImage.y=randint(0,root.height/2)
        newImage.width /= 4
        newImage.height /= 4
        newImage.angle=radians(330)+uniform(0,radians(60))
        imgDragger=draggable.Draggable(newImage)
        imgDragger.enable()
        imageList.append(imgDragger)
        
def onFrame():
        Bitmap = Tracker.getImage(avg.IMG_FINGERS)
        Node = Player.getElementByID("TrackerBitmap")
        Node.setBitmap(Bitmap)
        Node.width=1280
        Node.height=720
        Node.angle=pi

def onClick():
        pass

Player = avg.Player()
##- Player.loadFile('lightbox.avg')
Player.loadString('''
<avg width="1280" height="720">
<div id="lightbox">
</div>
<image id="TrackerBitmap" sensitive="False"/>
</avg>''')
Player.setResolution(1,0,0,0)
Player.setVBlankFramerate(1)
Player.setOnFrameHandler(onFrame)
Tracker=Player.addTracker("trackerrc")
Tracker.setDebugImages(True,True)
anim.init(Player)
populateLightbox()
Player.play()
