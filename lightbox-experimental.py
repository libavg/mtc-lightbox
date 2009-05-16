#!/usr/bin/python2.5

import os
import time
import re
from math import *
from random import *
from libavg import avg, anim, draggable
from collections import deque

draggablesList=[]
imageList=[]
isImg=re.compile('.*jpg|.*png')
imgScale=4


class fifo(deque):
    def __init__(self, capacity):
        deque.__init__(self)
        assert capacity > 0
        self.capacity = capacity
    
    def append(self, x):
        while len(self) >= self.capacity:
            self.popleft()
        deque.append(self, x)


class dragState():
    def __init__(self, dragX, dragY):
        self.dragX=dragX
        self.dragY=dragY
    
    def calcDragVector(self, event):
        self.dragX.append(event.node.x)
        self.dragY.append(event.node.y)
        self.movX=self.dragX[9]-self.dragX[0]
        self.movY=self.dragY[9]-self.dragY[0]
#        print "calculating drag vector for ",event.node," X ",self.movX," Y ",self.movY
    
    def nullifyDragVector(self, event):
        image = event.node
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
        image = event.node
        parent = image.getParent()
        if float(image.angle) == 0.0:
            shrinkFullsizeImage(image)
        if parent == PublishStack:
            if self.movX < -15:
                dropFromPublishStack(image)
        animX = anim.SplineAnim(image, "x", 500 , image.x, 5*self.movX, image.x+(2*self.movX), 0, useInt=True)
        animY = anim.SplineAnim(image, "y", 500 , image.y, 5*self.movY, image.y+(2*self.movY), 0, useInt=True)


def animSlideWithMomentum(imgid, movX, movY, duration):
    img = Player.getElementByID(imgid)
    print "animating ",imgid,"/",img," ",movX," ",movY
    animX = anim.SplineAnim(img, "x", duration , img.x, movX/2, img.x+movX, movX/10, useInt=True)
    animY = anim.SplineAnim(img, "y", duration , img.y, movY/2, img.y+movY, movY/10, useInt=True)

def animBlowUp(imgid, scale, duration):
    img = Player.getElementByID(imgid)
    print "blowing ",imgid,"/",img," up to ",img.width/scale,"x",img.height/scale
    animX = anim.SplineAnim(img, "width", duration , img.width/scale/10, scale, img.width/scale, scale/10, useInt=False)
    animY = anim.SplineAnim(img, "height", duration , img.height/scale/10, scale, img.height/scale, scale/10, useInt=False)

def scaleDown(image):
    root=Player.getRootNode()
    animSlideWithMomentum(image.id, uniform(0,200), uniform(0,root.height-image.height/imgScale), 500)
    animBlowUp(image.id, imgScale, 500)
    image.angle=radians(340)+uniform(0,radians(40))


def growFullsizeImage(image):
    anim.SplineAnim(image, "x", 500, image.x, 0, (root.width-image.width*imgScale)/2, 0)
    anim.SplineAnim(image, "y", 500, image.y, 0, (root.height-image.height*imgScale)/2, 0)
    anim.SplineAnim(image, "angle", 500, image.angle, 0, 0, 0)
    anim.SplineAnim(image, "width", 500, image.width, 0, image.width*imgScale, 0)
    anim.SplineAnim(image, "height", 500, image.height, 0, image.height*imgScale, 0)
    
def shrinkFullsizeImage(image):
    print "fullsize image detected"
    endwidth=image.width/imgScale
    endheight=image.height/imgScale
    print endwidth," ",endheight," ",root.width," ",root.height
    anim.SplineAnim(image, "width", 500, image.width, 0, endwidth, 0)
    anim.SplineAnim(image, "height", 500, image.height, 0, endheight, 0)
    anim.SplineAnim(image, "angle", 500, image.angle, 0, radians(340)+uniform(0,radians(40)), 0)
    anim.SplineAnim(image, "x", 500, image.x, 0, (root.width-endwidth)/2, 0)
    anim.SplineAnim(image, "y", 500, image.y, 0, (root.height-endheight-(endheight/2)), 0)


def deleteObject(image):
    print "deleting object ",image.id," at ", image.x,",",image.y
    try:
        imageList.remove(image)
        Lightbox.removeChild(image)
    except RuntimeError, err:
        print "RuntimeError occured: ", err

def addToPublishStack(image):
    image.unlink()
    PublishStack.appendChild(image)
    imgIndex=PublishStack.indexOf(image)
    print image.id," added to PublishStack, index ", imgIndex
      
def dropFromPublishStack(image):
    image.unlink()
    Lightbox.appendChild(image)
    try:
        imgIndex=Lightbox.indexOf(image)
        print imgIndex
    except RuntimeError, err:
        print "RuntimeError occured: ", err
    imageList.append(image)
    print image.id," dropped from PublishStack"

def moveToPublishStack(image):
    imgIndex = PublishStack.indexOf(image)
    anim.SplineAnim(image, "x", 500 , image.x, 0, root.width-image.width+image.width/2, 0, useInt=False)
    anim.SplineAnim(image, "y", 500, image.y, 0, 40+imgIndex*30, 0, useInt=False)
    anim.SplineAnim(image, "angle", 500, image.angle, 0, radians(320), 0, useInt=False)

def reorderPublishStack():
    numKids = PublishStack.getNumChildren()
    imgsInLightbox = Lightbox.getNumChildren()
    if imgsInLightbox > 0:
        while numKids > 0:
            numKids = numKids-1
            kid=PublishStack.getChild(numKids)
            moveToPublishStack(kid)
    elif imgsInLightbox == 0:
        print imgsInLightbox," images in Lightbox"
        while numKids > 0:
            numKids = numKids-1
            total=PublishStack.getNumChildren()
            kid=PublishStack.getChild(numKids)
            moveToGrid(kid, numKids, total)

def moveToGrid(image, index, total):
    pass
'''
### this code is completely broken, i feel kind of stupid
    imgsPerRow = int((root.width+(10*total))/image.width)
    numCols = int(total/imgsPerRow)
    col = index/(numCols)
    row = (total) % (index+1)
    print image.id,"grid: ",imgsPerRow,"x",numCols," ind",index," tot",total," col",col," row",row
    anim.SplineAnim(image, "x", 500 , image.x, 0, ((10+image.width)*col), 0, useInt=False)
    anim.SplineAnim(image, "y", 500, image.y, 0, ((10+image.height)*row), 0, useInt=False)
    anim.SplineAnim(image, "angle", 500, image.angle, 0, radians(358), 0, useInt=False)    
###
'''

def handleOutsiders():
    for image in imageList:
        if int(image.x)>root.width-(image.width/2):
            addToPublishStack(image)
            moveToPublishStack(image)
        elif int(image.x)<0-int(image.width)+int(image.width/6):
            deleteObject(image)
        elif int(image.y)>root.height-(image.height/2): 
            growFullsizeImage(image)
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
        Lightbox.appendChild(newImage)
        print "adding ",fname," - ",origwidth,"x",origheight," scaled down to ",int(newImage.width/imgScale),"x",int(newImage.height/imgScale)
        animSlideWithMomentum(newImage.id, uniform(0,root.width-newImage.width/imgScale), uniform(0,root.height-newImage.height/imgScale), 500)
        animBlowUp(newImage.id, imgScale, 500)
        newImage.angle=radians(340)+uniform(0,radians(40))
        imageList.append(newImage)
        d=dragState(fifo(10), fifo(10))
        d.nullifyDragVector
        imgDragger=draggable.Draggable(newImage, onDragStart=d.nullifyDragVector, onDragMove=d.calcDragVector, onDragEnd=d.continueDragMotion)
        imgDragger.enable()
        draggablesList.append(imgDragger)


def onFrame():
        Bitmap = Tracker.getImage(avg.IMG_FINGERS)
        Node = Player.getElementByID("TrackerBitmap")
        Node.setBitmap(Bitmap)
        Node.width=1280
        Node.height=720
        Node.angle=pi

Player = avg.Player.get()
Player.loadString('''
    <avg width="1280" height="720">
        <div id="PublishStack"></div>
        <div id="LightBox"></div>
        <image id="TrackerBitmap" sensitive="False"/>
    </avg>''')
Player.setResolution(1,0,0,0)
Player.setVBlankFramerate(1)
Player.setOnFrameHandler(onFrame)
Tracker=Player.addTracker("trackerrc")
Tracker.setDebugImages(True,True)
root=Player.getRootNode()
Lightbox=Player.getElementByID("LightBox")
PublishStack=Player.getElementByID("PublishStack")
populateLightbox()
Player.setInterval(1000, handleOutsiders)
Player.setInterval(900, reorderPublishStack)
Player.showCursor(False)
Player.play()
