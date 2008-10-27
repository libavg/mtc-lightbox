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
          image=event.node
          print float(image.angle)
          if float(image.angle) == 0.0:
            root=Player.getRootNode()
            print "fullsize image detected"
            endwidth=image.width/imgScale
            endheight=image.height/imgScale
            print endwidth," ",endheight," ",root.width," ",root.height
            anim.SplineAnim(image, "width", 500, image.width, 0, endwidth, 0)
            anim.SplineAnim(image, "height", 500, image.height, 0, endheight, 0)
            anim.SplineAnim(image, "angle", 500, image.angle, 0, radians(340)+uniform(0,radians(40)), 0)
            anim.SplineAnim(image, "x", 500, image.x, 0, (root.width-endwidth)/2, 0)
            anim.SplineAnim(image, "y", 500, image.y, 0, (root.height-endheight-(endheight/2)), 0)
          print "nullifying drag vectors for ",event.node.id
          for null in [0,0,0,0,0,0,0,0,0,0]:  	# fill fifo if it's empty
            self.dragX.append(null)
            self.dragY.append(null)
          for x in list(self.dragX):		# fill fifo with current position
            self.dragX.append(event.node.x)
          for y in list(self.dragY):		# see last comment ;)
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
    imageList.remove(image)


def addObjectToPublishStack(image):
    root=Player.getRootNode()
    Lightbox=Player.getElementByID("LightBox")
    PublishStack=Player.getElementByID("PublishStack")    
    Parent=image.getParent()
    if Parent == Lightbox:
      image.unlink()
      PublishStack.appendChild(image)
      imgIndex=PublishStack.indexOf(image)
      print image.id," added to pubstack as ", imgIndex
    elif Parent == PublishStack:
      imgIndex=PublishStack.indexOf(image)
      print image.id," is member of pubstack ", imgIndex
    anim.SplineAnim(image, "x", 500 , image.x, root.width/10, root.width-image.width+image.width/7, 0, useInt=True)
    anim.SplineAnim(image, "y", 500, image.y, root.width/10, 40+imgIndex*20, 0, useInt=True)
    anim.SplineAnim(image, "angle", 500, image.angle, 0, radians(340), 0, useInt=False)
        

def makeFullSize(image):
    root=Player.getRootNode()
    anim.SplineAnim(image, "x", 500, image.x, 0, (root.width-image.width*imgScale)/2, 0)
    anim.SplineAnim(image, "y", 500, image.y, 0, (root.height-image.height*imgScale)/2, 0)
    anim.SplineAnim(image, "angle", 500, image.angle, 0, 0, 0)
    anim.SplineAnim(image, "width", 500, image.width, 0, image.width*imgScale, 0)
    anim.SplineAnim(image, "height", 500, image.height, 0, image.height*imgScale, 0)
    

def scaleDown(image):
    root=Player.getRootNode()
    animSlideIntoPosition(image.id, uniform(0,200), uniform(0,root.height-image.height/imgScale), 500)
    animBlowUp(image.id, imgScale, 500)
    image.angle=radians(340)+uniform(0,radians(40))
                

def handleOutsiders():
#      print "deciding what to do with ",image
    root=Player.getRootNode()
#    print "checking for objects outside of display area"
    for image in imageList:
      if int(image.x)>root.width-(image.width/2):
        addObjectToPublishStack(image)
      elif int(image.x)<0-int(image.width)+int(image.width/6):
#        scaleDown(image)
        deleteObject(image)
      elif int(image.y)>root.height-(image.height/2): 
        makeFullSize(image)
      elif int(image.y)<0-int(image.height):
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
#        animSlideIntoPosition(newImage.id, uniform(0,root.width-newImage.width/imgScale), uniform(0,root.height-newImage.height/imgScale), 500)
        animSlideIntoPosition(newImage.id, uniform(0,200), uniform(0,root.height-newImage.height/imgScale), 500)
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
<div id="PublishStack">
</div>
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
Player.setInterval(1000, handleOutsiders)
Player.showCursor(False)
Player.play()
