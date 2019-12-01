# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 14:05:23 2019

@author: elifs
"""

class Basic():
    def __init__(self):
        self.item = []
   
    def push(self, value):
        self.item.append(value)

    def pop(self):
        return self.item.pop()

    def size(self):
        return len(self.item)

    def checkEmpty(self):
        return self.size() == 0
