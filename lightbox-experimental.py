#!/usr/bin/python2.5

import os
import time
from math import *
from random import *
from libavg import avg, anim, draggable
from collections import deque

global Player
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

class dragState():
      def __init__(self, dragX, dragY, node):
        self.dragX=dragX
        self.dragY=dragY
        self.node=node

      def calcDragVector(self, event):
          print "calculating drag vector for ",event.node
          self.dragX.append(event.node.x)
          self.dragY.append(event.node.y)
#          print list(self.dragX)
#          print list(self.dragY)
          print self.node," ",event.node
          if len(self.dragX)==10&len(self.dragY)==10:
            movX=self.dragX[9]-self.dragX[0]
            print "X ",movX
            movY=self.dragY[9]-self.dragY[0]
            print "Y ",movY

      def nullifyDragVector(self, event):
          print "nullifying drag vectors for "
          for x in list(self.dragX):
            self.dragX.append(event.node.x)
          for y in list(self.dragY):
            self.dragY.append(event.node.y)
          print list(self.dragX)," ",list(self.dragY)

      def storeDragMotion(self, event):
          print "storing movX and movY of ",self.node
          self.node.movX= self.movX
          self.node.movY= self.movY

      def retrDragMotion(self, event):
          print "retrDragMotion"
          print self.node.movX

      def continueDragMotion(self, event):
          print "continuing drag motion of ",event," ",event.node
          print list(self.dragX)," ",list(self.dragY)
          
      def decelerateDragMotion(self):
          print "foo ",self.movX," bar ",self.node
          

#def retrDragHist(node):
#        print list(dragX)
#        print list(dragY)

def printDrags(node):
    print 
                
def populateLightbox(): 
    path="./images"
    dirList=os.listdir(path)
    for fname in dirList:
        newImage=Player.createNode("image", {"href":path+"/"+fname})
        print newImage
        origwidth=newImage.width
        origheight=newImage.height
        Player.getElementByID("lightbox").appendChild(newImage)
        root=Player.getRootNode()
        newImage.width /= imgScale
        newImage.height /= imgScale
##-        newImage.opacity = 0.8
        print "adding ",fname," - ",origwidth,"x",origheight," scaled down to ",newImage.width,"x",newImage.height
#        newImage.x=uniform(0,root.width-newImage.width)
#        newImage.y=uniform(0,root.height-newImage.height)
#        newImage.angle=radians(340)+uniform(0,radians(40))
        newImage.x=100
        newImage.y=550
        imageList.append(newImage)
        a=dragState(fifo(10), fifo(10), newImage)
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
##-        for img in imageList:
##-          d=dragState(0,0,img)
##-          d.retrDragMotion 
          
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
