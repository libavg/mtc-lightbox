#!/usr/bin/python2.5

import os
import time
import re
from math import *
from random import *
from libavg import avg, anim, draggable
from collections import deque

#global Player
draggablesList=[]
imageList=[]
imgScale=3


class fifo(deque):
    def __init__(self, capacity):
         deque.__init__(self)
         assert capacity > 0
         self.capacity = capacity


    def append(self, x):
         while len(self) >= self.capacity:
             self.popleft()
         deque.append(self, x)


def animSlideIntoPosition(imgid, movX, movY, duration):
        img = Player.getElementByID(imgid)
        print "animating ",imgid,"/",img," ",movX," ",movY
        animX = anim.SplineAnim(img, "x", duration , img.x, movX/2, img.x+movX, movX/10, useInt=True)
        animY = anim.SplineAnim(img, "y", duration , img.y, movY/2, img.y+movY, movY/10, useInt=True)


def animBlowUp(imgid, scale, duration):
        img = Player.getElementByID(imgid)
        print "blowing ",imgid,"/",img," up to ",img.width/scale,"x",img.height/scale
        animX = anim.SplineAnim(img, "width", duration , img.width/scale/10, scale, img.width/scale, scale/10, useInt=False)
        animY = anim.SplineAnim(img, "height", duration , img.height/scale/10, scale, img.height/scale, scale/10, useInt=False)


class dragState():
      def __init__(self, dragX, dragY):
        self.dragX=dragX
        self.dragY=dragY


      def calcDragVector(self, event):
          self.dragX.append(event.node.x)
          self.dragY.append(event.node.y)
          self.movX=self.dragX[9]-self.dragX[0]
          self.movY=self.dragY[9]-self.dragY[0]
#          print "calculating drag vector for ",event.node," X ",self.movX," Y ",self.movY


      def nullifyDragVector(self, event):
          print "nullifying drag vectors for ",event.node.id
          for null in [0,0,0,0,0,0,0,0,0,0]:
            self.dragX.append(null)
            self.dragY.append(null)
          for x in list(self.dragX):
            self.dragX.append(event.node.x)
          for y in list(self.dragY):
            self.dragY.append(event.node.y)
          print list(self.dragX)," ",list(self.dragY)
          self.movX=0
          self.movY=0

          
      def continueDragMotion(self, event):
          print "continuing drag motion of ",event.node.id
          print event.node.id," ",self.movX," ",self.movY
          img=event.node
          animX = anim.SplineAnim(img, "x", 500 , img.x, 5*self.movX, img.x+(2*self.movX), 0, useInt=True)
          animY = anim.SplineAnim(img, "y", 500 , img.y, 5*self.movY, img.y+(2*self.movY), 0, useInt=True)



isImg=re.compile('.*jpg|.*png')

def deleteObject(image):
    print "deleting object ",image.id," at ", image.x,",",image.y
    Lightbox=Player.getElementByID("LightBox")
    Lightbox.removeChild(image)
    
    
def removeOutsiders():
    root=Player.getRootNode()
    print "checking for objects outside of display area"
    for image in imageList:
      if int(image.x)>root.width:
        deleteObject(image)
      if int(image.x)<0-int(image.width):
        deleteObject(image)
      if int(image.y)>root.height: 
        deleteObject(image)
      if int(image.y)<0-int(image.height):
        deleteObject(image)
      
    
def populateLightbox(): 
    path="./images"
    dirList=os.listdir(path)
    for fname in dirList:
      if isImg.match(fname):
        newImage=Player.createNode("image", {"href":path+"/"+fname, "id":fname})
        origwidth=newImage.width
        origheight=newImage.height
        Player.getElementByID("LightBox").appendChild(newImage)
        root=Player.getRootNode()
        print "adding ",fname," - ",origwidth,"x",origheight," scaled down to ",int(newImage.width/imgScale),"x",int(newImage.height/imgScale)
        animSlideIntoPosition(newImage.id, uniform(0,root.width-newImage.width/imgScale), uniform(0,root.height-newImage.height/imgScale), 500)
        animBlowUp(newImage.id, imgScale, 500)
        newImage.angle=radians(340)+uniform(0,radians(40))
        imageList.append(newImage)
        a=dragState(fifo(10), fifo(10))
        a.nullifyDragVector
        imgDragger=draggable.Draggable(newImage, onDragStart=a.nullifyDragVector, onDragMove=a.calcDragVector, onDragEnd=a.continueDragMotion)
        imgDragger.enable()
        draggablesList.append(imgDragger)


def onFrame():
        Bitmap = Tracker.getImage(avg.IMG_FINGERS)
        Node = Player.getElementByID("TrackerBitmap")
        Node.setBitmap(Bitmap)
        Node.width=1280
        Node.height=720
        Node.angle=pi

Player = avg.Player()
##- Player.loadFile('lightbox.avg')
Player.loadString('''
<avg width="1280" height="720">
<div id="LightBox">
</div>
<image id="TrackerBitmap" sensitive="False"/>
</avg>''')
Player.setResolution(1,0,0,0)
Player.setVBlankFramerate(1)
Player.setOnFrameHandler(onFrame)
Tracker=Player.addTracker("trackerrc")
Tracker.setDebugImages(True,True)
populateLightbox()
#for img in imageList:
#    animContDragMotion(img.id, uniform(-150,150), uniform(-150,150))
Player.setInterval(5000, removeOutsiders)
Player.play()
