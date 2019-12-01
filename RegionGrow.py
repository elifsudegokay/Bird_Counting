# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 13:53:22 2019

@author: elifs
"""
import cv2
import numpy as np
import Basic

class regionGrow():
  
    def __init__(self, image_path, th_value):
        
        self.readImage(image_path)
        self.height, self.width,_ =  self.im.shape
        self.changed = np.zeros((self.height, self.width), np.double)
        self.currentRegion = 0
        self.iterations = 0
        
        #segmentation shape
        self.segmentation_s = np.zeros((self.height, self.width,3), dtype='uint8')
        
        self.heap = Basic.Basic()
        self.thresh = float(th_value)
        
        
    def readImage(self, img_path):
        self.im = cv2.imread(img_path, 1)
    

    def getNeighbour(self, x_, y_):
        
        neighbour = []
        
        for i in (-1 ,0, 1):
            for j in (-1, 0, 1):
                if (i, j) == (0, 0): 
                    continue
                x = x_ + i
                y = y_ + j
                if self.border(x, y):
                    neighbour.append((x, y))
        return neighbour
    
    
    def ApplyRegionGrow(self):
        
        randomseeds=[[self.height / 2, self.width / 2],
            [self.height / 3, self.width / 3], [2 * self.height / 3, self.width / 3], [self.height/3-10,self.width/3],
            [self.height / 3, 2 * self.width / 3], [2 * self.height / 3, 2 * self.width / 3],[self.height / 3 - 10, 2 * self.width / 3],
            [self.height /3, self.width - 10], [2 * self.height / 3, self.width - 10], [self.height / 3 - 10, self.width - 10]
                    ]
        np.random.shuffle(randomseeds)
        
        for x_ in range (self.height):
            for y_ in range (self.width):
         
                if self.changed[x_,y_] == 0 and (int(self.im[x_, y_, 0]) * int(self.im[x_, y_, 1]) * int(self.im[x_, y_, 2]) > 0) :  
                    self.currentRegion += 1
                    self.changed[x_,y_] = self.currentRegion
                    self.heap.push((x_,y_))
                    while not self.heap.checkEmpty():
                        x,y = self.heap.pop()
                        self.BreadthFirstSearch(x, y)
                        self.iterations += 1
                    if(self.endChange()):
                        break
                    count = np.count_nonzero(self.changed == self.currentRegion)
                    if(count < 8 * 8):     
                        self.changed[self.changed == self.currentRegion]=0
                        x_-=1
                        y_-=1   
                        self.currentRegion-=1

        for i in range(0, self.height):
            for j in range (0, self.width):
                val = self.changed[i][j]
                if(val == 0):
                    self.segmentation_s[i][j] = 255, 255, 255
                else:
                    self.segmentation_s[i][j] =val * 35, val * 90, val * 30
                    
        if(self.iterations > 200000):
            print("Max Iterations")
        #print("Iterations : " + str(self.iterations))
        
        return  self.segmentation_s
        
        #breadth-first search algorithm
    def BreadthFirstSearch(self, x_, y_):
        
        regionNum = self.changed[x_, y_]
        itemlist=[]
        itemlist.append((int(self.im[x_, y_, 0]) + int(self.im[x_, y_, 1])+int(self.im[x_,y_,2]))/3)
        var = self.thresh
        neighbours = self.getNeighbour(x_,y_)
        
        for x,y in neighbours:
            if self.changed[x,y] == 0 and self.distance(x, y, x_, y_) < var:
                if(self.endChange()):
                    break;
                self.changed[x, y] = regionNum
                self.heap.push((x, y))
                itemlist.append((int(self.im[x, y, 0])+int(self.im[x, y, 1]) + int(self.im[x, y, 2])) / 3)
                var = np.var(itemlist)
            var = max(var, self.thresh)
                
    
    
    def endChange(self):
   
        return self.iterations > 200000 or np.count_nonzero(self.changed > 0) == self.width * self.height


    def border(self, x,y):
        return  0 <= x < self.height and 0 <= y < self.width
    
    def distance(self, x, y, x_, y_):
        return ((int(self.im[x, y, 0]) - int(self.im[x_, y_, 0])) ** 2 + (int(self.im[x, y, 1]) - int(self.im[x_, y_, 1])) ** 2 + (int(self.im[x, y, 2]) - int(self.im[x_, y_, 2])) ** 2) ** 0.5

