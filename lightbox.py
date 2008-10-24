#!/usr/bin/python2.5

import os
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
        Player.getRootNode().appendChild(newImage)
        newImage.x=randint(10,300)
        newImage.y=randint(5,200)
        newImage.width /= 3
        newImage.height /= 3
        newImage.angle=radians(320)+uniform(0,radians(80))
        imgDragger=draggable.Draggable(newImage)
        imgDragger.enable()
        imageList.append(imgDragger)
        
def onFrame():
    pass


Player = avg.Player()
##- Player.loadFile('lightbox.avg')
Player.loadString('<avg width="1280" height="720"/>')
Player.setResolution(1,0,0,0)
Player.setVBlankFramerate(1)
Player.setOnFrameHandler(onFrame)
##- Player.addTracker()
anim.init(Player)
populateLightbox()
Player.play()

