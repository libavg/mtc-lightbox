#!/usr/bin/python2.5

import          os
                from math import *
                from random import *
                from libavg import avg, anim, draggable

global          Player
                imageList =[]
imgScale = 2

def 
populateLightbox():
path = "./images"
dirList = os.listdir(path)
for fname in dirList:
newImage = Player.createNode("image", {"href":path + "/" + fname})
origwidth = newImage.width
origheight = newImage.height
Player.getElementByID("lightbox").appendChild(newImage)
root = Player.getRootNode()
newImage.width /= imgScale
newImage.height /= imgScale
##-        newImage.opacity = 0.8
print "adding ", fname, " - ", origwidth, "x", origheight, " scaled down to ", newImage.width, "x", newImage.height
newImage.x = uniform(0, root.width - newImage.width)
newImage.y = uniform(0, root.height - newImage.height)
newImage.angle = radians(340) + uniform(0, radians(40))
imgDragger = draggable.Draggable(newImage)
imgDragger.enable()
imageList.append(imgDragger)
	def             onFrame():
                Bitmap = Tracker.
getImage(avg.IMG_FINGERS)
Node = Player.getElementByID("TrackerBitmap")
Node.setBitmap(Bitmap)
Node.width = 1280
Node.height = 720
Node.angle = pi

def onClick():
pass

Player = avg.Player()
##- Player.loadFile('lightbox.avg')
Player.loadString('' '
		  < avg width = "1280" height = "720" >
		  <div id = "lightbox" >
		  </div >
		  <image id = "TrackerBitmap" sensitive = "False" / >
		  </avg > '' ')
		  Player.setResolution(1, 0, 0, 0)
		  Player.setVBlankFramerate(1)
#Player.setOnFrameHandler(onFrame)
#Tracker=Player.addTracker("trackerrc")
#Tracker.setDebugImages(True,True)
		  anim.init(Player)
		  populateLightbox()
		  Player.play()
