# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 15:06:10 2019

@author: elifs
"""

import RegionGrow
import counting

orj_counts = [10, 3, 22]

image1 = RegionGrow.regionGrow("bird_images/1.jpg",20)
first_image = image1.ApplyRegionGrow()

image2 = RegionGrow.regionGrow("bird_images/2.jpg",5)
second_image = image2.ApplyRegionGrow()

image3 = RegionGrow.regionGrow("bird_images/3.bmp",25)
third_image = image3.ApplyRegionGrow()


count1 = counting.count_birds(first_image, 24)
count2 = counting.count_birds(second_image, 24)
count3 = counting.count_birds(third_image, 14)

count = [count1, count2, count3]

print("Results:")
for c in range(len(count)):
    print("Number of Birds: {:2d} and Counted Birds: {:2d}".format(count[c], orj_counts[c]))
